import logging
import json
from datetime import datetime
from typing import List, Dict

logging.basicConfig(
    filename="logs/utils.log",
    filemode="w",
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    level=logging.DEBUG,
)
logger = logging.getLogger("utils")


def get_date(date_str: str) -> str:
    logger.info(f"Вызвана функция get_date с аргументом: {date_str}")
    try:
        date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        formatted_date = date_obj.strftime("%d.%m.%Y")
        logger.info(f"Результат: {formatted_date}")
        return formatted_date
    except Exception as e:
        logger.error(f"Ошибка в get_date: {str(e)}")
        raise


def load_transactions(file_path: str) -> List[Dict]:
    logger.info(f"Вызвана функция load_transactions с аргументом: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            transactions = json.load(file)
        logger.info(f"Загружено {len(transactions)} транзакций")
        return transactions
    except Exception as e:
        logger.error(f"Ошибка в load_transactions: {str(e)}")
        raise
