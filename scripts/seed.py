from datetime import date, timedelta
from sqlmodel import Session, select
from app.core.db import engine
from app.core.security import hash_password
from app.models import User, Habit, Checkin


def seed():
    with Session(engine) as s:
        # Clear existing demo user if re-seeding
        demo = s.exec(select(User).where(User.email == "demo@demo.dev")).first()
        if demo:
            s.delete(demo)
            s.commit()

        # Create demo user
        demo = User(email="demo@demo.dev", password_hash=hash_password("demo123"))
        s.add(demo)
        s.commit()
        s.refresh(demo)

        # Add a habit
        h = Habit(user_id=demo.id, name="Drink Water", period="daily")
        s.add(h)
        s.commit()
        s.refresh(h)

        # Add some check-ins for the last 5 days
        for i in range(5):
            s.add(Checkin(habit_id=h.id, day=date.today() - timedelta(days=i)))
        s.commit()

    print("✅ Seeded demo user: demo@demo.dev / demo123")


if __name__ == "__main__":
    seed()
