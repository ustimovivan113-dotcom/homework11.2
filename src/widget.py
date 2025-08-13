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
    year = date[:4]
    month = date[5:7]
    day = date[8:10]
    return day + "." + month + "." + year
