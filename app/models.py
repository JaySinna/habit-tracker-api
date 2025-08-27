from typing import Optional
from datetime import datetime, date
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Habit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)  # simple FK by id
    name: str
    period: str  # "daily" or "weekly"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Checkin(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    habit_id: int = Field(index=True)  # FK to Habit.id (kept simple)
    day: date
    created_at: datetime = Field(default_factory=datetime.utcnow)
