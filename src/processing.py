def filter_by_state(data: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Фильтрует список словарей по значению ключа 'state'.
    """
    new_data = list()

    for item in data:
        if item.get("state") == state:
            new_data.append(item)

    return new_data


def sort_by_date(data: list[dict], is_reverse: bool = True) -> list[dict]:
    """
    Сортирует список словарей по значению ключа 'date'
    """
    sorted_by_date_data = sorted(data, key=lambda date: date["date"], reverse=is_reverse)

    return sorted_by_date_data
