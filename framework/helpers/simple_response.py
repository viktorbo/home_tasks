from dataclasses import dataclass
from typing import Any


@dataclass
class SimpleResponse:
    """
    Структура для упрощения работы с ответами на запросы
    """
    status_code: int
    time: float
    headers: dict
    content: Any
