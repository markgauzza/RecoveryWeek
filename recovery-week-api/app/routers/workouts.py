from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, case, cast, Date
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Workout, WorkoutType
from app.schemas import (
    WorkoutCreate,
    WorkoutResponse,
    WorkoutOut,
    WorkoutDailySummary,
    PaginatedDailySummary,
    WorkoutTypeOut,
)

router = APIRouter(
    prefix="/workouts",
    tags=["workouts"],
)

@router.get("/types", response_model=List[WorkoutTypeOut])
def get_workout_types(db: Session = Depends(get_db)):
    """
    Returns the full list from the lookup table.
    """
    items = db.query(WorkoutType).order_by(WorkoutType.WorkoutName).all()
    return items

@router.post("/", response_model=WorkoutResponse, status_code=201)
def create_workout(workout: WorkoutCreate, db: Session = Depends(get_db)):
    db_workout = Workout(
        WorkoutTypeId=workout.WorkoutTypeId,
        WorkoutDate=workout.WorkoutDate,
        TotalSeconds=workout.TotalSeconds,
        Sequence=workout.Sequence,
        CreateDate=datetime.now(),
    )

    try:
        db.add(db_workout)
        db.commit()
        db.refresh(db_workout)
    except IntegrityError as e:
        db.rollback()
        print(f"IntegrityError: {e.orig}")
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Could not create workout",
                "database_error": str(e.orig),
                "statement": str(e.statement) if e.statement else None,
            },
        )

    return db_workout


@router.get("/", response_model=List[WorkoutOut])
def get_workouts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    workouts = (
        db.query(Workout)
        .order_by(Workout.WorkoutDate.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return workouts


@router.get("/daily-summary", response_model=PaginatedDailySummary)
def get_daily_workout_summary(
    skip: int = Query(0, ge=0),
    limit: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
):
    workout_date = cast(Workout.WorkoutDate, Date).label("WorkoutDate")
    day_of_week = func.dayname(Workout.WorkoutDate).label("DayOfWeek")
    sequence = func.max(Workout.Sequence).label("Sequence")
    day_parity = case(
        (func.day(Workout.WorkoutDate) % 2 == 1, "Odd"),
        else_="Even",
    ).label("DayParity")
    workouts_list = func.group_concat(
        WorkoutType.WorkoutName.distinct().op("ORDER BY")(WorkoutType.WorkoutName)
    ).label("Workouts")

    base_query = (
        db.query(
            workout_date,
            workouts_list,
            sequence,
            day_of_week,
            day_parity,
        )
        .join(WorkoutType, Workout.WorkoutTypeId == WorkoutType.WorkoutTypeId)
        .group_by(workout_date, day_of_week, day_parity)
    )

    total = base_query.count()

    results = (
        base_query
        .order_by(workout_date.desc(), sequence.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    items = [
        WorkoutDailySummary(
            WorkoutDate=row.WorkoutDate,
            Workouts=row.Workouts or "",
            Sequence=row.Sequence,
            DayOfWeek=row.DayOfWeek,
            DayParity=row.DayParity,
        )
        for row in results
    ]

    return PaginatedDailySummary(
        total=total,
        skip=skip,
        limit=limit,
        items=items,
    )