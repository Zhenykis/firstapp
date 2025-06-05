from fastapi import APIRouter
from comment import router as comment_router
from advertisement import  router as advert_router
from registration import router as reg_router


router = APIRouter()

router.include_router(comment_router)
router.include_router(advert_router)
router.include_router(reg_router)