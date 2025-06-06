from datetime import datetime
from pydantic import BaseModel
from enum import StrEnum


class AdvertType(StrEnum):
    VEHICLE = "vehicle"
    ELECTRONICS = "electronics"

class AdvertIn(BaseModel):
    advert_id: int
    title: str
    description: str
    type: AdvertType
    user_id: int
    created_at: datetime

class AdvertOut(BaseModel):
    advert_id: int
    title: str
    description: str
    type: AdvertType
    user_id: int
    created_at: datetime

# class AdvertWithComments(AdvertOut):
#     comments: List[CommentIn]


class PaginatedAdverts(BaseModel):
    items: list[AdvertIn]
    total: int
    page: int
    per_page: int
    total_pages: int