from sqlalchemy.ext.asyncio import AsyncSession

from src.app.orm_sender.manager_sqlalchemy import ManagerSQLAlchemy
from src.app.routes.base.general_routes import GeneralBaseRouter
from src.app.routes.general_models import GeneralHeadersModel, GeneralParamsWithFormat
from src.app.routes.mixins.main_router_mixin import MainRouterMIXIN


class RecordsBaseRouter(
    MainRouterMIXIN,
    GeneralBaseRouter,
    ManagerSQLAlchemy,
):
    _records = [
        {"id": 1, "label": "Элемент A", "code": "A-01", "is_active": True},
        {"id": 2, "label": "Элемент B", "code": "B-01", "is_active": True},
        {"id": 3, "label": "Элемент C", "code": "C-01", "is_active": False},
    ]

    async def get_records(self, session: AsyncSession, params: GeneralParamsWithFormat):
        del session
        records = list(self._records)

        if params.search:
            pattern = params.search.lower()
            records = [
                record for record in records
                if pattern in record["label"].lower() or pattern in record["code"].lower()
            ]

        if params.filter_by:
            filters = self.parse_filter_by(params.filter_by, allowed_keys=["is_active"])
            if "is_active" in filters:
                bool_values = self._parse_bool_values(filters["is_active"])
                records = [record for record in records if record["is_active"] in bool_values]

        total = len(records)
        records = self.set_order_by(params.order_by, records)

        start = int(params.start) if params.start is not None else 0
        limit = int(params.limit) if params.limit is not None else 20
        start = max(start, 0)

        if limit > 0:
            records = records[start:start + limit]
        else:
            records = records[start:]

        data = [{"id": record["id"], "label": record["label"]} for record in records]
        return self.get_data(
            data=data,
            status_code=200,
            meta={
                "total": len(data),
                "counts": total
            },
            fmt=params.response_fmt,
            is_download=bool(params.is_download),
        )

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

    @staticmethod
    def _parse_bool_values(values: list[str]) -> set[bool]:
        truthy = {"true", "1", "yes", "y", "on", "t"}
        falsy = {"false", "0", "no", "n", "off", "f"}
        result = set()
        for raw_value in values:
            value = raw_value.strip().lower()
            if value in truthy:
                result.add(True)
            if value in falsy:
                result.add(False)
        return result or {True, False}

    async def validate_query(self, headers: GeneralHeadersModel):
        if not headers.authorization_token:
            return self.make_response_by_auth_error()
        return None
