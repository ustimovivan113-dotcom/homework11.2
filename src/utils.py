import json
import os
import logging

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("../logs/utils.log", mode="w")
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
