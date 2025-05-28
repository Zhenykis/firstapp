from fastapi import Depends, Request, HTTPException, status


async def get_current_user(request: Request):
    if not hasattr(request.state, "user"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Требуется аутентификация!"
        )
    return request.state.user
