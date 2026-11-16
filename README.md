# E-Commerce Public Dataset Analysis & Dashboard (Olist)

Dashboard interaktif berbasis Streamlit untuk menganalisis performa kategori produk (berdasarkan jumlah pesanan dan total pendapatan dalam BRL) serta pengaruh lama waktu pengiriman terhadap kepuasan pelanggan (*review score*).

## Live Dashboard

Aplikasi dapat diakses secara daring melalui tautan berikut:
- [Olist E-Commerce Dashboard](https://ecommerce-dashboard-zahwa.streamlit.app/)

---

## Cara Menjalankan Dashboard Secara Lokal

Ikuti langkah-langkah berikut untuk menyiapkan *virtual environment*, menginstal *library* yang dibutuhkan, dan menjalankan aplikasi dashboard di perangkat lokal Anda:

### Opsi 1: Menggunakan `venv` (Python Bawaan)

1. **Masuk ke direktori utama proyek (`submission/`):**
   ```bash
   cd submission
   ```

2. **Buat *virtual environment* baru:**
   ```bash
   python -m venv venv
   ```

3. **Aktifkan *virtual environment*:**
   - **Windows (Command Prompt / PowerShell):**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS / Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Instal seluruh *library* yang dibutuhkan dari `requirements.txt`:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Jalankan aplikasi dashboard Streamlit:**
   ```bash
   streamlit run dashboard/dashboard.py
   ```

Setelah perintah `streamlit run dashboard/dashboard.py` dijalankan, dashboard akan otomatis terbuka pada *browser* Anda di alamat `http://localhost:8501`.

---

## Struktur Direktori

```text
submission/
├── dashboard/
│   ├── main_data.csv
│   └── dashboard.py
├── data/
│   ├── orders_dataset.csv
│   ├── order_items_dataset.csv
│   ├── products_dataset.csv
│   ├── product_category_name_translation.csv
│   └── order_reviews_dataset.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt