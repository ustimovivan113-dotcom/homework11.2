from decorators import log


@log
def add_numbers(a: int, b: int) -> int:
    """Складывает два числа."""
    return a + b


@log
def divide_numbers(a: int, b: int) -> float:
    """Делит два числа."""
    if b == 0:
        raise ValueError("Деление на ноль невозможно")
    return a / b


# Тестирование
if __name__ == "__main__":
    # Успешный вызов
    result1 = add_numbers(5, 3)
    print(f"Результат сложения: {result1}")

    # Вызов с ошибкой
    try:
        result2 = divide_numbers(10, 0)
    except ValueError as e:
        print(f"Поймана ошибка: {e}")

    # Успешное деление
    result3 = divide_numbers(10, 2)
    print(f"Результат деления: {result3}")
