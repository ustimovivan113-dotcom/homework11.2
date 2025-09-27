import re
from collections import Counter
from datetime import datetime

from src.widget import get_date


def filter_by_state(data: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Фильтрует список словарей по значению ключа 'state'.
    """
    if not data:
        raise ValueError("Пустой список")

    new_data = list()

    for item in data:
        if item.get("state") == state:
            new_data.append(item)

    return new_data


def sort_by_date(data: list[dict], is_reverse: bool = True) -> list[dict]:
    """
    Сортирует список словарей по значению ключа 'date'
    """
    sorted_by_date_data = sorted(
        data, key=lambda item: datetime.strptime(get_date(item["date"].split("T")[0]), "%d.%m.%Y"), reverse=is_reverse
    )
    return sorted_by_date_data


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """
    Фильтрует список банковских операций, оставляя только те,
    в описании которых содержится указанная строка поиска.
    """
    pattern = re.compile(re.escape(search), re.IGNORECASE)

    result = []
    for operation in data:
        desc = str(operation.get("description", ""))
        if pattern.search(desc):
            result.append(operation)
    return result


def process_bank_operations(data: list[dict], categories: list[str]) -> Counter:
    """
    Принимает список словарей с данными о банковских операциях и
    список категорий операций, а возвращает Counter, в котором ключи
    — это названия категорий, а значения — это количество операций
    в каждой категории
    """
    categories_from_data = [str(operation.get("description", "")) for operation in data if str(operation.get("description", "")) in categories]
    return Counter(categories_from_data)
