from typing import List
from fastapi import Query

from sqlalchemy import func, case, cast, Date
from sqlalchemy.exc import IntegrityError
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.database import get_db
from app.database import engine, Base
from app.routers import workouts

from app.schemas import WorkoutCreate, WorkoutResponse, WorkoutOut, WorkoutDailySummary, WorkoutTypeOut, PaginatedDailySummary
from app.models import Workout, WorkoutType
from datetime import datetime



Base.metadata.create_all(bind=engine)  # for small apps; prefer Alembic later

app = FastAPI(title="Recovery Week API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4300"],  # Angular dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(workouts.router, prefix="/api")


PaginatedDailySummary.model_rebuild()

