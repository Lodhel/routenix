from collections.abc import Callable

from fastapi import Depends, FastAPI
from fastapi.openapi.docs import get_redoc_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
from starlette.responses import JSONResponse

from src.app.routes.includes_routes.prefixes import DEFAULT_PREFIX

GROUP_TITLES: dict[str, str] = {
    "default": "DOC v.0.1 - default API",
}


def _detect_group(path: str) -> str | None:
    if path.startswith(f"{DEFAULT_PREFIX}/"):
        return "default"

    return None


def _build_schema(app: FastAPI, group: str) -> dict:
    selected_routes = []
    for route in app.routes:
        if _detect_group(getattr(route, "path", "")) == group:
            selected_routes.append(route)

    return get_openapi(
        title=GROUP_TITLES[group],
        version=app.version,
        description=app.description,
        routes=selected_routes,
    )


def register_docs_routes(
    app: FastAPI,
    check_default_credentials: Callable,
) -> None:
    @app.get("/default/openapi", response_class=HTMLResponse)
    def default_redoc(credentials=Depends(check_default_credentials)):
        return get_redoc_html(
            openapi_url="/default/openapi.json",
            title="DOC v.0.1 - default ReDoc",
            redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@2.5.2/bundles/redoc.standalone.js",
        )

    @app.get("/default/openapi.json")
    def default_openapi_json(credentials=Depends(check_default_credentials)):
        return JSONResponse(_build_schema(app, group="default"))
