from typing import Callable
from fastapi import FastAPI

from app.db.tasks import start_engine, destroy_engine


def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        await start_engine(app)

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    async def stop_app() -> None:
        await destroy_engine(app)

    return stop_app
