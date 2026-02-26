"""
Определение HTTP эндпоинтов API.

Содержит обработчики запросов и возвращает ответы клиенту.
"""
from typing import Optional
import httpx

from fastapi import APIRouter,  HTTPException, Query
from fastapi.responses import JSONResponse

from app.services.nlp_service import NLPService
from app.services.geosearch.manual_client import ManualGeosearchClient
from app.schemas.request import UserQuery
from app.schemas.response import ParseResponse

# Инициализация роутера и сервисов
router = APIRouter(prefix="/api/v2")
nlp_service = NLPService()
geosearch_client = ManualGeosearchClient()



@router.get("/health")
async def health_check() -> dict:
    """
    Эндпоинт для проверки работоспособности сервиса.
    """
    return {
        "status": "healthy",
        "service": "Adventure"
    }


@router.post(
    "/parse",
    response_model=ParseResponse,
    summary="Семантический разбор запроса",
    description="Принимает текстовый запрос и возвращает структурированные параметры"
)
async def parse_query(query: UserQuery) -> ParseResponse:
    """
    Эндпоинт для семантического разбора запроса пользователя.

    Ожидает JSON:
        {
            "user_id": 123,
            "text": "Хочу в тихий бар с друзьями"
        }

    Возвращает структурированный JSON с разобранными параметрами.
    """
    try:
        # FastAPI автоматически валидирует query по схеме UserQuery
        result = await nlp_service.process_query(query)
        return result
    except Exception as e:
        # В случае ошибки возвращаем 500
        raise HTTPException(
            status_code=500,
            detail=f"Внутренняя ошибка сервера: {str(e)}"
        )


@router.get("/search/raw")
async def search_raw(
        q: str = Query(..., description="Поисковый запрос "),
        lat: Optional[float] = Query(55.754, description="Широта центра поиска(Москва) "),
        lon: Optional[float] = Query(37.620, description="Долгота центра поиска(Москва) "),
        radius: Optional[int] = Query(None, description="Радиус поиска в метрах "),
        results: int = Query(10, description="Количество результатов")
) -> JSONResponse:
    """
    **Параметры:**
    - `q`: текст запроса (обязательно)
    - `lat`: широта центра (опционально)
    - `lon`: долгота центра (опционально)
    - `radius`: радиус в метрах (опционально)
    - `results`: количество результатов (по умолчанию 10)
    """
    try:
        # Выполняем поиск через клиент
        result = await geosearch_client.search(
            text=q,
            latitude=lat,
            longitude=lon,
            radius=radius,
            results=results
        )

        return JSONResponse(content=result)

    except httpx.HTTPStatusError as e:
        # Ошибка от Яндекс API
        return JSONResponse(
            status_code=e.response.status_code,
            content={
                "error": "Ошибка при обращении к Яндекс API",
                "details": e.response.text
            }
        )
    except Exception as e:
        # Другие ошибки
        return JSONResponse(
            status_code=500,
            content={
                "error": "Внутренняя ошибка сервера",
                "details": str(e)
            }
        )