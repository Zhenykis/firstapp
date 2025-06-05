from advert.models import AdvertIn

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Depends, status
from models import User, Advert
from repository.advertisements import (
    AdvertRepository,
    AdvertNotFound,
    CurrentUserError,
    AdvertType
)
from app.db_helper import get_db
from auth.current_user import get_current_user
from advert.models import PaginatedAdverts
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
    current_user: User = Depends(get_current_user),
):
    try:
        advert = await AdvertRepository(db).delete_advert(
            advert_id=advert_id, current_user=current_user
        )
    except AdvertNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Объявление не существует!",
        )
    except CurrentUserError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.get("/",response_model=PaginatedAdverts, status_code=status.HTTP_200_OK)
async def get_all_advert(page: int,
                         per_page: int,
                         advert_type: AdvertType,
                         is_active:bool,
                         db: AsyncSession = Depends(get_db)):
    return await AdvertRepository(db).get_list_advert(
        page=page,
        per_page=per_page,
        advert_type=advert_type,
        is_active=is_active
    )
    #return advert


@router.get("/{advert_id}", status_code=status.HTTP_200_OK)
async def get_advert(advert_id: int, db: AsyncSession = Depends(get_db)):
    advert = await db.get(Advert, advert_id)
    if not advert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Объявление отсутствует!"
        )
    full_advert = await AdvertRepository(db).get_full_advert(advert_id=advert_id)
    return full_advert
