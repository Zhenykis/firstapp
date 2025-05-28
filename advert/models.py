from datetime import datetime
from pydantic import BaseModel, ConfigDict
from enum import Enum, StrEnum
from comments.models import CommentIn
from typing import List

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

class AdvertWithComments(AdvertOut):
    comments: List[CommentIn]


class PaginatedAdverts(BaseModel):
    items: List[AdvertIn]
    total: int
    page: int
    per_page: int
    total_pages: int