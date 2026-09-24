from pydantic import BaseModel
from datetime import datetime
from datetime import date

class PaginatedDailySummary(BaseModel):
    total: int
    skip: int
    limit: int
    items: List[WorkoutDailySummary]

class WorkoutTypeOut(BaseModel):
    WorkoutTypeId: int
    WorkoutName: str

    class Config:
        from_attributes = True   # for SQLAlchemy 2.0 / Pydantic v2

class WorkoutDailySummary(BaseModel):
    WorkoutDate: date
    Workouts: str                    # e.g. "Running, Cycling, Yoga"
    DayOfWeek: str                   # e.g. "Monday"
    DayParity: str                   # "Odd" or "Even"
    Sequence: int

    class Config:
        from_attributes = True


class WorkoutOut(BaseModel):
    WorkoutId: int
    WorkoutDate: datetime
    WorkoutTypeId: int
    CreateDate: datetime
    TotalSeconds: int | None = None
    Sequence: int | None = None

    class Config:
        from_attributes = True


class WorkoutCreate(BaseModel):
    WorkoutTypeId: int
    WorkoutDate: datetime | None = None
    TotalSeconds: int | None = None
    Sequence: int | None = None

class WorkoutResponse(BaseModel):
    WorkoutId: int
    WorkoutDate: datetime
    WorkoutTypeId: int
    CreateDate: datetime
    TotalSeconds: int | None
    Sequence: int | None

    class Config:
        from_attributes = True

WorkoutDailySummary.model_rebuild()

        