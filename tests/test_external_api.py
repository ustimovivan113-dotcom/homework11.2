from unittest.mock import MagicMock, patch

import pytest

from src.external_api import get_transaction_amount_in_rubles


# Фикстуры для тестовых данных
@pytest.fixture
def rub_transaction():
    return {"operationAmount": {"amount": "100.50", "currency": {"code": "RUB", "name": "руб."}}}


@pytest.fixture
def usd_transaction():
    return {"operationAmount": {"amount": "50.75", "currency": {"code": "USD", "name": "USD"}}}


@pytest.fixture
def eur_transaction():
    return {"operationAmount": {"amount": "30.25", "currency": {"code": "EUR", "name": "EUR"}}}


@pytest.fixture
def invalid_transaction():
    return {"invalid": "data"}


@pytest.fixture
def transaction_missing_currency():
    return {"operationAmount": {"amount": "100.50"}}


@pytest.fixture
def transaction_missing_amount():
    return {"operationAmount": {"currency": {"code": "USD"}}}


# Тесты для RUB транзакций (без API вызова)
def test_rub_transaction_returns_same_amount(rub_transaction):
    """Тест RUB транзакции возвращает ту же сумму"""
    result = get_transaction_amount_in_rubles(rub_transaction)
    assert result == 100.50


def test_rub_transaction_no_api_call(rub_transaction):
    """Тест что для RUB не происходит API вызов"""
    with patch("requests.get") as mock_get:
        result = get_transaction_amount_in_rubles(rub_transaction)
        mock_get.assert_not_called()
        assert result == 100.50


def test_usd_transaction_successful_conversion(usd_transaction):
    """Тест успешной конвертации USD в RUB"""
    mock_response = MagicMock()
    mock_response.json.return_value = {"result": 3806.25}  # 50.75 USD * 75

    with patch("requests.get", return_value=mock_response):
        result = get_transaction_amount_in_rubles(usd_transaction)
        assert result == 3806.25


def test_eur_transaction_successful_conversion(eur_transaction):
    """Тест успешной конвертации EUR в RUB"""
    mock_response = MagicMock()
    mock_response.json.return_value = {"result": 2571.25}  # 30.25 EUR * 85

    with patch("requests.get", return_value=mock_response):
        result = get_transaction_amount_in_rubles(eur_transaction)
        assert result == 2571.25


# Параметризованные тесты для разных валют
@pytest.mark.parametrize(
    "currency_code,amount,expected_multiplier",
    [
        ("USD", "100.0", 75.0),  # USD -> RUB
        ("EUR", "100.0", 85.0),  # EUR -> RUB
        ("GBP", "100.0", 95.0),  # GBP -> RUB
        ("JPY", "100.0", 0.65),  # JPY -> RUB
    ],
)
def test_different_currencies_conversion(currency_code, amount, expected_multiplier):
    """Тест конвертации разных валют"""
    transaction = {"operationAmount": {"amount": amount, "currency": {"code": currency_code}}}

    expected_result = float(amount) * expected_multiplier
    mock_response = MagicMock()
    mock_response.json.return_value = {"result": expected_result}

    with patch("requests.get", return_value=mock_response):
        result = get_transaction_amount_in_rubles(transaction)
        assert result == expected_result


# Тесты для различных форматов amount
@pytest.mark.parametrize("amount_str", ["100.50", "100", "0.75", "9999.99", "0.01"])
def test_different_amount_formats(amount_str):
    """Тест различных форматов суммы"""
    transaction = {"operationAmount": {"amount": amount_str, "currency": {"code": "USD"}}}

    expected_result = float(amount_str) * 75.0
    mock_response = MagicMock()
    mock_response.json.return_value = {"result": expected_result}

    with patch("requests.get", return_value=mock_response):
        result = get_transaction_amount_in_rubles(transaction)
        assert result == expected_result
