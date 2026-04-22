from pydantic import BaseModel, Field


class RecordListItem(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор")
    label: str = Field(..., description="Отображаемое имя")


class RecordListResponse(BaseModel):
    data: list[RecordListItem] = Field(default_factory=list, description="Список записей")
    success: bool = Field(True, description="Флаг успешности операции")
