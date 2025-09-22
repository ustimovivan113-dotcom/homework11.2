import pytest
from utils import get_date, load_transactions


def test_get_date():
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"


def test_load_transactions():
    transactions = load_transactions("data/operations.json")
    assert isinstance(transactions, list)
    assert len(transactions) > 0


def test_load_transactions_error():
    with pytest.raises(FileNotFoundError):
        load_transactions("nonexistent.json")


def test_get_date_error():
    with pytest.raises(ValueError):
        get_date("invalid_date")
