import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pytest
from decorators import log
import io
from contextlib import redirect_stdout


def test_log_success_to_console(capsys):
    @log()  # В консоль
    def add(x, y):
        return x + y

    result = add(1, 2)
    assert result == 3

    captured = capsys.readouterr()
    assert "Function 'add' called with args: (1, 2), kwargs: {}. Result: 3" in captured.out


def test_log_success_to_file(tmp_path):
    log_file = tmp_path / "test_log.txt"

    @log(filename=str(log_file))
    def add(x, y):
        return x + y

    result = add(1, 2)
    assert result == 3

    assert log_file.exists()
    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "Function 'add' called with args: (1, 2), kwargs: {}. Result: 3" in content


def test_log_error_to_console(capsys):
    @log()
    def divide(x, y):
        return x / y

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    captured = capsys.readouterr()
    assert "Error type: ZeroDivisionError" in captured.out
    assert "message: division by zero" in captured.out
    assert "Input args: (1, 0), kwargs: {}" in captured.out


def test_log_error_to_file(tmp_path):
    log_file = tmp_path / "test_log.txt"

    @log(filename=str(log_file))
    def divide(x, y):
        return x / y

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "Error type: ZeroDivisionError" in content
    assert "message: division by zero" in content
    assert "Input args: (1, 0), kwargs: {}" in content