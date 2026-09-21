from sqlalchemy import Column, Integer, String
from .database import Base

class WorkoutType(Base):
    __tablename__ = "WorkoutType"   # ← change to your real table name

    WorkoutTypeId = Column(Integer, primary_key=True, index=True)
    WorkoutName = Column(String(350), unique=True, nullable=False)
    