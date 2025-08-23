import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture()
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
    Тест сортировки в порядке возростания
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
    with pytest.raises(KeyError, match="date"):  # Или другой код ошибки, если `x[data_key]` вызовет ее
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
