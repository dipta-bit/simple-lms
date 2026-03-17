# Simple LMS

Proyek ini adalah kerangka awal untuk aplikasi Learning Management System (LMS) sederhana menggunakan Django dan PostgreSQL, yang dijalankan di dalam container Docker.

## 🚀 Cara Menjalankan Project

Ikuti langkah-langkah berikut untuk menjalankan aplikasi ini di komputer lokal:

1. **Siapkan Environment Variables**
   Duplikat file `.env.example` dan ubah namanya menjadi `.env`.
   bash
   cp .env.example .env

## 🚀 Query Optimization Demo (N+1 Problem)

Proyek ini telah menerapkan optimasi database untuk mengatasi **N+1 Problem** menggunakan `select_related` dan `prefetch_related` melalui Custom Model Managers.

Untuk membuktikannya, sebuah skrip `demo.py` telah dibuat. Skrip ini menghasilkan data dummy awal (fixtures) dan membandingkan eksekusi query dengan dan tanpa optimasi.

**Hasil Perbandingan:**

- **Tanpa Optimasi:** Menghasilkan **21 Queries** ke database (1 query untuk mengambil daftar Course, ditambah 10 query untuk Instructor dan 10 query untuk Category).
- **Dengan Optimasi (`select_related`):** Menghasilkan **HANYA 1 Query** ke database. Django menggunakan SQL `JOIN` untuk mengambil seluruh data terkait secara bersamaan.

**Cara Menjalankan Skrip Demo:**
Jalankan perintah berikut di terminal:
`docker-compose exec web python demo.py`
