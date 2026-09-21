from pydantic import BaseModel

class WorkoutTypeOut(BaseModel):
    WorkoutTypeId: int
    WorkoutName: str

    class Config:
        from_attributes = True   # for SQLAlchemy 2.0 / Pydantic v2