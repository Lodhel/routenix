from sqlalchemy.ext.asyncio import AsyncSession

from src.app.orm_sender.manager_sqlalchemy import ManagerSQLAlchemy
from src.app.routes.base.general_routes import GeneralBaseRouter
from src.app.routes.general_models import GeneralParamsWithFormat


class RecordsBaseRouter(
    GeneralBaseRouter,
    ManagerSQLAlchemy,
):
    _records = [
        {"id": 1, "label": "Элемент A", "code": "A-01", "is_active": True},
        {"id": 2, "label": "Элемент B", "code": "B-01", "is_active": True},
        {"id": 3, "label": "Элемент C", "code": "C-01", "is_active": False},
    ]

    async def get_records(self, session: AsyncSession, params: GeneralParamsWithFormat):
        pass

    @staticmethod
    def set_order_by(order_by: str, records: list[dict]) -> list[dict]:
        order_map = {
            "id_asc": ("id", False),
            "id_desc": ("id", True),
            "label_asc": ("label", False),
            "label_desc": ("label", True),
        }
        field, is_reverse = order_map.get(order_by, ("id", False))
        return sorted(records, key=lambda record: record[field], reverse=is_reverse)

    @staticmethod
    async def get_data_by_response_created(session, instance):
        del session
        return instance

    @staticmethod
    async def get_data_by_response(session, ids, params):
        del session, ids, params
        return []
