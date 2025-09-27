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


@pytest.fixture
def account_number() -> int:
    return 11112222333344445555


@pytest.mark.parametrize("expected", ["**5555"])
def test_get_mask_account(account_number: int, expected: str) -> None:
    """
    Тест маски номера счёта
    """
    assert get_mask_account(account_number) == expected
