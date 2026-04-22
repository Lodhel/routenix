from fastapi import APIRouter

from src.app.routes.includes_routes.default.exchange import include_default_exchange_routes


def include_default_routes(router: APIRouter) -> None:
    include_default_exchange_routes(router)
