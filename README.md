
# 🖨️ Fast Print - Product Management Dashboard

<div align="center">
  <img src="https://github.com/user-attachments/assets/0e160546-8d8b-4446-8f46-5818deb440f3" width="100%" alt="Banner">
</div>

<div align="center">
  <video src="https://github.com/user-attachments/assets/9381c0e2-e293-47cb-b789-031639b53472" width="100%" controls></video>
</div>

Aplikasi **Manajemen Produk** yang dibangun menggunakan **Django** & **React-style Vanilla JS** untuk memenuhi tantangan programmer di Fast Print Indonesia. Dashboard ini dirancang dengan estetika premium, performa tinggi (PostgreSQL), dan fitur manipulasi data yang lengkap.

---

## 🚀 Fitur Unggulan

- **Smart Filtering**: Secara default hanya menampilkan produk dengan status **"Bisa Dijual"** sesuai instruksi tes.
- **Bulk Management**: Fitur hapus massal (Bulk Delete) untuk manajemen data yang cepat.
- **Full CRUD**: Tambah, Edit, dan Hapus produk dengan validasi server-side (Serializer) & client-side.
- **Dynamic API Fetch**: Script cerdas penarik data API dengan dukungan input **Username Manual** jika kredensial server berubah.
- **Dashboard Statistik**: Ringkasan jumlah produk, kategori, dan status secara real-time.
- **Modern UI**: Menggunakan **Tailwind CSS**, **DataTables**, dan **Lucide Icons**.

---

## 🛠️ Teknologi yang Digunakan

| Komponen          | Teknologi             | Keterangan                                |
| :---------------- | :-------------------- | :---------------------------------------- |
| **Framework**     | Django 5.2            | High-level Python Web Framework           |
| **API Layer**     | Django REST Framework | Untuk handling data JSON & CSRF           |
| **Database**      | PostgreSQL            | Database relasional robust (fastprint_db) |
| **Styling**       | Tailwind CSS          | Utility-first CSS untuk desain modern     |
| **Interactivity** | Vanilla JavaScript    | Performa maksimal tanpa framework berat   |
| **Table Engine**  | DataTables            | Fitur search & pagination instan          |

---

## 📦 Panduan Instalasi & Konfigurasi

Ikuti langkah-langkah di bawah ini untuk menjalankan aplikasi di lingkungan lokal Anda:

### 1. Persyaratan Sistem

Pastikan perangkat Anda sudah terinstal:

- **Python 3.10** atau lebih baru.
- **PostgreSQL** (sudah berjalan).
- **pip** (Python package manager).

### 2. Persiapan Database

Buat database baru di PostgreSQL:

```sql
CREATE DATABASE fastprint_db;
```

### 3. Kloning & Install Dependencies

Buka terminal/command prompt, lalu jalankan:

```bash
# Clone repository
git clone <repository-url>
cd fast-print-indonesia

# (Opsional) Buat virtual environment
python -m venv venv
source venv/bin/scripts/activate  # Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 4. Konfigurasi Environment (.env)

Aplikasi menggunakan file `.env` untuk menyimpan data sensitif. Salin file contoh yang disediakan:

```bash
cp .env.example .env
```

Buka file `.env` dan sesuaikan nilainya:

- `SECRET_KEY`: Bisa diisi bebas untuk keperluan lokal (sudah ada contoh di `.env.example`).
- `DB_PASSWORD`: Masukkan password PostgreSQL Anda.
- Sesuaikan `DB_USER` jika bukan `postgres`.

### 5. Setup Database & Migrasi

Jalankan migrasi untuk membuat struktur tabel di database:

```bash
python manage.py migrate
```

### 6. Menarik Data Awal dari API

Aplikasi membutuhkan data awal dari API Fast Print. Jalankan perintah berikut:

```bash
# Menjalankan fetch data (otomatis generate username & password)
python manage.py fetch_products
```

> **Catatan**: Jika muncul error kredensial, lihat bagian [Menarik Data dari API](#-menarik-data-dari-api) di bawah untuk input username manual.

### 7. Menjalankan Server

```bash
python manage.py runserver
```

Akses dashboard di: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 📡 Menarik Data dari API

Aplikasi ini dilengkapi dengan command khusus untuk menarik data dari API recruitment Fast Print.

### Menggunakan Username Otomatis (Default)

Script akan mencoba men-generate username berdasarkan tanggal hari ini:

```bash
python manage.py fetch_products
```

### Menggunakan Username Manual (PORTAL HINT)

Jika username di portal berubah (misal: Suffix C21, C22, dst.), Anda bisa memasukkannya secara manual:

```bash
python manage.py fetch_products --username tesprogrammer050226C21
```

---

## 📁 Struktur Folder Penting

- `products/models.py`: Definisi tabel `Produk`, `Kategori`, dan `Status`.
- `products/serializers.py`: Validasi data harga (numeric) dan nama (required).
- `products/views.py`: Logic bisnis untuk penarikan data API dan CRUD.
- `products/management/commands/`: Script background penarik data.
- `products/templates/products/index.html`: UI utama (Frontend).

---

## 📝 Catatan Tambahan (HINT Reward)

Sesuai petunjuk **"HINT: CEK RESPONSE, HEADER, COOKIES"**, aplikasi ini telah diuji untuk menangani response server dengan baik, mendukung CSRF Token (Header) untuk keamanan POST/DELETE, dan mematuhi struktur data yang diminta oleh Fast Print.

---
