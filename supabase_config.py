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
import socket
from urllib.parse import urlparse

# Load environment variables
# 1) Prefer Streamlit secrets (for Streamlit Cloud)
try:
    if hasattr(st, "secrets"):
        for k, v in st.secrets.items():
            # Skip nested structures; only flat key/value expected
            if isinstance(v, (dict, list)):
                continue
            os.environ[k] = str(v)
except Exception:
    # If not on Streamlit, ignore
    pass

# 2) Fallback to .env (for local development)
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
        
        # Debug: Check if secrets are loaded (after debug_mode is set)
        if hasattr(st, 'secrets') and self.debug_mode:
            st.write("🔍 Debug: Checking secrets...")
            st.write(f"SUPABASE_URL: {'✅ Set' if self.url else '❌ Missing'}")
            st.write(f"SUPABASE_ANON_KEY: {'✅ Set' if self.anon_key else '❌ Missing'}")
            st.write(f"SUPABASE_DATABASE_URL: {'✅ Set' if self.database_url else '❌ Missing'}")
        
    def validate_config(self) -> bool:
        """Validate that all required configuration is present"""
        # If connection string is provided, that's sufficient
        if self.database_url:
            minimal = [self.url, self.anon_key]
            missing = [field for field in minimal if not field]
            if missing:
                st.error("Missing Supabase URL or ANON key. Please check configuration.")
                return False
            return True

        required_fields = [
            self.url, self.anon_key, self.db_host, 
            self.db_password, self.db_user
        ]
        
        missing_fields = [field for field in required_fields if not field]
        
        if missing_fields:
            st.error("Missing Supabase configuration. Please check your .env or Streamlit secrets.")
            st.info("Required fields: SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_DB_HOST, SUPABASE_DB_PASSWORD, SUPABASE_DB_USER (or SUPABASE_DATABASE_URL)")
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
    
    def _with_sslmode(self, url: str) -> str:
        """Ensure connection string enforces SSL"""
        if not url:
            return url
        # If sslmode already present, return as is
        if "sslmode=" in url:
            return url
        # Preserve existing query params
        if "?" in url:
            return url + "&sslmode=require"
        return url + "?sslmode=require"
    
    def _connect_via_ipv4(self, dsn_url: str) -> Optional[psycopg2.extensions.connection]:
        """
        Attempt to connect forcing IPv4 to avoid IPv6 issues on some platforms.
        """
        try:
            parsed = urlparse(dsn_url)
            host = parsed.hostname
            port = parsed.port or 5432
            user = parsed.username
            password = parsed.password
            dbname = (parsed.path or "/postgres").lstrip("/") or "postgres"

            # Resolve only IPv4 addresses
            addrinfo = socket.getaddrinfo(host, port, family=socket.AF_INET, type=socket.SOCK_STREAM)
            if not addrinfo:
                return None
            ipv4 = addrinfo[0][4][0]

            return psycopg2.connect(
                host=host,          # keep host for SNI/ssl checks
                hostaddr=ipv4,      # force IPv4 connection
                port=port,
                user=user,
                password=password,
                dbname=dbname,
                sslmode="require",
            )
        except Exception:
            return None

    def get_db_connection(self) -> Optional[psycopg2.extensions.connection]:
        """
        Create PostgreSQL connection to Supabase.
        Tries connection pooler first (more reliable for serverless), then direct connection.
        """
        # Try connection pooler first (better for Streamlit Cloud)
        if self.database_url:
            pooler_url = self._get_pooler_connection_string()
            if pooler_url:
                try:
                    if self.debug_mode:
                        st.info("Trying Supabase connection pooler...")
                    conn = psycopg2.connect(pooler_url, connect_timeout=10)
                    if conn:
                        return conn
                except Exception as e:
                    if self.debug_mode:
                        st.warning(f"Pooler connection failed: {e}, trying direct connection...")
        
        # Fallback to direct connection
        try:
            if self.database_url:
                # Use connection string if available and enforce SSL
                conn_str = self._with_sslmode(self.database_url)
                # Try IPv4-first connection to avoid IPv6 issues
                conn = self._connect_via_ipv4(conn_str)
                if conn is None:
                    conn = psycopg2.connect(conn_str, connect_timeout=10)
            else:
                # Use individual parameters
                conn = psycopg2.connect(
                    host=self.db_host,
                    database=self.db_name,
                    user=self.db_user,
                    password=self.db_password,
                    port=self.db_port,
                    sslmode='require',  # Supabase requires SSL
                    connect_timeout=10
                )
            
            return conn
        except Exception as e:
            # Don't show error here - let caller handle it
            # This allows fallback to REST API
            if self.debug_mode:
                st.warning(f"Direct PostgreSQL connection failed: {e}")
            return None
    
    def query_via_rest_api(self, query: str) -> Optional[pd.DataFrame]:
        """
        Query database using Supabase REST API as fallback when direct PostgreSQL fails.
        This works better in environments like Streamlit Cloud that may block direct DB connections.
        """
        try:
            # Use service role key for full database access
            client = self.get_supabase_client(use_service_role=True)
            if not client:
                return None
            
            # For simple SELECT queries, we can use Supabase REST API
            # Note: Complex queries with JOINs need to be handled differently
            # This is a simplified version - for production, consider using RPC functions
            
            # Try to execute via RPC if available, otherwise use table queries
            # For now, return None to indicate REST API is not fully implemented
            # The main app should handle this gracefully
            return None
            
        except Exception as e:
            if self.debug_mode:
                st.warning(f"REST API query failed: {e}")
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
