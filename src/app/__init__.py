from fastapi import FastAPI

from src.app.app_setup import build_docs_auth_checks
from src.app.app_setup.docs import register_docs_routes
from src.app.app_setup.lifecycle import register_startup_tasks
from src.app.app_setup.middleware import configure_cors
from src.app.routes import router


def create_app() -> FastAPI:
    app = FastAPI(
        title="DOC v.1.1",
        version="1.1.0",
        description="API DOC services.",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )

    check_default = build_docs_auth_checks()
    register_docs_routes(app, check_default)
    register_startup_tasks(
        app,
    )
    configure_cors(app)

    app.include_router(router)
    return app


application: FastAPI = create_app()

__all__ = ["application", "create_app"]
