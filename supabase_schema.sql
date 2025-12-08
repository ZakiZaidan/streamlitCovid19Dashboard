-- =====================================================
-- COVID-19 INDONESIA DATABASE SCHEMA FOR SUPABASE
-- =====================================================
-- Compatible with Supabase PostgreSQL
-- Run this script in Supabase SQL Editor

-- Note: Supabase automatically creates database, no need for CREATE DATABASE
-- Enable Row Level Security will be handled separately

-- =====================================================
-- MAIN TABLES
-- =====================================================

-- Create LOKASI table
CREATE TABLE IF NOT EXISTS LOKASI (
    iso_code VARCHAR(10) PRIMARY KEY,
    nama_provinsi VARCHAR(100) NOT NULL,
    populasi BIGINT,
    luas_wilayah DECIMAL(12,2),
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    island VARCHAR(50),
    population_density DECIMAL(10,2),
    area_km2 DECIMAL(12,2),
    total_regencies INTEGER,
    total_cities INTEGER,
    total_districts INTEGER,
    total_urban_villages INTEGER,
    total_rural_villages INTEGER,
    time_zone VARCHAR(20),
    special_status VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create STATISTIK_HARIAN table
CREATE TABLE IF NOT EXISTS STATISTIK_HARIAN (
    id_transaksi BIGSERIAL PRIMARY KEY,
    iso_code VARCHAR(10) REFERENCES LOKASI(iso_code) ON DELETE CASCADE,
    tanggal DATE NOT NULL,
    kasus_baru INTEGER DEFAULT 0,
    kematian_baru INTEGER DEFAULT 0,
    sembuh_baru INTEGER DEFAULT 0,
    total_kasus INTEGER DEFAULT 0,
    total_kematian INTEGER DEFAULT 0,
    total_sembuh INTEGER DEFAULT 0,
    total_aktif INTEGER DEFAULT 0,
    kasus_baru_per_juta DECIMAL(10,2),
    total_kasus_per_juta DECIMAL(10,2),
    kematian_baru_per_juta DECIMAL(10,2),
    total_kematian_per_juta DECIMAL(10,2),
    case_fatality_rate DECIMAL(8,2),
    case_recovered_rate DECIMAL(8,2),
    growth_factor_cases DECIMAL(10,4),
    growth_factor_deaths DECIMAL(10,4),
    
    -- Healthcare & Testing Metrics
    tests_conducted INTEGER DEFAULT 0,
    positivity_rate DECIMAL(5,2),
    hospital_capacity DECIMAL(5,2),
    icu_occupancy DECIMAL(5,2),
    
    -- Vaccination Data
    vaccinations_total BIGINT DEFAULT 0,
    vaccinations_new INTEGER DEFAULT 0,
    fully_vaccinated BIGINT DEFAULT 0,
    vaccination_rate DECIMAL(8,2),
    
    -- Economic & Social Impact
    mobility_index DECIMAL(6,2),
    economic_impact_score INTEGER CHECK (economic_impact_score BETWEEN 1 AND 10),
    school_closure_level INTEGER CHECK (school_closure_level BETWEEN 0 AND 3),
    stringency_index DECIMAL(5,2) CHECK (stringency_index BETWEEN 0 AND 100),
    
    -- Demographics & Risk Factors
    age_group_risk VARCHAR(10) CHECK (age_group_risk IN ('Low', 'Medium', 'High', 'Very High')),
    comorbidity_rate DECIMAL(5,2),
    healthcare_workers_infected INTEGER DEFAULT 0,
    
    -- Weather & Environmental Data
    temperature_avg DECIMAL(5,2),
    humidity_avg DECIMAL(5,2),
    air_quality_index INTEGER CHECK (air_quality_index BETWEEN 0 AND 500),
    rainfall_mm DECIMAL(8,2),
    
    -- Social & Economic Indicators
    unemployment_rate DECIMAL(5,2),
    poverty_rate DECIMAL(5,2),
    education_index DECIMAL(4,3) CHECK (education_index BETWEEN 0 AND 1),
    internet_penetration DECIMAL(5,2),
    
    -- Healthcare Infrastructure
    hospital_beds_per_1000 DECIMAL(6,2),
    doctors_per_1000 DECIMAL(6,3),
    nurses_per_1000 DECIMAL(6,3),
    ventilators_available INTEGER DEFAULT 0,
    
    -- Transportation & Mobility
    public_transport_usage DECIMAL(5,2),
    private_vehicle_density DECIMAL(8,2),
    flight_frequency INTEGER DEFAULT 0,
    
    -- Demographic Details
    median_age DECIMAL(4,1),
    elderly_population_pct DECIMAL(5,2),
    urban_population_pct DECIMAL(5,2),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- ADDITIONAL TABLES FOR ENHANCED VISUALIZATION
-- =====================================================

-- 1. RUMAH_SAKIT - Data Rumah Sakit per Provinsi
CREATE TABLE IF NOT EXISTS RUMAH_SAKIT (
    id_rumah_sakit BIGSERIAL PRIMARY KEY,
    iso_code VARCHAR(10) REFERENCES LOKASI(iso_code) ON DELETE CASCADE,
    nama_rumah_sakit VARCHAR(200) NOT NULL,
    tipe_rumah_sakit VARCHAR(50) CHECK (tipe_rumah_sakit IN ('Pemerintah', 'Swasta', 'TNI/Polri', 'BUMN')),
    kelas_rumah_sakit VARCHAR(10) CHECK (kelas_rumah_sakit IN ('A', 'B', 'C', 'D')),
    
    -- Kapasitas Tempat Tidur
    total_bed INTEGER DEFAULT 0,
    icu_bed INTEGER DEFAULT 0,
    isolation_bed INTEGER DEFAULT 0,
    emergency_bed INTEGER DEFAULT 0,
    
    -- Fasilitas Medis
    ventilator_count INTEGER DEFAULT 0,
    oxygen_capacity INTEGER DEFAULT 0, -- dalam liter per menit
    ct_scan_available BOOLEAN DEFAULT FALSE,
    pcr_lab_available BOOLEAN DEFAULT FALSE,
    
    -- Tenaga Medis
    doctor_count INTEGER DEFAULT 0,
    nurse_count INTEGER DEFAULT 0,
    specialist_count INTEGER DEFAULT 0,
    
    -- Lokasi
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    alamat TEXT,
    
    -- Status Operasional
    covid_referral BOOLEAN DEFAULT FALSE,
    operational_status VARCHAR(20) CHECK (operational_status IN ('Aktif', 'Tutup Sementara', 'Renovasi')),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. VAKSINASI_DETAIL - Data Vaksinasi Terperinci
CREATE TABLE IF NOT EXISTS VAKSINASI_DETAIL (
    id_vaksinasi BIGSERIAL PRIMARY KEY,
    iso_code VARCHAR(10) REFERENCES LOKASI(iso_code) ON DELETE CASCADE,
    tanggal DATE NOT NULL,
    
    -- Jenis Vaksin
    vaksin_sinovac INTEGER DEFAULT 0,
    vaksin_astrazeneca INTEGER DEFAULT 0,
    vaksin_pfizer INTEGER DEFAULT 0,
    vaksin_moderna INTEGER DEFAULT 0,
    vaksin_novavax INTEGER DEFAULT 0,
    vaksin_lainnya INTEGER DEFAULT 0,
    
    -- Dosis
    dosis_1 INTEGER DEFAULT 0,
    dosis_2 INTEGER DEFAULT 0,
    dosis_booster INTEGER DEFAULT 0,
    
    -- Kelompok Sasaran
    lansia_vaksin INTEGER DEFAULT 0,
    dewasa_vaksin INTEGER DEFAULT 0,
    remaja_vaksin INTEGER DEFAULT 0,
    anak_vaksin INTEGER DEFAULT 0,
    
    -- Profesi Prioritas
    nakes_vaksin INTEGER DEFAULT 0,
    guru_vaksin INTEGER DEFAULT 0,
    petugas_publik_vaksin INTEGER DEFAULT 0,
    
    -- Lokasi Vaksinasi
    puskesmas_vaksin INTEGER DEFAULT 0,
    rumah_sakit_vaksin INTEGER DEFAULT 0,
    sentra_vaksin INTEGER DEFAULT 0,
    drive_thru_vaksin INTEGER DEFAULT 0,
    
    -- Efek Samping (KIPI)
    kipi_ringan INTEGER DEFAULT 0,
    kipi_sedang INTEGER DEFAULT 0,
    kipi_berat INTEGER DEFAULT 0,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. KEBIJAKAN_PEMERINTAH - Timeline Kebijakan COVID-19
CREATE TABLE IF NOT EXISTS KEBIJAKAN_PEMERINTAH (
    id_kebijakan BIGSERIAL PRIMARY KEY,
    iso_code VARCHAR(10) REFERENCES LOKASI(iso_code) ON DELETE CASCADE,
    tanggal_mulai DATE NOT NULL,
    tanggal_selesai DATE,
    
    -- Jenis Kebijakan
    jenis_kebijakan VARCHAR(50) CHECK (jenis_kebijakan IN (
        'PPKM Level 1', 'PPKM Level 2', 'PPKM Level 3', 'PPKM Level 4',
        'PSBB', 'Lockdown', 'Work From Home', 'Sekolah Daring',
        'Pembatasan Transportasi', 'Penutupan Mall', 'Pembatasan Ibadah'
    )),
    
    nama_kebijakan VARCHAR(200) NOT NULL,
    deskripsi_kebijakan TEXT,
    
    -- Level Pembatasan (1-10, 10 = paling ketat)
    tingkat_keketatan INTEGER CHECK (tingkat_keketatan BETWEEN 1 AND 10),
    
    -- Sektor yang Terdampak
    sektor_pendidikan BOOLEAN DEFAULT FALSE,
    sektor_ekonomi BOOLEAN DEFAULT FALSE,
    sektor_transportasi BOOLEAN DEFAULT FALSE,
    sektor_pariwisata BOOLEAN DEFAULT FALSE,
    sektor_ibadah BOOLEAN DEFAULT FALSE,
    
    -- Compliance Rate (estimasi kepatuhan masyarakat %)
    compliance_rate DECIMAL(5,2),
    
    -- Dampak Ekonomi (estimasi penurunan aktivitas ekonomi %)
    dampak_ekonomi_pct DECIMAL(5,2),
    
    status_kebijakan VARCHAR(20) CHECK (status_kebijakan IN ('Aktif', 'Berakhir', 'Diperpanjang', 'Dicabut')),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. EKONOMI_REGIONAL - Dampak Ekonomi Regional
CREATE TABLE IF NOT EXISTS EKONOMI_REGIONAL (
    id_ekonomi BIGSERIAL PRIMARY KEY,
    iso_code VARCHAR(10) REFERENCES LOKASI(iso_code) ON DELETE CASCADE,
    tahun INTEGER NOT NULL,
    bulan INTEGER CHECK (bulan BETWEEN 1 AND 12),
    
    -- Indikator Ekonomi Makro
    pdrb_milyar DECIMAL(15,2), -- PDRB dalam milyar rupiah
    pertumbuhan_ekonomi DECIMAL(5,2), -- % YoY
    inflasi_rate DECIMAL(5,2), -- %
    
    -- Ketenagakerjaan
    tingkat_pengangguran DECIMAL(5,2), -- %
    tingkat_partisipasi_kerja DECIMAL(5,2), -- %
    upah_minimum_regional BIGINT, -- dalam rupiah
    
    -- Sektor Ekonomi (kontribusi terhadap PDRB dalam %)
    sektor_pertanian DECIMAL(5,2),
    sektor_industri DECIMAL(5,2),
    sektor_perdagangan DECIMAL(5,2),
    sektor_jasa DECIMAL(5,2),
    sektor_pariwisata DECIMAL(5,2),
    
    -- Dampak COVID-19
    penurunan_omzet_umkm DECIMAL(5,2), -- %
    penutupan_usaha INTEGER DEFAULT 0, -- jumlah usaha yang tutup
    bantuan_sosial_milyar DECIMAL(10,2), -- bantuan pemerintah dalam milyar
    
    -- Indikator Pemulihan
    recovery_index DECIMAL(5,2) CHECK (recovery_index BETWEEN 0 AND 100), -- 0-100
    business_confidence DECIMAL(5,2), -- indeks kepercayaan bisnis
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. TESTING_LABS - Laboratorium Testing COVID-19
CREATE TABLE IF NOT EXISTS TESTING_LABS (
    id_lab BIGSERIAL PRIMARY KEY,
    iso_code VARCHAR(10) REFERENCES LOKASI(iso_code) ON DELETE CASCADE,
    nama_lab VARCHAR(200) NOT NULL,
    
    -- Jenis Lab
    jenis_lab VARCHAR(50) CHECK (jenis_lab IN ('PCR', 'Antigen', 'Antibodi', 'Kombinasi')),
    tipe_kepemilikan VARCHAR(50) CHECK (tipe_kepemilikan IN ('Pemerintah', 'Swasta', 'Universitas', 'TNI/Polri')),
    
    -- Kapasitas Testing
    kapasitas_harian_pcr INTEGER DEFAULT 0,
    kapasitas_harian_antigen INTEGER DEFAULT 0,
    kapasitas_harian_antibodi INTEGER DEFAULT 0,
    
    -- Peralatan
    mesin_pcr_count INTEGER DEFAULT 0,
    extraction_kit_stock INTEGER DEFAULT 0,
    reagent_stock INTEGER DEFAULT 0,
    
    -- Tenaga Ahli
    analis_count INTEGER DEFAULT 0,
    teknisi_count INTEGER DEFAULT 0,
    
    -- Waktu Pemrosesan (dalam jam)
    turnaround_time_pcr INTEGER DEFAULT 24,
    turnaround_time_antigen INTEGER DEFAULT 1,
    
    -- Akreditasi
    akreditasi_kemenkes BOOLEAN DEFAULT FALSE,
    iso_certified BOOLEAN DEFAULT FALSE,
    
    -- Lokasi
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    alamat TEXT,
    
    -- Operational Status
    operational_24_hours BOOLEAN DEFAULT FALSE,
    drive_thru_available BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 6. CLUSTER_PENULARAN - Data Cluster Penularan
CREATE TABLE IF NOT EXISTS CLUSTER_PENULARAN (
    id_cluster BIGSERIAL PRIMARY KEY,
    iso_code VARCHAR(10) REFERENCES LOKASI(iso_code) ON DELETE CASCADE,
    tanggal_terdeteksi DATE NOT NULL,
    tanggal_selesai DATE,
    
    -- Identifikasi Cluster
    nama_cluster VARCHAR(200) NOT NULL,
    jenis_cluster VARCHAR(50) CHECK (jenis_cluster IN (
        'Perkantoran', 'Pabrik', 'Sekolah', 'Universitas', 'Pasar',
        'Mall', 'Rumah Sakit', 'Panti Jompo', 'Asrama', 'Pernikahan',
        'Keagamaan', 'Olahraga', 'Transportasi', 'Keluarga', 'Lainnya'
    )),
    
    -- Lokasi Cluster
    nama_lokasi VARCHAR(200),
    alamat_lokasi TEXT,
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    
    -- Data Penularan
    kasus_index INTEGER DEFAULT 1, -- pasien pertama
    total_kasus_terkait INTEGER DEFAULT 0,
    total_kontak_erat INTEGER DEFAULT 0,
    total_suspect INTEGER DEFAULT 0,
    
    -- Demografi Terdampak
    kasus_anak INTEGER DEFAULT 0, -- 0-17 tahun
    kasus_dewasa INTEGER DEFAULT 0, -- 18-59 tahun
    kasus_lansia INTEGER DEFAULT 0, -- 60+ tahun
    
    kasus_laki INTEGER DEFAULT 0,
    kasus_perempuan INTEGER DEFAULT 0,
    
    -- Tingkat Keparahan
    kasus_tanpa_gejala INTEGER DEFAULT 0,
    kasus_ringan INTEGER DEFAULT 0,
    kasus_sedang INTEGER DEFAULT 0,
    kasus_berat INTEGER DEFAULT 0,
    kasus_kritis INTEGER DEFAULT 0,
    kasus_meninggal INTEGER DEFAULT 0,
    
    -- Tindakan Pengendalian
    contact_tracing_completed BOOLEAN DEFAULT FALSE,
    area_disinfection BOOLEAN DEFAULT FALSE,
    temporary_closure BOOLEAN DEFAULT FALSE,
    mass_testing BOOLEAN DEFAULT FALSE,
    
    -- Status Cluster
    status_cluster VARCHAR(20) CHECK (status_cluster IN ('Aktif', 'Terkendali', 'Selesai')),
    
    -- Catatan
    catatan TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 7. MOBILITAS_HARIAN - Data Mobilitas Masyarakat
CREATE TABLE IF NOT EXISTS MOBILITAS_HARIAN (
    id_mobilitas BIGSERIAL PRIMARY KEY,
    iso_code VARCHAR(10) REFERENCES LOKASI(iso_code) ON DELETE CASCADE,
    tanggal DATE NOT NULL,
    
    -- Mobilitas berdasarkan lokasi (% perubahan dari baseline)
    retail_recreation DECIMAL(6,2), -- toko, restoran, mall
    grocery_pharmacy DECIMAL(6,2), -- supermarket, apotek
    parks DECIMAL(6,2), -- taman, pantai
    transit_stations DECIMAL(6,2), -- stasiun, terminal
    workplaces DECIMAL(6,2), -- tempat kerja
    residential DECIMAL(6,2), -- area residensial
    
    -- Mobilitas berdasarkan transportasi
    private_vehicle_movement DECIMAL(6,2),
    public_transport_usage DECIMAL(6,2),
    walking_cycling DECIMAL(6,2),
    
    -- Mobilitas berdasarkan waktu
    morning_rush_hour DECIMAL(6,2), -- 06:00-09:00
    afternoon_activity DECIMAL(6,2), -- 09:00-17:00
    evening_rush_hour DECIMAL(6,2), -- 17:00-20:00
    night_activity DECIMAL(6,2), -- 20:00-06:00
    
    -- Indeks Mobilitas Gabungan
    overall_mobility_index DECIMAL(6,2),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- INDEXES FOR OPTIMAL PERFORMANCE
-- =====================================================

-- Indexes untuk LOKASI
CREATE INDEX IF NOT EXISTS idx_lokasi_nama_provinsi ON LOKASI(nama_provinsi);
CREATE INDEX IF NOT EXISTS idx_lokasi_island ON LOKASI(island);

-- Indexes untuk STATISTIK_HARIAN
CREATE INDEX IF NOT EXISTS idx_statistik_tanggal ON STATISTIK_HARIAN(tanggal);
CREATE INDEX IF NOT EXISTS idx_statistik_iso_code ON STATISTIK_HARIAN(iso_code);
CREATE INDEX IF NOT EXISTS idx_statistik_iso_tanggal ON STATISTIK_HARIAN(iso_code, tanggal);
CREATE INDEX IF NOT EXISTS idx_statistik_vaccination_rate ON STATISTIK_HARIAN(vaccination_rate);
CREATE INDEX IF NOT EXISTS idx_statistik_positivity_rate ON STATISTIK_HARIAN(positivity_rate);
CREATE INDEX IF NOT EXISTS idx_statistik_stringency_index ON STATISTIK_HARIAN(stringency_index);
CREATE INDEX IF NOT EXISTS idx_statistik_air_quality ON STATISTIK_HARIAN(air_quality_index);
CREATE INDEX IF NOT EXISTS idx_statistik_unemployment ON STATISTIK_HARIAN(unemployment_rate);
CREATE INDEX IF NOT EXISTS idx_statistik_education ON STATISTIK_HARIAN(education_index);
CREATE INDEX IF NOT EXISTS idx_statistik_median_age ON STATISTIK_HARIAN(median_age);

-- Indexes untuk RUMAH_SAKIT
CREATE INDEX IF NOT EXISTS idx_rumah_sakit_iso_code ON RUMAH_SAKIT(iso_code);
CREATE INDEX IF NOT EXISTS idx_rumah_sakit_tipe ON RUMAH_SAKIT(tipe_rumah_sakit);
CREATE INDEX IF NOT EXISTS idx_rumah_sakit_covid_referral ON RUMAH_SAKIT(covid_referral);

-- Indexes untuk VAKSINASI_DETAIL
CREATE INDEX IF NOT EXISTS idx_vaksinasi_iso_tanggal ON VAKSINASI_DETAIL(iso_code, tanggal);
CREATE INDEX IF NOT EXISTS idx_vaksinasi_tanggal ON VAKSINASI_DETAIL(tanggal);

-- Indexes untuk KEBIJAKAN_PEMERINTAH
CREATE INDEX IF NOT EXISTS idx_kebijakan_iso_tanggal ON KEBIJAKAN_PEMERINTAH(iso_code, tanggal_mulai);
CREATE INDEX IF NOT EXISTS idx_kebijakan_jenis ON KEBIJAKAN_PEMERINTAH(jenis_kebijakan);
CREATE INDEX IF NOT EXISTS idx_kebijakan_status ON KEBIJAKAN_PEMERINTAH(status_kebijakan);

-- Indexes untuk EKONOMI_REGIONAL
CREATE INDEX IF NOT EXISTS idx_ekonomi_iso_tahun_bulan ON EKONOMI_REGIONAL(iso_code, tahun, bulan);
CREATE INDEX IF NOT EXISTS idx_ekonomi_tahun_bulan ON EKONOMI_REGIONAL(tahun, bulan);

-- Indexes untuk TESTING_LABS
CREATE INDEX IF NOT EXISTS idx_testing_labs_iso_code ON TESTING_LABS(iso_code);
CREATE INDEX IF NOT EXISTS idx_testing_labs_jenis ON TESTING_LABS(jenis_lab);

-- Indexes untuk CLUSTER_PENULARAN
CREATE INDEX IF NOT EXISTS idx_cluster_iso_tanggal ON CLUSTER_PENULARAN(iso_code, tanggal_terdeteksi);
CREATE INDEX IF NOT EXISTS idx_cluster_jenis ON CLUSTER_PENULARAN(jenis_cluster);
CREATE INDEX IF NOT EXISTS idx_cluster_status ON CLUSTER_PENULARAN(status_cluster);

-- Indexes untuk MOBILITAS_HARIAN
CREATE INDEX IF NOT EXISTS idx_mobilitas_iso_tanggal ON MOBILITAS_HARIAN(iso_code, tanggal);
CREATE INDEX IF NOT EXISTS idx_mobilitas_tanggal ON MOBILITAS_HARIAN(tanggal);

-- =====================================================
-- VIEWS FOR EASIER ANALYSIS
-- =====================================================

-- View: Latest statistics per province
CREATE OR REPLACE VIEW latest_statistics AS
SELECT 
    l.iso_code,
    l.nama_provinsi,
    l.populasi,
    l.latitude,
    l.longitude,
    l.island,
    l.population_density,
    s.tanggal,
    s.total_kasus,
    s.total_kematian,
    s.total_sembuh,
    s.total_aktif,
    s.case_fatality_rate,
    s.case_recovered_rate,
    s.positivity_rate,
    s.hospital_capacity,
    s.icu_occupancy,
    s.vaccination_rate,
    s.fully_vaccinated,
    s.mobility_index,
    s.stringency_index,
    s.age_group_risk,
    s.comorbidity_rate,
    s.temperature_avg,
    s.humidity_avg,
    s.air_quality_index,
    s.unemployment_rate,
    s.poverty_rate,
    s.education_index,
    s.internet_penetration,
    s.hospital_beds_per_1000,
    s.doctors_per_1000,
    s.median_age,
    s.elderly_population_pct,
    s.urban_population_pct
FROM LOKASI l
JOIN STATISTIK_HARIAN s ON l.iso_code = s.iso_code
WHERE s.tanggal = (
    SELECT MAX(tanggal) 
    FROM STATISTIK_HARIAN s2 
    WHERE s2.iso_code = s.iso_code
);

-- View: National daily statistics
CREATE OR REPLACE VIEW national_daily_stats AS
SELECT 
    tanggal,
    SUM(kasus_baru) as total_kasus_baru_nasional,
    SUM(kematian_baru) as total_kematian_baru_nasional,
    SUM(sembuh_baru) as total_sembuh_baru_nasional,
    SUM(total_kasus) as total_kasus_nasional,
    SUM(total_kematian) as total_kematian_nasional,
    SUM(total_sembuh) as total_sembuh_nasional,
    SUM(total_aktif) as total_aktif_nasional,
    SUM(tests_conducted) as total_tests_nasional,
    AVG(positivity_rate) as avg_positivity_rate_nasional,
    AVG(hospital_capacity) as avg_hospital_capacity_nasional,
    AVG(icu_occupancy) as avg_icu_occupancy_nasional,
    SUM(vaccinations_new) as total_vaccinations_new_nasional,
    SUM(fully_vaccinated) as total_fully_vaccinated_nasional,
    AVG(mobility_index) as avg_mobility_index_nasional,
    AVG(stringency_index) as avg_stringency_index_nasional,
    AVG(temperature_avg) as avg_temperature_nasional,
    AVG(humidity_avg) as avg_humidity_nasional,
    AVG(air_quality_index) as avg_air_quality_nasional,
    AVG(unemployment_rate) as avg_unemployment_rate_nasional,
    AVG(poverty_rate) as avg_poverty_rate_nasional,
    AVG(education_index) as avg_education_index_nasional,
    AVG(internet_penetration) as avg_internet_penetration_nasional,
    AVG(hospital_beds_per_1000) as avg_hospital_beds_nasional,
    AVG(doctors_per_1000) as avg_doctors_nasional,
    SUM(ventilators_available) as total_ventilators_nasional,
    AVG(public_transport_usage) as avg_public_transport_nasional,
    SUM(flight_frequency) as total_flight_frequency_nasional,
    AVG(median_age) as avg_median_age_nasional,
    AVG(elderly_population_pct) as avg_elderly_population_nasional,
    AVG(urban_population_pct) as avg_urban_population_nasional
FROM STATISTIK_HARIAN
WHERE iso_code != 'IDN'  -- Exclude national level data to avoid double counting
GROUP BY tanggal
ORDER BY tanggal;

-- View: Healthcare capacity per province
CREATE OR REPLACE VIEW kapasitas_kesehatan_provinsi AS
SELECT 
    l.iso_code,
    l.nama_provinsi,
    COUNT(rs.id_rumah_sakit) as total_rumah_sakit,
    SUM(rs.total_bed) as total_tempat_tidur,
    SUM(rs.icu_bed) as total_icu,
    SUM(rs.isolation_bed) as total_isolasi,
    SUM(rs.ventilator_count) as total_ventilator,
    SUM(rs.doctor_count) as total_dokter,
    SUM(rs.nurse_count) as total_perawat,
    COUNT(tl.id_lab) as total_lab_testing,
    SUM(tl.kapasitas_harian_pcr) as kapasitas_pcr_harian,
    SUM(tl.kapasitas_harian_antigen) as kapasitas_antigen_harian
FROM LOKASI l
LEFT JOIN RUMAH_SAKIT rs ON l.iso_code = rs.iso_code
LEFT JOIN TESTING_LABS tl ON l.iso_code = tl.iso_code
GROUP BY l.iso_code, l.nama_provinsi;

-- View: Latest vaccination per province
CREATE OR REPLACE VIEW vaksinasi_terkini AS
SELECT 
    l.iso_code,
    l.nama_provinsi,
    vd.tanggal,
    vd.dosis_1,
    vd.dosis_2,
    vd.dosis_booster,
    (vd.dosis_1 + vd.dosis_2 + vd.dosis_booster) as total_vaksinasi,
    vd.vaksin_sinovac,
    vd.vaksin_astrazeneca,
    vd.vaksin_pfizer,
    vd.vaksin_moderna
FROM LOKASI l
JOIN VAKSINASI_DETAIL vd ON l.iso_code = vd.iso_code
WHERE vd.tanggal = (
    SELECT MAX(tanggal) 
    FROM VAKSINASI_DETAIL vd2 
    WHERE vd2.iso_code = vd.iso_code
);

-- View: Active clusters per province
CREATE OR REPLACE VIEW cluster_aktif AS
SELECT 
    l.iso_code,
    l.nama_provinsi,
    COUNT(cp.id_cluster) as total_cluster_aktif,
    SUM(cp.total_kasus_terkait) as total_kasus_cluster,
    cp.jenis_cluster,
    AVG(cp.total_kasus_terkait) as rata_rata_kasus_per_cluster
FROM LOKASI l
JOIN CLUSTER_PENULARAN cp ON l.iso_code = cp.iso_code
WHERE cp.status_cluster = 'Aktif'
GROUP BY l.iso_code, l.nama_provinsi, cp.jenis_cluster;

-- View: Latest economic impact
CREATE OR REPLACE VIEW dampak_ekonomi_terkini AS
SELECT 
    l.iso_code,
    l.nama_provinsi,
    er.tahun,
    er.bulan,
    er.pertumbuhan_ekonomi,
    er.tingkat_pengangguran,
    er.recovery_index,
    er.penurunan_omzet_umkm,
    er.bantuan_sosial_milyar
FROM LOKASI l
JOIN EKONOMI_REGIONAL er ON l.iso_code = er.iso_code
WHERE (er.tahun, er.bulan) = (
    SELECT tahun, bulan 
    FROM EKONOMI_REGIONAL er2 
    WHERE er2.iso_code = er.iso_code 
    ORDER BY tahun DESC, bulan DESC 
    LIMIT 1
);

-- =====================================================
-- FUNCTIONS AND TRIGGERS
-- =====================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for automatic timestamp updates
CREATE TRIGGER update_lokasi_updated_at 
    BEFORE UPDATE ON LOKASI 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_statistik_harian_updated_at 
    BEFORE UPDATE ON STATISTIK_HARIAN 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_rumah_sakit_updated_at 
    BEFORE UPDATE ON RUMAH_SAKIT 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_testing_labs_updated_at 
    BEFORE UPDATE ON TESTING_LABS 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_cluster_penularan_updated_at 
    BEFORE UPDATE ON CLUSTER_PENULARAN 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- ROW LEVEL SECURITY (RLS) SETUP
-- =====================================================
-- Note: Enable RLS in Supabase Dashboard or run these commands:

-- Enable RLS on all tables
-- ALTER TABLE LOKASI ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE STATISTIK_HARIAN ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE RUMAH_SAKIT ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE VAKSINASI_DETAIL ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE KEBIJAKAN_PEMERINTAH ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE EKONOMI_REGIONAL ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE TESTING_LABS ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE CLUSTER_PENULARAN ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE MOBILITAS_HARIAN ENABLE ROW LEVEL SECURITY;

-- Create policies for public read access (adjust as needed)
-- CREATE POLICY "Allow public read access" ON LOKASI FOR SELECT USING (true);
-- CREATE POLICY "Allow public read access" ON STATISTIK_HARIAN FOR SELECT USING (true);
-- CREATE POLICY "Allow public read access" ON RUMAH_SAKIT FOR SELECT USING (true);
-- CREATE POLICY "Allow public read access" ON VAKSINASI_DETAIL FOR SELECT USING (true);
-- CREATE POLICY "Allow public read access" ON KEBIJAKAN_PEMERINTAH FOR SELECT USING (true);
-- CREATE POLICY "Allow public read access" ON EKONOMI_REGIONAL FOR SELECT USING (true);
-- CREATE POLICY "Allow public read access" ON TESTING_LABS FOR SELECT USING (true);
-- CREATE POLICY "Allow public read access" ON CLUSTER_PENULARAN FOR SELECT USING (true);
-- CREATE POLICY "Allow public read access" ON MOBILITAS_HARIAN FOR SELECT USING (true);

-- =====================================================
-- COMMENTS FOR DOCUMENTATION
-- =====================================================

COMMENT ON TABLE LOKASI IS 'Data lokasi provinsi Indonesia dengan informasi geografis dan demografis';
COMMENT ON TABLE STATISTIK_HARIAN IS 'Data statistik COVID-19 harian per provinsi dengan indikator lengkap';
COMMENT ON TABLE RUMAH_SAKIT IS 'Data rumah sakit dan fasilitas kesehatan per provinsi';
COMMENT ON TABLE VAKSINASI_DETAIL IS 'Data vaksinasi terperinci per provinsi dan tanggal';
COMMENT ON TABLE KEBIJAKAN_PEMERINTAH IS 'Timeline kebijakan pemerintah terkait COVID-19';
COMMENT ON TABLE EKONOMI_REGIONAL IS 'Data dampak ekonomi regional akibat COVID-19';
COMMENT ON TABLE TESTING_LABS IS 'Data laboratorium testing COVID-19';
COMMENT ON TABLE CLUSTER_PENULARAN IS 'Data cluster penularan COVID-19';
COMMENT ON TABLE MOBILITAS_HARIAN IS 'Data mobilitas masyarakat harian';

COMMENT ON VIEW latest_statistics IS 'Statistik terkini per provinsi';
COMMENT ON VIEW national_daily_stats IS 'Statistik harian nasional';
COMMENT ON VIEW kapasitas_kesehatan_provinsi IS 'Ringkasan kapasitas kesehatan per provinsi';
COMMENT ON VIEW vaksinasi_terkini IS 'Data vaksinasi terkini per provinsi';
COMMENT ON VIEW cluster_aktif IS 'Cluster penularan yang masih aktif';
COMMENT ON VIEW dampak_ekonomi_terkini IS 'Dampak ekonomi terkini per provinsi';

-- =====================================================
-- SCHEMA CREATION COMPLETE
-- =====================================================
-- 
-- NEXT STEPS:
-- 1. Run this script in Supabase SQL Editor
-- 2. Configure Row Level Security policies as needed
-- 3. Import your data using the updated import scripts
-- 4. Update your Streamlit app connection settings
-- 
-- For data import, use the supabase_data_import.py script
-- For Streamlit connection, update the connection parameters
-- 
-- =====================================================
