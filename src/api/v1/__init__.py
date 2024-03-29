from fastapi import APIRouter

from api.v1.users import router as auth_router

router_v1 = APIRouter(prefix="/v1")

router_v1.include_router(auth_router, tags=["user"])
