from fastapi import APIRouter

from app.api.v1.controllers import *

api_router = APIRouter()

api_router.include_router(
    router,
    tags=["movies"]
)