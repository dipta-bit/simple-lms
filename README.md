# Simple LMS

Proyek ini adalah kerangka awal untuk aplikasi Learning Management System (LMS) sederhana menggunakan Django dan PostgreSQL, yang dijalankan di dalam container Docker.

## Cara Menjalankan Project Progress 1: Simple LMS - Docker & Django Foundation

Pastikan **Docker** dan **Docker Desktop** sudah ter-*install*di komputermu sebelum memulai langkah-langkah di bawah ini.

### 1. Menyalakan Container

Buka terminal, arahkan ke folder proyek ini, lalu jalankan perintah berikut untuk mengunduh semua kebutuhan dan menyalakan mesinnya di latar belakang:

```bash
docker-compose up -d --build
```

Tunggu hingga proses selesai dan terminal menampilkan status Started atau Up warna hijau.

### 2. Jalankan Migrasi Database

Setelah mesin menyala,buat struktur tabel standar Django di dalam database. Jalankan perintah ini:

```bash
docker-compose exec web python manage.py migrate
```

### 3. Buat Akun Admin

Agar bisa masuk ke panel kontrol LMS, buat satu akun Superuser dengan perintah:

```bash
docker-compose exec web python manage.py createsuperuser
```

### 4. Akses Aplikasi di Browser

Jika semua langkah di atas berhasil, buka browser dan kunjungi alamat berikut:

Halaman Utama Django: http://localhost:8000
