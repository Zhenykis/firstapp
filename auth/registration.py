from idlelib.rpc import response_queue

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Depends, status, Response, Request
from starlette.responses import JSONResponse
from sqlalchemy import update
from auth.utils import get_password_hash, generate_token
from repository.user import (
    create_user,
    DoubleNameException,
    delete_user as del_user,
    get_user,
    UserNotFound,
    authenticate_user,
)
from auth.schemas import UserIn
from db_helper import get_db
from models import User

router = APIRouter(
    prefix="/reg",
    tags=["registration"],
)


@router.post("/registration/", status_code=status.HTTP_201_CREATED)
async def registration_users(user_data: UserIn, db: AsyncSession = Depends(get_db)):
    hash_password = get_password_hash(user_data.password)
    try:
        db_user = await create_user(
            username=user_data.username, password=hash_password, db=db, is_admin=False
        )
    except DoubleNameException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Пользователь {user_data.username} уже существует!",
        )
    return f"Пользователь {user_data.username} создан!"


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    request: Request, user_id: int, db: AsyncSession = Depends(get_db)
):

    if not hasattr(request.state, "user"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Требуется авторизация!"
        )

    try:
        remove_user = await del_user(user_id=user_id, db=db)
    except UserNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователя не существует!"
        )


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        user = await get_user(user_id=user_id, db=db)
        return user
    except UserNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователя не существует!"
        )


@router.post("/authenticate/", status_code=status.HTTP_200_OK)
async def auth_user(
    response: Response, user_data: UserIn, db: AsyncSession = Depends(get_db)
):
    try:
        user = await authenticate_user(
            username=user_data.username, password=user_data.password, db=db
        )
    except UserNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Неверный логин или пароль!"
        )

    token = generate_token()
    user.token = token
    await db.commit()

    response.set_cookie(key="user_cookie", value=user.token)

    return f"Пользователь {user_data.username} успешно авторизован!"


@router.post("/logout/", status_code=status.HTTP_200_OK)
async def logout_user(request: Request, db: AsyncSession = Depends(get_db)):
    if not hasattr(request.state, "user"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Не авторизован!"
        )
    user_token = request.state.user.token
    result = await db.execute(
        update(User).where(User.token == user_token).values(token=None)
    )
    # token = result.scalars().first()
    # if User.token == None:
    # await db.delete(token)
    await db.commit()
    response = JSONResponse(content={"msg": "Успешный выход!"})
    response.delete_cookie("user_cookie")
    return response
