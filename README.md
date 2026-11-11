# Online Book Catalog Organizer (Automation Systems UTS)

Aplikasi otomatisasi berbasis Python CLI (*Command Line Interface*) untuk mengambil data katalog buku dari website [Books to Scrape](https://books.toscrape.com/), memvalidasi dan membersihkan data menggunakan *Regular Expressions*, menyusun output ke dalam file `.csv` dan `.txt`, mengorganisasi folder secara otomatis, serta membuat cadangan (*backup*) data dalam format `.zip`.

Project ini disusun untuk memenuhi ujian tengah semester mata kuliah **Automation Systems** di Universitas Pelita Bangsa.

---

## 📌 Anggota Kelompok

| No. | Nama Mahasiswa | NIM | Peran / Kontribusi |
| --- | --- | --- | --- |
| 1. | [Intan Virginia Aulia Putri] | [312310657] | Scraping & Parsing Logic |
| 2. | [Dendi Permana] | [312310694] | Regex & Data Cleaning |

---

## 🚀 Fitur Utama & Integrasi Materi

1. **Web Scraping (`requests` & `BeautifulSoup`)**: Mengambil minimal 30 data buku secara otomatis lengkap dengan navigasi pagination (Chapter 13).
2. **Regular Expressions (`re`)**: 
   - Pola 1: Ekstraksi dan pembersihan angka harga desimal.
   - Pola 2: Validasi ketersediaan stok (*In stock* / *Out of stock*) (Chapter 9).
3. **Reading & Writing Files (`open`)**: Menyimpan data rapi dalam format `.csv` dan raw data dalam format `.txt` (Chapter 10).
4. **File & Directory Automation (`pathlib` & `zipfile`)**: Membuat struktur folder otomatis (`data/`, `output/`, `backup/`) dan kompresi cadangan data otomatis (Chapter 11).
5. **Command Line Interface (`argparse`)**: Mendukung opsi argumen dinamis seperti `--url`, `--keyword`, `--limit`, `--output-dir`, dan `--backup` (Chapter 12).

---

## 📂 Struktur Project

```text
UTS_Project_Kelompok_01/
├── main.py                     # Script utama aplikasi Python
├── requirements.txt            # Daftar dependensi library eksternal
├── README.md                   # Petunjuk penggunaan & dokumen repo
├── data/
│   └── raw_data.txt            # Hasil ekstraksi awal data (TXT)
├── output/
│   └── hasil_scraping.csv      # Hasil data bersih dan terstruktur (CSV)
├── backup/
│   └── backup_data.zip         # File kompresi ZIP otomatis
└── dokumentasi/
    └── laporan_uts.pdf         # Laporan resmi UTS
```

---

## ⚙️ Persyaratan Sistem

- **Python**: Versi 3.8 atau lebih baru.
- **Pip**: Manajer paket Python standar.

---

## 🛠️ Cara Instalasi

1. **Clone repository ini**:
   ```bash
   git clone https://github.com/username/UTS_Project_Kelompok_01.git
   cd UTS_Project_Kelompok_01
   ```

2. **(Opsional) Buat dan aktifkan Virtual Environment**:
   - **Linux/macOS**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - **Windows**:
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```

3. **Install dependensi**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🖥️ Cara Penggunaan (CLI)

Jalankan perintah script melalui terminal / command prompt.

### 1. Eksekusi Standar (30 Data + Backup ZIP)
```bash
python main.py --url https://books.toscrape.com/ --limit 30 --backup
```

### 2. Pencarian Berdasarkan Kata Kunci
```bash
python main.py --keyword "Light" --limit 30 --backup
```

### 3. Mengubah Folder Output
```bash
python main.py --output-dir "hasil_penyimpanan" --limit 50
```

### 4. Menampilkan Bantuan Argumen CLI
```bash
python main.py --help
```

---

## 📋 Parameter CLI yang Tersedia

| Argument | Type | Default | Deskripsi |
| --- | --- | --- | --- |
| `--url` | `str` | `https://books.toscrape.com/` | URL website target yang akan di-scrape |
| `--keyword` | `str` | `""` | Kata kunci opsional untuk memfilter judul buku |
| `--limit` | `int` | `30` | Jumlah minimal record data yang ingin diambil |
| `--output-dir` | `str` | `output` | Nama directory folder untuk menyimpan file CSV |
| `--backup` | `flag` | `False` | Mengaktifkan pembuatan backup file ZIP otomatis |

---

## 📝 Contoh Output Terminal

```text
[*] Memulai scraping dari: https://books.toscrape.com/
[+] Backup berhasil dibuat: backup/backup_data.zip

========================================
      RINGKASAN PEMROSESAN DATA
========================================
Total Record Diambil : 30
File CSV Hasil       : output/hasil_scraping.csv
File Raw TXT        : data/raw_data.txt
Status Backup       : Berhasil (backup/backup_data.zip)
========================================
```

---

## 🔒 Etika & Keamanan

Pengambilan data ini dilakukan semata-mata untuk tujuan pendidikan pada website latihan scraping publik [Books to Scrape](https://books.toscrape.com/). Program ini mematuhi batas akses rate-limit normal tanpa melakukan tindakan pemrosesan secara berlebihan.
