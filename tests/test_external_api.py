import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pytest
from unittest.mock import patch, Mock
from src.external_api import convert_to_rub

def test_convert_to_rub_rub_currency():
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "RUB"}
        }
    }
    assert convert_to_rub(transaction) == 100.0

def test_convert_to_rub_unsupported_currency():
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "GBP"}
        }
    }
    with pytest.raises(ValueError, match="Unsupported currency: GBP"):
        convert_to_rub(transaction)

@patch('src.external_api.requests.get')
def test_convert_to_rub_usd(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {'result': 9000.0}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "USD"}
        }
    }
    assert convert_to_rub(transaction) == 9000.0
    mock_get.assert_called_once()

@patch('src.external_api.requests.get')
def test_convert_to_rub_api_failure(mock_get):
    mock_get.side_effect = Mock(side_effect=requests.RequestException("API error"))
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "USD"}
        }
    }
    with pytest.raises(ValueError, match="API request failed: API error"):
        convert_to_rub(transaction)