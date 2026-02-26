"""
Простой клиент для ручного поиска через Яндекс API.
Возвращает сырые данные без дополнительной обработки.
"""

import httpx
from typing import Dict, Any, Optional

from app.core.config import settings


class ManualGeosearchClient:
    """
    Простой клиент для тестирования поиска по организациям.
    """

    # Базовый URL API
    BASE_URL = "https://search-maps.yandex.ru/v1/"

    def __init__(self):
        """Инициализация клиента."""
        self.api_key = settings.GEO_SEARCH_KEY
        if not self.api_key:
            raise ValueError("ключ не задан в .env")

    async def search(
        self,
        text: str,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        radius: Optional[int] = None,
        results: int = 10
    ) -> Dict[str, Any]:

        # Формируем параметры запроса
        params: Dict[str, Any] = {
            "apikey": self.api_key,
            "text": text,
            "lang": "ru_RU",
            "type": "biz",
            "results": results ,
        }

        # Добавляем координаты, если они есть
        if latitude is not None and longitude is not None:
            params["ll"] = f"{longitude},{latitude}"

        # Добавляем радиус, конвертируя в spn
        if radius is not None and latitude is not None:
            # Грубая конвертация: 1 градус ~ 111 000 метров
            # spn = (radius / 111000) * 2
            spn_degrees = (radius / 111000) * 2
            params["spn"] = f"{spn_degrees:.6f},{spn_degrees:.6f}"

        # Выполняем запрос
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.BASE_URL,
                params=params,
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()

    async def search_raw(self, query: str) -> Dict[str, Any]:
        """
     поиск только по тексту
        """
        params = {
            "apikey": self.api_key,
            "text": query,
            "lang": "ru_RU",
            "type": "biz",
            "results": 20,
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(self.BASE_URL, params=params)
            response.raise_for_status()
            return response.json()