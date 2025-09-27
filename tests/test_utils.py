import pytest

from src.utils import load_transactions


def test_load_transactions_csv():
    transactions = load_transactions('C:/Users/IVAN/Downloads/homework11.2/transactions.csv')
    assert len(transactions) > 0
    assert 'id' in transactions[0]


def test_load_transactions_xlsx():
    transactions = load_transactions('C:/Users/IVAN/Downloads/homework11.2/transactions_excel.xlsx')
    assert len(transactions) > 0
    assert 'id' in transactions[0]


def test_invalid_file():
    with pytest.raises(ValueError):
        load_transactions('invalid.txt')
