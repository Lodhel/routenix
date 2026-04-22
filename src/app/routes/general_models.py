from fastapi import Query
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field

security = HTTPBearer()


class GeneralHeadersModel:
    def __init__(self, credentials: HTTPAuthorizationCredentials = Depends(security)):
        if credentials.scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme"
            )
        self.authorization_token = credentials.credentials


class GeneralParams:
    def __init__(
        self,
        start: int = Query(
            default=0,
            description="С какого порядкового инстанса начинать (для пагинации)"
        ),
        limit: int = Query(
            default=20,
            description="Сколько инстансов вернуть"
        ),
        order_by: str = Query(
            default='id_asc',
            description="Сортировка (id_asc, id_desc)"
        ),
        search: str = Query(
            default=None,
            description="Поисковая строка (может по нескольким полям, если реализовано)"
        ),
        filter_by: str = Query(
            default='',
            description="Фильтрация по полям в формате field:value1,value2;field2:value3"
        ),
    ):
        self.start = start
        self.limit = limit
        self.order_by = order_by
        self.search = search
        self.filter_by = filter_by


class GeneralParamsWithFormat(GeneralParams):
    def __init__(
        self,
        start: int = Query(
            default=0,
            description="С какого порядкового инстанса начинать (для пагинации)"
        ),
        limit: int = Query(
            default=20,
            description="Сколько инстансов вернуть"
        ),
        order_by: str = Query(
            default='id_asc',
            description="Сортировка (id_asc, id_desc)"
        ),
        search: str = Query(
            default=None,
            description="Поисковая строка (может по нескольким полям, если реализовано)"
        ),
        filter_by: str = Query(
            default='',
            description="Фильтрация по полям в формате field:value1,value2;field2:value3"
        ),
        response_fmt: str = Query(
            default='json',
            description="Формат респонса (json, yaml, yml, xml)"
        ),
        is_download: int = Query(
            default=0,
            description="Нужно ли выгрузить результат файлом"
        ),
    ):
        super().__init__(
            start=start,
            limit=limit,
            order_by=order_by,
            search=search,
            filter_by=filter_by,
        )
        self.response_fmt = response_fmt
        self.is_download = is_download
