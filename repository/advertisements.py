from datetime import datetime
from math import ceil

from sqlalchemy.exc import NoResultFound

from app.core.db_helper import get_db
from models.models import AdvertType, Advert
from schemas.advert import AdvertIn, AdvertOut
from models.models import User
from sqlalchemy import select, func, insert
from sqlalchemy.orm import selectinload
from typing import Annotated, Optional
from fastapi import Query
class UserNotFound(Exception): ...
from schemas.advert import PaginatedAdverts

class AdvertNotFound(Exception): ...


class CurrentUserError(Exception): ...


class AdvertRepository:
    def __init__(self):
        self._db = get_db()
        self._table = Advert
        self._user = User

    async def create_advert(
        self,
        title: str,
        description: str,
        advert_type: AdvertType,
        created_at: datetime,
        user_id: int,
    ):


        user = await self._db.fetch_one(select(self._user).where(self._user.id == user_id))

        if not user:
            raise UserNotFound(f"Нет пользователя с таким ID({user_id})!")

        new_advert = insert(self._table).values(
            title=title,
            description=description,
            type=advert_type,
            created_at=created_at,
            user_id=user_id,
        ).returning(self._table)

        return AdvertOut(**new_advert)

    async def delete_advert(self, advert_id: int, current_user: User):
        try:
            result = await self._db.execute(select(Advert).where(Advert.id == advert_id))
            advert = result.scalars().one()

            if advert.user_id != current_user.id:
                raise CurrentUserError(
                    "Данный пользователь не может удалить объявление!"
                )

            await self.db.delete(advert)
            await self.db.commit()
        except NoResultFound as e:
            raise AdvertNotFound("Объявления не существует!")

    async def get_list_advert(
            self,
            page: Annotated[int, Query(description="Номер страницы", ge=1)]  = 1,
            per_page: Annotated[int, Query(description="Количество элементов на странице", ge=1,le=10)] = 10,
            advert_type: Annotated[Optional[AdvertType], Query(description="Фильтр по типу объявления")] = None,
            is_active: Annotated[Optional[bool], Query(description="Фильтр статуса объявления")] = None,

    ):
        query = select(Advert).options(selectinload(Advert.comments))

        if advert_type is not None:
            query = query.where(Advert.type == advert_type)
        if is_active is not None:
            query = query.where(Advert.is_active == is_active)

        count_advert = select(func.count()).select_from(query.subquery())
        total_result =  await self.db.execute(count_advert)
        total_advert = total_result.scalar()

        offset = (page -1) * per_page
        total_pages = ceil(total_advert / per_page) if total_advert > 0 else 1

        query = query.order_by(Advert.created_at.desc()).offset(offset).limit(per_page)
        result = await self.db.execute(query)
        adverts = result.unique().scalars().all()

        adverts_in = [
            AdvertIn(
                advert_id= advert.id,
                title= advert.title,
                description= advert.description,
                type= advert.type,
                user_id=advert.user_id,
                created_at=advert.created_at,
            )
            for advert in adverts
        ]
        return PaginatedAdverts(
            items=adverts_in,
            total=total_advert,
            page=page,
            per_page=per_page,
            total_pages=total_pages,
        )

        # result = await self.db.execute(select(Advert).limit(limit_advert))
        # all_advert = result.scalars().all()
        # return all_advert


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
