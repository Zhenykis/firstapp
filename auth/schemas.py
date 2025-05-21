from pydantic import BaseModel


class UserIn(BaseModel):
    username: str
    password: str


class UserOut(UserIn):
    username: str


class UserToken(UserIn):
    token: str
