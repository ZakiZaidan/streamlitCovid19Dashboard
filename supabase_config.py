"""
Supabase Configuration Module for COVID-19 Indonesia Dashboard
"""

import os
import psycopg2
import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import pandas as pd
from typing import Optional, Tuple

# Load environment variables
load_dotenv()

class SupabaseConfig:
    """Supabase configuration and connection management"""
    
    def __init__(self):
        self.url = os.getenv('SUPABASE_URL')
        self.anon_key = os.getenv('SUPABASE_ANON_KEY')
        self.service_role_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
        
        # Database connection details
        self.db_host = os.getenv('SUPABASE_DB_HOST')
        self.db_name = os.getenv('SUPABASE_DB_NAME', 'postgres')
        self.db_user = os.getenv('SUPABASE_DB_USER', 'postgres')
        self.db_password = os.getenv('SUPABASE_DB_PASSWORD')
        self.db_port = os.getenv('SUPABASE_DB_PORT', '5432')
        
        # Alternative: Use connection string
        self.database_url = os.getenv('SUPABASE_DATABASE_URL')
        
        # App configuration
        self.app_title = os.getenv('APP_TITLE', 'COVID-19 Indonesia Dashboard')
        self.cache_ttl = int(os.getenv('CACHE_TTL', '3600'))
        self.debug_mode = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
        
    def validate_config(self) -> bool:
        """Validate that all required configuration is present"""
        required_fields = [
            self.url, self.anon_key, self.db_host, 
            self.db_password, self.db_user
        ]
        
        missing_fields = [field for field in required_fields if not field]
        
        if missing_fields:
            st.error(f"Missing Supabase configuration. Please check your .env file.")
            st.info("Required fields: SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_DB_HOST, SUPABASE_DB_PASSWORD, SUPABASE_DB_USER")
            return False
        
        return True
    
    def get_supabase_client(self, use_service_role: bool = False) -> Optional[Client]:
        """Create Supabase client"""
        try:
            key = self.service_role_key if use_service_role else self.anon_key
            if not key:
                st.error("Supabase key not found in configuration")
                return None
                
            supabase: Client = create_client(self.url, key)
            return supabase
        except Exception as e:
            st.error(f"Failed to create Supabase client: {e}")
            return None
    
    def get_db_connection(self) -> Optional[psycopg2.extensions.connection]:
        """Create direct PostgreSQL connection to Supabase"""
        try:
            if self.database_url:
                # Use connection string if available
                conn = psycopg2.connect(self.database_url)
            else:
                # Use individual parameters
                conn = psycopg2.connect(
                    host=self.db_host,
                    database=self.db_name,
                    user=self.db_user,
                    password=self.db_password,
                    port=self.db_port,
                    sslmode='require'  # Supabase requires SSL
                )
            
            return conn
        except Exception as e:
            st.error(f"Database connection error: {e}")
            if self.debug_mode:
                st.exception(e)
            return None
    
    def test_connection(self) -> Tuple[bool, str]:
        """Test database connection"""
        try:
            conn = self.get_db_connection()
            if not conn:
                return False, "Failed to establish connection"
            
            # Test query
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                version = cur.fetchone()[0]
            
            conn.close()
            return True, f"Connection successful. PostgreSQL version: {version}"
            
        except Exception as e:
            return False, f"Connection test failed: {str(e)}"
    
    def get_connection_info(self) -> dict:
        """Get connection information for display"""
        return {
            "Supabase URL": self.url,
            "Database Host": self.db_host,
            "Database Name": self.db_name,
            "Database User": self.db_user,
            "Database Port": self.db_port,
            "Cache TTL": f"{self.cache_ttl} seconds",
            "Debug Mode": self.debug_mode
        }

# Global configuration instance
supabase_config = SupabaseConfig()

def get_db_connection():
    """Get database connection - compatible with existing code"""
    return supabase_config.get_db_connection()

def get_supabase_client(use_service_role: bool = False):
    """Get Supabase client"""
    return supabase_config.get_supabase_client(use_service_role)

@st.cache_data(ttl=supabase_config.cache_ttl)
def load_data_cached():
    """Cached data loading function"""
    return load_data()

def load_data():
    """Load data from Supabase database"""
    conn = get_db_connection()
    if not conn:
        return None, None, None
    
    try:
        # Load latest statistics
        latest_stats_query = """
        SELECT * FROM latest_statistics
        ORDER BY nama_provinsi
        """
        latest_stats = pd.read_sql(latest_stats_query, conn)
        
        # Load daily statistics
        daily_stats_query = """
        SELECT 
            s.*,
            l.nama_provinsi,
            l.island,
            l.populasi,
            l.population_density
        FROM STATISTIK_HARIAN s
        JOIN LOKASI l ON s.iso_code = l.iso_code
        ORDER BY s.tanggal, l.nama_provinsi
        """
        daily_stats = pd.read_sql(daily_stats_query, conn)
        
        # Load national daily statistics
        national_stats_query = """
        SELECT * FROM national_daily_stats
        ORDER BY tanggal
        """
        national_stats = pd.read_sql(national_stats_query, conn)
        
        return latest_stats, daily_stats, national_stats
    
    except Exception as e:
        st.error(f"Error loading data: {e}")
        if supabase_config.debug_mode:
            st.exception(e)
        return None, None, None
    finally:
        if conn:
            conn.close()

def load_enhanced_data():
    """Load enhanced data from additional tables"""
    conn = get_db_connection()
    if not conn:
        return {}
    
    try:
        enhanced_data = {}
        
        # Load healthcare capacity
        healthcare_query = "SELECT * FROM kapasitas_kesehatan_provinsi"
        enhanced_data['healthcare'] = pd.read_sql(healthcare_query, conn)
        
        # Load vaccination data
        vaccination_query = "SELECT * FROM vaksinasi_terkini"
        enhanced_data['vaccination'] = pd.read_sql(vaccination_query, conn)
        
        # Load active clusters
        cluster_query = "SELECT * FROM cluster_aktif"
        enhanced_data['clusters'] = pd.read_sql(cluster_query, conn)
        
        # Load economic impact
        economic_query = "SELECT * FROM dampak_ekonomi_terkini"
        enhanced_data['economic'] = pd.read_sql(economic_query, conn)
        
        # Load hospital data
        hospital_query = "SELECT * FROM RUMAH_SAKIT WHERE operational_status = 'Aktif'"
        enhanced_data['hospitals'] = pd.read_sql(hospital_query, conn)
        
        # Load testing labs
        labs_query = "SELECT * FROM TESTING_LABS"
        enhanced_data['labs'] = pd.read_sql(labs_query, conn)
        
        # Load policies
        policies_query = """
        SELECT * FROM KEBIJAKAN_PEMERINTAH 
        WHERE status_kebijakan = 'Aktif' 
        ORDER BY tanggal_mulai DESC
        """
        enhanced_data['policies'] = pd.read_sql(policies_query, conn)
        
        # Load mobility data (last 30 days)
        mobility_query = """
        SELECT * FROM MOBILITAS_HARIAN 
        WHERE tanggal >= CURRENT_DATE - INTERVAL '30 days'
        ORDER BY tanggal DESC
        """
        enhanced_data['mobility'] = pd.read_sql(mobility_query, conn)
        
        return enhanced_data
    
    except Exception as e:
        st.error(f"Error loading enhanced data: {e}")
        if supabase_config.debug_mode:
            st.exception(e)
        return {}
    finally:
        if conn:
            conn.close()

def check_table_exists(table_name: str) -> bool:
    """Check if a table exists in the database"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = %s
                );
            """, (table_name,))
            return cur.fetchone()[0]
    except Exception as e:
        if supabase_config.debug_mode:
            st.error(f"Error checking table {table_name}: {e}")
        return False
    finally:
        conn.close()

def get_table_row_count(table_name: str) -> int:
    """Get row count for a table"""
    conn = get_db_connection()
    if not conn:
        return 0
    
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT COUNT(*) FROM {table_name};")
            return cur.fetchone()[0]
    except Exception as e:
        if supabase_config.debug_mode:
            st.error(f"Error counting rows in {table_name}: {e}")
        return 0
    finally:
        conn.close()

def display_connection_status():
    """Display connection status in Streamlit sidebar"""
    st.sidebar.markdown("### 🔗 Database Connection")
    
    if not supabase_config.validate_config():
        st.sidebar.error("❌ Configuration Invalid")
        return False
    
    # Test connection
    success, message = supabase_config.test_connection()
    
    if success:
        st.sidebar.success("✅ Connected to Supabase")
        
        # Show basic info
        with st.sidebar.expander("Connection Details"):
            info = supabase_config.get_connection_info()
            for key, value in info.items():
                if key not in ["Database User", "Database Password"]:  # Hide sensitive info
                    st.write(f"**{key}:** {value}")
        
        # Show table status
        with st.sidebar.expander("Database Status"):
            main_tables = ['LOKASI', 'STATISTIK_HARIAN']
            enhanced_tables = ['RUMAH_SAKIT', 'VAKSINASI_DETAIL', 'KEBIJAKAN_PEMERINTAH']
            
            st.write("**Main Tables:**")
            for table in main_tables:
                if check_table_exists(table.lower()):
                    count = get_table_row_count(table)
                    st.write(f"✅ {table}: {count:,} rows")
                else:
                    st.write(f"❌ {table}: Not found")
            
            st.write("**Enhanced Tables:**")
            for table in enhanced_tables:
                if check_table_exists(table.lower()):
                    count = get_table_row_count(table)
                    st.write(f"✅ {table}: {count:,} rows")
                else:
                    st.write(f"❌ {table}: Not found")
        
        return True
    else:
        st.sidebar.error("❌ Connection Failed")
        st.sidebar.error(message)
        return False

# Initialize configuration validation
if __name__ == "__main__":
    # Test configuration when run directly
    if supabase_config.validate_config():
        success, message = supabase_config.test_connection()
        print(f"Connection test: {'SUCCESS' if success else 'FAILED'}")
        print(f"Message: {message}")
    else:
        print("Configuration validation failed")
