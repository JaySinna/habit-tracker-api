from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..core.db import get_session
from ..models import Habit
from ..schemas import HabitCreate, HabitRead
from .auth import get_current_user, User

router = APIRouter(prefix="/habits", tags=["habits"])


@router.get("", response_model=list[HabitRead])
def list_habits(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    q = select(Habit).where(Habit.user_id == user.id).order_by(Habit.id)
    return session.exec(q).all()


@router.post("", response_model=HabitRead, status_code=201)
def create_habit(
    payload: HabitCreate,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    if payload.period not in {"daily", "weekly"}:
        raise HTTPException(status_code=422, detail="period must be daily|weekly")
    habit = Habit(user_id=user.id, name=payload.name, period=payload.period)
    session.add(habit)
    session.commit()
    session.refresh(habit)
    return habit
