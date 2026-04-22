# Routenix API Framework Template

`Routenix` — каркас для FastAPI-проекта с упором на:
- модульные роуты в стиле `CBV`;
- единые параметры выборки (пагинация, фильтрация, сортировка, поиск);
- переиспользуемую базовую логику через `GeneralBaseRouter`;
- готовность к расширению под многозадачные сервисные решения.

## Технологии

- Python 3.12
- FastAPI
- SQLAlchemy (async)
- Uvicorn
- Docker / Docker Compose

## Структура проекта

```text
src/
  app/
    app_setup/                  # auth/docs/lifecycle/middleware
    orm_sender/                 # SQLAlchemy engine и ORM-утилиты
    routes/
      base/                     # базовые абстракции роутеров
      includes_routes/          # точки подключения роутов по префиксам
      records/                  # пример полноценного модуля роута
```

Ключевые точки:
- `src/app/__init__.py` — сборка приложения (`application`).
- `src/run.py` — entrypoint для Uvicorn.
- `src/app/routes/base/general_routes.py` — `GeneralBaseRouter` (ядро общей логики выборки).

## Быстрый запуск

```bash
./manage.sh start
```

API поднимается на `http://localhost:2300`.

Документация:
- ReDoc: `GET /default/openapi` (c Basic Auth)
- OpenAPI JSON: `GET /default/openapi.json` (c Basic Auth)

## Конфигурация окружения

Используется файл `src/.env`.

Минимально ожидаемые переменные:
- `SQL_HOST`
- `SQL_PORT`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `DOCS_DEFAULT_USERNAME`
- `DOCS_DEFAULT_PASSWORD`

## Паттерн модуля роута

Каждый предметный роут хранится в отдельной директории в `src/app/routes/<module_name>/` и должен включать:
- `base.py` — бизнес-логика и интеграция с базовыми миксинами/роутером;
- `models.py` — Pydantic response models;
- `response_models.py` — словарь `responses` для OpenAPI examples;
- `router.py` — основной CBV-роутер;
- `__init__.py` — экспорт роутера.

Пример в проекте: `src/app/routes/records/`.

Подключение в API делается через:
1. `src/app/routes/includes_routes/default/exchange.py`
2. `src/app/routes/includes_routes/default/__init__.py`
3. `src/app/routes/includes_routes/__init__.py`

## GeneralBaseRouter (важно)

`GeneralBaseRouter` в `src/app/routes/base/general_routes.py` — основной слой общей логики для list-like запросов.

Что дает из коробки:
- `get_response_by_select_rel(...)` — единый flow получения данных + meta;
- `get_instances_by_response(...)` — пагинация (`start`, `limit`);
- `apply_filter_by(...)` / `parse_filter_by(...)` — фильтрация по query `filter_by`;
- `get_count_by_select_rel(...)` — подсчет общего количества;
- `set_order_by(...)`, `get_data_by_response(...)`, `get_data(...)` — контракт для реализации в конкретном роуте.

### apply_search: обязательное пояснение

Сейчас базовая реализация:

```python
@staticmethod
def apply_search(search: str, model_class, select_rel):
    if not search:
        return select_rel
    search_expr = model_class.field.ilike(f"%{search}%")
    return select_rel.where(search_expr)
```

Важно:
- по умолчанию поиск идет по `model_class.field`;
- это placeholder-поведение;
- в реальном модуле нужно переопределять `apply_search(...)` и явно указывать нужные поля модели (одно или несколько через `or_`).

Если в вашей модели нет колонки `field`, и метод не переопределен, запрос поиска работать корректно не будет.

## Query-параметры (базовый контракт)

Через `GeneralParams` / `GeneralParamsWithFormat`:
- `start` — смещение;
- `limit` — лимит;
- `order_by` — ключ сортировки;
- `search` — поисковая строка;
- `filter_by` — фильтрация (`field:value1,value2;field2:value3`);
- `response_fmt` — `json|yaml|yml|xml`;
- `is_download` — вернуть как downloadable файл.

## Рекомендации для новых роутов

1. Унаследовать `*BaseRouter` от `GeneralBaseRouter`.
2. Явно определить:
   - `set_order_by(...)`
   - `get_data_by_response(...)`
   - `apply_search(...)` с конкретными полями модели.
3. Возвращать ответ через `get_data(...)` и при необходимости декоратор `make_data_by_response`.
4. Добавить OpenAPI `response_model` и `responses` examples.
