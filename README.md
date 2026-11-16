# E-Commerce Public Dataset Analysis & Dashboard (Olist)

Dashboard interaktif berbasis Streamlit untuk menganalisis performa kategori produk (berdasarkan jumlah pesanan dan total pendapatan dalam BRL) serta pengaruh lama waktu pengiriman terhadap kepuasan pelanggan (*review score*).

## Live Dashboard

Aplikasi dapat diakses secara daring melalui tautan berikut:
- [Olist E-Commerce Dashboard](https://ecommerce-dashboard-zahwa.streamlit.app/)

---

## Cara Menjalankan Dashboard Secara Lokal

### 1. Prasyarat
Pastikan Anda sudah menginstal **Python 3.9+** (atau Anaconda/Miniconda) pada perangkat Anda.

### 2. Instalasi Dependensi
Buka terminal (Command Prompt, PowerShell, atau Terminal VS Code), arahkan ke folder utama `submission/`, lalu jalankan perintah berikut untuk menginstal seluruh *library* yang dibutuhkan:

**Menggunakan `pip`:**
```bash
cd submission
pip install -r requirements.txt
```
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