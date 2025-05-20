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

        mock_spreadsheets = mock_service.spreadsheets.return_value
        mock_values = mock_spreadsheets.values.return_value
        mock_update = mock_values.update.return_value
        mock_update.execute.return_value = None

        save_to_google_sheets(df)

        mock_values.update.assert_called_once()
        mock_update.execute.assert_called_once()

    @patch('utils.load.create_engine')
    @patch('pandas.DataFrame.to_sql')
    def test_load_to_postgresql_success(self, mock_to_sql, mock_create_engine):
        df = pd.DataFrame({'title': ['Product 1'], 'price': [10000], 'rating': [4.5]})

        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine

        load_to_postgresql(df)
        mock_to_sql.assert_called_once()

    @patch('utils.load.create_engine')
    def test_load_to_postgresql_error(self, mock_create_engine):
        mock_create_engine.side_effect = Exception("Database connection failed")

        with self.assertRaises(Exception) as context:
            load_to_postgresql(pd.DataFrame({'title': ['Test']}))

        self.assertIn("Gagal menyimpan ke PostgreSQL", str(context.exception))

if __name__ == '__main__':
    unittest.main()
