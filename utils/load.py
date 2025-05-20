import pandas as pd
import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from sqlalchemy import create_engine

# Fungsi menyimpan data ke CSV
def save_to_csv(products, filename="products.csv"):
    print("🚀 Menyimpan data ke CSV...")
    products.to_csv(filename, index=False)
    print(f"✅ Data berhasil disimpan ke file: {filename}")

# Fungsi menyimpan data ke Google Sheets
def save_to_google_sheets(products):
    try:
        print("🚀 Menyimpan data ke Google Sheets...")

        # Path relatif ke file JSON credentials (pastikan file ada di folder yang sama atau folder utils)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        creds_path = os.path.join(current_dir, 'etl-sederhana-459412-f78290530d1a.json')  # Ganti dengan nama file JSON kamu

        # Cek apakah file JSON ada
        if not os.path.exists(creds_path):
            raise FileNotFoundError(f"❌ File credentials tidak ditemukan: {creds_path}")

        creds = Credentials.from_service_account_file(creds_path)
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        values = [products.columns.values.tolist()] + products.values.tolist()
        body = {'values': values}

        sheet_name = 'Sheet1'
        sheet.values().update(
            spreadsheetId='1hAzAXLRdhD4l0OxCaD6C9vSMzOoi084n-GgFG9YVbgo',
            range=f'{sheet_name}!A1',
            valueInputOption='RAW',
            body=body
        ).execute()

        print("✅ Data berhasil disimpan ke Google Sheets.")

    except FileNotFoundError as e:
        print(f"❌ Gagal menyimpan data ke Google Sheets: {str(e)}")
    except Exception as e:
        print(f"❌ Terjadi kesalahan saat menyimpan data ke Google Sheets: {str(e)}")



# Fungsi menyimpan data ke PostgreSQL
def load_to_postgresql(products, table_name='scraped_items'):
    print("🚀 Memulai proses penyimpanan ke PostgreSQL...")
    try:
        engine = create_engine('postgresql+psycopg2://developer:supersecretpassword@localhost:5432/fashion')
        products.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"✅ Data berhasil disimpan ke PostgreSQL table '{table_name}'.")

    except Exception as e:
        print(f"❌ Gagal menyimpan ke PostgreSQL: {e}")
        raise Exception("Gagal menyimpan ke PostgreSQL")
