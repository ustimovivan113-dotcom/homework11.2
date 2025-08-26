import pytest

from src.widget import get_date, mask_account_card


def test_mask_card_number() -> None:
    assert mask_account_card("Maestro 1596837868705199") == "Maestro 1596 83** **** 5199"


def test_mask_account_number() -> None:
    assert mask_account_card("Счет 64686473678894779589") == "Счет **9589"


def test_mask_account_card_empty() -> None:
    assert mask_account_card("") == "Информация неверна"


@pytest.mark.parametrize(
    "value, expected",
    [
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Счет 35383033474447895560", "Счет **5560"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
        ("Visa Platinum 8990922113665229", "Visa Platinum 8990 92** **** 5229"),
        ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ],
)
def test_mask_account_card(value: str, expected: str) -> None:
    assert mask_account_card(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2024/03/11", "11.03.2024"),
        ("2024.03.11", "11.03.2024"),
    ],
)
def test_get_date(value: str, expected: str) -> None:
    assert get_date(value) == expected


def test_get_date_empty() -> None:
    assert get_date("") == "Дата не может быть пустой"


def test_get_date_wrong_format() -> None:
    assert get_date("2024-Март-11") == "Неверный формат даты"
