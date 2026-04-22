from fastapi import APIRouter

from src.app.routes.includes_routes.default import include_default_routes


def include_all_routes(router: APIRouter) -> None:
    include_default_routes(router)


__all__ = ["include_all_routes"]
