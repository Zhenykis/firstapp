
from databases import Database

import settings

_global: dict[str, Database] = {}
DATABASE_URL = f"postgresql+asyncpg://{settings.BD_USER}:{settings.BD_PASSWORD}@{settings.APP_HOST}:{settings.BD_PORT}/{settings.BD_NAME}"

class DBInitError(Exception): ...

async def init_db():
    _global["db"] = Database(DATABASE_URL)
    await _global["db"].connect()


async def close_db():
    await _global["db"].disconnect()


def get_db():
    if not _global.get("db"):
        raise DBInitError()
    return _global["db"]




# from databases import Database
# #from app.main import app
# from app.core.config import DATABASE_URL
# import settings
# from app.exception import DBInitError
# from contextlib import asynccontextmanager
# from fastapi import FastAPI
#
#
# _global: dict[str, Database] = {}
#
#
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Старт приложения (аналог startup)
#     _global["db"] = Database(DATABASE_URL)
#     await _global["db"].connect()
#
#     yield  # Здесь приложение работает
#
#     # Завершение (аналог shutdown)
#     await _global["db"].disconnect()
#
#
# def get_db() -> Database:
#     if not _global.get("db"):
#         raise DBInitError()
#     return _global["db"]
#
#
#
#
#

# @app.on_event("startup")
# async def init_db():
#     _global["db"] = Database(DATABASE_URL)
#     await _global["db"].connect()
#
#
# @app.on_event("shutdown")
# async def close_db():
#     await _global["db"].disconnect()
#
#
# def get_db():
#     if not _global.get("db"):
#         raise DBInitError()
#     return _global["db"]
