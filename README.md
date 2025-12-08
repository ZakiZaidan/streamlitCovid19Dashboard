# 🦠 COVID-19 Indonesia Dashboard

Dashboard interaktif untuk memvisualisasikan data COVID-19 Indonesia menggunakan **Streamlit** dan **Supabase**.

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Copy template environment file
cp supabase.env.template .env

# Edit .env file dengan konfigurasi Supabase Anda
```

### 2. Install Dependencies
```bash
pip install -r requirements_supabase.txt
```

### 3. Setup Database
```bash
# Import schema ke Supabase (via SQL Editor)
# Copy paste isi file supabase_schema.sql ke Supabase SQL Editor

# Import data
python supabase_data_import.py

# (Optional) Import enhanced data
python generate_enhanced_dummy_data.py
python import_enhanced_data.py
```

### 4. Run Dashboard
```bash
# Menggunakan runner script
python run_supabase_dashboard.py

# Atau langsung
streamlit run streamlit_supabase_app.py
```

## 📊 Fitur Dashboard

### 🏠 KPI Terpadu
- Metrics COVID-19 inti (kasus, sembuh, meninggal, tingkat kesembuhan)
- Metrics infrastruktur kesehatan (rumah sakit, tempat tidur, ICU, lab)
- Metrics vaksinasi & ekonomi (dosis vaksin, indeks pemulihan)

### 🗺️ Geospasial & Tren
- Peta sebaran COVID-19 Indonesia (bubble map)
- Analisis tren waktu dengan 4 subplot
- Moving average 7 hari

### 🔍 Analisis Provinsi
- Analisis detail per provinsi
- Tren harian dan kumulatif
- Infrastruktur kesehatan per provinsi

### 🏥 Kapasitas Kesehatan
- Distribusi rumah sakit berdasarkan tipe
- Kapasitas ICU per provinsi
- Analisis kapasitas vs beban COVID-19

### 💉 Analitik Vaksinasi
- Progress vaksinasi nasional
- Distribusi jenis vaksin
- Grafik kumulatif dosis

### 📋 Dampak Kebijakan
- Timeline kebijakan COVID-19
- Analisis tingkat keketatan
- Tingkat kepatuhan per jenis kebijakan

## 📁 Struktur File

```
TubesABD/
├── streamlit_supabase_app.py      # Dashboard utama
├── supabase_config.py             # Konfigurasi Supabase
├── supabase_data_import.py        # Import data ke Supabase
├── supabase_schema.sql            # Schema database
├── run_supabase_dashboard.py      # Runner script
├── requirements_supabase.txt      # Dependencies
├── supabase.env.template          # Template environment
├── covid_19_indonesia_time_series_all.csv  # Data COVID-19
├── dummy_data/                    # Data tambahan
├── generate_enhanced_dummy_data.py # Generator data dummy
├── import_enhanced_data.py        # Import data tambahan
└── SUPABASE_SETUP_GUIDE.md       # Panduan setup detail
```

## 🔧 Konfigurasi Supabase

1. Buat akun di [Supabase](https://supabase.com)
2. Buat project baru
3. Copy konfigurasi dari Settings > API:
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`
4. Copy konfigurasi dari Settings > Database:
   - `SUPABASE_DB_HOST`
   - `SUPABASE_DB_PASSWORD`

## 📈 Data Sources

- **Data Utama**: COVID-19 Indonesia time series
- **Data Tambahan**: 7 tabel enhancement (rumah sakit, vaksinasi, kebijakan, ekonomi, testing labs, cluster, mobilitas)

## 🎯 Tech Stack

- **Frontend**: Streamlit
- **Backend**: Supabase (PostgreSQL)
- **Visualization**: Plotly Express & Graph Objects
- **Data Processing**: Pandas, NumPy

## 📝 License

MIT License - Lihat file LICENSE untuk detail.