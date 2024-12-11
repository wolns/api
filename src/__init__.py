from fastapi import FastAPI

from src.core.lifespan import lifespan
from src.core.server import Server
from . import models


def create_app(_=None) -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    return Server(app).get_app()
