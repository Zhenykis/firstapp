from os.path import defpath

from fastapi import APIRouter
from starlette import status
from advert.models import AdvertIn
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Depends, status, Response
from auth.auth_middleware import AuthMiddleWare
from models import User, Advert
from repository.advertisements import (
    AdvertRepository,
    UserNotFound,
    AdvertNotFound,
    CurrentUserError
)
from db_helper import get_db
from auth.current_user import get_current_user

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
            detail=f"Нет пользователя с таким ID!",
        )
    db_advert = await AdvertRepository(db).create_advert(
        title=advert_data.title,
        description=advert_data.description,
        advert_type=advert_data.type,
        user_id=advert_data.user_id,
        created_at=advert_data.created_at,
    )

    return f"Объявление создано!"


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_advert(
        advert_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    try:
        advert = await AdvertRepository(db).delete_advert(
            advert_id=advert_id,
            current_user=current_user
        )
    except AdvertNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Объявление не существует!",
        )
    except CurrentUserError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )



@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_advert(limit_advert: int, db: AsyncSession = Depends(get_db)):
    advert = await AdvertRepository(db).get_list_advert(limit_advert=limit_advert)
    return advert


@router.get("/{advert_id}", status_code=status.HTTP_200_OK)
async def get_advert(advert_id: int, db: AsyncSession = Depends(get_db)):
    advert =  await db.get(Advert, advert_id)
    if not advert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Объявление отсутствует!"
        )
    full_advert = await AdvertRepository(db).get_full_advert(advert_id=advert_id)
    return full_advert


