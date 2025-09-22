import re
from datetime import datetime


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
        data, key=lambda date: datetime.strptime(date["date"], "%Y-%m-%dT%H:%M:%S.%f"), reverse=is_reverse
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
