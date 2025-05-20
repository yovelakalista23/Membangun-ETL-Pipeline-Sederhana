from utils.extract import scrape_main
from utils.transform import transform_data
from utils.load import save_to_csv, save_to_google_sheets, load_to_postgresql

# Fungsi scraping halaman 
def main():
    url = 'https://fashion-studio.dicoding.dev/'
    all_items = []
    
    print(f"Scraping halaman: {url}")
    try:
        fashion_items = scrape_main(url)
        all_items.extend(fashion_items)  
    except Exception as e:
        print(f"Halaman gagal discraping: {e}")
        
    # Scraping halaman berikutnya
    for page in range(2, 51):  # Menggunakan halaman 2 sampai 50
        all_url = f"{url}page{page}"
        print(f"Scraping halaman {page}: {all_url}")
        try:
            fashion_items = scrape_main(all_url)
            all_items.extend(fashion_items)  
        except Exception as e:
            print(f"Halaman gagal discraping {page}: {e}")
            
    # Transformasi Data
    transformed_data = transform_data(all_items)
    
    if transformed_data is not None:  # Pastikan ada data setelah transformasi
        # Menyimpan Data
        save_to_csv(transformed_data)
        load_to_postgresql(transformed_data)
        
        # Menyimpan data ke Google Sheets
        save_to_google_sheets(transformed_data)
    else:
        print("❌ Data gagal ditransformasi.")
    

if __name__ == '__main__':  # Pemanggilan fungsi utama
    main()
