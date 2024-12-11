from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database.database import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db()
    yield
