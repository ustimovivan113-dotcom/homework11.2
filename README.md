# Проект "Виджет банковских операций"

## Описание:

Проект созданный для обучения языка python

## Установка:

1. Клонируйте репозиторий:
```
git clone https://github.com/ZloyKINDER/Educational_Bank.git
```

## Реализованные функции:

1. get_mask_card_number - Возвращает маску номера карты в формате XXXX XX** **** XXXX.

2. get_mask_account - Возвращает маску номера аккаунта в формате **XXXX.

3. mask_account_card - Обрабатывает номер карты или номер счёта.

4. get_date - Возвращает дату из формата ГГГГ-ММ-ДД в ДД.ММ.ГГГГ.

5. filter_by_state - Фильтрует список словарей по значению ключа 'state'.

6. sort_by_date - Сортирует список словарей по значению ключа 'date'.

7. filter_by_currency - Возвращает итератор, который поочередно выдает транзакции, где валюта операции соответствует заданной (например, USD)..

8. transaction_descriptions - Принимает список словарей с транзакциями и возвращает описание каждой операции по очереди.

9. card_number_generator - Генерирует номер карты в формате XXXX XXXX XXXX XXXX в заданном диапозоне.

## Примеры использования:

1. get_mask_card_number
```
# Пример для номера карты
print(get_mask_card_number('7000792289606361'))

7000792289606361     # входной аргумент
7000 79** **** 6361  # выход функции
```

2. get_mask_account

```
# Пример для номера счета
print(get_mask_account('73654108430135874305'))

73654108430135874305  # входной аргумент
**4305  # выход функции
```

3. mask_account_card
```
# Пример для карты
print(mask_account_card('Maestro 1596837868705199'))

Visa Platinum 7000792289606361  # входной аргумент
Visa Platinum 7000 79** **** 6361  # выход функции

# Пример для счета
print(mask_account_card('Счет 64686473678894779589'))

Счет 73654108430135874305  # входной аргумент
Счет **4305  # выход функции
```

4. get_date
```
print(get_date('2024-03-11T02:26:18.671407'))

2024-03-11T02:26:18.671407  # входной аргумент
11.03.2024  # выход функции
```

5. filter_by_state.
```

# Входной аргумент
data_list = [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}, {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]

print(filter_by_state(data_list))

# Выход функции со статусом по умолчанию 'EXECUTED'
[{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]

print(filter_by_state(data_list, 'CANCELED'))

# Выход функции, если вторым аргументов передано 'CANCELED'
[{'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]

```

6. sort_by_date.
```
# Входной аргумент
data_list = [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}, {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]

print(sort_by_date(data_list))

# Выход функции (сортировка по убыванию, т. е. сначала самые последние операции)
[{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}, {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]

print(sort_by_date(data_list, False))

# Выход функции, если вторым аргументов передано 'False'
[{'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}, {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}, {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}]
```

7. filter_by_currency.
```
usd_transactions = filter_by_currency(transactions, "USD")
for _ in range(2):
    print(next(usd_transactions))

>>> {
          "id": 939719570,
          "state": "EXECUTED",
          "date": "2018-06-30T02:08:58.425572",
          "operationAmount": {
              "amount": "9824.07",
              "currency": {
                  "name": "USD",
                  "code": "USD"
              }
          },
          "description": "Перевод организации",
          "from": "Счет 75106830613657916952",
          "to": "Счет 11776614605963066702"
      }
      {
              "id": 142264268,
              "state": "EXECUTED",
              "date": "2019-04-04T23:20:05.206878",
              "operationAmount": {
                  "amount": "79114.93",
                  "currency": {
                      "name": "USD",
                      "code": "USD"
                  }
              },
              "description": "Перевод со счета на счет",
              "from": "Счет 19708645243227258542",
              "to": "Счет 75651667383060284188"
       }
```

8. transaction_descriptions.
```
descriptions = transaction_descriptions(transactions)
for _ in range(5):
    print(next(descriptions))

>>> Перевод организации
    Перевод со счета на счет
    Перевод со счета на счет
    Перевод с карты на карту
    Перевод организации
```

9. card_number_generator.
```
for card_number in card_number_generator(1, 5):
    print(card_number)

>>> 0000 0000 0000 0001
    0000 0000 0000 0002
    0000 0000 0000 0003
    0000 0000 0000 0004
    0000 0000 0000 0005
```
## Реализованые декораторы:
1. log - автоматически регистрирует детали выполнения функций, такие как время вызова, имя функции, передаваемые аргументы, результат выполнения и информацию об ошибках.
```
# Пример использования декоратора
@log(filename="mylog.txt")
def my_function(x, y):
    return x + y

my_function(1, 2)
```

## Реализованны модули с тестированием:

1. test_mask - Тестирование для модуля masks.

2. test_widget - Тестирование для модуля widget.

3. test_processing - Тестировани для модуля processing.

4. test_generators - Тестировани для модуля generators.

5. test_decorators - Тестирование для модуля decorators.
