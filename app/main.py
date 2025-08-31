from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .core.db import init_db
from . import models  # ensure models are imported before init_db()
from .routers import auth, habits, checkins


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables at startup (Postgres on Heroku or SQLite locally)
    init_db()
    yield
    # Place for any shutdown cleanup if needed


app = FastAPI(
    title="Habit Tracker API",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/", include_in_schema=False)
def root():
    # Redirect the homepage to the interactive API docs
    return RedirectResponse(url="/docs")


# Routes
app.include_router(auth.router)
app.include_router(habits.router)
app.include_router(checkins.router)


# Simple healthcheck (kept public)
@app.get("/health", include_in_schema=False)
def health():
    return {"status": "ok"}
