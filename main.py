from email.policy import default
import uvicorn
from fastapi import FastAPI
from auth.registration import router as reg_router
from advert.advertisements import router as advert_router
from auth.auth_middleware import AuthMiddleWare
from comments.comments import router as comment_router

app = FastAPI()

app.include_router(reg_router)
app.include_router(advert_router)
app.add_middleware(AuthMiddleWare)
app.include_router(comment_router)


@app.get("/")
async def first_step():
    return {"msg:": "Road to InlyIT"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


# таблица user (user_name, password, is_admin, is_banned)
# таблица обьявления (названия обьявления, описание, тип обьявления(группа),
# таблица с комментариями к обьявлениям (текст и время создания)
