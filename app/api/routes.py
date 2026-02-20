"""
Определение HTTP эндпоинтов API.

Содержит обработчики запросов и возвращает ответы клиенту.
"""

from fastapi import APIRouter, HTTPException

from app.services.nlp_service import NLPService
from app.schemas.request import UserQuery
from app.schemas.response import ParseResponse

# Инициализация роутера и сервисов
router = APIRouter(prefix="/api")
nlp_service = NLPService()


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