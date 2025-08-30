from typing import Dict, List, Iterator


def filter_by_currency(transactions: list[dict], currency: str) -> Iterator[Dict]:
    '''
    Фукнция для возвращения итератора, которая поочередно
    выдаёт транзакции, где валюта операции соответсвует заданной
    '''
    result = (transaction for transaction in transactions
              if transaction.get('operationAmount', {}).get('currency', {}).get('code') == currency)

    return result
