from pydantic import BaseModel


class UserIn(BaseModel):
    username: str
    password: bytes
    is_admin: bool = False


class UserOut(UserIn):
    username: str


class UserToken(UserIn):
    token: str

class UserReg(BaseModel):
    username: str
    password: str
    is_admin: bool = False
