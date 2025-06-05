from sqlalchemy.exc import NoResultFound
from models.models import Comment
from sqlalchemy import insert, delete
from repository.user import UserRepository
from schemas.comment import CommentIn
from app.db_helper import get_db

class CommentNotFound(Exception): ...


class CommentRepository:
    def __init__(self):
        self.db = get_db()
        self._table = Comment
        self._user_repository = UserRepository()

    async def create_comment(
            self, data: CommentIn
    ) -> None:
        user = await self._user_repository.get_user(data.user_id)
        if not user:
            return

        stmt = insert(self._table).values(data.dict())

        await self.db.execute(stmt)

    async def del_comment(self, comment_id: int):
        stmt = delete(self._table).where(self._table.id == comment_id)
        await self.db.execute(stmt)
