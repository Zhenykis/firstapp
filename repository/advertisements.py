from datetime import datetime
from email.policy import default

from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from models import AdvertType, Advert
from advert.models import AdvertIn
from models import User
from sqlalchemy import select


class UserNotFound(Exception): ...


class AdvertNotFound(Exception): ...


async def create_advert(
    db: AsyncSession,
    title: str,
    description: str,
    advert_type: AdvertType,
    created_at: datetime,
    user_id: int,
):
    new_advert = Advert(
        title=title,
        description=description,
        type=advert_type,
        created_at=created_at,
        user_id=user_id
    )

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().one_or_none()
    if not user:
        raise UserNotFound(f"Нет пользователя с таким ID({user_id})!")

    db.add(new_advert)
    await db.commit()
    return AdvertIn


async def delete_advert(db: AsyncSession, advert_id: int):
    try:
        result = await db.execute(select(Advert).where(Advert.id == advert_id))
        advert = result.scalars().one()

        await db.delete(advert)
        await db.commit()
    except NoResultFound as e:
        raise AdvertNotFound("Объявления не существует!")


async def get_list_advert(db: AsyncSession, limit_advert: int):
    result = await db.execute(select(Advert).limit(limit_advert))
    all_advert = result.scalars().all()
    return all_advert
