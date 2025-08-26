from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_card: str) -> str:
    """
    Обрабатывает номер карты или номер счёта
    """
    is_card_number = False
    if "счет" not in account_card.lower().replace("ё", "e"):
        is_card_number = True

    account_card_arr = account_card.split()
    prefix_number = ""
    for word in account_card_arr:
        if word.isalpha():
            prefix_number = prefix_number + " " + word
        if word.isdigit():
            if is_card_number:
                card_number = get_mask_card_number(int(word))
                return prefix_number[1:] + " " + card_number
            else:
                account_number = get_mask_account((int(word)))
                return prefix_number[1:] + " " + account_number
    return "Информация неверна"


def get_date(date: str) -> str:
    """
    Возвращает дату из формата ГГГГ-ММ-ДД в ДД.ММ.ГГГГ
    """
    if len(date) <= 1:
        return "Дата не может быть пустой"
    year = date[:4]
    month = date[5:7]
    day = date[8:10]
    new_date = day + "." + month + "." + year

    if is_date(new_date):
        return new_date
    else:
        return "Неверный формат даты"


def is_date(date_string: str, date_format: str = "%d.%m.%Y") -> bool:
    """
    Проверяет, является ли строка допустимой датой по заданному формату.
    """
    try:
        datetime.strptime(date_string, date_format)
        return True
    except ValueError:
        return False
