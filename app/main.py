
import uvicorn
from fastapi import FastAPI
from app.api.public.registration import router as reg_router
from app.api.public.advertisement import router as advert_router
from auth.auth_middleware import AuthMiddleWare
from app.api.public.comment import router as comment_router

app = FastAPI()

app.include_router(reg_router)
app.include_router(advert_router)
app.add_middleware(AuthMiddleWare)
app.include_router(comment_router)




if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

