import argparse
import re
import sys
import zipfile
from pathlib import Path
import requests
from bs4 import BeautifulSoup


def parse_arguments():
    """Mengelola CLI Arguments (Persyaratan 6 & Chapter 12)."""
    parser = argparse.ArgumentParser(
        description="Online Book Catalog Organizer - UTS Automation Systems"
    )
    parser.add_argument(
        "--url",
        type=str,
        default="https://books.toscrape.com/",
        help="URL website target",
    )
    parser.add_argument(
        "--keyword",
        type=str,
        default="",
        help="Kata kunci pencarian judul (opsional)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=30,
        help="Jumlah minimum data yang diambil (default: 30)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="output",
        help="Folder penyimpanan output",
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        help="Buat file ZIP backup otomatis",
    )
    return parser.parse_args()


def scrape_books(base_url, limit, keyword_filter=""):
    """Mengambil data dari website (Chapter 13) dan memvalidasi via Regex (Chapter 9)."""
    print(f"[*] Memulai scraping dari: {base_url}")
    books_data = []
    current_page_url = base_url

    # REGEX PATTERNS (Persyaratan 2 & Chapter 9)
    # 1. Regex untuk ekstrak & pembersihan harga (mencari angka desimal/float)
    price_pattern = re.compile(r"\d+\.\d{2}")
    # 2. Regex untuk validasi status stok (mengecek kata 'In stock' atau 'Out of stock')
    stock_pattern = re.compile(r"In stock|Out of stock", re.IGNORECASE)

    page = 1
    while len(books_data) < limit:
        try:
            response = requests.get(current_page_url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"[!] Error koneksi ke {current_page_url}: {e}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("article", class_="product_pod")

        if not articles:
            print("[!] Tidak ada produk ditemukan pada halaman.")
            break

        for article in articles:
            # Ekstrak Judul & URL
            title_tag = article.h3.a
            title = title_tag["title"]
            rel_link = title_tag["href"]
            
            # Format URL Detail
            if "catalogue/" in rel_link:
                book_url = f"https://books.toscrape.com/{rel_link}"
            else:
                book_url = f"https://books.toscrape.com/catalogue/{rel_link}"

            # Filter berdasarkan Keyword (jika diisi)
            if keyword_filter and not re.search(keyword_filter, title, re.IGNORECASE):
                continue

            # Ekstrak Harga raw & gunakan REGEX 1
            price_raw = article.find("p", class_="price_color").text
            price_match = price_pattern.search(price_raw)
            price = price_match.group(0) if price_match else "0.00"

            # Ekstrak Rating
            star_tag = article.find("p", class_="star-rating")
            rating = star_tag["class"][1] if star_tag else "Unrated"

            # Ekstrak & Gunakan REGEX 2 untuk ketersediaan stok
            availability_raw = article.find("p", class_="instock availability").text
            stock_match = stock_pattern.search(availability_raw)
            stock_status = stock_match.group(0) if stock_match else "Unknown"

            books_data.append({
                "title": title,
                "price_gbp": price,
                "rating": rating,
                "stock": stock_status,
                "url": book_url
            })

            if len(books_data) >= limit:
                break

        # Navigasi Pagination
        next_button = soup.find("li", class_="next")
        if next_button and len(books_data) < limit:
            next_page_rel = next_button.a["href"]
            if "catalogue/" in next_page_rel:
                current_page_url = f"https://books.toscrape.com/{next_page_rel}"
            else:
                current_page_url = f"https://books.toscrape.com/catalogue/{next_page_rel}"
            page += 1
        else:
            break

    return books_data


def save_data(data, output_dir_path):
    """Menyimpan data dan mengorganisir folder menggunakan pathlib (Chapter 10 & 11)."""
    out_dir = Path(output_dir_path)
    raw_dir = Path("data")
    
    # Membuat folder otomatis (Persyaratan 4)
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)

    csv_file = out_dir / "hasil_scraping.csv"
    txt_file = raw_dir / "raw_data.txt"

    # Menyimpan CSV (Persyaratan 3)
    with open(csv_file, "w", encoding="utf-8") as f:
        f.write("Judul,Harga (GBP),Rating,Stok,URL\n")
        for item in data:
            clean_title = f'"{item["title"]}"'
            f.write(f'{clean_title},{item["price_gbp"]},{item["rating"]},{item["stock"]},{item["url"]}\n')

    # Menyimpan Raw TXT
    with open(txt_file, "w", encoding="utf-8") as f:
        for item in data:
            f.write(f"{item}\n")

    return csv_file, txt_file


def create_backup(source_dirs, backup_zip_path):
    """Membuat kompresi ZIP untuk backup (Persyaratan 5 & Chapter 11)."""
    backup_path = Path(backup_zip_path)
    backup_path.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for folder in source_dirs:
            folder_path = Path(folder)
            if folder_path.exists():
                for file in folder_path.rglob("*"):
                    zipf.write(file, arcname=file.relative_to(folder_path.parent))

    print(f"[+] Backup berhasil dibuat: {backup_path}")


def main():
    args = parse_arguments()

    # Eksekusi Scraping
    results = scrape_books(args.url, args.limit, args.keyword)

    if not results:
        print("[!] Data kosong atau tidak ditemukan. Program selesai.")
        sys.exit(0)

    # Simpan File
    csv_file, txt_file = save_data(results, args.output_dir)

    # Buat Backup jika flag --backup diaktifkan
    if args.backup:
        create_backup([args.output_dir, "data"], "backup/backup_data.zip")

    # Ringkasan Terminal (Persyaratan 8)
    print("\n" + "="*40)
    print("      RINGKASAN PEMROSESAN DATA")
    print("="*40)
    print(f"Total Record Diambil : {len(results)}")
    print(f"File CSV Hasil       : {csv_file}")
    print(f"File Raw TXT        : {txt_file}")
    if args.backup:
        print(f"Status Backup       : Berhasil (backup/backup_data.zip)")
    print("="*40)


if __name__ == "__main__":
    main()