import numpy as np

from src.generators import filter_by_currency
from src.processing import filter_by_state, process_bank_search, sort_by_date
from src.utils import load_json_data, read_transactions_csv, read_transactions_xlsx
from src.widget import get_date, mask_account_card

list_data_filepath = {1: "data/operations.json", 2: "data/transactions.csv", 3: "data/transactions_excel.xlsx"}


def get_transaction_path() -> str:
    """
    Выбор типа транзакции
    """
    file_path = ""
    while True:
        print("Введите 1-3")
        try:
            user_choice = int(input())
            if user_choice in list_data_filepath:
                file_path = str(list_data_filepath.get(user_choice))
                return file_path
        except ValueError:
            continue
    return file_path


def get_transaction_data(file_path: str, file_type: str) -> list[dict]:
    """
    Возвращает тип файла
    """
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
    state_list = ["EXECUTED", "CANCELED", "PENDING"]

    while True:
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")
        user_choice = input()
        if user_choice.upper() in state_list:
            return user_choice.upper()
        else:
            print(f'Статус операции "{user_choice}" недоступен')


def yes_or_not_approve(question: str) -> bool:
    """
    Функция для проверки корректности ответа на вопросы типа Да/Нет
    """
    while True:
        print(question)
        user_message = input()
        if user_message.upper() == "ДА":
            return True
        if user_message.upper() == "НЕТ":
            return False
        else:
            print(f'Ваш ответ "{user_message}" некорректен')


def is_reverse() -> bool:
    """
    Функция для проверки сортировки по убыванию или возрастанию
    """
    print("Отсортировать по возрастанию или по убыванию?")
    while True:
        user_message = input()
        if "УБЫВ" in user_message.upper():
            return True
        if "ВОЗРА" in user_message.upper():
            return False
        else:
            print(f'Ваш ответ "{user_message}" некорректен')
            print("Введите по возрастанию/по убыванию")


def response_layout(operation: dict) -> str:
    """
    Функция для компоновки ответа
    """
    date = get_date(operation.get("date", "") or "")
    description = operation.get("description", "")
    operation_result = ""

    value = operation.get("from")
    if value is not None and not (isinstance(value, float) and np.isnan(value)):
        operation_result = f"{mask_account_card(str(value))} -> "

    to_value = operation.get("to", "")
    operation_result += mask_account_card(str(to_value))

    amount = ""
    operation_amount = operation.get("operationAmount", {})
    if operation_amount and operation_amount.get("amount") is not None:
        amount_raw = operation_amount.get("amount", "")
        currency_name = operation_amount.get("currency", {}).get("name", "")
        amount = f"{amount_raw} {currency_name}"
    else:
        amount_raw = operation.get("amount", "")
        currency_name = operation.get("currency_name", "")
        amount = f"{amount_raw} {currency_name}"

    return f"{date} {description}\n{operation_result}\n{amount}"


def main() -> None:
    """
    Функция, которая отвечает за основную логику проекта и связывает функциональности между собой.
    """
    print("Добро пожаловать!")
    print(
        """Выберите необходимый пункт меню:
                    1. Получить информацию о транзакциях из JSON-файла
                    2. Получить информацию о транзакциях из CSV-файла
                    3. Получить информацию о транзакциях из XLSX-файла"""
    )

    transaction_path = get_transaction_path()
    transaction_file_type = transaction_path.rsplit(".", 1)[-1]

    print(f"Для обработки выбран {transaction_file_type} файл")

    data = get_transaction_data(transaction_path, transaction_file_type)

    print("Введите статус, по которому необходимо выполнить фильтрацию.")

    state = state_approve()
    print(f'Операции отфильтрованы по статусу "{state}"')

    data = filter_by_state(data, state)

    if yes_or_not_approve("Отсортировать операции по дате? Да/Нет"):
        revers_date = is_reverse()
        data = sort_by_date(data, revers_date)
    if yes_or_not_approve("Выводить только рублевые транзакции? Да/Нет"):
        iterator_result = filter_by_currency(data, "RUB")
        data = list(iterator_result)
    if yes_or_not_approve("Отфильтровать список транзакций по определенному слову в описании? Да/Нет"):
        print("Введите слово:")
        user_input = input()
        data = process_bank_search(data, user_input)

    print("Распечатываю итоговый список транзакций...")
    if len(data) > 0:
        print(f"Всего банковских операций в выборке: {len(data)}")
        for operation in data:
            print(response_layout(operation))
    else:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")


if __name__ == "__main__":
    main()
