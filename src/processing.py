def filter_by_state(data: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Фильтрует список словарей по значению ключа 'state'.
    """
    new_data = list()

    for item in data:
        if item.get("state") == state:
            new_data.append(item)

    return new_data
