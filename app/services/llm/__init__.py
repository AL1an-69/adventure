"""
Модуль интеграции с языковыми моделями.
"""

from app.services.llm.client import YandexGPTClient
from app.services.llm.parser import ResponseParser

__all__ = [
    "YandexGPTClient",
    "ResponseParser"
]