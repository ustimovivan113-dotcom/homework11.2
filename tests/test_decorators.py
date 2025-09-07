import os
import pytest
from src.decorators import log


# Имя файла для тестов логирования в файл
LOG_FILENAME = "test_log.txt"

@pytest.fixture(autouse=True)
def teardown_method():
    """Очистка после каждого теста"""
    if os.path.exists(LOG_FILENAME):
        os.remove(LOG_FILENAME)
    yield
    if os.path.exists(LOG_FILENAME):
        os.remove(LOG_FILENAME)


def test_log_to_console_success(capsys):
    """Тест логирования успешного выполнения в консоль"""
    @log()
    def add(a, b):
        return a + b

    result = add(2, 3)
    assert result == 5

    captured = capsys.readouterr()
    output = captured.out

    assert "add начала выполнение" in output
    assert "args: (2, 3), kwargs: {}" in output
    assert "add завершилась успешно" in output
    assert "Результат: 5" in output
    assert "Время выполнения:" in output



def test_log_to_file_success():
    """Тест логирования успешного выполнения в файл"""
    @log(filename=LOG_FILENAME)
    def add(a, b):
        return a + b

    result = add(2, 3)

    assert result == 5

    assert os.path.exists(LOG_FILENAME)

    with open(LOG_FILENAME, "r", encoding="utf-8") as f:
        content = f.read()

    assert "add начала выполнение" in content
    assert "args: (2, 3), kwargs: {}" in content
    assert "add завершилась успешно" in content
    assert "Результат: 5" in content
    assert "Время выполнения:" in content


def test_log_to_console_error(capsys):
    """Тест логирования с ошибкой в консоль"""
    @log()
    def division(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError, match="division by zero"):
        division(10, 0)

    captured = capsys.readouterr()
    output = captured.out

    assert "division начала выполнение" in output
    assert "args: (10, 0), kwargs: {}" in output
    assert "division завершилась с ошибкой" in output
    assert "ZeroDivisionError" in output
    assert "division by zero" in output
    assert "Время выполнения:" in output


def test_log_to_file_error():
    """Тест логирования с ошибкой в файл"""
    @log(filename=LOG_FILENAME)
    def division(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError, match="division by zero"):
        division(10, 0)

    assert os.path.exists(LOG_FILENAME)

    with open(LOG_FILENAME, "r", encoding="utf-8") as f:
        content = f.read()

    assert "division начала выполнение" in content
    assert "args: (10, 0), kwargs: {}" in content
    assert "division завершилась с ошибкой" in content
    assert "ZeroDivisionError" in content
    assert "division by zero" in content
    assert "Время выполнения:" in content


def test_log_none_result(capsys):
    """Тест логирования функции, возвращающей None"""

    @log()
    def return_none():
        return None

    result = return_none()

    assert result is None

    captured = capsys.readouterr()
    output = captured.out

    assert "Результат: None" in output


