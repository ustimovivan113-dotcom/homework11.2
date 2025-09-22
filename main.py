from src.processing import filter_by_state
from src.utils import load_json_data, read_transactions_csv,read_transactions_xlsx


list_data_filepath = {1: "data/operations.json",
                      2: "data/transactions.csv",
                      3: "data/transactions_excel.xlsx"}



def get_transaction_path() -> str:
    """
    Выбор типа транзакции
    """
    while True:
        messages = "Введите 1-3"
        try:
            print(messages)
            user_choice = int(input())
            if user_choice in list_data_filepath:
                file_path = str(list_data_filepath.get(user_choice))
                return file_path
        except ValueError:
            continue


def get_transaction_data(file_path: str, file_type: str) -> list[dict]:
    if file_type == "json":
        return load_json_data(file_path)
    if file_type == "csv":
        return read_transactions_csv(file_path)
    if file_type == "xlsx":
        return read_transactions_xlsx(file_path)
    return []

def state_approve() -> str:
    """
    Функция для проверки корректности ввода статуса
    """
    state_list = ["EXECUTED", "CANCELED","PENDING"]

    while True:
        messages = "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING"
        print(messages)
        user_choice = input()
        if user_choice.upper() in state_list:
            current_state = user_choice.upper()
            return current_state
        else:
            print(f"Статус операции \"{user_choice}\" недоступен")




def main():
    """
    Функция которая отвечает за основную логику проекта и связывает функциональности между собой.
    """
    print("Добро пожаловать!")
    print("""Выберите необходимый пункт меню:
                    1. Получить информацию о транзакциях из JSON-файла
                    2. Получить информацию о транзакциях из CSV-файла
                    3. Получить информацию о транзакциях из XLSX-файла""")

    #Получаем путь файла и его тип
    transaction_path = get_transaction_path()
    transaction_file_type = transaction_path.rsplit('.', 1)[-1]

    print(f"Для обработки выбран {transaction_file_type} файл")

    data = get_transaction_data(transaction_path, transaction_file_type)

    print("Введите статус, по которому необходимо выполнить фильтрацию.")

    state = state_approve()
    print(f"Операции отфильтрованы по статусу \"{state}\"")

    data = filter_by_state(data, state)














main()

