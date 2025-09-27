from unittest.mock import patch

import numpy as np

from main import get_transaction_path, state_approve, yes_or_not_approve, is_reverse, response_layout, main


def test_get_transaction_path():
    with patch("builtins.input", side_effect=["1"]):
        assert get_transaction_path() == "data/operations.json"
    with patch("builtins.input", side_effect=["2"]):
        assert get_transaction_path() == "data/transactions.csv"
    with patch("builtins.input", side_effect=["3"]):
        assert get_transaction_path() == "data/transactions_excel.xlsx"
    with patch("builtins.input", side_effect=["invalid", "1"]):
        assert get_transaction_path() == "data/operations.json"


def test_state_approve():
    with patch("builtins.input", side_effect=["EXECUTED"]):
        assert state_approve() == "EXECUTED"
    with patch("builtins.input", side_effect=["executed"]):
        assert state_approve() == "EXECUTED"
    with patch("builtins.input", side_effect=["INVALID", "PENDING"]):
        assert state_approve() == "PENDING"


def test_yes_or_not_approve():
    with patch("builtins.input", side_effect=["ДА"]):
        assert yes_or_not_approve("Question") is True
    with patch("builtins.input", side_effect=["Нет"]):
        assert yes_or_not_approve("Question") is False
    with patch("builtins.input", side_effect=["invalid", "ДА"]):
        assert yes_or_not_approve("Question") is True


def test_is_reverse():
    with patch("builtins.input", side_effect=["по убыванию"]):
        assert is_reverse() is True
    with patch("builtins.input", side_effect=["по возрастанию"]):
        assert is_reverse() is False
    with patch("builtins.input", side_effect=["invalid", "по убыванию"]):
        assert is_reverse() is True


def test_response_layout():
    operation = {
        "date": "2023-10-01T10:00:00.000Z",
        "description": "Перевод на карту",
        "from": "Visa 1234567890123456",
        "to": "Счет 12345678901234567890",
        "operationAmount": {"amount": "1000.00", "currency": {"name": "RUB"}},
    }
    expected = "01.10.2023 Перевод на карту\nVisa 1234 56** **** 3456 -> Счет **7890\n1000.00 RUB"
    assert response_layout(operation) == expected

    operation_no_from = {
        "date": "2023-10-01T10:00:00.000Z",
        "description": "Оплата",
        "to": "Счет 12345678901234567890",
        "operationAmount": {"amount": "500.00", "currency": {"name": "RUB"}},
    }
    expected_no_from = "01.10.2023 Оплата\nСчет **7890\n500.00 RUB"
    assert response_layout(operation_no_from) == expected_no_from

    operation_alt_format = {
        "date": "2023-10-01T10:00:00.000Z",
        "description": "Пополнение",
        "to": "Счет 12345678901234567890",
        "amount": "200.00",
        "currency_name": "USD",
    }
    expected_alt_format = "01.10.2023 Пополнение\nСчет **7890\n200.00 USD"
    assert response_layout(operation_alt_format) == expected_alt_format

    operation_with_nan = {
        "date": "2023-10-01T10:00:00.000Z",
        "description": "Пополнение",
        "from": np.nan,
        "to": "Счет 12345678901234567890",
        "amount": "200.00",
        "currency_name": "USD",
    }
    assert response_layout(operation_with_nan) == expected_alt_format


@patch("main.get_transaction_path", return_value="data/operations.json")
@patch(
    "main.get_transaction_data",
    return_value=[
        {
            "date": "2023-10-01T10:00:00.000Z",
            "description": "Перевод на карту",
            "from": "Visa 1234567890123456",
            "to": "Счет 12345678901234567890",
            "state": "EXECUTED",
            "operationAmount": {"amount": "1000.00", "currency": {"name": "RUB", "code": "RUB"}},
        }
    ],
)
@patch("main.state_approve", return_value="EXECUTED")
@patch("main.yes_or_not_approve", side_effect=[False, False, False])
@patch("builtins.print")
def test_main(mock_print, mock_yes_or_not, mock_state, mock_get_data, mock_get_path):
    main()
    mock_print.assert_any_call("Всего банковских операций в выборке: 1")
    mock_print.assert_any_call(
        "01.10.2023 Перевод на карту\nVisa 1234 56** **** 3456 -> Счет **7890\n1000.00 RUB"
    )
