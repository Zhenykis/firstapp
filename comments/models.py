from pydantic import BaseModel
from datetime import datetime

class CommentIn(BaseModel):
    text: str
    user_id: int
    advert_id: int
    created_at: datetime
