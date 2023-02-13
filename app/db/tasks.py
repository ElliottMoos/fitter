import logging

from fastapi import FastAPI
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection
from sqlmodel import create_engine

from app.models import *
from app.core.settings import settings

logger = logging.getLogger(__name__)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


async def start_engine(app: FastAPI) -> None:
    try:
        engine = create_engine(settings.DB_URL)
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
