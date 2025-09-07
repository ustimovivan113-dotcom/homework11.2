from typing import Callable, Optional, Any
from time import time
import functools
import datetime


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования вызовов функции
    """
    def decorator(func: Callable) -> Callable:
        """
        Обертка-декоратора функции.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            """
            Обертка, выполнения функции и отлавливания исключений.
            """
            # Формируем сообщение о начале выполнения
            start_time = time()
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            log_message = f"{current_time} - {func.__name__} начала выполнение. args: {args}, kwargs: {kwargs}"

            if filename:
                with open(filename, "a", encoding="utf-8") as f:
                    f.write(log_message + "\n")
            else:
                print(log_message)

            try:
                # Выполняем функцию
                result = func(*args, **kwargs)
                end_time = time()

                # Логируем успешное завершение
                success_message = (f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - "
                                   f"{func.__name__} завершилась успешно. "
                                   f"Результат: {result}, "
                                   f"Время выполнения: {end_time - start_time:.4f}с")
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(success_message + '\n')
                else:
                    print(success_message)

                return result

            except Exception as e:
                end_time = time()

                #Логируем ошибку
                error_message = (f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - "
                                f"{func.__name__} завершилась с ошибкой: {type(e).__name__}: {e}. "
                                f"Args: {args}, Kwargs: {kwargs}, "
                                f"Время выполнения: {end_time - start_time:.4f}с")

                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(error_message + '\n')
                else:
                    print(error_message)

                # Пробрасываем исключение дальше
                raise

        return wrapper

    return decorator
