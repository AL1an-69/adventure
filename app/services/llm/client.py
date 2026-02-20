"""
Клиент для взаимодействия с YandexGPT API.

Отвечает только за отправку запросов и получение сырых ответов.
"""

import asyncio

from yandex_ai_studio_sdk import AIStudio

from app.core.config import settings


class YandexGPTClient:
    """
    Клиент для вызова YandexGPT API.

    Инкапсулирует детали подключения и формата запросов к YandexGPT.
    """

    # Системный промпт с инструкциями для модели
    SYSTEM_PROMPT = """Ты — модуль семантического разбора запросов о местах.

Преобразуй запрос пользователя в JSON по этой схеме:
{
  "intent": ["типы_мест"],
  "categories": ["категории"],
  "radius": число,
  "mood": "настроение",
  "company": "с_кем",
  "time_context": "когда",
  "price_level": "none/low/medium/high/premium",
  "feature_tags": ["теги"]
}

Правила:
- radius: "рядом/недалеко" = 2000, иначе 5000
- price_level: только low, medium, high, premium, так же если нет никакой информации о цене поставить none
- Все остальные поля могут быть любыми словами
- Верни ТОЛЬКО JSON, без пояснений

Пример:
Запрос: "Хочу в тихий бар с друзьями"
Ответ: {"intent":["бар"],"categories":[],"radius":5000,"mood":"спокойное","company":"друзья","time_context":"вечер","price_level":"medium","feature_tags":["пиво"]}
"""

    def __init__(self):
        """Инициализация подключения к YandexGPT."""
        self.sdk = AIStudio(
            folder_id=settings.YANDEX_FOLDER_ID,
            auth=settings.YANDEX_API_KEY,
        )
        self.model = self.sdk.models.completions("yandexgpt")

    async def call(self, text: str) -> str:
        """
        Отправляет запрос к YandexGPT и возвращает сырой ответ.

        Args:
            text: Текст запроса пользователя

        Returns:
            str: Сырой текстовый ответ от YandexGPT
        """
        # Формирование сообщений для модели
        messages = [
            {"role": "system", "text": self.SYSTEM_PROMPT},
            {"role": "user", "text": text},
        ]

        # Получение event loop для выполнения синхронных вызовов
        loop = asyncio.get_event_loop()

        # Отправка запроса (синхронный вызов в отдельном потоке)
        operation = await loop.run_in_executor(
            None,
            lambda: self.model.run_deferred(messages)
        )

        # Ожидание ответа
        result = await loop.run_in_executor(
            None,
             lambda : operation.wait()
        )

        return (result.text or "").strip()