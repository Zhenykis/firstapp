import settings

DATABASE_URL = f"postgresql+asyncpg://{settings.BD_USER}:{settings.BD_PASSWORD}@{settings.APP_HOST}:{settings.BD_PORT}/{settings.BD_NAME}"