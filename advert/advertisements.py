from fastapi import APIRouter
from starlette import status
from advert.models import AdvertIn
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Depends, status, Response
from auth.schemas import UserIn
from models import User
from repository.advertisements import (
    create_advert,
    UserNotFound,
    delete_advert as del_advert,
    AdvertNotFound,
    get_list_advert,
)
from db_helper import get_db


router = APIRouter(
    prefix="/advertisements",
    tags=["advert"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_advertisement(
    advert_data: AdvertIn, db: AsyncSession = Depends(get_db)
):
    user = await db.get(User, advert_data.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Нет пользователя с таким ID({advert_data.user_id})!",
        )
    db_advert = await create_advert(
        title=advert_data.title,
        description=advert_data.description,
        advert_type=advert_data.type,
        user_id=advert_data.user_id,
        created_at=advert_data.created_at,
        db=db,
    )

    return f"Объявление {advert_data.title} создано!"


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_advert(advert_id: int, db: AsyncSession = Depends(get_db)):
    try:
        advert = await del_advert(advert_id=advert_id, db=db)
    except AdvertNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Объявления №{advert_id} не существует!",
        )


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_advert(limit_advert: int, db: AsyncSession = Depends(get_db)):
    advert = await get_list_advert(limit_advert=limit_advert, db=db)
    return advert
