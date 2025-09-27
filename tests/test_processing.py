import pytest
import re
from src.processing import filter_by_state, sort_by_date, process_bank_search, process_bank_operations
from typing import List, Dict

@pytest.fixture


def data() -> List[Dict]:
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 111111111, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]

@pytest.fixture


def sample_transactions() -> List[Dict]:
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
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
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
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
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
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
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229"
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657"
        }
    ]

@pytest.mark.parametrize(
    "expected",
    [
        [
            {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        ]
    ],
)


def test_filter_by_state(data: List[Dict], expected: List[Dict]) -> None:
    """Тест фильтрации (без state)."""
    assert filter_by_state(data) == expected

@pytest.mark.parametrize(
    "state, expected",
    [
        (
            "EXECUTED",
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
        ),
    ],
)


def test_filter_by_state_executed(data: List[Dict], state: str, expected: List[Dict]) -> None:
    """Тест фильтрации (EXECUTED)."""
    assert filter_by_state(data, state) == expected

@pytest.mark.parametrize(
    "state, expected",
    [
        (
            "CANCELED",
            [
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 111111111, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
        ),
    ],
)


def test_filter_by_state_canceled(data: List[Dict], state: str, expected: List[Dict]) -> None:
    """Тест фильтрации (CANCELED)."""
    assert filter_by_state(data, state) == expected


def test_filter_by_state_no_data():
    with pytest.raises(ValueError):
        filter_by_state([])

@pytest.mark.parametrize(
    "expected",
    [
        [
            {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            {"id": 111111111, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
            {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        ]
    ],
)


def test_sort_by_date_without_is_reverse(data: List[Dict], expected: List[Dict]) -> None:
    """
    Тест сортировки в порядке убывания.
    При одинаковых датах сортировка между двумя одинаковыми элементами с датой сохраняется
    """
    assert sort_by_date(data) == expected

@pytest.mark.parametrize(
    "expected",
    [
        [
            {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
            {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            {"id": 111111111, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        ]
    ],
)


def test_sort_by_date_is_reverse(data: List[Dict], expected: List[Dict]) -> None:
    """
    Тест сортировки в порядке возрастания
    При одинаковых датах сортировка между двумя одинаковыми элементами с датой сохраняется
    """
    assert sort_by_date(data, False) == expected


def test_sort_by_date_with_invalid_date_formats():
    # Случай с некорректным форматом даты
    invalid_format_data = [
        {"id": 1, "date": "2023-10-26T10:00:00.000000"},
        {"id": 2, "date": "26/10/2023 10:00"},  # Некорректный формат
        {"id": 3, "date": "2023-10-27T08:00:00.000000"},
    ]
    with pytest.raises(ValueError, match="time data '26/10/2023 10:00' does not match format '%Y-%m-%dT%H:%M:%S.%f'"):
        sort_by_date(invalid_format_data)

    # Случай с отсутствующим ключом "date"
    missing_key_data = [
        {"id": 1, "date": "2023-10-26T10:00:00.000000"},
        {"id": 2, "timestamp": "2023-10-25T12:00:00.000000"},  # Отсутствует 'date'
        {"id": 3, "date": "2023-10-27T08:00:00.000000"},
    ]
    with pytest.raises(KeyError, match="date"):
        sort_by_date(missing_key_data)

    # Случай с датой, которая не может быть преобразована (например, неполная)
    incomplete_date_data = [
        {"id": 1, "date": "2023-10-26T10:00:00.000000"},
        {"id": 2, "date": "2023-10-25T12:00:00"},  # Отсутствуют микросекунды
        {"id": 3, "date": "2023-10-27T08:00:00.000000"},
    ]
    with pytest.raises(
        ValueError, match="time data '2023-10-25T12:00:00' does not match format '%Y-%m-%dT%H:%M:%S.%f'"
    ):
        sort_by_date(incomplete_date_data)

    # Случай с пустым списком
    empty_list_data = []
    sorted_empty = sort_by_date(empty_list_data)
    assert sorted_empty == []


def test_process_bank_search(sample_transactions: List[Dict]) -> None:
    result = process_bank_search(sample_transactions, "Перевод")
    assert len(result) == 5  # Все транзакции содержат "Перевод"

    result = process_bank_search(sample_transactions, "организации")
    assert len(result) == 2  # Две транзакции содержат "организации"


def test_process_bank_operations(sample_transactions: List[Dict]) -> None:
    categories = ["Перевод организации", "Перевод со счета на счет", "Перевод с карты на карту"]
    result = process_bank_operations(sample_transactions, categories)
    assert result == {
        "Перевод организации": 2,
        "Перевод со счета на счет": 2,
        "Перевод с карты на карту": 1
    }
