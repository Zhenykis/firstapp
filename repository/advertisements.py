from datetime import datetime
from email.policy import default

from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from models import AdvertType, Advert
from advert.models import AdvertIn
from models import User
from sqlalchemy import select
from sqlalchemy.orm import selectinload

class UserNotFound(Exception): ...


class AdvertNotFound(Exception): ...


class CurrentUserError(Exception):
    ...


class AdvertRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    async def create_advert(
        self,
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
            user_id=user_id,
        )

        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalars().one_or_none()
        if not user:
            raise UserNotFound(f"Нет пользователя с таким ID({user_id})!")

        self.db.add(new_advert)
        await self.db.commit()
        return AdvertIn


    async def delete_advert(self, advert_id: int, current_user: User):
        try:
            result = await self.db.execute(select(Advert).where(Advert.id == advert_id))
            advert = result.scalars().one()

            if advert.user_id != current_user.id:
                raise CurrentUserError ("Данный пользователь не может удалить объявление!")

            await self.db.delete(advert)
            await self.db.commit()
        except NoResultFound as e:
            raise AdvertNotFound("Объявления не существует!")


    async def get_list_advert(self, limit_advert: int):
        result = await self.db.execute(select(Advert).limit(limit_advert))
        all_advert = result.scalars().all()
        return all_advert



    async def get_full_advert(self, advert_id: int):
        try:
            result = await self.db.execute(
                select(Advert)
                .where(Advert.id == advert_id)
                .options(selectinload(Advert.comments))
            )
            full_advert = result.scalars().one()
        except NoResultFound as e:
            raise AdvertNotFound("Объявления не существует!")
        return full_advert