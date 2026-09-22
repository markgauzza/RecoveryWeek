from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from .database import Base

class WorkoutType(Base):
    __tablename__ = "WorkoutType"

    WorkoutTypeId = Column(Integer, primary_key=True, index=True)
    WorkoutName = Column(String(100), nullable=False)

    workouts = relationship("Workout", back_populates="workout_type")


class Workout(Base):
    __tablename__ = "Workout"

    WorkoutId = Column(Integer, primary_key=True, index=True)
    WorkoutDate = Column(DateTime, nullable=False)
    WorkoutTypeId = Column(Integer, ForeignKey("WorkoutType.WorkoutTypeId"), nullable=False)
    CreateDate = Column(DateTime, nullable=False)
    TotalSeconds = Column(Integer, nullable=True)
    Sequence = Column("Sequence", Integer, nullable=True)   # "Order" is reserved

    workout_type = relationship("WorkoutType", back_populates="workouts")