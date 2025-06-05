from app.db_helper import get_db
from models.models import User
from schemas.user import UserOut, UserReg
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy import select
from auth.utils import verify_password
from schemas.user import UserIn

class DoubleNameException(Exception): ...


class UserNotFound(Exception): ...


class UserRepository:
    def __init__(self):
        self._db = get_db()
        self._table = User

    async def create_user(
        self,
      data: UserReg,
    ):
        new_user = self._table(
            username=data.username,
            password=data.password,
            is_admin=data.is_admin,
        )

        self._db.add(new_user)
        try:
            await self._db.commit()
        except IntegrityError as e:
            raise DoubleNameException("Пользователь с таким логином уже существует!")
        return UserOut

    async def del_user(self, user_id: int):
        try:
            result = await self._db.execute(select(self._table).where(self._table.id == user_id))
            user = result.scalars().one()

            await self._db.delete(user)
            await self._db.commit()
        except NoResultFound as e:
            raise UserNotFound("Пользователя не существует!")

    async def get_user(self, user_id: int):
        user = await self._db.get(self._table, user_id)
        if user is None:
            raise UserNotFound(f"Пользователя не существует")
        return user

    async def authenticate_user(self, username: str, password: str):
        try:
            result = await self._db.execute(
                select(self._table).where(self._table.username == username)
            )
            user = result.scalars().one()
        except NoResultFound as e:
            raise UserNotFound("Неверный логин!")
        # if not user:
        #     return False
        if not verify_password(password, user.password):
            raise UserNotFound("Неверный пароль!")
        return user
