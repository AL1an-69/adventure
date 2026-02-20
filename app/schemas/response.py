"""
Схемы данных для исходящих ответов.

Определяет структуру данных, которые сервер возвращает клиенту.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
import uuid
import time


class PriceLevel(str, Enum):

    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    PREMIUM = "premium"


class ParsedIntent(BaseModel):
    """
    Структурированное представление запроса после разбора.

    Все поля являются опциональными и заполняются YandexGPT
    в зависимости от контекста запроса.
    """

    intent: List[str] = Field(
        default_factory=list,
        description="Конкретные типы мест (бар, ресторан, кафе)",
        example=["бар"]
    )

    categories: List[str] = Field(
        default_factory=list,
        description="Общие категории (итальянская кухня, крафтовое пиво)",
        example=[]
    )

    radius: Optional[int] = Field(
        None,
        description="Радиус поиска в метрах",
        example=5000
    )

    mood: Optional[str] = Field(
        None,
        description="Желаемая атмосфера",
        example="спокойное"
    )

    company: Optional[str] = Field(
        None,
        description="С кем пользователь планирует посетить",
        example="друзья"
    )

    time_context: Optional[str] = Field(
        None,
        description="Временной контекст",
        example="вечер"
    )

    price_level: Optional[PriceLevel] = Field(
        None,
        description="Уровень цен",
        example="medium"
    )

    feature_tags: List[str] = Field(
        default_factory=list,
        description="Дополнительные требования",
        example=["пиво", "живая музыка"]
    )


class ParseResponse(BaseModel):
    """
    Ответ сервера на запрос парсинга.

    Attributes:
        request_id: Уникальный идентификатор запроса
        user_id: Идентификатор пользователя
        parsed_query: Результат разбора запроса
        processing_time_ms: Время обработки в миллисекундах
    """

    request_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Уникальный идентификатор запроса"
    )

    user_id: int = Field(
        ...,
        description="Идентификатор пользователя"
    )

    parsed_query: ParsedIntent = Field(
        ...,
        description="Результат разбора запроса"
    )

    processing_time_ms: int = Field(
        default_factory=lambda: int(time.time() * 1000),
        description="Время обработки в миллисекундах"
    )