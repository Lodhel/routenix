from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.routes.general_models import GeneralHeadersModel, GeneralParamsWithFormat
from src.app.routes.records.base import RecordsBaseRouter
from src.app.routes.records.models import RecordListResponse
from src.app.routes.records.response_models import record_list_responses

records_router = APIRouter()
records_tags = ["Records"]


@cbv(records_router)
class RecordsRouter(RecordsBaseRouter):
    @records_router.get(
        "/records/",
        name="get_records",
        summary="Получить список записей",
        response_model=RecordListResponse,
        responses=record_list_responses,
        tags=records_tags,
    )
    async def get(
        self,
        params: GeneralParamsWithFormat = Depends(),
        headers: GeneralHeadersModel = Depends(),
    ):
        if error := await self.validate_query(headers):
            return error

        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            return await self.get_records(session=session, params=params)
