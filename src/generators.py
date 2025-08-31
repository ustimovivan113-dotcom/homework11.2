from typing import Dict, List, Iterator



def filter_by_currency(transactions: list[dict], currency: str) -> Iterator[Dict]:
    """
    Фукнция для возвращения итератора, которая поочередно
    выдаёт транзакции, где валюта операции соответсвует заданной
    """
    result = (transaction for transaction in transactions
              if transaction.get('operationAmount', {}).get('currency', {}).get('code') == currency)

    return result

def transaction_descriptions(transactions: list[dict]) -> Iterator:
    """
    Генератор, который принимает список словарей с транзакциями
    и возвращает описание каждой операции по очереди
    """
    for transaction in transactions:
        description = transaction.get('description')
        yield description


def card_number_generator(start: int = 1, end: int = 9999999999999999) -> Iterator[str]:
    """
    Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.
    """
    if start < 1:
        raise ValueError("Начальный номер должен быть не менее 1")
    if end > 9999999999999999:
        raise ValueError("Конечный номер должен менее 16 символов")
    if start > end:
        raise ValueError("Начальный номер должен быть меньше или равен конечному")

    current = start
    while current <= end:
        card_number = str(current).zfill(16)

        formatted = f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:]}"
        yield formatted
        current += 1

