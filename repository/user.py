

from app.db_helper import get_db
from models.models import User
from schemas.user import UserOut, UserReg
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy import select, insert, delete, update
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
        hash_password: bytes,
        is_admin: bool,
    ) -> UserOut:
        stmt = insert(self._table).values(
            username=data.username,
            password=hash_password,
            is_admin=is_admin,
        )
        try:
            result = await self._db.execute(stmt)
        except IntegrityError:
            raise DoubleNameException("User already exist")
        return UserOut(**result)

    async def del_user(self, user_id: int):
        stmt = delete(self._table).where(self._table.id == user_id)
        await self._db.execute(stmt)

    async def get_user(self, user_id: int) -> UserOut | None:
        stmt = select(self._table).where(self._table.id == user_id)
        user = await self._db.execute(stmt)
        return UserOut(**user) if user else None

    async def authenticate_user(self, username: str, password: str) -> UserOut | None:

        result = await self._db.execute(
            select(self._table).where(self._table.username == username)
        )
        if not result:
            return None

        if not verify_password(password, result.password):
            return None

        return UserOut(**result)

    async def update(self, token: str):
        result = await self._db.execute(
            update(User).where(User.token == token).values(token=None)
        )
        return result
