from masks import get_mask_card_number, get_mask_account, mask_account_card
from utils import get_date  # Если utils.py есть

# Тест masks
print(get_mask_card_number('7000792289606361'))
print(get_mask_account('73654108430135874305'))
print(mask_account_card('Visa Platinum 7000792289606361'))

# Тест utils
print(get_date('2024-03-11T02:26:18.671407'))