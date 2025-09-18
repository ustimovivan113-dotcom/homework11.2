import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import json
from utils import load_transactions

def test_load_transactions_valid(tmp_path):
    file = tmp_path / "test.json"
    data = [{"id": 1, "operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}}]
    file.write_text(json.dumps(data), encoding='utf-8')
    assert load_transactions(str(file)) == data

def test_load_transactions_empty_file(tmp_path):
    file = tmp_path / "test.json"
    file.write_text("", encoding='utf-8')
    assert load_transactions(str(file)) == []

def test_load_transactions_not_list(tmp_path):
    file = tmp_path / "test.json"
    file.write_text(json.dumps({"id": 1}), encoding='utf-8')
    assert load_transactions(str(file)) == []

def test_load_transactions_not_found():
    assert load_transactions("nonexistent.json") == []