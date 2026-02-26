"""
Управление конфигурацией приложения.

Загружает и валидирует переменные окружения из файла .env.
"""

import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()


class Settings:
    """Контейнер настроек приложения."""

    # Учетные данные Yandex Cloud
    YANDEX_FOLDER_ID: str = os.getenv("YANDEX_FOLDER_ID", "")
    YANDEX_API_KEY: str = os.getenv("YANDEX_API_KEY", "")

    # Данные Geo Search
    GEO_SEARCH_KEY : str = os.getenv("GEO_SEARCH_KEY","")

    # Настройки приложения
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Настройки YandexGPT
    LLM_TIMEOUT: int = 15  # Таймаут запроса в секундах


# Глобальный экземпляр настроек
settings = Settings()

# Валидация обязательных параметров
if not settings.YANDEX_FOLDER_ID:
    raise ValueError("Не задан параметр YANDEX_FOLDER_ID в файле .env")

if not settings.YANDEX_API_KEY:
    raise ValueError("Не задан параметр YANDEX_API_KEY в файле .env")