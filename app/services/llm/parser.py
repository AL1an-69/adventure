"""
Парсер ответов от YandexGPT.

Отвечает только за извлечение структурированных данных из текстовых ответов.
"""

import json
from typing import Dict, Any


class ResponseParser:
    """
    Парсер ответов от языковых моделей.

    Извлекает JSON из текстового ответа и преобразует его в словарь.
    """

    def parse(self, text: str) -> Dict[str, Any]:
        """
        Извлекает JSON из текстового ответа.

        Args:
            text: Сырой текстовый ответ от YandexGPT

        Returns:
            Dict[str, Any]: Распарсенный JSON как словарь

        Notes:
            Если JSON не найден или невалиден, возвращается пустой словарь.
            YandexGPT иногда оборачивает JSON в ```json ... ``` маркдаун.
        """
        if not text:
            return {}

        # Очистка от маркдаун-оберток
        if text.startswith("```"):
            start = text.find("{")
            end = text.rfind("}") + 1
            if start != -1 and end != 0:
                text = text[start:end]

        # Парсинг JSON
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # В случае ошибки возвращаем пустой словарь
            return {}