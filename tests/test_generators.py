import pytest
from typing import Dict, List, Iterator
from src.generators import filter_by_currency


@pytest.fixture
def sample_transactions() -> List[Dict]:
    """Фикстура с тестовыми транзакциями."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"code": "USD", "name": "USD"}
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"code": "USD", "name": "USD"}
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {"code": "RUB", "name": "рублей"}
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {"code": "USD", "name": "USD"}
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229"
        }
    ]


def test_filter_usd_transactions(sample_transactions):
    """Тест корректной фильтрации USD транзакций."""
    # Act
    usd_transactions = list(filter_by_currency(sample_transactions, "USD"))

    # Assert
    assert len(usd_transactions) == 3
    assert all(t['operationAmount']['currency']['code'] == 'USD' for t in usd_transactions)
    assert usd_transactions[0]['id'] == 939719570
    assert usd_transactions[1]['id'] == 142264268
    assert usd_transactions[2]['id'] == 895315941


def test_filter_rub_transactions(sample_transactions):
    """Тест корректной фильтрации RUB транзакций."""
    # Act
    rub_transactions = list(filter_by_currency(sample_transactions, "RUB"))

    # Assert
    assert len(rub_transactions) == 1
    assert rub_transactions[0]['id'] == 873106923
    assert rub_transactions[0]['operationAmount']['currency']['code'] == 'RUB'


def test_filter_eur_transactions_none_found(sample_transactions):
    """Тест фильтрации EUR транзакций (отсутствуют)."""
    # Act
    eur_transactions = list(filter_by_currency(sample_transactions, "EUR"))

    # Assert
    assert len(eur_transactions) == 0
    assert eur_transactions == []


def test_empty_list(sample_transactions):
    """Тест обработки пустого списка транзакций."""
    # Act
    result = list(filter_by_currency([], "USD"))

    # Assert
    assert result == []
    assert len(result) == 0


def test_no_matching_currency(sample_transactions):
    """Тест обработки списка без подходящей валюты."""
    # Act
    result = list(filter_by_currency(sample_transactions, "JPY"))

    # Assert
    assert result == []
    assert len(result) == 0


def test_iterator_behavior(sample_transactions):
    """Тест поведения итератора (поочередная выдача)."""
    # Act
    usd_iterator = filter_by_currency(sample_transactions, "USD")

    # Assert
    assert isinstance(usd_iterator, Iterator)

    # Получаем транзакции по одной
    first = next(usd_iterator)
    second = next(usd_iterator)
    third = next(usd_iterator)

    assert first['id'] == 939719570
    assert second['id'] == 142264268
    assert third['id'] == 895315941

    # Проверяем, что больше нет элементов
    with pytest.raises(StopIteration):
        next(usd_iterator)





def test_case_sensitivity(sample_transactions):
    """Тест чувствительности к регистру."""
    # Act
    result_lower = list(filter_by_currency(sample_transactions, "usd"))
    result_upper = list(filter_by_currency(sample_transactions, "USD"))

    # Assert
    assert len(result_lower) == 0  # "usd" != "USD"
    assert len(result_upper) == 3  # "USD" == "USD"


@pytest.mark.parametrize("currency,expected_count", [
    ("USD", 3),
    ("RUB", 1),
    ("EUR", 0),
    ("GBP", 0),
    ("JPY", 0)
])
def test_parametrized_currency_filtering(sample_transactions, currency, expected_count):
    """Параметризованный тест для разных валют."""
    # Act
    result = list(filter_by_currency(sample_transactions, currency))

    # Assert
    assert len(result) == expected_count
    if expected_count > 0:
        assert all(t['operationAmount']['currency']['code'] == currency for t in result)
