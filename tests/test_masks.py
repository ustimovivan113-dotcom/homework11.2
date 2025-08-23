import pytest
from src.masks import get_mask_account, get_mask_card_number


@pytest.fixture
def card_number():
    return 1111222233334444


@pytest.mark.parametrize("expected", ["1111 22** **** 4444"])
def test_get_mask_card_number(card_number, expected):
    assert get_mask_card_number(card_number) == expected


def test_get_mask_card_number_long_length():
    with pytest.raises(ValueError):
        get_mask_card_number(11112222333344445555)


def test_get_mask_card_number_small_length():
    with pytest.raises(ValueError):
        get_mask_card_number(111122223333)


def test_get_mask_card_number_empty_length():
    with pytest.raises(ValueError):
        get_mask_card_number(None)


@pytest.fixture
def account_number():
    return 11112222333344445555


@pytest.mark.parametrize("expected", ["**5555"])
def test_get_mask_account(account_number, expected):
    assert get_mask_account(account_number) == expected


def test_get_mask_account_long_length():
    with pytest.raises(ValueError):
        get_mask_account(111122223333444455556666)


def test_get_mask_account_small_length():
    with pytest.raises(ValueError):
        get_mask_account(1111222233334444)


def test_get_mask_account_empty_length():
    with pytest.raises(ValueError):
        get_mask_account(None)
