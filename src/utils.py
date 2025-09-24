import json
import pandas as pd
from typing import List, Dict, Any
from src.log import log


@log
def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает транзакции из JSON, CSV или XLSX файла.
    """
    if file_path.endswith('.json'):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    elif file_path.endswith('.csv'):
        df = pd.read_csv(file_path, delimiter=';', na_values=['', 'None'], encoding='utf-8')
        df = df.dropna(how='all')
        return df.to_dict(orient='records')

    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path, sheet_name='Лист 1', na_values=['', 'None'])
        df = df.dropna(how='all')
        return df.to_dict(orient='records')

    else:
        raise ValueError(f"Unsupported file format: {file_path}")
