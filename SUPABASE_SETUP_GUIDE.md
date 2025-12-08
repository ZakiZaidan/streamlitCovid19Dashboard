# 🚀 COVID-19 Indonesia Dashboard - Supabase Setup Guide

Panduan lengkap untuk menggunakan Supabase sebagai database untuk COVID-19 Indonesia Dashboard.

## 📋 Daftar Isi

1. [Persyaratan](#persyaratan)
2. [Setup Supabase Project](#setup-supabase-project)
3. [Konfigurasi Environment](#konfigurasi-environment)
4. [Setup Database Schema](#setup-database-schema)
5. [Import Data](#import-data)
6. [Menjalankan Dashboard](#menjalankan-dashboard)
7. [Troubleshooting](#troubleshooting)

## 🔧 Persyaratan

- Python 3.8 atau lebih tinggi
- Akun Supabase (gratis di [supabase.com](https://supabase.com))
- Git (untuk clone repository)

## 🏗️ Setup Supabase Project

### 1. Buat Akun Supabase

1. Kunjungi [supabase.com](https://supabase.com)
2. Klik "Start your project" atau "Sign Up"
3. Daftar menggunakan GitHub, Google, atau email

### 2. Buat Project Baru

1. Di dashboard Supabase, klik "New Project"
2. Pilih organization (atau buat baru)
3. Isi detail project:
   - **Name**: `covid19-indonesia-dashboard`
   - **Database Password**: Buat password yang kuat (simpan dengan aman!)
   - **Region**: Pilih yang terdekat (Singapore untuk Indonesia)
4. Klik "Create new project"
5. Tunggu setup selesai (2-3 menit)

### 3. Dapatkan Kredensial

Setelah project siap, dapatkan kredensial dari dashboard:

#### Settings > API:
- **Project URL**: `https://your-project-ref.supabase.co`
- **Anon public key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
- **Service role key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (RAHASIA!)

#### Settings > Database:
- **Host**: `db.your-project-ref.supabase.co`
- **Database name**: `postgres`
- **Username**: `postgres`
- **Password**: Password yang Anda buat saat setup
- **Port**: `5432`

## ⚙️ Konfigurasi Environment

### 1. Copy Template Environment

```bash
cp supabase.env.template .env
```

### 2. Edit File .env

Buka file `.env` dan isi dengan kredensial Supabase Anda:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here

# Database Connection
SUPABASE_DB_HOST=db.your-project-ref.supabase.co
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=your-database-password
SUPABASE_DB_PORT=5432

# App Configuration
APP_TITLE=COVID-19 Indonesia Dashboard
CACHE_TTL=3600
DEBUG_MODE=false
```

⚠️ **PENTING**: 
- Ganti semua `your-*` dengan nilai sebenarnya
- Jangan commit file `.env` ke Git
- Simpan service role key dengan aman

## 🗄️ Setup Database Schema

### 1. Buka SQL Editor

1. Di dashboard Supabase, klik "SQL Editor" di sidebar
2. Atau kunjungi: `https://supabase.com/dashboard/project/[your-project-id]/sql`

### 2. Jalankan Schema SQL

1. Buka file `supabase_schema.sql` di project Anda
2. Copy seluruh isi file
3. Paste ke SQL Editor di Supabase
4. Klik "Run" atau tekan Ctrl+Enter
5. Tunggu hingga selesai (akan muncul "Success")

### 3. Verifikasi Schema

Setelah berhasil, Anda akan melihat tabel-tabel berikut di Database > Tables:

**Tabel Utama:**
- `LOKASI` - Data provinsi
- `STATISTIK_HARIAN` - Data COVID-19 harian

**Tabel Tambahan:**
- `RUMAH_SAKIT` - Data rumah sakit
- `VAKSINASI_DETAIL` - Data vaksinasi
- `KEBIJAKAN_PEMERINTAH` - Data kebijakan
- `EKONOMI_REGIONAL` - Data ekonomi
- `TESTING_LABS` - Data laboratorium
- `CLUSTER_PENULARAN` - Data cluster
- `MOBILITAS_HARIAN` - Data mobilitas

## 📊 Import Data

### 1. Install Dependencies

```bash
pip install -r requirements_supabase.txt
```

### 2. Jalankan Import Script

```bash
python supabase_data_import.py
```

Script akan:
- ✅ Validasi konfigurasi Supabase
- ✅ Test koneksi database
- ✅ Import data lokasi
- ✅ Import data statistik harian
- ✅ Import data tambahan (jika tersedia)
- ✅ Verifikasi import

### 3. Monitor Progress

Import akan menampilkan progress bar dan status:

```
🚀 Starting Supabase Data Import for COVID-19 Indonesia Dashboard
======================================================================
🔍 Validating Supabase configuration...
✅ Configuration and connection validated successfully!

📍 Importing LOKASI data...
Importing locations: 100%|████████████| 34/34 [00:01<00:00, 25.43it/s]
✅ Successfully imported 34 location records

📊 Importing STATISTIK_HARIAN data...
Importing daily statistics: 100%|████████████| 31790/31790 [02:15<00:00, 234.12it/s]
✅ Successfully imported 31790 daily statistics records
```

## 🚀 Menjalankan Dashboard

### Opsi 1: Menggunakan Launcher (Recommended)

```bash
python run_supabase_dashboard.py
```

Launcher akan:
- ✅ Check Python version
- ✅ Install dependencies
- ✅ Validate configuration
- ✅ Test Supabase connection
- ✅ Launch Streamlit dashboard

### Opsi 2: Langsung dengan Streamlit

```bash
streamlit run streamlit_supabase_app.py
```

### 3. Akses Dashboard

Dashboard akan terbuka di browser pada:
- **URL**: http://localhost:8501
- **Port**: 8501 (default)

## 🔧 Troubleshooting

### ❌ Connection Error

**Problem**: `Database connection error: connection to server failed`

**Solutions**:
1. Check kredensial di file `.env`
2. Pastikan Supabase project sudah aktif
3. Verify database password
4. Check network/firewall

### ❌ Authentication Error

**Problem**: `Authentication failed`

**Solutions**:
1. Verify `SUPABASE_DB_PASSWORD` di `.env`
2. Reset database password di Supabase dashboard
3. Update `.env` dengan password baru

### ❌ Table Not Found

**Problem**: `relation "lokasi" does not exist`

**Solutions**:
1. Jalankan `supabase_schema.sql` di SQL Editor
2. Check apakah schema berhasil dibuat
3. Verify table names (case-sensitive)

### ❌ Import Error

**Problem**: Data import gagal

**Solutions**:
1. Check file `covid_19_indonesia_enhanced.csv` exists
2. Verify file format dan encoding
3. Run dengan `DEBUG_MODE=true` untuk detail error
4. Check Supabase project limits (free tier)

### ❌ Streamlit Error

**Problem**: `ModuleNotFoundError` atau import error

**Solutions**:
1. Install dependencies: `pip install -r requirements_supabase.txt`
2. Check Python version (minimum 3.8)
3. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # atau
   venv\Scripts\activate     # Windows
   pip install -r requirements_supabase.txt
   ```

### 🔍 Debug Mode

Untuk troubleshooting detail, aktifkan debug mode:

```env
DEBUG_MODE=true
```

Kemudian jalankan ulang script untuk melihat error detail.

## 📊 Monitoring Supabase

### Database Usage

Monitor penggunaan database di Supabase dashboard:
- **Settings > Usage**: Lihat storage, bandwidth, requests
- **Database > Tables**: Monitor row counts
- **Logs**: Check query performance

### Free Tier Limits

Supabase free tier memiliki batasan:
- **Database size**: 500MB
- **Bandwidth**: 5GB/month
- **Requests**: 50,000/month

Untuk production, pertimbangkan upgrade ke Pro plan.

## 🔐 Security Best Practices

1. **Environment Variables**:
   - Jangan commit `.env` ke Git
   - Gunakan `.env.local` untuk development
   - Set environment variables di production

2. **Database Security**:
   - Enable Row Level Security (RLS) jika diperlukan
   - Gunakan service role key hanya untuk server-side
   - Monitor access logs

3. **API Keys**:
   - Simpan service role key dengan aman
   - Rotate keys secara berkala
   - Gunakan anon key untuk client-side

## 📞 Support

Jika mengalami masalah:

1. **Check Documentation**: 
   - [Supabase Docs](https://supabase.com/docs)
   - [Streamlit Docs](https://docs.streamlit.io)

2. **Community Support**:
   - [Supabase Discord](https://discord.supabase.com)
   - [Streamlit Forum](https://discuss.streamlit.io)

3. **GitHub Issues**: 
   - Buat issue di repository project ini

---

## 🎉 Selamat!

Jika semua langkah berhasil, Anda sekarang memiliki:

✅ **Supabase project** yang terkonfigurasi  
✅ **Database schema** yang lengkap  
✅ **Data COVID-19** yang terimport  
✅ **Dashboard interaktif** yang berjalan  

Dashboard Anda siap digunakan untuk analisis data COVID-19 Indonesia! 🚀

---

*Last updated: December 2024*
