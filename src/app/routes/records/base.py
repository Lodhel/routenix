from sqlalchemy import asc, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models import Record
from src.app.orm_sender.manager_sqlalchemy import ManagerSQLAlchemy
from src.app.routes.base.general_routes import GeneralBaseRouter
from src.app.routes.general_models import GeneralHeadersModel, GeneralParamsWithFormat
from src.app.routes.mixins.main_router_mixin import MainRouterMIXIN


class RecordsBaseRouter(
    MainRouterMIXIN,
    GeneralBaseRouter,
    ManagerSQLAlchemy,
):
    async def get_records(self, session: AsyncSession, params: GeneralParamsWithFormat):
        select_rel = self.apply_search(params.search, Record, select(Record))
        if params.filter_by:
            select_rel = self.apply_filter_by(
                filter_by=params.filter_by,
                model_class=Record,
                select_rel=select_rel,
                allowed_keys=["id", "label"],
            )
        select_rel = self.set_order_by(params.order_by, select_rel)
        return await self.get_response_by_select_rel(session, params, select_rel)

    async def validate_query(self, headers: GeneralHeadersModel):
        if not headers.authorization_token:
            return self.make_response_by_auth_error()
        return None

    @classmethod
    async def get_data_by_response(cls, session: AsyncSession, ids: list, params: GeneralParamsWithFormat):
        if not ids:
            return []
        result = await session.execute(
            cls.set_order_by(
                params.order_by,
                select(Record).where(Record.id.in_(ids)),
            )
        )
        records = result.scalars().all()
        return [record.data_by_list for record in records]

    @staticmethod
    def set_order_by(order_by: str, select_rel):
        order_map = {
            "id_asc": asc(Record.id),
            "id_desc": desc(Record.id),
            "label_asc": asc(Record.label),
            "label_desc": desc(Record.label),
        }
        return select_rel.order_by(order_map[order_by]) if order_by in order_map else select_rel.order_by(asc(Record.id))

    @staticmethod
    async def get_data_by_response_created(session: AsyncSession, instance: Record):
        result = await session.execute(select(Record).where(Record.id == instance.id))
        record = result.scalar_one_or_none()
        return record.data_by_list if record else {}

    @staticmethod
    async def get_data_by_response_default(session, ids, params):
        del session, ids, params
        return []

    @staticmethod
    async def get_data_by_response_sites(session, ids, site_id, params):
        del session, ids, site_id, params
        return []

    @staticmethod
    async def get_data_by_response_sites_identifications(session, ids, site_id, params):
        del session, ids, site_id, params
        return []

    @staticmethod
    def apply_search(search: str, model_class, select_rel):
        del model_class
        if not search:
            return select_rel
        pattern = f"%{search}%"
        return select_rel.where(Record.label.ilike(pattern))
