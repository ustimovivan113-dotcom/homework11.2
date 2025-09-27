import datetime
import functools
from typing import Any, Callable, TypeVar

T = TypeVar('T')


def log(filename: str | None = None) -> Callable[[Callable[..., T]], Callable[..., T]]:
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"{timestamp} - Function '{func.__name__}' called with args: {args}, kwargs: {kwargs}"

            try:
                result = func(*args, **kwargs)
                log_message += f". Result: {result}"
                success = True
            except Exception as e:
                error_type = type(e).__name__
                log_message += f". Error type: {error_type}, message: {str(e)}. Input args: {args}, kwargs: {kwargs}"
                success = False
                raise
            finally:
                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(log_message + '\n')
                else:
                    print(log_message)

            return result if success else None  # type: ignore

        return wrapper

    return decorator
