from fastapi import APIRouter

from .routes import router as router_organizations

router = APIRouter()
router.include_router(router_organizations)
