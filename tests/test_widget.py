import pytest
from src.widget import get_date, mask_account_card, get_mask_card_number, get_mask_account

def test_mask_card_number():
    assert get_mask_card_number("1234567890123456") == "**** **** **** 3456"
    with pytest.raises(ValueError):
        get_mask_card_number("abc")

def test_mask_account():
    assert get_mask_account("12345678901234567890") == "**7890"
    with pytest.raises(ValueError):
        get_mask_account("abc")

def test_mask_account_card():
    assert mask_account_card("Visa Platinum 1234567890123456") == "Visa Platinum **** **** **** 3456"
    assert mask_account_card("Счет 12345678901234567890") == "Счет **7890"
    assert mask_account_card("") is None

def test_get_date():
    pass  # Замените на тест для get_date, если есть реализация