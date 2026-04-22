from fastapi import APIRouter

from src.app.routes.includes_routes.prefixes import DEFAULT_PREFIX
from src.app.routes.records import records_router


def include_default_exchange_routes(router: APIRouter) -> None:
    router.include_router(records_router, prefix=DEFAULT_PREFIX)
