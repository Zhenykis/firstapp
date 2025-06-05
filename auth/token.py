from fastapi import Depends

from app.db_helper import get_db
from auth.utils import generate_token
from models.models import User


async def generate_and_set_token(user: User, db: get_db()) -> str:
    token = generate_token()  # Ваша существующая функция генерации токена
    user.token = token
    await db.commit()
    return token