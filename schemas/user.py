from pydantic import BaseModel


class UserIn(BaseModel):

    username: str
    password: str


# class UserOut(UserIn):
#     username: str


class UserToken(UserIn):
    token: str

class UserOut(BaseModel):
    id: int
    username: str
    is_admin: bool
