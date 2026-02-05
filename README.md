# 🖨️ Fast Print - Product Management Dashboard

![Banner](file:///C:/Users/sifaq/.gemini/antigravity/brain/9ebf804b-9f1c-4429-9562-ad3339e4c17b/media__1770302815252.png)

Aplikasi **Manajemen Produk** yang dibangun menggunakan **Django** & **React-style Vanilla JS** untuk memenuhi tantangan programmer di Fast Print Indonesia. Dashboard ini dirancang dengan estetika premium, performa tinggi (PostgreSQL), dan fitur manipulasi data yang lengkap.

---

## 🚀 Fitur Unggulan

- **Smart Filtering**: Secara default hanya menampilkan produk dengan status **"Bisa Dijual"** sesuai instruksi tes.
- **Bulk Management**: Fitur hapus massal (Bulk Delete) untuk manajemen data yang cepat.
- **Full CRUD**: Tambah, Edit, dan Hapus produk dengan validasi server-side (Serializer) & client-side.
- **Dynamic API Fetch**: Script cerdas penarik data API dengan dukungan input **Username Manual** jika kredensial server berubah.
- **Dashboard Statistik**: Ringkasan jumlah produk, kategori, dan status secara real-time.
- **Modern UI**: Menggunakan **Tailwind CSS**, **DataTables**, dan **Lucide Icons** dengan tema warna resmi Fast Print (Brand Yellow).

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

## 📦 Persiapan & Instalasi

### 1. Persyaratan Sistem

Pastikan Anda sudah menginstal:

- Python 3.10+
- PostgreSQL
- pip

### 2. Kloning & Install Dependencies

```bash
git clone <repository-url>
cd fast-print-indonesia
pip install -r requirements.txt
```

### 3. Konfigurasi Environment (.env)

Buat file baru bernama `.env` di root project (atau copy dari `.env.example`) dan isi dengan kredensial Anda:

```bash
cp .env.example .env
```

Isi dasar `.env`:

```text
DEBUG=True
SECRET_KEY=isi_dengan_key_anda

DB_NAME=fastprint_db
DB_USER=postgres
DB_PASSWORD=password_anda
DB_HOST=localhost
DB_PORT=5432
```

### 4. Migrasi & Jalankan Server

```bash
python manage.py migrate
python manage.py runserver
```

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

**Dibuat dengan ❤️ untuk Fast Print Indonesia.**
