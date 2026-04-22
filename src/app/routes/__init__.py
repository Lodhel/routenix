from fastapi import APIRouter

from src.app.routes.includes_routes import include_all_routes


router = APIRouter()
include_all_routes(router)

__all__ = ["router"]
