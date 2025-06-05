from databases import Database
from main import app

import settings
from app.exception import DBInitError

_global: dict[str, Database] = {}
DATABASE_URL = f"postgresql+asyncpg://{settings.BD_USER}:{settings.BD_PASSWORD}@{settings.APP_HOST}:{settings.BD_PORT}/{settings.BD_NAME}"


@app.on_event("startup")
async def init_db():
    _global["db"] = Database(DATABASE_URL)
    await _global["db"].connect()


@app.on_event("shutdown")
async def close_db():
    await _global["db"].disconnect()


def get_db():
    if not _global.get("db"):
        raise DBInitError()
    return _global["db"]
