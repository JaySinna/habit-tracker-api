from fastapi import FastAPI
from contextlib import asynccontextmanager
from .core.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs at startup
    init_db()
    yield
    # Runs at shutdown (if you ever need cleanup)
    # e.g. close connections, clear caches

app = FastAPI(title="Habit Tracker API", version="0.1.0", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}
