import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.fixture
def card_number() -> int:
    return 1111222233334444


@pytest.mark.parametrize("expected", ["1111 22** **** 4444"])
def test_get_mask_card_number(card_number: int, expected: str) -> None:
    """
    Тест маски номера карты
    """
    assert get_mask_card_number(card_number) == expected


def test_get_mask_card_number_long_length() -> None:
    """
    Тест маски номера карты (длинный номер)
    """
    with pytest.raises(ValueError):
        get_mask_card_number(11112222333344445555)


def test_get_mask_card_number_small_length() -> None:
    """
    Тест маски номера карты (короткий номер)
    """
    with pytest.raises(ValueError):
        get_mask_card_number(111122223333)


def test_get_mask_card_number_empty_length() -> None:
    """
    Тест маски номера карты (пустой номер)
    """
    with pytest.raises(ValueError):
        get_mask_card_number(0)


@pytest.fixture
def account_number() -> int:
    return 11112222333344445555


@pytest.mark.parametrize("expected", ["**5555"])
def test_get_mask_account(account_number: int, expected: str) -> None:
    """
    Тест маски номера счёта
    """
    assert get_mask_account(account_number) == expected


def test_get_mask_account_long_length() -> None:
    """
    Тест маски номера счёта (длинный номер)
    """
    with pytest.raises(ValueError):
        get_mask_account(111122223333444455556666)


def test_get_mask_account_small_length() -> None:
    """
    Тест маски номера счёта (короткий номер)
    """
    with pytest.raises(ValueError):
        get_mask_account(1111222233334444)


def test_get_mask_account_empty_length() -> None:
    """
    Тест маски номера счёта (пустой номер)
    """
    with pytest.raises(ValueError):
        get_mask_account(0)
