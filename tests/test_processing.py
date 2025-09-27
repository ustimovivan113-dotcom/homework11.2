from collections import Counter

import pytest

from src.processing import filter_by_state, process_bank_operations, process_bank_search, sort_by_date


@pytest.fixture
def data() -> list:
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 111111111, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.mark.parametrize(
    "expected",
    [
        (
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ]
        ),
    ],
)
def test_filter_by_state(data: list, expected: list) -> None:
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
def test_filter_by_state_executed(data: list, state: str, expected: list) -> None:
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
def test_filter_by_state_canceled(data: list, state: str, expected: list) -> None:
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
def test_sort_by_date_without_is_reverse(data, expected):
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
def test_sort_by_date_is_reverse(data, expected):
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
    with pytest.raises(ValueError, match="time data '26/10/2023 10:00' does not match format '%d.%m.%Y'"):
        sort_by_date(invalid_format_data)

    # Случай с отсутствующим ключом "date"
    missing_key_data = [
        {"id": 1, "date": "2023-10-26T10:00:00.000000"},
        {"id": 2, "timestamp": "2023-10-25T12:00:00.000000"},  # Отсутствует 'date'
        {"id": 3, "date": "2023-10-27T08:00:00.000000"},
    ]
    with pytest.raises(KeyError, match="date"):
        sort_by_date(missing_key_data)

    # Случай с неполной датой
    incomplete_date_data = [
        {"id": 1, "date": "2023-10-26T10:00:00.000000"},
        {"id": 2, "date": "2023-10"},  # Отсутствует день
        {"id": 3, "date": "2023-10-27T08:00:00.000000"},
    ]
    with pytest.raises(ValueError, match="time data '2023-10' does not match format '%d.%m.%Y'"):
        sort_by_date(incomplete_date_data)

    # Случай с пустым списком
    empty_list_data = []
    sorted_empty = sort_by_date(empty_list_data)
    assert sorted_empty == []


@pytest.fixture
def process_bank_search_data():
    """Фикстура с примером банковских операций"""
    return [
        {"description": "Покупка в магазине Пятерочка", "amount": 1000},
        {"description": "Перевод с карты на карту", "amount": 5000},
        {"description": "Оплата услуг ЖКХ", "amount": 3000},
        {"description": "ПЯТЕРОЧКА супермаркет", "amount": 1500},
        {"description": "Кафе STARBUCKS", "amount": 700},
        {"description": "", "amount": 2000},  # пустое описание
        {"description": "Перевод", "amount": 10000},
    ]


def test_basic_search(process_bank_search_data):
    """Тест базового поиска"""
    result = process_bank_search(process_bank_search_data, "Пятерочка")
    assert len(result) == 2
    descriptions = [op["description"] for op in result]
    assert "Покупка в магазине Пятерочка" in descriptions
    assert "ПЯТЕРОЧКА супермаркет" in descriptions


def test_case_insensitive_search(process_bank_search_data):
    """Тест поиска без учета регистра"""
    result_lower = process_bank_search(process_bank_search_data, "пятерочка")
    result_upper = process_bank_search(process_bank_search_data, "ПЯТЕРОЧКА")
    result_mixed = process_bank_search(process_bank_search_data, "ПяТеРоЧкА")
    assert len(result_lower) == len(result_upper) == len(result_mixed) == 2


def test_no_matches(process_bank_search_data):
    """Тест когда нет совпадений"""
    result = process_bank_search(process_bank_search_data, "Аптека")
    assert len(result) == 0
    assert result == []


def test_empty_search_string(process_bank_search_data):
    """Тест с пустой строкой поиска"""
    result = process_bank_search(process_bank_search_data, "")
    assert len(result) == len(process_bank_search_data)


def test_empty_search_data():
    """Тест с пустым списком данных"""
    result = process_bank_search([], "Пятерочка")
    assert len(result) == 0
    assert result == []


def test_operation_without_description():
    """Тест с операциями без поля description"""
    data = [
        {"amount": 1000},  # нет description
        {"description": "Оплата", "amount": 2000},
        {"description": None, "amount": 3000},  # description = None
    ]
    result = process_bank_search(data, "Оплата")
    assert len(result) == 1
    assert result[0]["description"] == "Оплата"


@pytest.fixture
def process_bank_operations_data():
    """Фикстура с примером банковских операций"""
    return [
        {"description": "Супермаркет", "amount": 1000, "date": "2024-01-01"},
        {"description": "Аптека", "amount": 500, "date": "2024-01-02"},
        {"description": "Супермаркет", "amount": 2000, "date": "2024-01-03"},
        {"description": "Кафе", "amount": 700, "date": "2024-01-04"},
        {"description": "Транспорт", "amount": 300, "date": "2024-01-05"},
        {"description": "Аптека", "amount": 1200, "date": "2024-01-06"},
        {"description": "Интернет", "amount": 500, "date": "2024-01-07"},
        {"description": "", "amount": 1000, "date": "2024-01-08"},
        {"description": "Супермаркет", "amount": 1500, "date": "2024-01-09"},
    ]


def test_basic_functionality(process_bank_operations_data):
    """Тест базовой функциональности"""
    categories = ["Супермаркет", "Аптека", "Кафе"]
    result = process_bank_operations(process_bank_operations_data, categories)
    expected = Counter({"Супермаркет": 3, "Аптека": 2, "Кафе": 1})
    assert result == expected
    assert isinstance(result, Counter)


def test_empty_categories_list(process_bank_operations_data):
    """Тест с пустым списком категорий"""
    result = process_bank_operations(process_bank_operations_data, [])
    assert result == Counter()
    assert len(result) == 0


def test_categories_not_in_data(process_bank_operations_data):
    """Тест когда запрошенные категории отсутствуют в данных"""
    categories = ["Кино", "Театр", "Концерт"]
    result = process_bank_operations(process_bank_operations_data, categories)
    assert result == Counter()
    assert len(result) == 0


def test_partial_categories_match(process_bank_operations_data):
    """Тест когда только часть категорий есть в данных"""
    categories = ["Супермаркет", "Аптека", "Кино", "Театр"]
    result = process_bank_operations(process_bank_operations_data, categories)
    expected = Counter({"Супермаркет": 3, "Аптека": 2})
    assert result == expected


def test_case_sensitivity(process_bank_operations_data):
    """Тест чувствительности к регистру"""
    categories = ["супермаркет", "аптека", "кафе"]
    result = process_bank_operations(process_bank_operations_data, categories)
    assert result == Counter()
    assert len(result) == 0


def test_empty_operations_data():
    """Тест с пустым списком операций"""
    categories = ["Супермаркет", "Аптека"]
    result = process_bank_operations([], categories)
    assert result == Counter()
    assert len(result) == 0


def test_operations_without_description():
    """Тест с операциями без поля description"""
    data = [
        {"amount": 1000},
        {"description": "Супермаркет", "amount": 2000},
        {"description": None, "amount": 3000},
        {"description": "", "amount": 4000},
    ]
    categories = ["Супермаркет"]
    result = process_bank_operations(data, categories)
    expected = Counter({"Супермаркет": 1})
    assert result == expected
