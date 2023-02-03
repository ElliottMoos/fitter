import logging
from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine
from app.models import *

logger = logging.getLogger(__name__)


async def start_engine(app: FastAPI) -> None:
    try:
        connect_args = {"check_same_thread": False}
        engine = create_engine("sqlite:///database.db", connect_args=connect_args)
        SQLModel.metadata.create_all(engine)
        app.state._engine = engine
    except Exception as e:
        logger.error("--- DB CONNECTION ERROR ---")
        logger.error(e)
        logger.error("--- DB CONNECTION ERROR ---")


async def destroy_engine(app: FastAPI) -> None:
    try:
        app.state._engine = None
    except Exception as e:
        logger.error("--- DB DISCONNECT ERROR ---")
        logger.error(e)
        logger.error("--- DB DISCONNECT ERROR ---")
