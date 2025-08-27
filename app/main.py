from fastapi import FastAPI
from contextlib import asynccontextmanager
from .core.db import init_db
from .routers import auth, habits


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Habit Tracker API", version="0.1.0", lifespan=lifespan)

app.include_router(auth.router)
app.include_router(habits.router)


@app.get("/health")
def health():
    return {"status": "ok"}
