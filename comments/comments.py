from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Depends, status, Response
from auth.schemas import UserIn
from models import User
from repository.comments import CommentNotFound

from db_helper import get_db
from comments.models import CommentIn

from repository.comments import CommentRepository

router = APIRouter(
    prefix="/comments",
    tags=["comment"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_comment(comment_data: CommentIn, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, comment_data.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Нет пользователя с таким ID!"
        )
    db_comment = await CommentRepository(db).create_comment(
        text=comment_data.text,
        user_id=comment_data.user_id,
        advert_id=comment_data.advert_id,
        created_at=comment_data.created_at,
    )

    return f"Комментарий к объявлению создан!"


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(comment_id: int, db: AsyncSession = Depends(get_db)):
    try:
        await CommentRepository(db).del_comment(comment_id=comment_id)
    except CommentNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Комментарий отсутствует!"
        )
