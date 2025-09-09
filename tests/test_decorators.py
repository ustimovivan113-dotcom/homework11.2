import unittest
import logging
from io import StringIO
from decorators import log


class TestLogDecorator(unittest.TestCase):

    def setUp(self):
        """Настройка перед каждым тестом."""
        self.log_capture = StringIO()
        self.handler = logging.StreamHandler(self.log_capture)
        logging.getLogger().addHandler(self.handler)

    def tearDown(self):
        """Очистка после каждого теста."""
        logging.getLogger().removeHandler(self.handler)
        self.log_capture.close()

    def test_successful_function_call(self):
        """Тест успешного вызова функции."""

        @log
        def test_func(x, y):
            return x + y

        result = test_func(2, 3)

        # Проверяем результат
        self.assertEqual(result, 5)

        # Проверяем логи
        log_output = self.log_capture.getvalue()
        self.assertIn("Вызов функции: test_func", log_output)
        self.assertIn("Аргументы: args=(2, 3), kwargs={}", log_output)
        self.assertIn("Функция test_func завершилась успешно", log_output)
        self.assertIn("Результат: 5", log_output)

    def test_function_with_error(self):
        """Тест вызова функции с ошибкой."""

        @log
        def error_func():
            raise ValueError("Test error")

        with self.assertRaises(ValueError):
            error_func()

        # Проверяем логи ошибки
        log_output = self.log_capture.getvalue()
        self.assertIn("Ошибка в функции error_func", log_output)
        self.assertIn("Test error", log_output)

    def test_function_with_keyword_args(self):
        """Тест функции с keyword arguments."""

        @log
        def kw_func(a, b=10):
            return a + b

        result = kw_func(5, b=15)

        self.assertEqual(result, 20)

        log_output = self.log_capture.getvalue()
        self.assertIn("Аргументы: args=(5,), kwargs={'b': 15}", log_output)


if __name__ == '__main__':
    unittest.main()
