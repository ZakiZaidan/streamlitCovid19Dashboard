#!/usr/bin/env python3
"""
Script untuk generate data dummy yang realistis untuk tabel-tabel baru
COVID-19 Indonesia Enhanced Database
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta, date
import json
import os

# Set random seed untuk reproducibility
np.random.seed(42)
random.seed(42)

# Data provinsi Indonesia
PROVINSI_DATA = {
    'ID-AC': 'Aceh', 'ID-SU': 'Sumatera Utara', 'ID-SB': 'Sumatera Barat', 'ID-RI': 'Riau',
    'ID-JA': 'Jambi', 'ID-SS': 'Sumatera Selatan', 'ID-BE': 'Bengkulu', 'ID-LA': 'Lampung',
    'ID-BB': 'Kepulauan Bangka Belitung', 'ID-KR': 'Kepulauan Riau', 'ID-JK': 'DKI Jakarta',
    'ID-JB': 'Jawa Barat', 'ID-JT': 'Jawa Tengah', 'ID-YO': 'Yogyakarta', 'ID-JI': 'Jawa Timur',
    'ID-BT': 'Banten', 'ID-BA': 'Bali', 'ID-NB': 'Nusa Tenggara Barat', 'ID-NT': 'Nusa Tenggara Timur',
    'ID-KB': 'Kalimantan Barat', 'ID-KT': 'Kalimantan Tengah', 'ID-KS': 'Kalimantan Selatan',
    'ID-KI': 'Kalimantan Timur', 'ID-KU': 'Kalimantan Utara', 'ID-SA': 'Sulawesi Utara',
    'ID-ST': 'Sulawesi Tengah', 'ID-SN': 'Sulawesi Selatan', 'ID-SG': 'Sulawesi Tenggara',
    'ID-GO': 'Gorontalo', 'ID-SR': 'Sulawesi Barat', 'ID-MA': 'Maluku', 'ID-MU': 'Maluku Utara',
    'ID-PA': 'Papua', 'ID-PB': 'Papua Barat'
}

def generate_rumah_sakit_data():
    """Generate data rumah sakit dummy"""
    print("🏥 Generating Rumah Sakit data...")
    
    data = []
    id_counter = 1
    
    for iso_code, nama_provinsi in PROVINSI_DATA.items():
        # Tentukan jumlah rumah sakit berdasarkan populasi provinsi
        if iso_code in ['ID-JK', 'ID-JB', 'ID-JI', 'ID-JT']:  # Provinsi besar
            num_hospitals = random.randint(15, 25)
        elif iso_code in ['ID-SU', 'ID-SB', 'ID-SS', 'ID-BA', 'ID-SN']:  # Provinsi sedang
            num_hospitals = random.randint(8, 15)
        else:  # Provinsi kecil
            num_hospitals = random.randint(3, 8)
        
        for i in range(num_hospitals):
            # Tipe rumah sakit
            tipe_rs = np.random.choice(['Pemerintah', 'Swasta', 'TNI/Polri', 'BUMN'], 
                                    p=[0.4, 0.45, 0.1, 0.05])
            
            # Kelas rumah sakit
            if tipe_rs == 'Pemerintah':
                kelas_rs = np.random.choice(['A', 'B', 'C', 'D'], p=[0.1, 0.3, 0.4, 0.2])
            else:
                kelas_rs = np.random.choice(['A', 'B', 'C'], p=[0.2, 0.5, 0.3])
            
            # Kapasitas berdasarkan kelas
            if kelas_rs == 'A':
                total_bed = random.randint(300, 800)
                icu_bed = int(total_bed * random.uniform(0.05, 0.1))
                isolation_bed = int(total_bed * random.uniform(0.1, 0.2))
            elif kelas_rs == 'B':
                total_bed = random.randint(150, 300)
                icu_bed = int(total_bed * random.uniform(0.03, 0.08))
                isolation_bed = int(total_bed * random.uniform(0.08, 0.15))
            elif kelas_rs == 'C':
                total_bed = random.randint(50, 150)
                icu_bed = int(total_bed * random.uniform(0.02, 0.05))
                isolation_bed = int(total_bed * random.uniform(0.05, 0.1))
            else:  # Kelas D
                total_bed = random.randint(20, 50)
                icu_bed = int(total_bed * random.uniform(0.01, 0.03))
                isolation_bed = int(total_bed * random.uniform(0.03, 0.08))
            
            emergency_bed = int(total_bed * random.uniform(0.05, 0.1))
            
            # Fasilitas medis
            ventilator_count = max(1, int(icu_bed * random.uniform(0.8, 1.2)))
            oxygen_capacity = total_bed * random.randint(5, 15)  # liter per menit per bed
            
            # Tenaga medis
            doctor_count = max(5, int(total_bed * random.uniform(0.1, 0.3)))
            nurse_count = max(10, int(total_bed * random.uniform(0.5, 1.2)))
            specialist_count = max(2, int(doctor_count * random.uniform(0.2, 0.5)))
            
            # Koordinat dummy (sekitar Indonesia)
            latitude = random.uniform(-11, 6)  # Range latitude Indonesia
            longitude = random.uniform(95, 141)  # Range longitude Indonesia
            
            data.append({
                'id_rumah_sakit': id_counter,
                'iso_code': iso_code,
                'nama_rumah_sakit': f'RS {random.choice(["Umum", "Daerah", "Swasta", "Bhayangkara", "TNI"])} {nama_provinsi} {i+1}',
                'tipe_rumah_sakit': tipe_rs,
                'kelas_rumah_sakit': kelas_rs,
                'total_bed': total_bed,
                'icu_bed': icu_bed,
                'isolation_bed': isolation_bed,
                'emergency_bed': emergency_bed,
                'ventilator_count': ventilator_count,
                'oxygen_capacity': oxygen_capacity,
                'ct_scan_available': random.choice([True, False]) if kelas_rs in ['A', 'B'] else False,
                'pcr_lab_available': random.choice([True, False]) if kelas_rs in ['A', 'B'] else random.choice([True, False, False]),
                'doctor_count': doctor_count,
                'nurse_count': nurse_count,
                'specialist_count': specialist_count,
                'latitude': round(latitude, 6),
                'longitude': round(longitude, 6),
                'alamat': f'Jl. Kesehatan No. {random.randint(1, 100)}, {nama_provinsi}',
                'covid_referral': random.choice([True, False]),
                'operational_status': np.random.choice(['Aktif', 'Tutup Sementara', 'Renovasi'], p=[0.9, 0.08, 0.02])
            })
            
            id_counter += 1
    
    return pd.DataFrame(data)

def generate_vaksinasi_detail_data():
    """Generate data vaksinasi detail dummy"""
    print("💉 Generating Vaksinasi Detail data...")
    
    data = []
    id_counter = 1
    
    # Generate data untuk periode Maret 2021 - September 2022 (program vaksinasi)
    start_date = date(2021, 3, 1)
    end_date = date(2022, 9, 15)
    current_date = start_date
    
    while current_date <= end_date:
        for iso_code, nama_provinsi in PROVINSI_DATA.items():
            # Populasi estimasi per provinsi (dalam jutaan)
            pop_estimates = {
                'ID-JB': 48, 'ID-JI': 40, 'ID-JT': 36, 'ID-SU': 15, 'ID-JK': 11,
                'ID-SN': 9, 'ID-RI': 6, 'ID-LA': 8, 'ID-SS': 8, 'ID-AC': 5
            }
            populasi = pop_estimates.get(iso_code, 3) * 1000000  # default 3 juta
            
            # Target vaksinasi harian (0.1% - 0.5% populasi per hari)
            target_harian = int(populasi * random.uniform(0.001, 0.005))
            
            # Distribusi jenis vaksin berdasarkan periode
            if current_date < date(2021, 6, 1):  # Awal program
                vaksin_sinovac = int(target_harian * random.uniform(0.7, 0.9))
                vaksin_astrazeneca = int(target_harian * random.uniform(0.1, 0.3))
                vaksin_pfizer = 0
                vaksin_moderna = 0
            elif current_date < date(2021, 10, 1):  # Pertengahan
                vaksin_sinovac = int(target_harian * random.uniform(0.4, 0.6))
                vaksin_astrazeneca = int(target_harian * random.uniform(0.2, 0.4))
                vaksin_pfizer = int(target_harian * random.uniform(0.1, 0.2))
                vaksin_moderna = int(target_harian * random.uniform(0.05, 0.15))
            else:  # Akhir program
                vaksin_sinovac = int(target_harian * random.uniform(0.2, 0.4))
                vaksin_astrazeneca = int(target_harian * random.uniform(0.1, 0.3))
                vaksin_pfizer = int(target_harian * random.uniform(0.3, 0.5))
                vaksin_moderna = int(target_harian * random.uniform(0.1, 0.3))
            
            vaksin_lainnya = max(0, target_harian - (vaksin_sinovac + vaksin_astrazeneca + vaksin_pfizer + vaksin_moderna))
            
            # Distribusi dosis
            total_vaksin = vaksin_sinovac + vaksin_astrazeneca + vaksin_pfizer + vaksin_moderna + vaksin_lainnya
            
            if current_date < date(2021, 8, 1):  # Fokus dosis 1
                dosis_1 = int(total_vaksin * random.uniform(0.7, 0.9))
                dosis_2 = int(total_vaksin * random.uniform(0.1, 0.3))
                dosis_booster = 0
            elif current_date < date(2022, 1, 1):  # Fokus dosis 2
                dosis_1 = int(total_vaksin * random.uniform(0.3, 0.5))
                dosis_2 = int(total_vaksin * random.uniform(0.5, 0.7))
                dosis_booster = int(total_vaksin * random.uniform(0.0, 0.1))
            else:  # Program booster
                dosis_1 = int(total_vaksin * random.uniform(0.2, 0.3))
                dosis_2 = int(total_vaksin * random.uniform(0.3, 0.5))
                dosis_booster = int(total_vaksin * random.uniform(0.2, 0.5))
            
            # Kelompok sasaran
            lansia_vaksin = int(total_vaksin * random.uniform(0.15, 0.25))
            dewasa_vaksin = int(total_vaksin * random.uniform(0.6, 0.75))
            remaja_vaksin = int(total_vaksin * random.uniform(0.05, 0.15))
            anak_vaksin = int(total_vaksin * random.uniform(0.0, 0.1)) if current_date > date(2021, 12, 1) else 0
            
            # Profesi prioritas
            nakes_vaksin = int(total_vaksin * random.uniform(0.05, 0.15))
            guru_vaksin = int(total_vaksin * random.uniform(0.03, 0.1))
            petugas_publik_vaksin = int(total_vaksin * random.uniform(0.02, 0.08))
            
            # Lokasi vaksinasi
            puskesmas_vaksin = int(total_vaksin * random.uniform(0.4, 0.6))
            rumah_sakit_vaksin = int(total_vaksin * random.uniform(0.2, 0.3))
            sentra_vaksin = int(total_vaksin * random.uniform(0.1, 0.2))
            drive_thru_vaksin = int(total_vaksin * random.uniform(0.05, 0.15))
            
            # KIPI (Kejadian Ikutan Pasca Imunisasi)
            kipi_ringan = int(total_vaksin * random.uniform(0.01, 0.05))
            kipi_sedang = int(total_vaksin * random.uniform(0.001, 0.01))
            kipi_berat = int(total_vaksin * random.uniform(0.0001, 0.001))
            
            data.append({
                'id_vaksinasi': id_counter,
                'iso_code': iso_code,
                'tanggal': current_date,
                'vaksin_sinovac': vaksin_sinovac,
                'vaksin_astrazeneca': vaksin_astrazeneca,
                'vaksin_pfizer': vaksin_pfizer,
                'vaksin_moderna': vaksin_moderna,
                'vaksin_novavax': int(vaksin_lainnya * 0.3),
                'vaksin_lainnya': int(vaksin_lainnya * 0.7),
                'dosis_1': dosis_1,
                'dosis_2': dosis_2,
                'dosis_booster': dosis_booster,
                'lansia_vaksin': lansia_vaksin,
                'dewasa_vaksin': dewasa_vaksin,
                'remaja_vaksin': remaja_vaksin,
                'anak_vaksin': anak_vaksin,
                'nakes_vaksin': nakes_vaksin,
                'guru_vaksin': guru_vaksin,
                'petugas_publik_vaksin': petugas_publik_vaksin,
                'puskesmas_vaksin': puskesmas_vaksin,
                'rumah_sakit_vaksin': rumah_sakit_vaksin,
                'sentra_vaksin': sentra_vaksin,
                'drive_thru_vaksin': drive_thru_vaksin,
                'kipi_ringan': kipi_ringan,
                'kipi_sedang': kipi_sedang,
                'kipi_berat': kipi_berat
            })
            
            id_counter += 1
        
        current_date += timedelta(days=7)  # Data mingguan untuk mengurangi volume
    
    return pd.DataFrame(data)

def generate_kebijakan_pemerintah_data():
    """Generate data kebijakan pemerintah dummy"""
    print("📋 Generating Kebijakan Pemerintah data...")
    
    data = []
    id_counter = 1
    
    # Timeline kebijakan nasional dan regional
    kebijakan_timeline = [
        # 2020
        {'tanggal': '2020-03-15', 'jenis': 'Work From Home', 'tingkat': 6, 'nasional': True},
        {'tanggal': '2020-04-01', 'jenis': 'PSBB', 'tingkat': 8, 'nasional': False},
        {'tanggal': '2020-06-01', 'jenis': 'PSBB', 'tingkat': 6, 'nasional': False},
        {'tanggal': '2020-09-01', 'jenis': 'Sekolah Daring', 'tingkat': 7, 'nasional': True},
        
        # 2021
        {'tanggal': '2021-01-11', 'jenis': 'PPKM Level 4', 'tingkat': 9, 'nasional': False},
        {'tanggal': '2021-03-01', 'jenis': 'PPKM Level 3', 'tingkat': 7, 'nasional': False},
        {'tanggal': '2021-06-01', 'jenis': 'PPKM Level 4', 'tingkat': 9, 'nasional': False},
        {'tanggal': '2021-08-01', 'jenis': 'PPKM Level 3', 'tingkat': 7, 'nasional': False},
        {'tanggal': '2021-10-01', 'jenis': 'PPKM Level 2', 'tingkat': 5, 'nasional': False},
        
        # 2022
        {'tanggal': '2022-01-01', 'jenis': 'PPKM Level 2', 'tingkat': 4, 'nasional': False},
        {'tanggal': '2022-03-01', 'jenis': 'PPKM Level 1', 'tingkat': 3, 'nasional': False},
        {'tanggal': '2022-06-01', 'jenis': 'PPKM Level 1', 'tingkat': 2, 'nasional': False},
    ]
    
    for kebijakan in kebijakan_timeline:
        if kebijakan['nasional']:
            # Kebijakan nasional - berlaku untuk semua provinsi
            provinsi_list = list(PROVINSI_DATA.keys())
        else:
            # Kebijakan regional - hanya beberapa provinsi
            if 'PPKM Level 4' in kebijakan['jenis']:
                # PPKM Level 4 biasanya di daerah dengan kasus tinggi
                provinsi_list = ['ID-JK', 'ID-JB', 'ID-JI', 'ID-JT', 'ID-BT', 'ID-BA']
            elif 'PPKM Level 3' in kebijakan['jenis']:
                provinsi_list = ['ID-JK', 'ID-JB', 'ID-JI', 'ID-JT', 'ID-BT', 'ID-BA', 'ID-SU', 'ID-SN', 'ID-SS']
            elif 'PSBB' in kebijakan['jenis']:
                provinsi_list = ['ID-JK', 'ID-JB', 'ID-JI']
            else:
                # Pilih random beberapa provinsi
                provinsi_list = random.sample(list(PROVINSI_DATA.keys()), random.randint(5, 15))
        
        for iso_code in provinsi_list:
            tanggal_mulai = datetime.strptime(kebijakan['tanggal'], '%Y-%m-%d').date()
            
            # Durasi kebijakan (2 minggu - 3 bulan)
            durasi_hari = random.randint(14, 90)
            tanggal_selesai = tanggal_mulai + timedelta(days=durasi_hari)
            
            # Sektor yang terdampak berdasarkan jenis kebijakan
            if 'PPKM Level 4' in kebijakan['jenis'] or 'PSBB' in kebijakan['jenis']:
                sektor_pendidikan = True
                sektor_ekonomi = True
                sektor_transportasi = True
                sektor_pariwisata = True
                sektor_ibadah = True
            elif 'PPKM Level 3' in kebijakan['jenis']:
                sektor_pendidikan = True
                sektor_ekonomi = True
                sektor_transportasi = random.choice([True, False])
                sektor_pariwisata = True
                sektor_ibadah = random.choice([True, False])
            elif 'Work From Home' in kebijakan['jenis']:
                sektor_pendidikan = False
                sektor_ekonomi = True
                sektor_transportasi = False
                sektor_pariwisata = False
                sektor_ibadah = False
            else:
                sektor_pendidikan = random.choice([True, False])
                sektor_ekonomi = random.choice([True, False])
                sektor_transportasi = random.choice([True, False])
                sektor_pariwisata = random.choice([True, False])
                sektor_ibadah = random.choice([True, False])
            
            # Compliance rate dan dampak ekonomi
            compliance_rate = random.uniform(60, 90)  # 60-90%
            dampak_ekonomi_pct = kebijakan['tingkat'] * random.uniform(2, 5)  # 2-5% per tingkat keketatan
            
            data.append({
                'id_kebijakan': id_counter,
                'iso_code': iso_code,
                'tanggal_mulai': tanggal_mulai,
                'tanggal_selesai': tanggal_selesai,
                'jenis_kebijakan': kebijakan['jenis'],
                'nama_kebijakan': f"{kebijakan['jenis']} {PROVINSI_DATA[iso_code]}",
                'deskripsi_kebijakan': f"Implementasi {kebijakan['jenis']} di {PROVINSI_DATA[iso_code]} untuk mengendalikan penyebaran COVID-19",
                'tingkat_keketatan': kebijakan['tingkat'],
                'sektor_pendidikan': sektor_pendidikan,
                'sektor_ekonomi': sektor_ekonomi,
                'sektor_transportasi': sektor_transportasi,
                'sektor_pariwisata': sektor_pariwisata,
                'sektor_ibadah': sektor_ibadah,
                'compliance_rate': round(compliance_rate, 1),
                'dampak_ekonomi_pct': round(dampak_ekonomi_pct, 1),
                'status_kebijakan': 'Berakhir' if tanggal_selesai < date.today() else 'Aktif'
            })
            
            id_counter += 1
    
    return pd.DataFrame(data)

def generate_ekonomi_regional_data():
    """Generate data ekonomi regional dummy"""
    print("💰 Generating Ekonomi Regional data...")
    
    data = []
    id_counter = 1
    
    # Generate data untuk 2020-2022 (bulanan)
    for tahun in [2020, 2021, 2022]:
        bulan_range = range(1, 13) if tahun < 2022 else range(1, 10)  # 2022 sampai September
        
        for bulan in bulan_range:
            for iso_code, nama_provinsi in PROVINSI_DATA.items():
                # PDRB base berdasarkan ukuran provinsi (dalam triliun rupiah)
                pdrb_base = {
                    'ID-JK': 2500, 'ID-JB': 1800, 'ID-JI': 1600, 'ID-JT': 1200,
                    'ID-SU': 700, 'ID-RI': 600, 'ID-SN': 500, 'ID-BA': 300
                }.get(iso_code, 200)  # default 200 miliar
                
                # Dampak COVID-19 pada pertumbuhan ekonomi
                if tahun == 2020:
                    if bulan <= 3:  # Sebelum pandemi
                        pertumbuhan_base = random.uniform(4, 6)
                    else:  # Selama pandemi
                        pertumbuhan_base = random.uniform(-8, -2)
                elif tahun == 2021:
                    # Pemulihan bertahap
                    pertumbuhan_base = random.uniform(-2, 4)
                else:  # 2022
                    # Pemulihan lebih baik
                    pertumbuhan_base = random.uniform(2, 6)
                
                # PDRB dengan fluktuasi
                pdrb_milyar = pdrb_base * random.uniform(0.9, 1.1)
                pertumbuhan_ekonomi = pertumbuhan_base + random.uniform(-1, 1)
                
                # Inflasi
                inflasi_rate = random.uniform(1, 4) if tahun != 2020 else random.uniform(0.5, 3)
                
                # Ketenagakerjaan
                if tahun == 2020 and bulan > 3:
                    tingkat_pengangguran = random.uniform(6, 12)  # Meningkat saat pandemi
                else:
                    tingkat_pengangguran = random.uniform(3, 8)
                
                tingkat_partisipasi_kerja = random.uniform(60, 75)
                
                # UMR berdasarkan provinsi
                umr_base = {
                    'ID-JK': 4500000, 'ID-JB': 1800000, 'ID-JI': 1900000, 'ID-JT': 1700000,
                    'ID-BA': 2500000, 'ID-SU': 2000000
                }.get(iso_code, 1500000)
                
                upah_minimum_regional = int(umr_base * random.uniform(0.95, 1.05))
                
                # Sektor ekonomi (kontribusi PDRB dalam %)
                if iso_code in ['ID-JK', 'ID-JB', 'ID-JI']:  # Provinsi industri
                    sektor_pertanian = random.uniform(5, 15)
                    sektor_industri = random.uniform(30, 45)
                    sektor_perdagangan = random.uniform(20, 30)
                    sektor_jasa = random.uniform(15, 25)
                    sektor_pariwisata = random.uniform(3, 8)
                else:  # Provinsi agraris
                    sektor_pertanian = random.uniform(20, 40)
                    sektor_industri = random.uniform(10, 25)
                    sektor_perdagangan = random.uniform(15, 25)
                    sektor_jasa = random.uniform(10, 20)
                    sektor_pariwisata = random.uniform(5, 15)
                
                # Dampak COVID-19
                if tahun == 2020 and bulan > 3:
                    penurunan_omzet_umkm = random.uniform(30, 70)
                    penutupan_usaha = random.randint(100, 1000)
                    bantuan_sosial_milyar = random.uniform(50, 500)
                elif tahun == 2021:
                    penurunan_omzet_umkm = random.uniform(10, 40)
                    penutupan_usaha = random.randint(50, 300)
                    bantuan_sosial_milyar = random.uniform(20, 200)
                else:  # 2022
                    penurunan_omzet_umkm = random.uniform(0, 20)
                    penutupan_usaha = random.randint(10, 100)
                    bantuan_sosial_milyar = random.uniform(10, 100)
                
                # Recovery index (0-100)
                if tahun == 2020:
                    recovery_index = random.uniform(20, 50)
                elif tahun == 2021:
                    recovery_index = random.uniform(40, 70)
                else:  # 2022
                    recovery_index = random.uniform(60, 90)
                
                business_confidence = recovery_index + random.uniform(-10, 10)
                business_confidence = max(0, min(100, business_confidence))
                
                data.append({
                    'id_ekonomi': id_counter,
                    'iso_code': iso_code,
                    'tahun': tahun,
                    'bulan': bulan,
                    'pdrb_milyar': round(pdrb_milyar, 2),
                    'pertumbuhan_ekonomi': round(pertumbuhan_ekonomi, 2),
                    'inflasi_rate': round(inflasi_rate, 2),
                    'tingkat_pengangguran': round(tingkat_pengangguran, 2),
                    'tingkat_partisipasi_kerja': round(tingkat_partisipasi_kerja, 2),
                    'upah_minimum_regional': upah_minimum_regional,
                    'sektor_pertanian': round(sektor_pertanian, 2),
                    'sektor_industri': round(sektor_industri, 2),
                    'sektor_perdagangan': round(sektor_perdagangan, 2),
                    'sektor_jasa': round(sektor_jasa, 2),
                    'sektor_pariwisata': round(sektor_pariwisata, 2),
                    'penurunan_omzet_umkm': round(penurunan_omzet_umkm, 2),
                    'penutupan_usaha': penutupan_usaha,
                    'bantuan_sosial_milyar': round(bantuan_sosial_milyar, 2),
                    'recovery_index': round(recovery_index, 2),
                    'business_confidence': round(business_confidence, 2)
                })
                
                id_counter += 1
    
    return pd.DataFrame(data)

def generate_testing_labs_data():
    """Generate data laboratorium testing dummy"""
    print("🔬 Generating Testing Labs data...")
    
    data = []
    id_counter = 1
    
    for iso_code, nama_provinsi in PROVINSI_DATA.items():
        # Jumlah lab berdasarkan ukuran provinsi
        if iso_code in ['ID-JK', 'ID-JB', 'ID-JI', 'ID-JT']:  # Provinsi besar
            num_labs = random.randint(8, 15)
        elif iso_code in ['ID-SU', 'ID-SB', 'ID-SS', 'ID-BA', 'ID-SN']:  # Provinsi sedang
            num_labs = random.randint(4, 8)
        else:  # Provinsi kecil
            num_labs = random.randint(2, 5)
        
        for i in range(num_labs):
            # Jenis lab
            jenis_lab = np.random.choice(['PCR', 'Antigen', 'Antibodi', 'Kombinasi'], 
                                       p=[0.3, 0.4, 0.1, 0.2])
            
            # Tipe kepemilikan
            tipe_kepemilikan = np.random.choice(['Pemerintah', 'Swasta', 'Universitas', 'TNI/Polri'], 
                                              p=[0.4, 0.45, 0.1, 0.05])
            
            # Kapasitas berdasarkan jenis lab
            if jenis_lab == 'PCR':
                kapasitas_harian_pcr = random.randint(100, 1000)
                kapasitas_harian_antigen = random.randint(0, 200)
                kapasitas_harian_antibodi = random.randint(0, 100)
                mesin_pcr_count = random.randint(2, 10)
                turnaround_time_pcr = random.randint(6, 24)
            elif jenis_lab == 'Antigen':
                kapasitas_harian_pcr = 0
                kapasitas_harian_antigen = random.randint(200, 2000)
                kapasitas_harian_antibodi = random.randint(0, 100)
                mesin_pcr_count = 0
                turnaround_time_pcr = 24
            elif jenis_lab == 'Antibodi':
                kapasitas_harian_pcr = 0
                kapasitas_harian_antigen = 0
                kapasitas_harian_antibodi = random.randint(100, 500)
                mesin_pcr_count = 0
                turnaround_time_pcr = 24
            else:  # Kombinasi
                kapasitas_harian_pcr = random.randint(50, 500)
                kapasitas_harian_antigen = random.randint(100, 1000)
                kapasitas_harian_antibodi = random.randint(50, 300)
                mesin_pcr_count = random.randint(1, 5)
                turnaround_time_pcr = random.randint(8, 24)
            
            # Stok dan tenaga ahli
            extraction_kit_stock = random.randint(100, 5000)
            reagent_stock = random.randint(500, 10000)
            analis_count = random.randint(3, 20)
            teknisi_count = random.randint(2, 15)
            
            # Waktu pemrosesan
            turnaround_time_antigen = random.randint(1, 4)
            
            # Akreditasi
            akreditasi_kemenkes = random.choice([True, False])
            iso_certified = random.choice([True, False]) if tipe_kepemilikan == 'Swasta' else random.choice([True, False, False])
            
            # Koordinat dummy
            latitude = random.uniform(-11, 6)
            longitude = random.uniform(95, 141)
            
            # Fasilitas
            operational_24_hours = random.choice([True, False]) if tipe_kepemilikan in ['Pemerintah', 'Swasta'] else False
            drive_thru_available = random.choice([True, False])
            
            data.append({
                'id_lab': id_counter,
                'iso_code': iso_code,
                'nama_lab': f'Lab {jenis_lab} {nama_provinsi} {i+1}',
                'jenis_lab': jenis_lab,
                'tipe_kepemilikan': tipe_kepemilikan,
                'kapasitas_harian_pcr': kapasitas_harian_pcr,
                'kapasitas_harian_antigen': kapasitas_harian_antigen,
                'kapasitas_harian_antibodi': kapasitas_harian_antibodi,
                'mesin_pcr_count': mesin_pcr_count,
                'extraction_kit_stock': extraction_kit_stock,
                'reagent_stock': reagent_stock,
                'analis_count': analis_count,
                'teknisi_count': teknisi_count,
                'turnaround_time_pcr': turnaround_time_pcr,
                'turnaround_time_antigen': turnaround_time_antigen,
                'akreditasi_kemenkes': akreditasi_kemenkes,
                'iso_certified': iso_certified,
                'latitude': round(latitude, 6),
                'longitude': round(longitude, 6),
                'alamat': f'Jl. Laboratorium No. {random.randint(1, 100)}, {nama_provinsi}',
                'operational_24_hours': operational_24_hours,
                'drive_thru_available': drive_thru_available
            })
            
            id_counter += 1
    
    return pd.DataFrame(data)

def generate_cluster_penularan_data():
    """Generate data cluster penularan dummy"""
    print("🦠 Generating Cluster Penularan data...")
    
    data = []
    id_counter = 1
    
    # Generate cluster untuk periode Maret 2020 - September 2022
    start_date = date(2020, 3, 1)
    end_date = date(2022, 9, 15)
    
    # Jenis cluster dan probabilitas berdasarkan periode
    jenis_cluster_list = [
        'Perkantoran', 'Pabrik', 'Sekolah', 'Universitas', 'Pasar',
        'Mall', 'Rumah Sakit', 'Panti Jompo', 'Asrama', 'Pernikahan',
        'Keagamaan', 'Olahraga', 'Transportasi', 'Keluarga', 'Lainnya'
    ]
    
    for iso_code, nama_provinsi in PROVINSI_DATA.items():
        # Jumlah cluster berdasarkan ukuran provinsi dan periode
        if iso_code in ['ID-JK', 'ID-JB', 'ID-JI', 'ID-JT']:  # Provinsi besar
            num_clusters = random.randint(50, 100)
        elif iso_code in ['ID-SU', 'ID-SB', 'ID-SS', 'ID-BA', 'ID-SN']:  # Provinsi sedang
            num_clusters = random.randint(20, 50)
        else:  # Provinsi kecil
            num_clusters = random.randint(5, 20)
        
        for i in range(num_clusters):
            # Tanggal terdeteksi (random dalam periode)
            days_diff = (end_date - start_date).days
            random_days = random.randint(0, days_diff)
            tanggal_terdeteksi = start_date + timedelta(days=random_days)
            
            # Jenis cluster berdasarkan periode
            if tanggal_terdeteksi < date(2020, 6, 1):  # Awal pandemi
                jenis_cluster = np.random.choice(['Perkantoran', 'Pasar', 'Rumah Sakit', 'Keluarga', 'Lainnya'])
            elif tanggal_terdeteksi < date(2021, 1, 1):  # Pertengahan 2020
                jenis_cluster = np.random.choice(['Pabrik', 'Perkantoran', 'Keluarga', 'Pernikahan', 'Keagamaan'])
            elif tanggal_terdeteksi < date(2021, 8, 1):  # Awal 2021
                jenis_cluster = np.random.choice(['Perkantoran', 'Pabrik', 'Keluarga', 'Mall', 'Transportasi'])
            else:  # Akhir periode
                jenis_cluster = np.random.choice(['Sekolah', 'Universitas', 'Perkantoran', 'Keluarga', 'Olahraga'])
            
            # Durasi cluster (1-8 minggu)
            durasi_hari = random.randint(7, 56)
            tanggal_selesai = tanggal_terdeteksi + timedelta(days=durasi_hari)
            
            # Ukuran cluster berdasarkan jenis
            if jenis_cluster in ['Pabrik', 'Perkantoran', 'Sekolah', 'Universitas']:
                total_kasus_terkait = random.randint(10, 100)
            elif jenis_cluster in ['Pernikahan', 'Keagamaan', 'Olahraga']:
                total_kasus_terkait = random.randint(20, 200)
            elif jenis_cluster in ['Rumah Sakit', 'Panti Jompo']:
                total_kasus_terkait = random.randint(5, 50)
            else:  # Keluarga, dll
                total_kasus_terkait = random.randint(3, 30)
            
            total_kontak_erat = int(total_kasus_terkait * random.uniform(2, 5))
            total_suspect = int(total_kontak_erat * random.uniform(0.1, 0.3))
            
            # Demografi terdampak
            if jenis_cluster in ['Sekolah', 'Universitas']:
                kasus_anak = int(total_kasus_terkait * random.uniform(0.3, 0.7))
                kasus_dewasa = int(total_kasus_terkait * random.uniform(0.2, 0.5))
                kasus_lansia = int(total_kasus_terkait * random.uniform(0.0, 0.1))
            elif jenis_cluster == 'Panti Jompo':
                kasus_anak = 0
                kasus_dewasa = int(total_kasus_terkait * random.uniform(0.2, 0.4))
                kasus_lansia = int(total_kasus_terkait * random.uniform(0.6, 0.8))
            else:  # Umum
                kasus_anak = int(total_kasus_terkait * random.uniform(0.1, 0.3))
                kasus_dewasa = int(total_kasus_terkait * random.uniform(0.5, 0.7))
                kasus_lansia = int(total_kasus_terkait * random.uniform(0.1, 0.2))
            
            # Gender
            kasus_laki = int(total_kasus_terkait * random.uniform(0.4, 0.6))
            kasus_perempuan = total_kasus_terkait - kasus_laki
            
            # Tingkat keparahan
            kasus_tanpa_gejala = int(total_kasus_terkait * random.uniform(0.2, 0.4))
            kasus_ringan = int(total_kasus_terkait * random.uniform(0.4, 0.6))
            kasus_sedang = int(total_kasus_terkait * random.uniform(0.1, 0.2))
            kasus_berat = int(total_kasus_terkait * random.uniform(0.02, 0.08))
            kasus_kritis = int(total_kasus_terkait * random.uniform(0.01, 0.03))
            kasus_meninggal = int(total_kasus_terkait * random.uniform(0.005, 0.02))
            
            # Tindakan pengendalian
            contact_tracing_completed = random.choice([True, False])
            area_disinfection = random.choice([True, True, False])  # Lebih sering True
            temporary_closure = random.choice([True, False]) if jenis_cluster in ['Perkantoran', 'Sekolah', 'Mall'] else False
            mass_testing = random.choice([True, False])
            
            # Status cluster
            if tanggal_selesai < date.today():
                status_cluster = np.random.choice(['Terkendali', 'Selesai'], p=[0.3, 0.7])
            else:
                status_cluster = 'Aktif'
            
            # Koordinat dummy
            latitude = random.uniform(-11, 6)
            longitude = random.uniform(95, 141)
            
            data.append({
                'id_cluster': id_counter,
                'iso_code': iso_code,
                'tanggal_terdeteksi': tanggal_terdeteksi,
                'tanggal_selesai': tanggal_selesai if status_cluster != 'Aktif' else None,
                'nama_cluster': f'Cluster {jenis_cluster} {nama_provinsi} {i+1}',
                'jenis_cluster': jenis_cluster,
                'nama_lokasi': f'Lokasi {jenis_cluster} {nama_provinsi}',
                'alamat_lokasi': f'Jl. {jenis_cluster} No. {random.randint(1, 100)}, {nama_provinsi}',
                'latitude': round(latitude, 6),
                'longitude': round(longitude, 6),
                'kasus_index': 1,
                'total_kasus_terkait': total_kasus_terkait,
                'total_kontak_erat': total_kontak_erat,
                'total_suspect': total_suspect,
                'kasus_anak': kasus_anak,
                'kasus_dewasa': kasus_dewasa,
                'kasus_lansia': kasus_lansia,
                'kasus_laki': kasus_laki,
                'kasus_perempuan': kasus_perempuan,
                'kasus_tanpa_gejala': kasus_tanpa_gejala,
                'kasus_ringan': kasus_ringan,
                'kasus_sedang': kasus_sedang,
                'kasus_berat': kasus_berat,
                'kasus_kritis': kasus_kritis,
                'kasus_meninggal': kasus_meninggal,
                'contact_tracing_completed': contact_tracing_completed,
                'area_disinfection': area_disinfection,
                'temporary_closure': temporary_closure,
                'mass_testing': mass_testing,
                'status_cluster': status_cluster,
                'catatan': f'Cluster {jenis_cluster} terdeteksi di {nama_provinsi} dengan {total_kasus_terkait} kasus terkait'
            })
            
            id_counter += 1
    
    return pd.DataFrame(data)

def generate_mobilitas_harian_data():
    """Generate data mobilitas harian dummy"""
    print("🚶 Generating Mobilitas Harian data...")
    
    data = []
    id_counter = 1
    
    # Generate data untuk periode Maret 2020 - September 2022 (mingguan untuk mengurangi volume)
    start_date = date(2020, 3, 1)
    end_date = date(2022, 9, 15)
    current_date = start_date
    
    while current_date <= end_date:
        for iso_code, nama_provinsi in PROVINSI_DATA.items():
            # Baseline mobilitas (0% = normal, negatif = berkurang, positif = meningkat)
            
            # Faktor periode (dampak kebijakan)
            if current_date < date(2020, 6, 1):  # Lockdown awal
                mobility_factor = random.uniform(-80, -40)
            elif current_date < date(2020, 12, 1):  # PSBB
                mobility_factor = random.uniform(-60, -20)
            elif current_date < date(2021, 6, 1):  # PPKM awal
                mobility_factor = random.uniform(-40, -10)
            elif current_date < date(2021, 12, 1):  # PPKM ketat
                mobility_factor = random.uniform(-50, -15)
            else:  # Pemulihan
                mobility_factor = random.uniform(-20, 10)
            
            # Mobilitas berdasarkan lokasi
            retail_recreation = mobility_factor + random.uniform(-20, 20)
            grocery_pharmacy = mobility_factor * 0.5 + random.uniform(-10, 10)  # Lebih stabil
            parks = mobility_factor + random.uniform(-30, 30)
            transit_stations = mobility_factor * 1.2 + random.uniform(-15, 15)
            workplaces = mobility_factor * 0.8 + random.uniform(-15, 15)
            residential = -mobility_factor * 0.3 + random.uniform(-5, 5)  # Berlawanan dengan mobilitas luar
            
            # Mobilitas berdasarkan transportasi
            private_vehicle_movement = mobility_factor * 0.7 + random.uniform(-10, 10)
            public_transport_usage = mobility_factor * 1.5 + random.uniform(-20, 20)  # Lebih terpengaruh
            walking_cycling = mobility_factor * 0.5 + random.uniform(-15, 15)
            
            # Mobilitas berdasarkan waktu
            morning_rush_hour = mobility_factor * 0.9 + random.uniform(-10, 10)
            afternoon_activity = mobility_factor * 0.8 + random.uniform(-15, 15)
            evening_rush_hour = mobility_factor * 0.9 + random.uniform(-10, 10)
            night_activity = mobility_factor * 1.2 + random.uniform(-20, 20)
            
            # Indeks mobilitas gabungan
            overall_mobility_index = (retail_recreation + transit_stations + workplaces) / 3
            
            data.append({
                'id_mobilitas': id_counter,
                'iso_code': iso_code,
                'tanggal': current_date,
                'retail_recreation': round(retail_recreation, 1),
                'grocery_pharmacy': round(grocery_pharmacy, 1),
                'parks': round(parks, 1),
                'transit_stations': round(transit_stations, 1),
                'workplaces': round(workplaces, 1),
                'residential': round(residential, 1),
                'private_vehicle_movement': round(private_vehicle_movement, 1),
                'public_transport_usage': round(public_transport_usage, 1),
                'walking_cycling': round(walking_cycling, 1),
                'morning_rush_hour': round(morning_rush_hour, 1),
                'afternoon_activity': round(afternoon_activity, 1),
                'evening_rush_hour': round(evening_rush_hour, 1),
                'night_activity': round(night_activity, 1),
                'overall_mobility_index': round(overall_mobility_index, 1)
            })
            
            id_counter += 1
        
        current_date += timedelta(days=7)  # Data mingguan
    
    return pd.DataFrame(data)

def main():
    """Main function untuk generate semua data dummy"""
    print("🚀 Starting Enhanced COVID-19 Dummy Data Generation")
    print("=" * 60)
    
    # Create output directory
    os.makedirs('dummy_data', exist_ok=True)
    
    # Generate semua tabel
    datasets = {}
    
    print("\n📊 Generating all dummy datasets...")
    
    datasets['rumah_sakit'] = generate_rumah_sakit_data()
    datasets['vaksinasi_detail'] = generate_vaksinasi_detail_data()
    datasets['kebijakan_pemerintah'] = generate_kebijakan_pemerintah_data()
    datasets['ekonomi_regional'] = generate_ekonomi_regional_data()
    datasets['testing_labs'] = generate_testing_labs_data()
    datasets['cluster_penularan'] = generate_cluster_penularan_data()
    datasets['mobilitas_harian'] = generate_mobilitas_harian_data()
    
    # Save to CSV files
    print("\n💾 Saving datasets to CSV files...")
    
    for table_name, df in datasets.items():
        filename = f'dummy_data/{table_name}.csv'
        df.to_csv(filename, index=False)
        print(f"✅ {filename} - {len(df):,} records")
    
    # Generate summary report
    print("\n📋 SUMMARY REPORT")
    print("=" * 40)
    
    total_records = 0
    for table_name, df in datasets.items():
        record_count = len(df)
        total_records += record_count
        print(f"{table_name:20}: {record_count:,} records")
    
    print(f"{'TOTAL':20}: {total_records:,} records")
    
    # Generate metadata
    metadata = {
        'generation_date': datetime.now().isoformat(),
        'total_tables': len(datasets),
        'total_records': total_records,
        'provinsi_count': len(PROVINSI_DATA),
        'date_range': {
            'start': '2020-03-01',
            'end': '2022-09-15'
        },
        'tables': {
            table_name: {
                'records': len(df),
                'columns': list(df.columns),
                'file': f'{table_name}.csv'
            }
            for table_name, df in datasets.items()
        }
    }
    
    with open('dummy_data/metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n🎉 Data generation completed!")
    print(f"📁 Files saved in: dummy_data/")
    print(f"📄 Metadata saved in: dummy_data/metadata.json")
    
    return datasets

if __name__ == "__main__":
    datasets = main()
