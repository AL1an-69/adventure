"""
Валидаторы для проверки корректности данных.

Выполняет дополнительную валидацию, выходящую за рамки Pydantic.
"""

from typing import Dict, Any


def validate_parsed_intent(data: Dict[str, Any]) -> None:
    """
    Проверяет корректность распарсенных данных от YandexGPT.

    Args:
        data: Словарь с данными от YandexGPT


        Функция не возвращает значение, но может выбрасывать исключения.
        В текущей версии валидация минимальна и может быть расширена.
    """
    # Проверка наличия обязательных полей
    if not isinstance(data.get("intent", []), list):
        data["intent"] = []

    if not isinstance(data.get("categories", []), list):
        data["categories"] = []

    if not isinstance(data.get("feature_tags", []), list):
        data["feature_tags"] = []

    # Проверка радиуса
    radius = data.get("radius")
    if radius is not None:
        try:
            radius = int(radius)
            if radius < 100:
                data["radius"] = 100
            elif radius > 50000:
                data["radius"] = 50000
        except (ValueError, TypeError):
            data["radius"] = 5000