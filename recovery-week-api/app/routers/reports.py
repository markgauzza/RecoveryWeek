# routers/reports.py
from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, case, extract

from app.database import get_db
from app.models import Workout, WorkoutType
from app.schemas import WorkoutDayOfWeekReportRow

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/workouts-by-day-of-week", response_model=List[WorkoutDayOfWeekReportRow])
def workouts_by_day_of_week(
    # optional filters later: start_date, end_date
    db: Session = Depends(get_db),
):
    # MySQL DAYOFWEEK: 1=Sun ... 7=Sat
    day_num = func.dayofweek(Workout.WorkoutDate)
    day_of_month = func.day(Workout.WorkoutDate)

    rows = (
        db.query(
            WorkoutType.WorkoutName.label("Workout"),
            func.sum(case((day_of_month % 2 == 1, 1), else_=0)).label("Odd"),
            func.sum(case((day_of_month % 2 == 0, 1), else_=0)).label("Even"),
            func.sum(case((day_num == 1, 1), else_=0)).label("Sunday"),
            func.sum(case((day_num == 2, 1), else_=0)).label("Monday"),
            func.sum(case((day_num == 3, 1), else_=0)).label("Tuesday"),
            func.sum(case((day_num == 4, 1), else_=0)).label("Wednesday"),
            func.sum(case((day_num == 5, 1), else_=0)).label("Thursday"),
            func.sum(case((day_num == 6, 1), else_=0)).label("Friday"),
            func.sum(case((day_num == 7, 1), else_=0)).label("Saturday")
        )
        .join(WorkoutType, Workout.WorkoutTypeId == WorkoutType.WorkoutTypeId)
        .group_by(WorkoutType.WorkoutName)
        .order_by(WorkoutType.WorkoutName)
        .all()
    )

    return [
        WorkoutDayOfWeekReportRow(
            Workout=r.Workout,
            Odd =int(r.Odd or 0),
            Even=int(r.Even or 0),
            Sunday=int(r.Sunday or 0),
            Monday=int(r.Monday or 0),
            Tuesday=int(r.Tuesday or 0),
            Wednesday=int(r.Wednesday or 0),
            Thursday=int(r.Thursday or 0),
            Friday=int(r.Friday or 0),
            Saturday=int(r.Saturday or 0),
        )
        for r in rows
    ]