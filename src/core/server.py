from fastapi import FastAPI

from src.api import api_router


class Server:
    app: FastAPI

    def __init__(self, app: FastAPI) -> None:
        self.app = app
        self.register_routes()

    def get_app(self) -> FastAPI:
        return self.app

    def register_routes(self):
        self.app.include_router(api_router)
