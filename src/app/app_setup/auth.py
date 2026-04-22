from typing import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.app.config import DOCS_DEFAULT_USERNAME, DOCS_DEFAULT_PASSWORD


def build_docs_auth_checks() -> tuple[Callable]:
    security = HTTPBasic()

    def _check_basic(credentials: HTTPBasicCredentials, username: str, password: str) -> None:
        if credentials.username != username or credentials.password != password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Basic"},
            )

    def check_default_credentials(credentials: HTTPBasicCredentials = Depends(security)):
        _check_basic(credentials, DOCS_DEFAULT_USERNAME, DOCS_DEFAULT_PASSWORD)

    return (
        check_default_credentials,
    )
