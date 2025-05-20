import requests
from bs4 import BeautifulSoup

# Fungsi untuk melakukan scraping data produk dari URL
def scrape_main(url):
    try:
        # Mengirim permintaan HTTP GET ke URL
        print(f"🚀 Mengakses URL: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Memastikan status code 200
    except requests.exceptions.RequestException as e:
        raise Exception(f"Gagal mengakses URL: {url}. Detail: {e}")
    
    try:
        # Parsing HTML menggunakan BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        fashion_items = []

        # Memastikan ada produk yang ditemukan
        if not soup.find_all('div', class_='collection-card'):
            raise Exception("Gagal melakukan parsing HTML: Struktur HTML tidak valid")
        
        for card in soup.find_all('div', class_='collection-card'):
            title_tag = card.find('h3', class_='product-title')
            title = title_tag.text.strip() if title_tag else 'Unknown Title'
            
            price_tag = card.find('div', class_='price-container')
            price = price_tag.text.strip() if price_tag else 'Price Unavailable'
            
            rating_tag = card.find('p', string=lambda text: text and 'Rating' in text)
            rating = rating_tag.text.strip() if rating_tag else 'No Rating'
            
            colors_tag = card.find('p', string=lambda text: text and 'Colors' in text)
            colors = colors_tag.text.strip() if colors_tag else 'No Color Info'
            
            size_tag = card.find('p', string=lambda text: text and 'Size' in text)
            size = size_tag.text.strip() if size_tag else 'No Size Info'
            
            gender_tag = card.find('p', string=lambda text: text and 'Gender' in text)
            gender = gender_tag.text.strip() if gender_tag else 'No Gender Info'


            # Menambahkan produk ke list
            fashion_items.append({
                'title': title,
                'price': price,
                'rating': rating,
                'colors': colors,
                'size': size,
                'gender': gender
            })

        print(f"✅ Berhasil mengambil {len(fashion_items)} produk.")
        return fashion_items
    
    except Exception as e:
        raise Exception(f"Gagal melakukan parsing: {str(e)}")

