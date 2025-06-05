from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException, status
from starlette.middleware.base import RequestResponseEndpoint
from app.db_helper import AsyncSessionLocal
from models import User
from sqlalchemy import select


class AuthMiddleWare(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):

        if request.url.path in [
            "/reg/authenticate/",
            "/reg/registration/",
            "/docs",
            "/docs#",
            "/openapi.json",
            "/favicon.ico",
            "/",
        ]:
            return await call_next(request)

        token = request.cookies.get("user_cookie")
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Отсутствует токен!"
            )

        db = AsyncSessionLocal()
        result = await db.execute(select(User).where(User.token == token))
        user_token_db = result.scalars().first()

        try:
            if not user_token_db:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Неверный токен!"
                )

            request.state.user = user_token_db
            return await call_next(request)
        finally:
            await db.close()
