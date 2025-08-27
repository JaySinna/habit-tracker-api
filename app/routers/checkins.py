from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..core.db import get_session
from ..models import Habit, Checkin
from ..schemas import CheckinCreate, CheckinRead, HabitStats
from .auth import get_current_user, User
from ..services.streaks import compute_daily_streaks

router = APIRouter(prefix="/habits", tags=["checkins"])


@router.post("/{habit_id}/checkins", response_model=CheckinRead, status_code=201)
def add_checkin(
    habit_id: int,
    payload: CheckinCreate,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    habit = session.get(Habit, habit_id)
    if not habit or habit.user_id != user.id:
        raise HTTPException(status_code=404, detail="Habit not found")

    exists = session.exec(
        select(Checkin).where(Checkin.habit_id == habit_id, Checkin.day == payload.day)
    ).first()
    if exists:
        raise HTTPException(status_code=409, detail="Already checked in for this day")

    c = Checkin(habit_id=habit_id, day=payload.day)
    session.add(c)
    session.commit()
    session.refresh(c)
    return c


@router.get("/stats", response_model=list[HabitStats])
def stats(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    habits = session.exec(select(Habit).where(Habit.user_id == user.id)).all()
    out: list[HabitStats] = []
    for h in habits:
        if h.period == "daily":
            current, longest = compute_daily_streaks(session, h.id)
        else:
            # Simple placeholder for weekly (you can enhance later)
            current, longest = 0, 0
        out.append(HabitStats(id=h.id, name=h.name, current_streak=current, longest_streak=longest))
    return out
