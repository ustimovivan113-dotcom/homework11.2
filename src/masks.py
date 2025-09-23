import logging
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
LOG_DIR = MODULE_DIR.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)
log_file = LOG_DIR / "masks.log"
file_handler = logging.FileHandler(log_file, mode="w")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(funcName)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: int) -> str:
    """
    Возвращает маску номера карты в формате XXXX XX** **** XXXX
    """

    if isinstance(card_number, str):
        logger.warning(f"Card number: {card_number} is stroke")

    card_number_str = str(card_number)

    logger.info(f"A mask is created for the card number. {card_number}")
    card_mask = card_number_str[:6] + "******" + card_number_str[-4:]
    card_mask = " ".join(card_mask[i : i + 4] for i in range(0, len(card_mask), 4))
    return card_mask


def get_mask_account(account_number: int) -> str:
    """
    Возвращает маску номера аккаунта в формате **XXXX
    """
    if isinstance(account_number, str):
        logger.warning(f"Account number: {account_number} is stroke")
    account_number_str = str(account_number)

    logger.info(f"A mask is created for the account number. {account_number}")
    mask_account = "**" + account_number_str[-4:]
    return mask_account
