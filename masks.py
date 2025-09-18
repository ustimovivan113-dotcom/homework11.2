import logging

# Настройка логирования
logging.basicConfig(
    filename='logs/masks.log',
    filemode='w',
    format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('masks')

def get_mask_card_number(card_number: str) -> str:
    logger.info(f"Вызвана функция get_mask_card_number с аргументом: {card_number}")
    try:
        if len(card_number) != 16 or not card_number.isdigit():
            raise ValueError("Неверный номер карты")
        masked = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
        logger.info(f"Результат: {masked}")
        return masked
    except Exception as e:
        logger.error(f"Ошибка в get_mask_card_number: {str(e)}")
        raise

def get_mask_account(account_number: str) -> str:
    logger.info(f"Вызвана функция get_mask_account с аргументом: {account_number}")
    try:
        if len(account_number) < 4:
            raise ValueError("Неверный номер счёта")
        masked = f"**{account_number[-4:]}"
        logger.info(f"Результат: {masked}")
        return masked
    except Exception as e:
        logger.error(f"Ошибка: {str(e)}")
        raise

def mask_account_card(input_str: str) -> str:
    logger.info(f"Вызвана функция mask_account_card с аргументом: {input_str}")
    try:
        parts = input_str.split()
        if "Счет" in input_str:
            account_number = parts[-1]
            masked = f"Счет {get_mask_account(account_number)}"
        else:
            card_number = parts[-1]
            masked = f"{' '.join(parts[:-1])} {get_mask_card_number(card_number)}"
        logger.info(f"Результат: {masked}")
        return masked
    except Exception as e:
        logger.error(f"Ошибка: {str(e)}")
        raise