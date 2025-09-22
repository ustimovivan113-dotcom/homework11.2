import pytest
from masks import get_mask_card_number, get_mask_account


def test_get_mask_card_number():
    assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"


def test_get_mask_card_number_long_length():
    with pytest.raises(ValueError):
        get_mask_card_number("7000792289606361111")


def test_get_mask_card_number_small_length():
    with pytest.raises(ValueError):
        get_mask_card_number("700079228960")


def test_get_mask_card_number_empty_length():
    with pytest.raises(ValueError):
        get_mask_card_number("")


def test_get_mask_account():
    assert get_mask_account("73654108430135874305") == "**4305"


def test_get_mask_account_long_length():
    with pytest.raises(ValueError):
        get_mask_account("736541084301358743051111")


def test_get_mask_account_small_length():
    with pytest.raises(ValueError):
        get_mask_account("123")


def test_get_mask_account_empty_length():
    with pytest.raises(ValueError):
        get_mask_account("")
