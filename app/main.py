
import uvicorn
from fastapi import FastAPI
from app.core.db_helper import init_db, close_db
from auth.auth_middleware import AuthMiddleWare
import settings

app = FastAPI()
#app.add_middleware(AuthMiddleWare)

@app.on_event('startup')
async def on_startup():
    # TODO: перенсти в __init__, чтобы не было понятно от куда тянутся
    from app.api.public.user import router as reg_router
    from app.api.public.advertisement import router as advert_router
    from app.api.public.comment import router as comment_router

    await init_db()

    app.include_router(reg_router)
    app.include_router(advert_router)
    app.include_router(comment_router)


@app.on_event("shutdown")
async def on_shutdown():
    await close_db()


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=True)





















# import uvicorn
# from fastapi import FastAPI
# from app.api.public.user import router as reg_router
# from app.api.public.advertisement import router as advert_router
# from auth.auth_middleware import AuthMiddleWare
# from app.api.public.comment import router as comment_router
# from core.db_helper import lifespan
#
# app = FastAPI(lifespan=lifespan)
#
# app.include_router(reg_router)
# app.include_router(advert_router)
# app.add_middleware(AuthMiddleWare)
# app.include_router(comment_router)
#
#
#
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
#
