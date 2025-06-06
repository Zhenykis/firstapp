from fastapi import APIRouter
from app.api.public.comment import router as comment_router
from app.api.public.advertisement import  router as advert_router
from app.api.public.user import router as reg_router


router = APIRouter()

router.include_router(comment_router)
router.include_router(advert_router)
router.include_router(reg_router)