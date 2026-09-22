from typing import List
from fastapi import Query

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.database import get_db
from app.database import engine, Base
from app.routers import items
from app.schemas import WorkoutCreate, WorkoutResponse, WorkoutOut   # ← Pydantic models
from app.models import Workout          # ← SQLAlchemy model


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
    )

    try:
        db.add(db_workout)
        db.commit()
        db.refresh(db_workout)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Workout with this WorkoutTypeId + Sequence already exists, "
                   "or invalid WorkoutTypeId (foreign key)."
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

from .routers import workouts   # or whatever you named the file

