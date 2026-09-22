from pydantic import BaseModel
from datetime import datetime


class WorkoutTypeOut(BaseModel):
    WorkoutTypeId: int
    WorkoutName: str

    class Config:
        from_attributes = True   # for SQLAlchemy 2.0 / Pydantic v2

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