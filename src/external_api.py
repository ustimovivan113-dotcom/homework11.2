import requests
from dotenv import load_dotenv
import os
from typing import Dict, Any

load_dotenv()

API_KEY = os.getenv('EXCHANGE_API_KEY')
BASE_URL = 'https://api.apilayer.com/exchangerates_data/convert'

def convert_to_rub(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в RUB.
    Если валюта RUB — возвращает amount.
    Если USD/EUR — конвертирует через API.
    """
    amount = float(transaction.get('operationAmount', {}).get('amount', '0'))
    currency = transaction.get('operationAmount', {}).get('currency', {}).get('code', 'RUB')

    if currency == 'RUB':
        return amount

    if currency not in ['USD', 'EUR']:
        raise ValueError(f"Unsupported currency: {currency}")

    if not API_KEY:
        raise ValueError("API key not provided in .env")

    headers = {"apikey": API_KEY}
    params = {
        'to': 'RUB',
        'from': currency,
        'amount': amount
    }

    try:
        response = requests.get(BASE_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return float(data['result'])
    except requests.RequestException as e:
        raise ValueError(f"API request failed: {str(e)}")