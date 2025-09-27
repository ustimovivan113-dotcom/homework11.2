import logging

import requests

logging.basicConfig(
    filename="logs/external_api.log",
    filemode="w",
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    level=logging.DEBUG,
)
logger = logging.getLogger("external_api")


def convert_to_rub(amount: float, currency: str) -> float:
    logger.info(f"Вызвана функция convert_to_rub с аргументами amount={amount}, currency={currency}")
    try:
        if currency == "USD":
            response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
            response.raise_for_status()
            rate = response.json()["rates"]["RUB"]
            result = amount * rate
        else:
            result = amount
        logger.info(f"Результат конвертации: {result} RUB")
        return result
    except Exception as e:
        logger.error(f"Ошибка в convert_to_rub: {str(e)}")
        raise


def get_currency_rate(currency: str) -> float:
    logger.info(f"Вызвана функция get_currency_rate с аргументом currency={currency}")
    try:
        response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{currency}")
        response.raise_for_status()
        rate = response.json()["rates"]["RUB"]
        logger.info(f"Курс {currency} к RUB: {rate}")
        return rate
    except Exception as e:
        logger.error(f"Ошибка в get_currency_rate: {str(e)}")
        raise
