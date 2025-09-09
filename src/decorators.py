import functools
import logging
from typing import Callable, Any

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('function_calls.log'),
        logging.StreamHandler()
    ]
)


def log(func: Callable) -> Callable:
    """
    Декоратор для логирования вызовов функций, их результатов и ошибок.

    Args:
        func: Функция, которую нужно декорировать

    Returns:
        Обернутая функция с логированием
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            # Логируем начало вызова функции
            logging.info(f"Вызов функции: {func.__name__}")
            logging.info(f"Аргументы: args={args}, kwargs={kwargs}")

            # Выполняем функцию
            result = func(*args, **kwargs)

            # Логируем результат
            logging.info(f"Функция {func.__name__} завершилась успешно")
            logging.info(f"Результат: {result}")

            return result

        except Exception as e:
            # Логируем ошибку
            logging.error(f"Ошибка в функции {func.__name__}: {str(e)}")
            raise

    return wrapper
