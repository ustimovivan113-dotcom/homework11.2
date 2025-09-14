import json
import os
import pytest
from unittest.mock import mock_open, patch, MagicMock
from src.utils import load_json_data


# Фикстуры для тестовых данных
@pytest.fixture
def sample_transactions():
    return [
        {"id": 1, "amount": "100.50", "currency": "RUB"},
        {"id": 2, "amount": "200.75", "currency": "USD"}
    ]


@pytest.fixture
def empty_list():
    return []


# Тесты для функции load_json_data
def test_load_json_data_valid_file(sample_transactions):
    """Тест загрузки корректного JSON файла"""
    mock_file = mock_open(read_data=json.dumps(sample_transactions))

    with patch('os.path.exists', return_value=True), \
            patch('os.path.getsize', return_value=100), \
            patch('builtins.open', mock_file), \
            patch('json.load', return_value=sample_transactions):
        result = load_json_data('test.json')
        assert result == sample_transactions

def test_load_json_data_file_not_exists():
    """Тест когда файл не существует"""
    with patch('os.path.exists', return_value=False):
        result = load_json_data('nonexistent.json')
        assert result == []


def test_load_json_data_empty_file():
    """Тест пустого файла"""
    with patch('os.path.exists', return_value=True), \
            patch('os.path.getsize', return_value=0):
        result = load_json_data('empty.json')
        assert result == []


def test_load_json_data_invalid_json():
    """Тест некорректного JSON"""
    with patch('os.path.exists', return_value=True), \
            patch('os.path.getsize', return_value=100), \
            patch('builtins.open', mock_open(read_data='invalid json')), \
            patch('json.load', side_effect=json.JSONDecodeError("Error", "doc", 0)):
        result = load_json_data('invalid.json')
        assert result == []


def test_load_json_data_not_list():
    """Тест когда JSON не является списком"""
    not_list_data = {"data": "not a list"}

    with patch('os.path.exists', return_value=True), \
            patch('os.path.getsize', return_value=100), \
            patch('builtins.open', mock_open(read_data=json.dumps(not_list_data))), \
            patch('json.load', return_value=not_list_data):
        result = load_json_data('not_list.json')
        assert result == []


@pytest.mark.parametrize("exception", [
    PermissionError("No permission"),
    OSError("OS error"),
    FileNotFoundError("File not found")
])
def test_load_json_data_exceptions(exception):
    """Тест обработки исключений"""
    with patch('os.path.exists', return_value=True), \
            patch('os.path.getsize', return_value=100), \
            patch('builtins.open', side_effect=exception):
        result = load_json_data('test.json')
        assert result == []


def test_load_json_data_empty_list(empty_list):
    """Тест загрузки пустого списка"""
    mock_file = mock_open(read_data=json.dumps(empty_list))

    with patch('os.path.exists', return_value=True), \
            patch('os.path.getsize', return_value=100), \
            patch('builtins.open', mock_file), \
            patch('json.load', return_value=empty_list):
        result = load_json_data('empty_list.json')
        assert result == empty_list


def test_load_json_data_permission_error():
    """Тест ошибки прав доступа"""
    with patch('os.path.exists', return_value=True), \
            patch('os.path.getsize', return_value=100), \
            patch('builtins.open', side_effect=PermissionError("Access denied")):
        result = load_json_data('restricted.json')
        assert result == []


def test_load_json_data_nested_structure():
    """Тест с вложенной структурой данных"""
    nested_data = [
        {
            "id": 1,
            "operationAmount": {
                "amount": "100.50",
                "currency": {"name": "RUB", "code": "RUB"}
            }
        }
    ]
    mock_file = mock_open(read_data=json.dumps(nested_data))

    with patch('os.path.exists', return_value=True), \
            patch('os.path.getsize', return_value=100), \
            patch('builtins.open', mock_file), \
            patch('json.load', return_value=nested_data):
        result = load_json_data('nested.json')
        assert result == nested_data
        assert result[0]['operationAmount']['amount'] == "100.50"


def test_load_json_data_file_path_variations():
    """Тест различных путей к файлам"""
    test_data = [{"test": "data"}]
    mock_file = mock_open(read_data=json.dumps(test_data))

    with patch('os.path.exists', return_value=True), \
            patch('os.path.getsize', return_value=100), \
            patch('builtins.open', mock_file), \
            patch('json.load', return_value=test_data):
        # Test different path formats
        paths = [
            'data.json',
            '/absolute/path/data.json',
            '../relative/path/data.json',
            'C:\\Windows\\Path\\data.json'
        ]

        for path in paths:
            result = load_json_data(path)
            assert result == test_data