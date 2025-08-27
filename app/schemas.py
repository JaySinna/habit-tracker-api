from sqlmodel import SQLModel
from datetime import date


class UserCreate(SQLModel):
    email: str
    password: str


class TokenOut(SQLModel):
    access_token: str
    token_type: str = "bearer"


class HabitCreate(SQLModel):
    name: str
    period: str  # "daily" | "weekly"


class HabitRead(SQLModel):
    id: int
    name: str
    period: str


class CheckinCreate(SQLModel):
    day: date


class CheckinRead(SQLModel):
    id: int
    habit_id: int
    day: date


class HabitStats(SQLModel):
    id: int
    name: str
    current_streak: int
    longest_streak: int
