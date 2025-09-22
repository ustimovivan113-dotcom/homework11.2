import json
import logging
import os
from pathlib import Path
from typing import Dict, List

import pandas as pd

MODULE_DIR = Path(__file__).resolve().parent
LOG_DIR = MODULE_DIR.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
log_file = LOG_DIR / "utils.log"
file_handler = logging.FileHandler(log_file, mode="w")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(funcName)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def load_json_data(file_path: str) -> list[dict]:
    """
    Возвращает данные о финансовых транзакция из JSON
    """
    try:
        if not os.path.exists(file_path):
            logger.warning("File not found")
            return []

        if os.path.getsize(file_path) == 0:
            logger.warning("File is empty")
            return []

        with open(file_path, "r", encoding="utf-8") as file:
            logger.info(f"Reading file from: {file_path}")
            data = json.load(file)

        if not isinstance(data, list):
            logger.warning("File does not contain valid data")
            return []

        return data

    except (json.JSONDecodeError, FileNotFoundError, PermissionError, OSError):
        logger.error("Incorrect data")
        return []


def read_transactions_csv(file_path: str) -> List[Dict]:
    """
    Функция для считывания финансовых операций из CSV
    """
    csv_data = pd.read_csv(file_path, sep=";")
    return csv_data.to_dict(orient="records")


def read_transactions_xlsx(file_path: str) -> List[Dict]:
    """
    Функция для считывания финансовых операций из Excel
    """
    xlsx_data = pd.read_excel(file_path)
    return xlsx_data.to_dict(orient="records")
