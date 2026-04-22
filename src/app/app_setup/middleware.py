from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


ORIGINS = []


def configure_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
