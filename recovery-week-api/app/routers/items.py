from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import WorkoutType
from ..schemas import WorkoutTypeOut

router = APIRouter(
    prefix="/workouts",          # final URL will be /api/lookups/...
    tags=["workouts"]
)

@router.get("/types", response_model=List[WorkoutTypeOut])
def get_workout_types(db: Session = Depends(get_db)):
    """
    Returns the full list from the lookup table.
    """
    items = db.query(WorkoutType).order_by(WorkoutType.WorkoutName).all()
    return items