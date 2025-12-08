"""
Supabase Data Import Script for COVID-19 Indonesia Dashboard
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')

# Import Supabase configuration (standalone version)
from supabase_config_standalone import supabase_config, get_db_connection

def validate_environment():
    """Validate environment configuration"""
    print("Validating Supabase configuration...")
    
    if not supabase_config.validate_config():
        print("ERROR: Configuration validation failed!")
        print("Please check your .env file and ensure all required fields are filled.")
        return False
    
    # Test connection
    success, message = supabase_config.test_connection()
    if not success:
        print(f"ERROR: Connection test failed: {message}")
        return False
    
    print("SUCCESS: Configuration and connection validated successfully!")
    return True

def check_file_exists(filename):
    """Check if required data file exists"""
    if not os.path.exists(filename):
        print(f"ERROR: File not found: {filename}")
        return False
    print(f"SUCCESS: Found file: {filename}")
    return True

def import_lokasi_data():
    """Import location data"""
    print("\nImporting LOKASI data...")
    
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        # Read the enhanced CSV file
        df = pd.read_csv('covid_19_indonesia_enhanced.csv')
        
        # Strip whitespace from column names and data
        df.columns = df.columns.str.strip()
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        
        # Map column names from CSV to database columns
        column_mapping = {
            'Location ISO Code': 'iso_code',
            'Province': 'nama_provinsi', 
            'Population': 'populasi',
            'Area (km2)': 'luas_wilayah',
            'Latitude': 'latitude',
            'Longitude': 'longitude',
            'Island': 'island',
            'Population Density': 'population_density'
        }
        
        # Rename columns
        df_renamed = df.rename(columns=column_mapping)
        
        # Get unique locations with renamed columns
        lokasi_data = df_renamed[['iso_code', 'nama_provinsi', 'populasi', 'luas_wilayah', 
                                 'latitude', 'longitude', 'island', 'population_density']].drop_duplicates()
        
        # Add additional location fields with default values
        lokasi_data['area_km2'] = lokasi_data['luas_wilayah']
        
        # Use existing data from CSV if available, otherwise use random
        if 'Total Regencies' in df.columns:
            lokasi_data['total_regencies'] = df_renamed.groupby('iso_code')['Total Regencies'].first()
        else:
            lokasi_data['total_regencies'] = np.random.randint(5, 30, len(lokasi_data))
            
        if 'Total Cities' in df.columns:
            lokasi_data['total_cities'] = df_renamed.groupby('iso_code')['Total Cities'].first()
        else:
            lokasi_data['total_cities'] = np.random.randint(1, 10, len(lokasi_data))
            
        # Fill other fields
        lokasi_data['total_districts'] = np.random.randint(50, 500, len(lokasi_data))
        lokasi_data['total_urban_villages'] = np.random.randint(100, 1000, len(lokasi_data))
        lokasi_data['total_rural_villages'] = np.random.randint(200, 2000, len(lokasi_data))
        lokasi_data['time_zone'] = 'WIB'  # Default timezone
        lokasi_data['special_status'] = None
        
        # Clean data
        lokasi_data = lokasi_data.fillna(0)
        
        # Insert data
        cursor = conn.cursor()
        
        # Clear existing data
        cursor.execute("DELETE FROM LOKASI")
        
        insert_query = """
        INSERT INTO LOKASI (
            iso_code, nama_provinsi, populasi, luas_wilayah, latitude, longitude,
            island, population_density, area_km2, total_regencies, total_cities,
            total_districts, total_urban_villages, total_rural_villages, time_zone, special_status
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        for _, row in tqdm(lokasi_data.iterrows(), total=len(lokasi_data), desc="Importing locations"):
            cursor.execute(insert_query, tuple(row))
        
        conn.commit()
        print(f"SUCCESS: Successfully imported {len(lokasi_data)} location records")
        return True
        
    except Exception as e:
        print(f"ERROR: Error importing LOKASI data: {e}")
        conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

def import_statistik_harian_data():
    """Import daily statistics data"""
    print("\nImporting STATISTIK_HARIAN data...")
    
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        # Read the enhanced CSV file
        df = pd.read_csv('covid_19_indonesia_enhanced.csv')
        
        # Strip whitespace from column names and data
        df.columns = df.columns.str.strip()
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        
        # Map column names from CSV to database columns
        column_mapping = {
            'Date': 'tanggal',
            'Location ISO Code': 'iso_code',
            'New Cases': 'kasus_baru',
            'New Deaths': 'kematian_baru', 
            'New Recovered': 'sembuh_baru',
            'Total Cases': 'total_kasus',
            'Total Deaths': 'total_kematian',
            'Total Recovered': 'total_sembuh',
            'Total Active Cases': 'total_aktif',
            'New Cases per Million': 'kasus_baru_per_juta',
            'Total Cases per Million': 'total_kasus_per_juta',
            'New Deaths per Million': 'kematian_baru_per_juta',
            'Total Deaths per Million': 'total_kematian_per_juta',
            'Case Fatality Rate': 'case_fatality_rate',
            'Case Recovered Rate': 'case_recovered_rate',
            'Growth Factor of New Cases': 'growth_factor_cases',
            'Growth Factor of New Deaths': 'growth_factor_deaths'
        }
        
        # Rename columns
        df = df.rename(columns=column_mapping)
        
        # Prepare data
        df['tanggal'] = pd.to_datetime(df['tanggal'])
        
        # Fill NaN values with appropriate defaults
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        df[numeric_columns] = df[numeric_columns].fillna(0)
        
        # Fill categorical columns
        df['age_group_risk'] = df['age_group_risk'].fillna('Medium')
        
        cursor = conn.cursor()
        
        # Clear existing data
        cursor.execute("DELETE FROM STATISTIK_HARIAN")
        
        # Prepare insert query with all columns
        columns = [
            'iso_code', 'tanggal', 'kasus_baru', 'kematian_baru', 'sembuh_baru',
            'total_kasus', 'total_kematian', 'total_sembuh', 'total_aktif',
            'kasus_baru_per_juta', 'total_kasus_per_juta', 'kematian_baru_per_juta',
            'total_kematian_per_juta', 'case_fatality_rate', 'case_recovered_rate',
            'growth_factor_cases', 'growth_factor_deaths', 'tests_conducted',
            'positivity_rate', 'hospital_capacity', 'icu_occupancy',
            'vaccinations_total', 'vaccinations_new', 'fully_vaccinated',
            'vaccination_rate', 'mobility_index', 'economic_impact_score',
            'school_closure_level', 'stringency_index', 'age_group_risk',
            'comorbidity_rate', 'healthcare_workers_infected', 'temperature_avg',
            'humidity_avg', 'air_quality_index', 'rainfall_mm', 'unemployment_rate',
            'poverty_rate', 'education_index', 'internet_penetration',
            'hospital_beds_per_1000', 'doctors_per_1000', 'nurses_per_1000',
            'ventilators_available', 'public_transport_usage', 'private_vehicle_density',
            'flight_frequency', 'median_age', 'elderly_population_pct', 'urban_population_pct'
        ]
        
        placeholders = ', '.join(['%s'] * len(columns))
        insert_query = f"""
        INSERT INTO STATISTIK_HARIAN ({', '.join(columns)})
        VALUES ({placeholders})
        """
        
        # Insert data in batches
        batch_size = 1000
        total_rows = len(df)
        
        for i in tqdm(range(0, total_rows, batch_size), desc="Importing daily statistics"):
            batch = df.iloc[i:i+batch_size]
            
            for _, row in batch.iterrows():
                values = [row[col] if col in row and pd.notna(row[col]) else None for col in columns]
                cursor.execute(insert_query, values)
            
            conn.commit()
        
        print(f"SUCCESS: Successfully imported {total_rows} daily statistics records")
        return True
        
    except Exception as e:
        print(f"ERROR: Error importing STATISTIK_HARIAN data: {e}")
        if supabase_config.debug_mode:
            import traceback
            traceback.print_exc()
        conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

def import_enhanced_data():
    """Import enhanced data from dummy_data folder"""
    print("\nImporting enhanced data...")
    
    enhanced_tables = {
        'RUMAH_SAKIT': 'dummy_data/rumah_sakit.csv',
        'VAKSINASI_DETAIL': 'dummy_data/vaksinasi_detail.csv',
        'KEBIJAKAN_PEMERINTAH': 'dummy_data/kebijakan_pemerintah.csv',
        'EKONOMI_REGIONAL': 'dummy_data/ekonomi_regional.csv',
        'TESTING_LABS': 'dummy_data/testing_labs.csv',
        'CLUSTER_PENULARAN': 'dummy_data/cluster_penularan.csv',
        'MOBILITAS_HARIAN': 'dummy_data/mobilitas_harian.csv'
    }
    
    conn = get_db_connection()
    if not conn:
        return False
    
    success_count = 0
    
    for table_name, file_path in enhanced_tables.items():
        try:
            if not os.path.exists(file_path):
                print(f"WARNING: File not found: {file_path}, skipping {table_name}")
                continue
            
            print(f"Importing {table_name}...")
            
            # Read CSV
            df = pd.read_csv(file_path)
            
            # Clean data
            df = df.fillna('')
            
            # Convert date columns
            date_columns = [col for col in df.columns if 'tanggal' in col.lower() or 'date' in col.lower()]
            for col in date_columns:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
            
            cursor = conn.cursor()
            
            # Clear existing data
            cursor.execute(f"DELETE FROM {table_name}")
            
            # Get column names (excluding auto-generated ID columns)
            columns = [col for col in df.columns if not col.lower().startswith('id_')]
            
            if not columns:
                print(f"WARNING: No valid columns found for {table_name}")
                continue
            
            placeholders = ', '.join(['%s'] * len(columns))
            insert_query = f"""
            INSERT INTO {table_name} ({', '.join(columns)})
            VALUES ({placeholders})
            """
            
            # Insert data
            for _, row in tqdm(df.iterrows(), total=len(df), desc=f"Importing {table_name}"):
                values = [row[col] if pd.notna(row[col]) else None for col in columns]
                cursor.execute(insert_query, values)
            
            conn.commit()
            print(f"SUCCESS: Successfully imported {len(df)} records to {table_name}")
            success_count += 1
            
        except Exception as e:
            print(f"ERROR: Error importing {table_name}: {e}")
            if supabase_config.debug_mode:
                import traceback
                traceback.print_exc()
            conn.rollback()
    
    conn.close()
    print(f"\nSUCCESS: Successfully imported {success_count}/{len(enhanced_tables)} enhanced tables")
    return success_count > 0

def verify_import():
    """Verify imported data"""
    print("\nVerifying imported data...")
    
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Check main tables
        main_tables = ['LOKASI', 'STATISTIK_HARIAN']
        
        for table in main_tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"TABLE {table}: {count:,} records")
        
        # Check enhanced tables
        enhanced_tables = [
            'RUMAH_SAKIT', 'VAKSINASI_DETAIL', 'KEBIJAKAN_PEMERINTAH',
            'EKONOMI_REGIONAL', 'TESTING_LABS', 'CLUSTER_PENULARAN', 'MOBILITAS_HARIAN'
        ]
        
        for table in enhanced_tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"TABLE {table}: {count:,} records")
            except:
                print(f"WARNING: {table}: Table not found or empty")
        
        # Test views
        print("\nTesting views...")
        views = ['latest_statistics', 'national_daily_stats']
        
        for view in views:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {view}")
                count = cursor.fetchone()[0]
                print(f"VIEW {view}: {count:,} records")
            except Exception as e:
                print(f"ERROR: Error with view {view}: {e}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Error verifying data: {e}")
        return False
    finally:
        if conn:
            conn.close()

def main():
    """Main import function"""
    print("Starting Supabase Data Import for COVID-19 Indonesia Dashboard")
    print("=" * 70)
    
    # Validate environment
    if not validate_environment():
        sys.exit(1)
    
    # Check required files
    required_files = ['covid_19_indonesia_enhanced.csv']
    for file in required_files:
        if not check_file_exists(file):
            print(f"\nERROR: Required file missing: {file}")
            print("Please ensure you have run the data generation scripts first.")
            sys.exit(1)
    
    print("\nStarting data import process...")
    
    # Import main data
    success = True
    
    # Import LOKASI data
    if not import_lokasi_data():
        success = False
    
    # Import STATISTIK_HARIAN data
    if not import_statistik_harian_data():
        success = False
    
    # Import enhanced data (optional)
    if os.path.exists('dummy_data'):
        import_enhanced_data()
    else:
        print("\nWARNING: dummy_data folder not found, skipping enhanced data import")
        print("Run 'python generate_enhanced_dummy_data.py' to create enhanced data")
    
    # Verify import
    if success:
        verify_import()
        print("\nSUCCESS: Data import completed successfully!")
        print("\nNext steps:")
        print("1. Run the Streamlit app: streamlit run streamlit_supabase_app.py")
        print("2. Or use the launcher: python run_supabase_dashboard.py")
    else:
        print("\nERROR: Data import completed with errors")
        print("Please check the error messages above and try again")
        sys.exit(1)

if __name__ == "__main__":
    main()
