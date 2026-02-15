"""
Схемы данных для входящих запросов.

Определяет структуру данных, которые клиент отправляет на сервер.
"""

from pydantic import BaseModel, Field


class UserQuery(BaseModel):
    """
    Схема запроса от пользователя.

    Attributes:
        user_id: Идентификатор пользователя
        text: Текст запроса на естественном языке
    """

    user_id: int = Field(
        ...,
        description="Идентификатор пользователя",
        example=12345
    )

    text: str = Field(
        ...,
        description="Текст запроса",
        example="Хочу в тихий бар с друзьями",
        min_length=1,
        max_length=1000
    )