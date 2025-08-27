from sqlmodel import SQLModel


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
