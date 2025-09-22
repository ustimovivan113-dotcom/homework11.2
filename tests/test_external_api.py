import pytest
import requests
from src.external_api import convert_to_rub, get_currency_rate


def test_convert_to_rub_usd():
    result = convert_to_rub(100, "USD")
    assert isinstance(result, float)
    assert result > 0


def test_convert_to_rub_rub():
    assert convert_to_rub(100, "RUB") == 100


def test_get_currency_rate():
    rate = get_currency_rate("USD")
    assert isinstance(rate, float)
    assert rate > 0


def test_get_currency_rate_error(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.RequestException("API error")
    monkeypatch.setattr(requests, "get", mock_get)
    with pytest.raises(requests.RequestException):
        get_currency_rate("USD")
