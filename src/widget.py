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


def mask_account_card(account_card: str) -> Optional[str]:
    """
    Маскирует номер карты или счёта на основе входной строки.
    Пример: 'Visa Platinum 1234567890123456' -> 'Visa Platinum **** **** **** 3456'
            'Счет 12345678901234567890' -> 'Счет **7890'
    """
    if not account_card:
        return None
    parts = account_card.split()
    if not parts:
        return None
    number = parts[-1]
    if "Счет" in account_card:
        return f"{' '.join(parts[:-1])} {get_mask_account(number)}"
    return f"{' '.join(parts[:-1])} {get_mask_card_number(number)}"


def get_date() -> str:
    """
    Возвращает текущую дату в формате строки (заглушка для теста).
    Замените на реальную реализацию, если требуется.
    """
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d")
