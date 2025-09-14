import os
import requests
from dotenv import load_dotenv
load_dotenv('../.env')

API_KEY = os.getenv('API_KEY')

def get_transaction_amount_in_rubles(transaction: dict) -> float:
    """
    Функция конвертации валюты в рубли
    """
    current_currency_code = transaction.get('operationAmount', {}).get('currency', {}).get('code')
    amount = transaction.get('operationAmount', {}).get('amount')

    if current_currency_code == 'RUB':
        return amount

    url = "https://api.apilayer.com/exchangerates_data/convert"
    headers = {
        "apikey": API_KEY
    }
    params = {
        "from": current_currency_code,
        "to": 'RUB',
        "amount": amount
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()['result']
