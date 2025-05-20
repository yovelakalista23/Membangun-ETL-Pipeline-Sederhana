import pandas as pd
import numpy as np
from datetime import datetime

# Fungsi untuk mentransformasi data produk
def transform_data(fashion_items):
    try:
        print("🚀 Memulai proses transformasi data...")

        # Mengecek apakah scraped_items valid
        if not fashion_items:
            print("❌ Data kosong atau tidak ada untuk diproses.")
            return None

        # Mengubah data produk menjadi DataFrame
        products = pd.DataFrame(fashion_items)
        print("✅ Data sebelum transformasi:")
        print(products.head())

        # Membersihkan data title
        products = products[products['title'].str.strip().str.lower() != 'unknown product']

        # Membersihkan dan mengonversi rating
        products['rating'] = products['rating'].replace(r'[^0-9.]', '', regex=True)
        products['rating'] = products['rating'].replace('', np.nan)
        products.dropna(subset=['rating'], inplace=True)
        
        # Kemudian mengubah rating menjadi float
        products['rating'] = products['rating'].astype(float)


        # Membersihkan data colors
        products['colors'] = products['colors'].replace(r'\D', '', regex=True)
        products['colors'] = products['colors'].replace('', np.nan)
        products.dropna(subset=['colors'], inplace=True)
    
        # Kemudian mengubah color menjadi integer
        products['colors'] = products['colors'].astype(int)
        
        
        # Membersihkan kolom size dan gender
        products['size'] = products['size'].replace(r'Size:\s*', '', regex=True)
        products['gender'] = products['gender'].replace(r'Gender:\s*', '', regex=True)

        # Mengonversi harga dari USD ke IDR
        products['price'] = pd.to_numeric(
        products['price'].str.replace(r'[^\d.]', '', regex=True),
        errors='coerce'
        )
        products.dropna(subset=['price'], inplace=True)
        products['price'] *= 16000
        
        
        # Menghapus data duplikat dan null
        products.drop_duplicates(inplace=True)
        products.dropna(inplace=True)
        return products

    except Exception as e:
        print(f"❌ Terjadi kesalahan dalam proses transformasi: {e}")
        return None

