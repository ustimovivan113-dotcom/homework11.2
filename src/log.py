import logging
from typing import Any, Callable

# Устанавливаем уровень логирования DEBUG для всех логгеров
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger('').setLevel(logging.DEBUG)  # Устанавливаем для корневого логгера
logging.getLogger('test').setLevel(logging.DEBUG)  # Явно для логгера "test"


def log(func: Callable) -> Callable:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            result = func(*args, **kwargs)
            logging.info(f"Function {func.__name__} executed successfully with args: {args}")
            return result
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {str(e)}")
            raise
    return wrapper
