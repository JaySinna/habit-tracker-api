from __future__ import annotations
from datetime import timedelta
from sqlmodel import Session, select
from ..models import Checkin


def compute_daily_streaks(session: Session, habit_id: int) -> tuple[int, int]:
    # Get all check-in days sorted
    days = session.exec(
        select(Checkin.day).where(Checkin.habit_id == habit_id).order_by(Checkin.day)
    ).all()
    if not days:
        return 0, 0

    longest = current = 1
    prev = days[0]
    for d in days[1:]:
        if d == prev + timedelta(days=1):
            current += 1
            if current > longest:
                longest = current
        elif d == prev:
            # ignore duplicates if they ever slipped in
            pass
        else:
            current = 1
        prev = d

    # current streak is based on the tail of the sequence
    # Recompute from the end backwards to be safe
    tail = 1
    i = len(days) - 1
    while i > 0 and days[i] == days[i-1] + timedelta(days=1):
        tail += 1
        i -= 1
    current = tail
    return current, longest
