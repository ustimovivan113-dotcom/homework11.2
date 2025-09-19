from unittest.mock import patch, MagicMock
from src.transaction_reader_csv_xlsx import read_transactions_csv, read_transactions_xlsx


def test_read_transactions_csv():
    mock_df = MagicMock()
    mock_df.to_dict.return_value = [
        {"date": "2024-01-01", "amount": 100, "description": "income"},
        {"date": "2024-01-02", "amount": -50, "description": "expense"},
    ]

    with patch("pandas.read_csv", return_value=mock_df) as mock_read_csv:
        result = read_transactions_csv("fake_path.csv")
        mock_read_csv.assert_called_once_with("fake_path.csv")
        mock_df.to_dict.assert_called_once_with(orient="records")

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["amount"] == 100
    assert result[1]["description"] == "expense"


def test_read_transactions_xlsx():
    mock_df = MagicMock()
    mock_df.to_dict.return_value = [
        {"date": "2024-01-01", "amount": 200, "description": "salary"},
        {"date": "2024-01-02", "amount": -80, "description": "bill"},
    ]

    with patch("pandas.read_excel", return_value=mock_df) as mock_read_excel:
        result = read_transactions_xlsx("fake_path.xlsx")
        mock_read_excel.assert_called_once_with("fake_path.xlsx")
        mock_df.to_dict.assert_called_once_with(orient="records")

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["amount"] == 200
    assert result[1]["description"] == "bill"