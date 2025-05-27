from fastapi import HTTPException
from logging import exception

import sqlalchemy.exc
from click import password_option
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from auth.schemas import UserIn, UserOut
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy import select
from auth.utils import verify_password


class DoubleNameException(Exception): ...


class UserNotFound(Exception): ...


class  UserRepository:
    def __init__(self,db: AsyncSession):
        self.db = db

    async def create_user(
        self,
        username: str,
        password: bytes,
        is_admin: bool = False,
    ):
        new_user = User(
            username=username,
            password=password,
            is_admin=is_admin,
        )

        self.db.add(new_user)
        try:
            await self.db.commit()
        except IntegrityError as e:
            raise DoubleNameException("Пользователь с таким логином уже существует!")
        return UserOut


    async def del_user(self, user_id: int):
        try:
            result = await self.db.execute(select(User).where(User.id == user_id))
            user = result.scalars().one()

            await self.db.delete(user)
            await self.db.commit()
        except NoResultFound as e:
            raise UserNotFound("Пользователя не существует!")


    async def get_user(self, user_id: int):
        user = await self.db.get(User, user_id)
        if user is None:
            raise UserNotFound(f"Пользователя не существует")
        return user


    async def authenticate_user(self, username: str, password: str):
        try:
            result = await self.db.execute(select(User).where(User.username == username))
            user = result.scalars().one()
        except NoResultFound as e:
            raise UserNotFound("Неверный логин!")
        # if not user:
        #     return False
        if not verify_password(password, user.password):
            raise UserNotFound("Неверный пароль!")
        return user
