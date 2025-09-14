import json
import os


def load_json_data(file_path: str) -> list[dict]:
    """
    Возвращает данные о финансовых транзакция из JSON
    """
    try:
        if not os.path.exists(file_path):
            return []

        if os.path.getsize(file_path) == 0:
            return []

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            return []

        return data

    except (json.JSONDecodeError, FileNotFoundError, PermissionError, OSError):
        return []
