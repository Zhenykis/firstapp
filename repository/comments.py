from datetime import datetime
from email.policy import default
from http.client import HTTPException

from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from models import AdvertType, Advert, Comment
from advert.models import AdvertIn
from models import User
from sqlalchemy import select
from comments.models import CommentIn


class CommentNotFound(Exception): ...


class CommentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_comment(
        self, text: str, user_id: int, advert_id: int, created_at: datetime
    ):
        new_comment = Comment(
            text=text, user_id=user_id, advert_id=advert_id, created_at=created_at
        )

        self.db.add(new_comment)
        await self.db.commit()
        return CommentIn

    async def del_comment(self, comment_id: int):
        try:
            result = await self.db.execute(
                select(Comment).where(Comment.id == comment_id)
            )
            comment = result.scalars().one()
        except NoResultFound as e:
            raise CommentNotFound("Комментарий отсутствует!")

        await self.db.delete(comment)
        await self.db.commit()
