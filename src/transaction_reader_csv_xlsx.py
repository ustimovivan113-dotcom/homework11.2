from typing import List, Dict
import pandas as pd
import os



def read_transactions_csv(file_path:str) -> List[Dict]:
    """
    Функция для считывания финансовых операций из CSV
    """
    csv_data = pd.read_csv(file_path)
    return csv_data.to_dict(orient='records')

def read_transactions_xlsx(file_path:str) -> List[Dict]:
    """
    Функция для считывания финансовых операций из Excel
    """
    xlsx_data = pd.read_excel(file_path)
    return xlsx_data.to_dict(orient='records')

