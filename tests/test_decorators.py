import pytest

from src.decorators import log


def test_log_decorator():
    @log()
    def sample_func(x: int) -> int:
        return x * 2
    assert sample_func(5) == 10


def test_log_decorator_error():
    @log()
    def error_func():
        raise ValueError("Test error")
    with pytest.raises(ValueError):
        error_func()
