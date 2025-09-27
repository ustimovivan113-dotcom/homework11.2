from datetime import datetime
from typing import Optional


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер карты: показывает последние 4 цифры.
    Пример: '1234567890123456' -> '**** **** **** 3456'
    """
    if not isinstance(card_number, str) or not card_number.isdigit():
        raise ValueError("Card number must be a string of digits")
    if len(card_number) < 4:
        return card_number
    return f"**** **** **** {card_number[-4:]}"


def get_mask_account(account: str) -> str:
    """
    Маскирует номер счёта: показывает последние 4 цифры.
    Пример: '12345678901234567890' -> '**7890'
    """
    if not isinstance(account, str) or not account.isdigit():
        raise ValueError("Account number must be a string of digits")
    if len(account) < 4:
        raise ValueError("Account number is too short")  # Изменено: выброс ошибки
    if len(account) > 20:
        raise ValueError("Account number is too long")
    return f"**{account[-4:]}"


def mask_account_card(card_or_account: str) -> str:
    if not card_or_account:
        return "Информация неверна"
    if card_or_account.startswith("Счет"):
        account_number = card_or_account.split()[-1]
        if len(account_number) < 4:
            raise ValueError("Account number must be at least 4 characters long")
        if len(account_number) > 20:
            raise ValueError("Account number must not exceed 20 characters")
        return "Счет **" + account_number[-4:]
    # Для карт
    card_type, card_number = card_or_account.rsplit(" ", 1)
    if len(card_number) != 16:
        raise ValueError("Card number must be 16 digits long")
    return f"{card_type} {card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def get_date(date_str: str) -> str:
    if not date_str:
        return "Дата не может быть пустой"
    try:
        # Пробуем разные форматы даты
        for fmt in ["%Y-%m-%dT%H:%M:%S.%f", "%Y/%m/%d", "%Y.%m.%d"]:
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                return parsed_date.strftime("%d.%m.%Y")
            except ValueError:
                continue
        return "Неверный формат даты"
    except Exception:
        return "Неверный формат даты"
