import functools
import datetime


def log(filename=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
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

            if success:
                return result

        return wrapper

    return decorator