from sqlalchemy import ForeignKey, DATETIME, func, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from enum import StrEnum, Enum
from sqlalchemy import LargeBinary
from datetime import datetime, timezone
from sqlalchemy import DateTime


class Base(DeclarativeBase):
    __abstract__ = True


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes] = mapped_column(LargeBinary)
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_banned: Mapped[bool] = mapped_column(default=False)
    token: Mapped[str] = mapped_column(nullable=True)


class AdvertType(StrEnum):
    VEHICLE = "vehicle"
    ELECTRONICS = "electronics"


class Advert(Base):
    __tablename__ = "advert"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    type: Mapped[AdvertType]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=datetime.now(timezone.utc)
    )
    is_active: Mapped[bool] = mapped_column(
        default=True,
        server_default=text('true'),
        nullable=False)

# таблица user (user_name, password, is_admin, is_banned)
# таблица обьявления (названия обьявления, описание, тип обьявления(группа),
# таблица с комментариями к обьявлениям (текст и время создания)


# сделать нинициализацию алембика
# сделать миграцию алембика (постараться сделать так, чтобы каждая таблица была в новой миграции)
# нужно накатить миграции на новую базу
