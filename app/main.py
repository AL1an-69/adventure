"""
Главный модуль FastAPI приложения.

Отвечает за инициализацию и настройку веб-сервера,
подключение middleware и роутеров.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes import router

# Жизненый цикл
async def lifespan(app:FastAPI):
    print('Сервер Запущен')
    yield
    print('Сервер Остановлен')


# Создание экземпляра приложения
app = FastAPI(
    title="Adventure",
    version="1.0.0",
    debug=settings.DEBUG
)

# Настройка CORS для доступа с клиентских приложений
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Для продакшена указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(router, prefix="/api/v1")


