import pandas as pd
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
    print("🚀 Menyimpan data ke Google Sheets...")
    creds = Credentials.from_service_account_file('etl-sederhana-459412-f78290530d1a.json')
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    values = [products.columns.values.tolist()] + products.values.tolist()
    body = {'values': values}

    sheet.values().append(
        spreadsheetId='1hAzAXLRdhD4l0OxCaD6C9vSMzOoi084n-GgFG9YVbgo',
        range='Sheet1!A1',
        valueInputOption='RAW',
        body=body
    ).execute()

    print("✅ Data berhasil disimpan ke Google Sheets.")

# Fungsi menyimpan data ke PostgreSQL
def load_to_postgresql(products, table_name='scraped_items'):
    print("🚀 Memulai proses penyimpanan ke PostgreSQL...")
    try:
        engine = create_engine('postgresql+psycopg2://developer:supersecretpassword@localhost:5432/fashion')
        products.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"✅ Data berhasil disimpan ke PostgreSQL table '{table_name}'.")

    except Exception as e:
        print(f"❌ Gagal menyimpan ke PostgreSQL: {e}")
