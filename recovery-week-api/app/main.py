from typing import List
from fastapi import Query

from sqlalchemy import func, case, cast, Date
from sqlalchemy.exc import IntegrityError
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.database import get_db
from app.database import engine, Base
from app.routers import items
from app.schemas import WorkoutCreate, WorkoutResponse, WorkoutOut, WorkoutDailySummary, WorkoutTypeOut
from app.models import Workout, WorkoutType
from datetime import datetime



Base.metadata.create_all(bind=engine)  # for small apps; prefer Alembic later

app = FastAPI(title="Recovery Week API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items.router, prefix="/api")

@app.post("/workouts/", response_model=WorkoutResponse, status_code=201)
def create_workout(workout: WorkoutCreate, db: Session = Depends(get_db)):
    db_workout = Workout(
        WorkoutTypeId=workout.WorkoutTypeId,
        WorkoutDate=workout.WorkoutDate,       # None → DB default
        TotalSeconds=workout.TotalSeconds,
        Sequence=workout.Sequence,
        CreateDate=datetime.now()
    )

    try:
        db.add(db_workout)
        db.commit()
        db.refresh(db_workout)

    except IntegrityError as e:
        db.rollback()

    
        print(f"IntegrityError: {e.orig}")   # or use logging

        raise HTTPException(
            status_code=400,
            detail={
                "message": "Could not create workout",
                "database_error": str(e.orig),           # MySQL message
                "statement": str(e.statement) if e.statement else None,
            }
        )


    return db_workout


@app.get("/workouts/", response_model=List[WorkoutOut])
def get_workouts(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Max number of records to return"),
    db: Session = Depends(get_db)
):
    workouts = (
        db.query(Workout)
        .order_by(Workout.WorkoutDate.desc())   # newest first
        .offset(skip)
        .limit(limit)
        .all()
    )
    return workouts

@app.get("/workouts/daily-summary", response_model=List[WorkoutDailySummary])
def get_daily_workout_summary(db: Session = Depends(get_db)):
    workout_date = cast(Workout.WorkoutDate, Date).label("WorkoutDate")

    day_of_week = func.dayname(Workout.WorkoutDate).label("DayOfWeek")

    day_parity = case(
        (func.day(Workout.WorkoutDate) % 2 == 1, "Odd"),
        else_="Even"
    ).label("DayParity")

    # IMPORTANT: use WorkoutType (SQLAlchemy), NOT WorkoutTypeOut (Pydantic)
    workouts_list = func.group_concat(
        WorkoutType.WorkoutName.distinct().op("ORDER BY")(WorkoutType.WorkoutName)
    ).label("Workouts")

    sequence = func.max(Workout.Sequence).label("Sequence")

    results = (
        db.query(
            workout_date,
            workouts_list,
            sequence,
            day_of_week,
            day_parity,
        )
        .join(WorkoutType, Workout.WorkoutTypeId == WorkoutType.WorkoutTypeId)
        .group_by(workout_date, day_of_week, day_parity)
        .order_by(workout_date.desc())
        .all()
    )

    return [
        WorkoutDailySummary(
            WorkoutDate=row.WorkoutDate,
            Workouts=row.Workouts or "",
            Sequence=row.Sequence,
            DayOfWeek=row.DayOfWeek,
            DayParity=row.DayParity,
        )
        for row in results
    ] 

from .routers import workouts   # or whatever you named the file

