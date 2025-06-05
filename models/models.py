from sqlalchemy import ForeignKey, DATETIME, func, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
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

    comments: Mapped[list["Comment"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


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
        default=datetime.now(timezone.utc),
    )
    is_active: Mapped[bool] = mapped_column(
        default=True, server_default=text("true"), nullable=False
    )

    comments: Mapped[list["Comment"]] = relationship(
        back_populates="advert", cascade="all, delete-orphan"
    )
    # comments = relationship("Comment", back_populates="advert", cascade="all, delete-orphan")


class Comment(Base):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    advert_id: Mapped[int] = mapped_column(ForeignKey("advert.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=datetime.now(timezone.utc),
    )

    user = relationship("User", back_populates="comments")
    advert = relationship("Advert", back_populates="comments")
