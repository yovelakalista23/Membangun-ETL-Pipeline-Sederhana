import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.load import save_to_csv, save_to_google_sheets, load_to_postgresql

class TestLoad(unittest.TestCase):

    @patch('utils.load.pd.DataFrame.to_csv')
    def test_save_to_csv(self, mock_to_csv):
        df = pd.DataFrame({
            'title': ['Product 1', 'Product 2'],
            'price': [10000, 20000],
            'rating': [4.5, 5.0]
        })

        save_to_csv(df, 'test.csv')
        mock_to_csv.assert_called_once_with('test.csv', index=False)

    @patch('utils.load.build')
    @patch('utils.load.Credentials.from_service_account_file')
    def test_save_to_google_sheets(self, mock_creds, mock_build):
        df = pd.DataFrame({'title': ['Product 1'], 'price': [10000], 'rating': [4.5]})

        mock_creds.return_value = MagicMock()
        mock_service = MagicMock()
        mock_build.return_value = mock_service

        save_to_google_sheets(df)
        mock_service.spreadsheets.return_value.values.return_value.update.assert_called_once()

    @patch('utils.load.create_engine')
    def test_load_to_postgresql_success(self, mock_create_engine):
        df = pd.DataFrame({'title': ['Product 1'], 'price': [10000], 'rating': [4.5]})

        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine

        with patch('pandas.DataFrame.to_sql') as mock_to_sql:
            load_to_postgresql(df)
            mock_to_sql.assert_called_once()

    def test_main_block(self):
        with patch.object(unittest, 'main'):
            import tests.test_load

if __name__ == '__main__':
    unittest.main()
