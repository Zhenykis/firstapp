from fastapi import APIRouter, HTTPException, Depends, status, Response, Request

import settings
from auth.utils import get_password_hash, generate_token
from repository.user import UserRepository, DoubleNameException

from schemas.user import UserIn, UserOut

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post("/registration/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def registration_users(user_data: UserIn, user_repository: UserRepository = Depends()):
    hash_password = get_password_hash(user_data.password)
    try:
        db_user = await user_repository.create_user(user_data, hash_password, is_admin=False, is_banned=False)
    except DoubleNameException as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex),
        )
    return db_user


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(request: Request, user_id: int, user_repository: UserRepository = Depends()):
    # TODO: перенести в middleweare
    if not hasattr(request.state, "user"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Требуется авторизация!"
        )
    await user_repository.del_user(user_id=user_id)


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserOut)
async def get_user_by_id(user_id: int, user_repository: UserRepository = Depends()):
    user = await user_repository.get_user(user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )
    return user


@router.post("/authenticate", status_code=status.HTTP_200_OK)
async def auth_user(
    response: Response,
    user_data: UserIn,
    user_repository: UserRepository = Depends(),
):
    user = await user_repository.authenticate_user(
        username=user_data.username, password=user_data.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid password or username"
        )
    # TODO: перенести в сервисный слой
    token = generate_token()
    await user_repository.update(user_id=user.id,token=token)
    response.set_cookie(key=settings.COOKIES_KEY, value=token)
    return user


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout_user(request: Request, response: Response, user_repository: UserRepository = Depends()):
    # TODO: перенести в middleweare
    if not hasattr(request.state, "user"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    await user_repository.update(user_id=request.state.id,token=None)
    response.delete_cookie(settings.COOKIES_KEY)
