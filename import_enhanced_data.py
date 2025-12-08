#!/usr/bin/env python3
"""
Script untuk import data dummy tabel-tabel baru ke database PostgreSQL
COVID-19 Indonesia Enhanced Database
"""

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import os
import sys
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'covid19_indonesia',
    'user': 'postgres',
    'password': '1234'  # Ganti dengan password PostgreSQL Anda
}

def connect_to_db():
    """Connect to PostgreSQL database"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        return None

def import_rumah_sakit_data(conn, csv_file):
    """Import data rumah sakit"""
    logger.info("📥 Importing Rumah Sakit data...")
    
    try:
        df = pd.read_csv(csv_file)
        logger.info(f"Loaded {len(df)} records from {csv_file}")
        
        cursor = conn.cursor()
        
        # Clear existing data
        cursor.execute("DELETE FROM RUMAH_SAKIT")
        logger.info("Cleared existing Rumah Sakit data")
        
        # Prepare data for insertion
        records = []
        for _, row in df.iterrows():
            record = (
                row['iso_code'],
                row['nama_rumah_sakit'],
                row['tipe_rumah_sakit'],
                row['kelas_rumah_sakit'],
                int(row['total_bed']),
                int(row['icu_bed']),
                int(row['isolation_bed']),
                int(row['emergency_bed']),
                int(row['ventilator_count']),
                int(row['oxygen_capacity']),
                bool(row['ct_scan_available']),
                bool(row['pcr_lab_available']),
                int(row['doctor_count']),
                int(row['nurse_count']),
                int(row['specialist_count']),
                float(row['latitude']),
                float(row['longitude']),
                row['alamat'],
                bool(row['covid_referral']),
                row['operational_status']
            )
            records.append(record)
        
        # Insert data
        insert_query = """
            INSERT INTO RUMAH_SAKIT (
                iso_code, nama_rumah_sakit, tipe_rumah_sakit, kelas_rumah_sakit,
                total_bed, icu_bed, isolation_bed, emergency_bed,
                ventilator_count, oxygen_capacity, ct_scan_available, pcr_lab_available,
                doctor_count, nurse_count, specialist_count,
                latitude, longitude, alamat, covid_referral, operational_status
            ) VALUES %s
        """
        
        execute_values(cursor, insert_query, records)
        conn.commit()
        
        logger.info(f"✅ Successfully imported {len(records)} Rumah Sakit records")
        
    except Exception as e:
        logger.error(f"❌ Error importing Rumah Sakit data: {e}")
        conn.rollback()

def import_vaksinasi_detail_data(conn, csv_file):
    """Import data vaksinasi detail"""
    logger.info("📥 Importing Vaksinasi Detail data...")
    
    try:
        df = pd.read_csv(csv_file)
        df['tanggal'] = pd.to_datetime(df['tanggal']).dt.date
        logger.info(f"Loaded {len(df)} records from {csv_file}")
        
        cursor = conn.cursor()
        
        # Clear existing data
        cursor.execute("DELETE FROM VAKSINASI_DETAIL")
        logger.info("Cleared existing Vaksinasi Detail data")
        
        # Prepare data for insertion
        records = []
        for _, row in df.iterrows():
            record = (
                row['iso_code'],
                row['tanggal'],
                int(row['vaksin_sinovac']),
                int(row['vaksin_astrazeneca']),
                int(row['vaksin_pfizer']),
                int(row['vaksin_moderna']),
                int(row['vaksin_novavax']),
                int(row['vaksin_lainnya']),
                int(row['dosis_1']),
                int(row['dosis_2']),
                int(row['dosis_booster']),
                int(row['lansia_vaksin']),
                int(row['dewasa_vaksin']),
                int(row['remaja_vaksin']),
                int(row['anak_vaksin']),
                int(row['nakes_vaksin']),
                int(row['guru_vaksin']),
                int(row['petugas_publik_vaksin']),
                int(row['puskesmas_vaksin']),
                int(row['rumah_sakit_vaksin']),
                int(row['sentra_vaksin']),
                int(row['drive_thru_vaksin']),
                int(row['kipi_ringan']),
                int(row['kipi_sedang']),
                int(row['kipi_berat'])
            )
            records.append(record)
        
        # Insert data in batches
        insert_query = """
            INSERT INTO VAKSINASI_DETAIL (
                iso_code, tanggal, vaksin_sinovac, vaksin_astrazeneca, vaksin_pfizer,
                vaksin_moderna, vaksin_novavax, vaksin_lainnya,
                dosis_1, dosis_2, dosis_booster,
                lansia_vaksin, dewasa_vaksin, remaja_vaksin, anak_vaksin,
                nakes_vaksin, guru_vaksin, petugas_publik_vaksin,
                puskesmas_vaksin, rumah_sakit_vaksin, sentra_vaksin, drive_thru_vaksin,
                kipi_ringan, kipi_sedang, kipi_berat
            ) VALUES %s
        """
        
        batch_size = 1000
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            execute_values(cursor, insert_query, batch)
            conn.commit()
            logger.info(f"Imported batch {i//batch_size + 1}/{(len(records)//batch_size) + 1}")
        
        logger.info(f"✅ Successfully imported {len(records)} Vaksinasi Detail records")
        
    except Exception as e:
        logger.error(f"❌ Error importing Vaksinasi Detail data: {e}")
        conn.rollback()

def import_kebijakan_pemerintah_data(conn, csv_file):
    """Import data kebijakan pemerintah"""
    logger.info("📥 Importing Kebijakan Pemerintah data...")
    
    try:
        df = pd.read_csv(csv_file)
        df['tanggal_mulai'] = pd.to_datetime(df['tanggal_mulai']).dt.date
        df['tanggal_selesai'] = pd.to_datetime(df['tanggal_selesai']).dt.date
        logger.info(f"Loaded {len(df)} records from {csv_file}")
        
        cursor = conn.cursor()
        
        # Clear existing data
        cursor.execute("DELETE FROM KEBIJAKAN_PEMERINTAH")
        logger.info("Cleared existing Kebijakan Pemerintah data")
        
        # Prepare data for insertion
        records = []
        for _, row in df.iterrows():
            record = (
                row['iso_code'],
                row['tanggal_mulai'],
                row['tanggal_selesai'],
                row['jenis_kebijakan'],
                row['nama_kebijakan'],
                row['deskripsi_kebijakan'],
                int(row['tingkat_keketatan']),
                bool(row['sektor_pendidikan']),
                bool(row['sektor_ekonomi']),
                bool(row['sektor_transportasi']),
                bool(row['sektor_pariwisata']),
                bool(row['sektor_ibadah']),
                float(row['compliance_rate']),
                float(row['dampak_ekonomi_pct']),
                row['status_kebijakan']
            )
            records.append(record)
        
        # Insert data
        insert_query = """
            INSERT INTO KEBIJAKAN_PEMERINTAH (
                iso_code, tanggal_mulai, tanggal_selesai, jenis_kebijakan,
                nama_kebijakan, deskripsi_kebijakan, tingkat_keketatan,
                sektor_pendidikan, sektor_ekonomi, sektor_transportasi,
                sektor_pariwisata, sektor_ibadah, compliance_rate,
                dampak_ekonomi_pct, status_kebijakan
            ) VALUES %s
        """
        
        execute_values(cursor, insert_query, records)
        conn.commit()
        
        logger.info(f"✅ Successfully imported {len(records)} Kebijakan Pemerintah records")
        
    except Exception as e:
        logger.error(f"❌ Error importing Kebijakan Pemerintah data: {e}")
        conn.rollback()

def import_ekonomi_regional_data(conn, csv_file):
    """Import data ekonomi regional"""
    logger.info("📥 Importing Ekonomi Regional data...")
    
    try:
        df = pd.read_csv(csv_file)
        logger.info(f"Loaded {len(df)} records from {csv_file}")
        
        cursor = conn.cursor()
        
        # Clear existing data
        cursor.execute("DELETE FROM EKONOMI_REGIONAL")
        logger.info("Cleared existing Ekonomi Regional data")
        
        # Prepare data for insertion
        records = []
        for _, row in df.iterrows():
            record = (
                row['iso_code'],
                int(row['tahun']),
                int(row['bulan']),
                float(row['pdrb_milyar']),
                float(row['pertumbuhan_ekonomi']),
                float(row['inflasi_rate']),
                float(row['tingkat_pengangguran']),
                float(row['tingkat_partisipasi_kerja']),
                int(row['upah_minimum_regional']),
                float(row['sektor_pertanian']),
                float(row['sektor_industri']),
                float(row['sektor_perdagangan']),
                float(row['sektor_jasa']),
                float(row['sektor_pariwisata']),
                float(row['penurunan_omzet_umkm']),
                int(row['penutupan_usaha']),
                float(row['bantuan_sosial_milyar']),
                float(row['recovery_index']),
                float(row['business_confidence'])
            )
            records.append(record)
        
        # Insert data in batches
        insert_query = """
            INSERT INTO EKONOMI_REGIONAL (
                iso_code, tahun, bulan, pdrb_milyar, pertumbuhan_ekonomi, inflasi_rate,
                tingkat_pengangguran, tingkat_partisipasi_kerja, upah_minimum_regional,
                sektor_pertanian, sektor_industri, sektor_perdagangan,
                sektor_jasa, sektor_pariwisata, penurunan_omzet_umkm,
                penutupan_usaha, bantuan_sosial_milyar, recovery_index, business_confidence
            ) VALUES %s
        """
        
        batch_size = 1000
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            execute_values(cursor, insert_query, batch)
            conn.commit()
            logger.info(f"Imported batch {i//batch_size + 1}/{(len(records)//batch_size) + 1}")
        
        logger.info(f"✅ Successfully imported {len(records)} Ekonomi Regional records")
        
    except Exception as e:
        logger.error(f"❌ Error importing Ekonomi Regional data: {e}")
        conn.rollback()

def import_testing_labs_data(conn, csv_file):
    """Import data testing labs"""
    logger.info("📥 Importing Testing Labs data...")
    
    try:
        df = pd.read_csv(csv_file)
        logger.info(f"Loaded {len(df)} records from {csv_file}")
        
        cursor = conn.cursor()
        
        # Clear existing data
        cursor.execute("DELETE FROM TESTING_LABS")
        logger.info("Cleared existing Testing Labs data")
        
        # Prepare data for insertion
        records = []
        for _, row in df.iterrows():
            record = (
                row['iso_code'],
                row['nama_lab'],
                row['jenis_lab'],
                row['tipe_kepemilikan'],
                int(row['kapasitas_harian_pcr']),
                int(row['kapasitas_harian_antigen']),
                int(row['kapasitas_harian_antibodi']),
                int(row['mesin_pcr_count']),
                int(row['extraction_kit_stock']),
                int(row['reagent_stock']),
                int(row['analis_count']),
                int(row['teknisi_count']),
                int(row['turnaround_time_pcr']),
                int(row['turnaround_time_antigen']),
                bool(row['akreditasi_kemenkes']),
                bool(row['iso_certified']),
                float(row['latitude']),
                float(row['longitude']),
                row['alamat'],
                bool(row['operational_24_hours']),
                bool(row['drive_thru_available'])
            )
            records.append(record)
        
        # Insert data
        insert_query = """
            INSERT INTO TESTING_LABS (
                iso_code, nama_lab, jenis_lab, tipe_kepemilikan,
                kapasitas_harian_pcr, kapasitas_harian_antigen, kapasitas_harian_antibodi,
                mesin_pcr_count, extraction_kit_stock, reagent_stock,
                analis_count, teknisi_count, turnaround_time_pcr, turnaround_time_antigen,
                akreditasi_kemenkes, iso_certified, latitude, longitude, alamat,
                operational_24_hours, drive_thru_available
            ) VALUES %s
        """
        
        execute_values(cursor, insert_query, records)
        conn.commit()
        
        logger.info(f"✅ Successfully imported {len(records)} Testing Labs records")
        
    except Exception as e:
        logger.error(f"❌ Error importing Testing Labs data: {e}")
        conn.rollback()

def import_cluster_penularan_data(conn, csv_file):
    """Import data cluster penularan"""
    logger.info("📥 Importing Cluster Penularan data...")
    
    try:
        df = pd.read_csv(csv_file)
        df['tanggal_terdeteksi'] = pd.to_datetime(df['tanggal_terdeteksi']).dt.date
        df['tanggal_selesai'] = pd.to_datetime(df['tanggal_selesai'], errors='coerce').dt.date
        logger.info(f"Loaded {len(df)} records from {csv_file}")
        
        cursor = conn.cursor()
        
        # Clear existing data
        cursor.execute("DELETE FROM CLUSTER_PENULARAN")
        logger.info("Cleared existing Cluster Penularan data")
        
        # Prepare data for insertion
        records = []
        for _, row in df.iterrows():
            record = (
                row['iso_code'],
                row['tanggal_terdeteksi'],
                row['tanggal_selesai'] if pd.notna(row['tanggal_selesai']) else None,
                row['nama_cluster'],
                row['jenis_cluster'],
                row['nama_lokasi'],
                row['alamat_lokasi'],
                float(row['latitude']),
                float(row['longitude']),
                int(row['kasus_index']),
                int(row['total_kasus_terkait']),
                int(row['total_kontak_erat']),
                int(row['total_suspect']),
                int(row['kasus_anak']),
                int(row['kasus_dewasa']),
                int(row['kasus_lansia']),
                int(row['kasus_laki']),
                int(row['kasus_perempuan']),
                int(row['kasus_tanpa_gejala']),
                int(row['kasus_ringan']),
                int(row['kasus_sedang']),
                int(row['kasus_berat']),
                int(row['kasus_kritis']),
                int(row['kasus_meninggal']),
                bool(row['contact_tracing_completed']),
                bool(row['area_disinfection']),
                bool(row['temporary_closure']),
                bool(row['mass_testing']),
                row['status_cluster'],
                row['catatan']
            )
            records.append(record)
        
        # Insert data in batches
        insert_query = """
            INSERT INTO CLUSTER_PENULARAN (
                iso_code, tanggal_terdeteksi, tanggal_selesai, nama_cluster, jenis_cluster,
                nama_lokasi, alamat_lokasi, latitude, longitude,
                kasus_index, total_kasus_terkait, total_kontak_erat, total_suspect,
                kasus_anak, kasus_dewasa, kasus_lansia, kasus_laki, kasus_perempuan,
                kasus_tanpa_gejala, kasus_ringan, kasus_sedang, kasus_berat,
                kasus_kritis, kasus_meninggal, contact_tracing_completed,
                area_disinfection, temporary_closure, mass_testing,
                status_cluster, catatan
            ) VALUES %s
        """
        
        batch_size = 1000
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            execute_values(cursor, insert_query, batch)
            conn.commit()
            logger.info(f"Imported batch {i//batch_size + 1}/{(len(records)//batch_size) + 1}")
        
        logger.info(f"✅ Successfully imported {len(records)} Cluster Penularan records")
        
    except Exception as e:
        logger.error(f"❌ Error importing Cluster Penularan data: {e}")
        conn.rollback()

def import_mobilitas_harian_data(conn, csv_file):
    """Import data mobilitas harian"""
    logger.info("📥 Importing Mobilitas Harian data...")
    
    try:
        df = pd.read_csv(csv_file)
        df['tanggal'] = pd.to_datetime(df['tanggal']).dt.date
        logger.info(f"Loaded {len(df)} records from {csv_file}")
        
        cursor = conn.cursor()
        
        # Clear existing data
        cursor.execute("DELETE FROM MOBILITAS_HARIAN")
        logger.info("Cleared existing Mobilitas Harian data")
        
        # Prepare data for insertion
        records = []
        for _, row in df.iterrows():
            record = (
                row['iso_code'],
                row['tanggal'],
                float(row['retail_recreation']),
                float(row['grocery_pharmacy']),
                float(row['parks']),
                float(row['transit_stations']),
                float(row['workplaces']),
                float(row['residential']),
                float(row['private_vehicle_movement']),
                float(row['public_transport_usage']),
                float(row['walking_cycling']),
                float(row['morning_rush_hour']),
                float(row['afternoon_activity']),
                float(row['evening_rush_hour']),
                float(row['night_activity']),
                float(row['overall_mobility_index'])
            )
            records.append(record)
        
        # Insert data in batches
        insert_query = """
            INSERT INTO MOBILITAS_HARIAN (
                iso_code, tanggal, retail_recreation, grocery_pharmacy, parks,
                transit_stations, workplaces, residential,
                private_vehicle_movement, public_transport_usage, walking_cycling,
                morning_rush_hour, afternoon_activity, evening_rush_hour,
                night_activity, overall_mobility_index
            ) VALUES %s
        """
        
        batch_size = 1000
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            execute_values(cursor, insert_query, batch)
            conn.commit()
            logger.info(f"Imported batch {i//batch_size + 1}/{(len(records)//batch_size) + 1}")
        
        logger.info(f"✅ Successfully imported {len(records)} Mobilitas Harian records")
        
    except Exception as e:
        logger.error(f"❌ Error importing Mobilitas Harian data: {e}")
        conn.rollback()

def main():
    """Main function untuk import semua data"""
    logger.info("🚀 Starting Enhanced COVID-19 Data Import")
    logger.info("=" * 60)
    
    # Check if dummy_data directory exists
    if not os.path.exists('dummy_data'):
        logger.error("❌ dummy_data directory not found!")
        logger.info("💡 Please run generate_enhanced_dummy_data.py first")
        return
    
    # Connect to database
    conn = connect_to_db()
    if not conn:
        logger.error("❌ Failed to connect to database")
        return
    
    try:
        # Import all tables
        import_functions = {
            'rumah_sakit.csv': import_rumah_sakit_data,
            'vaksinasi_detail.csv': import_vaksinasi_detail_data,
            'kebijakan_pemerintah.csv': import_kebijakan_pemerintah_data,
            'ekonomi_regional.csv': import_ekonomi_regional_data,
            'testing_labs.csv': import_testing_labs_data,
            'cluster_penularan.csv': import_cluster_penularan_data,
            'mobilitas_harian.csv': import_mobilitas_harian_data
        }
        
        total_imported = 0
        
        for csv_file, import_func in import_functions.items():
            csv_path = f'dummy_data/{csv_file}'
            
            if os.path.exists(csv_path):
                import_func(conn, csv_path)
                
                # Count imported records
                table_name = csv_file.replace('.csv', '').upper()
                cursor = conn.cursor()
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                total_imported += count
                
            else:
                logger.warning(f"⚠️  File not found: {csv_path}")
        
        # Show final summary
        logger.info("\n" + "=" * 60)
        logger.info("📊 IMPORT SUMMARY")
        logger.info("=" * 60)
        
        cursor = conn.cursor()
        
        # Get record counts for all tables
        tables = [
            'RUMAH_SAKIT', 'VAKSINASI_DETAIL', 'KEBIJAKAN_PEMERINTAH',
            'EKONOMI_REGIONAL', 'TESTING_LABS', 'CLUSTER_PENULARAN', 'MOBILITAS_HARIAN'
        ]
        
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                logger.info(f"{table:20}: {count:,} records")
            except:
                logger.info(f"{table:20}: Table not found")
        
        logger.info(f"{'TOTAL IMPORTED':20}: {total_imported:,} records")
        
        logger.info("\n🎉 Enhanced data import completed successfully!")
        logger.info("🔍 You can now run queries on the new tables for visualization")
        
    except Exception as e:
        logger.error(f"❌ Error during import: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    main()




