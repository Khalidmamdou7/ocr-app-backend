# registration of all system routes (fastapi)

from fastapi import APIRouter
from .auth.router import router as auth_router
from .production_lines.router import router as production_lines_router
from .pet_lines.router import router as pet_lines_router
from .machines.router import router as machines_router
from .counters.router import router as counters_router

routes = APIRouter()

routes.include_router(auth_router, prefix="/auth", tags=["auth"])
routes.include_router(production_lines_router, prefix="/production-lines", tags=["production_lines"])
routes.include_router(pet_lines_router, prefix="/pet-lines", tags=["pet_lines"])
routes.include_router(machines_router, prefix="/machines", tags=["machines"])
routes.include_router(counters_router, prefix="/counters", tags=["counters"])