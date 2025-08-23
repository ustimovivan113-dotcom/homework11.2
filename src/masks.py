def get_mask_card_number(card_number: int) -> str:
    """
    Возвращает маску номера карты в формате XXXX XX** **** XXXX
    """
    card_number_str = str(card_number)
    if len(card_number_str) != 16:
        raise ValueError("Неверная длина номера")

    card_mask = card_number_str[:6] + "******" + card_number_str[-4:]
    card_mask = " ".join(card_mask[i : i + 4] for i in range(0, len(card_mask), 4))
    return card_mask


def get_mask_account(account_number: int) -> str:
    """
    Возвращает маску номера аккаунта в формате **XXXX
    """
    account_number_str = str(account_number)

    if len(account_number_str) != 20:
        raise ValueError("Неверная длина номера")

    mask_account = "**" + account_number_str[-4:]
    return mask_account
