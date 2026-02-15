"""
Сервис обработки естественного языка.

Координирует работу компонентов для разбора запросов:
- Клиент YandexGPT для вызова API
- Парсер для обработки ответов
- Валидаторы для проверки данных
"""

import time

from app.services.llm.client import YandexGPTClient
from app.services.llm.parser import ResponseParser
from app.validators.schema_validator import validate_parsed_intent
from app.schemas.request import UserQuery
from app.schemas.response import ParseResponse, ParsedIntent


class NLPService:
    """
    Сервис для обработки естественно-языковых запросов.

    Предоставляет метод process_query для разбора пользовательских запросов
    с использованием YandexGPT.
    """

    def __init__(self):
        """Инициализация сервиса и его компонентов."""
        self.llm_client = YandexGPTClient()
        self.parser = ResponseParser()

    async def process_query(self, query: UserQuery) -> ParseResponse:
        """
        Обрабатывает запрос пользователя.

        Алгоритм работы:
        1. Фиксация времени начала обработки
        2. Вызов YandexGPT для получения сырого ответа
        3. Парсинг ответа в структурированный формат
        4. Валидация полученных данных
        5. Формирование ответа с метаинформацией

        Args:
            query: Объект запроса пользователя

        Returns:
            ParseResponse: Структурированный ответ с результатами
        """
        # Фиксация времени начала
        start_time = time.time()

        # Вызов YandexGPT
        raw_response = await self.llm_client.call(query.text)

        # Парсинг ответа
        parsed_data = self.parser.parse(raw_response)

        # Валидация
        validate_parsed_intent(parsed_data)

        # Создание объекта с результатами
        parsed_intent = ParsedIntent(**parsed_data)

        # Вычисление времени обработки
        processing_time = int((time.time() - start_time) * 1000)

        # Формирование ответа
        return ParseResponse(
            user_id=query.user_id,
            parsed_query=parsed_intent,
            processing_time_ms=processing_time
        )