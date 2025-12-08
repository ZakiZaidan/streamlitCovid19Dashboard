"""
Import only STATISTIK_HARIAN data
"""
import pandas as pd
import numpy as np
from supabase_config_standalone import get_db_connection
from tqdm import tqdm

def import_statistik_harian():
    """Import daily statistics data"""
    print("Importing STATISTIK_HARIAN data...")
    
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
        
        # Clean all numeric columns - remove % signs and convert empty strings to NaN
        for col in df.columns:
            if col in ['iso_code', 'tanggal']:  # Skip non-numeric columns
                continue
            
            # Convert to string, clean, then to numeric
            df[col] = df[col].astype(str)
            df[col] = df[col].str.replace('%', '')  # Remove % signs
            df[col] = df[col].replace(['', 'nan', 'NaN', 'None'], np.nan)  # Replace empty/invalid with NaN
            df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert to numeric
        
        # Fill NaN values with appropriate defaults
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        df[numeric_columns] = df[numeric_columns].fillna(0)
        
        # Fill categorical columns
        if 'age_group_risk' in df.columns:
            df['age_group_risk'] = df['age_group_risk'].fillna('Medium')
        
        cursor = conn.cursor()
        
        # Clear existing data
        cursor.execute("DELETE FROM STATISTIK_HARIAN")
        print("Cleared existing STATISTIK_HARIAN data")
        
        # Prepare insert query with available columns
        available_columns = [
            'iso_code', 'tanggal', 'kasus_baru', 'kematian_baru', 'sembuh_baru',
            'total_kasus', 'total_kematian', 'total_sembuh', 'total_aktif',
            'kasus_baru_per_juta', 'total_kasus_per_juta', 'kematian_baru_per_juta',
            'total_kematian_per_juta', 'case_fatality_rate', 'case_recovered_rate',
            'growth_factor_cases', 'growth_factor_deaths'
        ]
        
        # Add enhanced columns if they exist
        enhanced_columns = [
            'temperature_avg', 'humidity_avg', 'air_quality_index', 'rainfall_mm',
            'unemployment_rate', 'poverty_rate', 'education_index', 'internet_penetration',
            'hospital_beds_per_1000', 'doctors_per_1000', 'nurses_per_1000',
            'ventilators_available', 'public_transport_usage', 'private_vehicle_density',
            'flight_frequency', 'median_age', 'elderly_population_pct', 'urban_population_pct'
        ]
        
        for col in enhanced_columns:
            if col in df.columns:
                available_columns.append(col)
        
        print(f"Using columns: {available_columns}")
        
        placeholders = ', '.join(['%s'] * len(available_columns))
        insert_query = f"""
        INSERT INTO STATISTIK_HARIAN ({', '.join(available_columns)})
        VALUES ({placeholders})
        """
        
        # Insert data in batches
        batch_size = 1000
        total_rows = len(df)
        
        print(f"Importing {total_rows} records in batches of {batch_size}...")
        
        for i in tqdm(range(0, total_rows, batch_size), desc="Importing batches"):
            batch = df.iloc[i:i+batch_size]
            
            for _, row in batch.iterrows():
                values = []
                for col in available_columns:
                    if col in row and pd.notna(row[col]):
                        values.append(row[col])
                    else:
                        values.append(None)
                
                cursor.execute(insert_query, values)
            
            conn.commit()
            print(f"Committed batch {i//batch_size + 1}")
        
        print(f"SUCCESS: Successfully imported {total_rows} daily statistics records")
        return True
        
    except Exception as e:
        print(f"ERROR: Error importing STATISTIK_HARIAN data: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    import_statistik_harian()
