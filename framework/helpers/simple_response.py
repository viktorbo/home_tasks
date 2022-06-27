from dataclasses import dataclass


@dataclass
class SimpleResponse:
    """
    Структура для упрощения работы с ответами на запросы
    """
    status_code: int
    content: str or int or float or bool or dict
