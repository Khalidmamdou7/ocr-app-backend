# registration of all system routes (fastapi)

from fastapi import APIRouter
from .auth.router import router as auth_router

routes = APIRouter()

routes.include_router(auth_router, prefix="/auth", tags=["auth"])