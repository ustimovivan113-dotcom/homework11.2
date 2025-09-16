from src.external_api import convert_to_rub
transaction = {
    "operationAmount": {
        "amount": "100.00",
        "currency": {"code": "USD"}
    }
}
print(convert_to_rub(transaction))  # Должен вывести ~amount в RUB