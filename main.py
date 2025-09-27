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
        messages = "Введите 1-3"
        try:
            print(messages)
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
        messages = "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING"
        print(messages)
        user_choice = input()
        if user_choice.upper() in state_list:
            current_state = user_choice.upper()
            return current_state
        else:
            print(f'Статус операции "{user_choice}" недоступен')


def yes_or_not_approve(question: str) -> bool:
    """
    Функция для проверки корректности ответа на вопросы типа Да/Нет
    """
    messages = question
    while True:
        print(messages)
        user_message = input()
        if user_message.upper() == "ДА":
            return True
        if user_message.upper() == "НЕТ":
            return False
        else:
            print(f'Ваш ответ "{user_message}" некоректен')


def is_reverse() -> bool:
    """
    Функция для провреки сортировки по убыванию или возростанию
    """
    messages = "Отсортировать по возрастанию или по убыванию?"
    print(messages)
    while True:
        user_message = input()
        if "УБЫВ" in user_message.upper():
            return True
        if "ВОЗРА" in user_message.upper():
            return False
        else:
            print(f'Ваш ответ "{user_message}" некоректен')
            print("Введите по возрастанию/по убыванию")


def response_layout(operation: dict) -> str:
    """
    Функция для компановки ответа
    """
    date = get_date(operation.get("date"))
    description = operation.get("description")
    operation_result = ""

    value = operation.get("from")
    if value is not None and str(value).lower() != "nan":
        operation_result = f"{mask_account_card(operation.get("from"))} -> "

    operation_result += mask_account_card(operation.get("to"))

    amount = ""
    if operation.get("operationAmount", {}).get("amount", {}):
        amount_raw = operation.get("operationAmount", {}).get("amount", {})
        currency_name = operation.get("operationAmount", {}).get("currency", {}).get("name")
        amount = f"{amount_raw} {currency_name}"

    else:
        amount_raw = operation.get("amount")
        currency_name = operation.get("currency_name")
        amount = f"{amount_raw} {currency_name}"

    result = f"""
{date} {description}
{operation_result}
{amount}
"""
    return result


def main():
    """
    Функция которая отвечает за основную логику проекта и связывает функциональности между собой.
    """
    print("Добро пожаловать!")
    print(
        """Выберите необходимый пункт меню:
                    1. Получить информацию о транзакциях из JSON-файла
                    2. Получить информацию о транзакциях из CSV-файла
                    3. Получить информацию о транзакциях из XLSX-файла"""
    )

    # Получаем путь файла и его тип
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


main()
