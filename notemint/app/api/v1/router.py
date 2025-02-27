from fastapi import APIRouter

from app.api.v1.endpoints import compositions

router = APIRouter()
router.include_router(compositions.router, prefix="/compositions", tags=["compositions"])