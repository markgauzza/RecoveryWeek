from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import Workout, WorkoutType
from ..schemas import WorkoutOut

router = APIRouter(
    prefix="/workouts",
    tags=["workouts"]
)

def format_duration(total_seconds: int | None) -> str:
    if total_seconds is None:
        return "00:00:00"
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


@router.get("/", response_model=List[WorkoutOut])
def get_workouts(db: Session = Depends(get_db)):
    results = (
        db.query(
            Workout.WorkoutId,
            WorkoutType.WorkoutName,
            Workout.WorkoutDate,
            Workout.TotalSeconds
        )
        .join(WorkoutType, Workout.WorkoutTypeId == WorkoutType.WorkoutTypeId)
        .order_by(Workout.WorkoutDate.desc())
        .all()
    )

    return [
        WorkoutOut(
            WorkoutId=row.WorkoutId,
            WorkoutName=row.WorkoutName,
            WorkoutDate=row.WorkoutDate,
            TotalDuration=format_duration(row.TotalSeconds)
        )
        for row in results
    ]