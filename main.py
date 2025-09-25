from src.utils import load_transactions
from src.widget import get_date, mask_account_card

if __name__ == "__main__":
    try:
        csv_data = load_transactions('C:/Users/IVAN/Downloads/homework11.2/transactions.csv')
        print(f"CSV загружено: {len(csv_data)} транзакций")
        xlsx_data = load_transactions('C:/Users/IVAN/Downloads/homework11.2/transactions_excel.xlsx')
        print(f"XLSX загружено: {len(xlsx_data)} транзакций")
        print(mask_account_card("Visa Platinum 1234567890123456"))
        print(mask_account_card("Счет 12345678901234567890"))
        print(f"Дата: {get_date()}")
    except Exception as e:
        print(f"Ошибка: {e}")
