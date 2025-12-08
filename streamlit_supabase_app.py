#!/usr/bin/env python3
"""
Comprehensive COVID-19 Indonesia Dashboard with Supabase
Menggabungkan dashboard original dengan 7 tabel enhancement baru
untuk analisis yang komprehensif dan lengkap menggunakan Supabase
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Import Supabase configuration
from supabase_config import (
    supabase_config, 
    display_connection_status,
    check_table_exists,
    get_db_connection
)

# Page configuration
st.set_page_config(
    page_title=supabase_config.app_title,
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Universal Theme Support
st.markdown("""
<style>
    /* Main Header - Visible in both themes */
    .main-header {
        font-size: 3.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Light theme header */
    .stApp .main-header {
        color: #1f77b4;
    }
    
    /* Dark theme header */
    .stApp[data-theme="dark"] .main-header {
        color: #4da6ff !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5) !important;
    }
    
    /* Metric Cards - Always white text on gradient */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin: 0.5rem 0;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 2rem;
        font-weight: bold;
        margin: 2rem 0 1rem 0;
        border-bottom: 3px solid #3498db;
        padding-bottom: 0.5rem;
    }
    
    /* Light theme section header */
    .stApp .section-header {
        color: #2c3e50;
    }
    
    /* Dark theme section header */
    .stApp[data-theme="dark"] .section-header {
        color: #ffffff !important;
        border-bottom-color: #4da6ff !important;
    }
    
    /* Feature Highlight Boxes */
    .feature-highlight {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border-left: 4px solid #e17055;
        font-weight: 500;
    }
    
    /* Light theme feature highlight */
    .stApp .feature-highlight {
        background: #fff3cd;
        color: #856404 !important;
        border-left-color: #ffc107;
    }
    
    /* Dark theme feature highlight */
    .stApp[data-theme="dark"] .feature-highlight {
        background: rgba(255, 193, 7, 0.2) !important;
        color: #ffffff !important;
        border-left-color: #ffc107 !important;
    }
    
    /* Info Boxes */
    .info-box {
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
        border-left: 5px solid #17a2b8;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    /* Light theme info box */
    .stApp .info-box {
        background: #d1ecf1;
        color: #0c5460 !important;
    }
    
    /* Dark theme info box */
    .stApp[data-theme="dark"] .info-box {
        background: rgba(23, 162, 184, 0.2) !important;
        color: #ffffff !important;
    }
    
    /* Metric card text always white */
    .metric-card * {
        color: white !important;
    }
    
    /* Additional Streamlit element fixes for dark theme */
    .stApp[data-theme="dark"] .stSelectbox label {
        color: #ffffff !important;
    }
    
    .stApp[data-theme="dark"] .stRadio label {
        color: #ffffff !important;
    }
    
    .stApp[data-theme="dark"] .stButton button {
        color: #ffffff !important;
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    .stApp[data-theme="dark"] .stSidebar .stMarkdown h1,
    .stApp[data-theme="dark"] .stSidebar .stMarkdown h2,
    .stApp[data-theme="dark"] .stSidebar .stMarkdown h3,
    .stApp[data-theme="dark"] .stSidebar .stMarkdown p,
    .stApp[data-theme="dark"] .stSidebar .stMarkdown div,
    .stApp[data-theme="dark"] .stSidebar .stMarkdown span {
        color: #ffffff !important;
    }
    
    /* Dashboard Tabs */
    .dashboard-tab {
        border-radius: 0.5rem;
        padding: 0.5rem;
        margin: 0.2rem 0;
    }
    
    /* Light theme dashboard tab */
    .stApp .dashboard-tab {
        background-color: #f8f9fa;
        color: #495057;
    }
    
    /* Dark theme dashboard tab */
    .stApp[data-theme="dark"] .dashboard-tab {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
    }
    
    /* Sidebar fixes for dark theme */
    .stApp[data-theme="dark"] .css-1d391kg {
        background-color: #262730 !important;
    }
    
    .stApp[data-theme="dark"] .css-1d391kg .stMarkdown {
        color: #ffffff !important;
    }
    
    .stApp[data-theme="dark"] .css-1d391kg h1,
    .stApp[data-theme="dark"] .css-1d391kg h2,
    .stApp[data-theme="dark"] .css-1d391kg h3,
    .stApp[data-theme="dark"] .css-1d391kg p,
    .stApp[data-theme="dark"] .css-1d391kg div {
        color: #ffffff !important;
    }
    
    /* Force visibility for all custom elements */
    .stApp[data-theme="dark"] .feature-highlight *,
    .stApp[data-theme="dark"] .info-box *,
    .stApp[data-theme="dark"] .dashboard-tab * {
        color: inherit !important;
    }
    
    .stApp .feature-highlight *,
    .stApp .info-box *,
    .stApp .dashboard-tab * {
        color: inherit !important;
    }
    
    /* Ensure sidebar navigation is visible */
    .stApp[data-theme="dark"] .css-1544g2n {
        color: #ffffff !important;
    }
    
    .stApp[data-theme="dark"] .css-1544g2n .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
    }
    
    /* Success/Info messages in sidebar */
    .stApp[data-theme="dark"] .stSuccess {
        background-color: rgba(40, 167, 69, 0.2) !important;
        color: #ffffff !important;
    }
    
    .stApp[data-theme="dark"] .stInfo {
        background-color: rgba(23, 162, 184, 0.2) !important;
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=supabase_config.cache_ttl)  # Cache with configured TTL
def load_all_data():
    """Load data from all tables using Supabase"""
    conn = get_db_connection()
    if not conn:
        return {}
    
    try:
        data = {}
        
        # Original core data
        data['latest_stats'] = pd.read_sql("SELECT * FROM latest_statistics ORDER BY nama_provinsi", conn)
        data['national_stats'] = pd.read_sql("SELECT * FROM national_daily_stats ORDER BY tanggal", conn)
        
        # Daily statistics for detailed analysis
        data['daily_stats'] = pd.read_sql("""
            SELECT 
                s.*,
                l.nama_provinsi,
                l.island,
                l.populasi,
                l.population_density
            FROM STATISTIK_HARIAN s
            JOIN LOKASI l ON s.iso_code = l.iso_code
            ORDER BY s.tanggal, l.nama_provinsi
        """, conn)
        
        # Data from additional tables (with error handling)
        additional_tables = {
            'rumah_sakit': """
                SELECT rs.*, l.nama_provinsi 
                FROM RUMAH_SAKIT rs 
                JOIN LOKASI l ON rs.iso_code = l.iso_code
            """,
            'vaksinasi': """
                SELECT vd.*, l.nama_provinsi 
                FROM VAKSINASI_DETAIL vd 
                JOIN LOKASI l ON vd.iso_code = l.iso_code
                ORDER BY vd.tanggal DESC
            """,
            'kebijakan': """
                SELECT kp.*, l.nama_provinsi 
                FROM KEBIJAKAN_PEMERINTAH kp 
                JOIN LOKASI l ON kp.iso_code = l.iso_code
                ORDER BY kp.tanggal_mulai DESC
            """,
            'ekonomi': """
                SELECT er.*, l.nama_provinsi 
                FROM EKONOMI_REGIONAL er 
                JOIN LOKASI l ON er.iso_code = l.iso_code
                ORDER BY er.tahun DESC, er.bulan DESC
            """,
            'testing_labs': """
                SELECT tl.*, l.nama_provinsi 
                FROM TESTING_LABS tl 
                JOIN LOKASI l ON tl.iso_code = l.iso_code
            """,
            'cluster': """
                SELECT cp.*, l.nama_provinsi 
                FROM CLUSTER_PENULARAN cp 
                JOIN LOKASI l ON cp.iso_code = l.iso_code
                ORDER BY cp.tanggal_terdeteksi DESC
            """,
            'mobilitas': """
                SELECT mh.*, l.nama_provinsi 
                FROM MOBILITAS_HARIAN mh 
                JOIN LOKASI l ON mh.iso_code = l.iso_code
                ORDER BY mh.tanggal DESC
            """
        }
        
        # Load additional tables with error handling
        for table_name, query in additional_tables.items():
            try:
                data[table_name] = pd.read_sql(query, conn)
            except Exception as e:
                st.warning(f"Table '{table_name}' not available: {e}")
                data[table_name] = pd.DataFrame()
        
        # Load aggregated views (with error handling)
        additional_views = {
            'kapasitas_kesehatan': "SELECT * FROM kapasitas_kesehatan_provinsi",
            'vaksinasi_terkini': "SELECT * FROM vaksinasi_terkini", 
            'cluster_aktif': "SELECT * FROM cluster_aktif",
            'dampak_ekonomi': "SELECT * FROM dampak_ekonomi_terkini"
        }
        
        for view_name, query in additional_views.items():
            try:
                data[view_name] = pd.read_sql(query, conn)
            except Exception as e:
                st.warning(f"View '{view_name}' not available: {e}")
                data[view_name] = pd.DataFrame()
        
        return data
    
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return {}
    finally:
        if conn:
            conn.close()

def create_unified_kpi_dashboard(data):
    """Create comprehensive KPI dashboard"""
    st.markdown('<div class="section-header">📊 Dashboard KPI Terpadu</div>', unsafe_allow_html=True)
    
    if 'national_stats' not in data or len(data['national_stats']) == 0:
        st.error("Data nasional tidak tersedia")
        return
    
    latest_national = data['national_stats'].iloc[-1]
    
    # Row 1: Core COVID-19 Metrics (Original)
    st.subheader("🦠 Metrics COVID-19 Inti")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🦠 Total Kasus",
            value=f"{latest_national['total_kasus_nasional']:,}",
            delta=f"+{latest_national['total_kasus_baru_nasional']:,}"
        )
    
    with col2:
        st.metric(
            label="💚 Total Sembuh", 
            value=f"{latest_national['total_sembuh_nasional']:,}",
            delta=f"+{latest_national['total_sembuh_baru_nasional']:,}"
        )
    
    with col3:
        st.metric(
            label="💔 Total Meninggal",
            value=f"{latest_national['total_kematian_nasional']:,}",
            delta=f"+{latest_national['total_kematian_baru_nasional']:,}"
        )
    
    with col4:
        recovery_rate = (latest_national['total_sembuh_nasional'] / latest_national['total_kasus_nasional']) * 100
        st.metric(
            label="📈 Tingkat Kesembuhan",
            value=f"{recovery_rate:.1f}%"
        )
    
    # Row 2: Infrastructure Metrics (if available)
    if 'kapasitas_kesehatan' in data and len(data['kapasitas_kesehatan']) > 0:
        st.subheader("🏥 Metrics Infrastruktur Kesehatan")
        col1, col2, col3, col4 = st.columns(4)
        
        total_rs = data['kapasitas_kesehatan']['total_rumah_sakit'].sum()
        total_beds = data['kapasitas_kesehatan']['total_tempat_tidur'].sum()
        total_icu = data['kapasitas_kesehatan']['total_icu'].sum()
        total_labs = data['kapasitas_kesehatan']['total_lab_testing'].sum()
        
        with col1:
            st.metric(label="🏥 Total Rumah Sakit", value=f"{total_rs:,}")
        with col2:
            st.metric(label="🛏️ Total Tempat Tidur", value=f"{total_beds:,}")
        with col3:
            st.metric(label="🚨 Total ICU", value=f"{total_icu:,}")
        with col4:
            st.metric(label="🔬 Total Lab Testing", value=f"{total_labs:,}")
    
    # Row 3: Vaccination & Economic Metrics (if available)
    if 'vaksinasi' in data and len(data['vaksinasi']) > 0:
        st.subheader("💉 Metrics Vaksinasi & Ekonomi")
        col1, col2, col3, col4 = st.columns(4)
        
        total_dosis_1 = data['vaksinasi']['dosis_1'].sum()
        total_dosis_2 = data['vaksinasi']['dosis_2'].sum()
        total_booster = data['vaksinasi']['dosis_booster'].sum()
        
        with col1:
            st.metric(label="💉 Total Dosis 1", value=f"{total_dosis_1:,}")
        with col2:
            st.metric(label="💉 Total Dosis 2", value=f"{total_dosis_2:,}")
        with col3:
            st.metric(label="💉 Total Booster", value=f"{total_booster:,}")
        
        if 'ekonomi' in data and len(data['ekonomi']) > 0:
            avg_recovery = data['ekonomi']['recovery_index'].mean()
            with col4:
                st.metric(label="📈 Indeks Pemulihan", value=f"{avg_recovery:.1f}")

def create_kpi_metrics(national_stats):
    """Create KPI metrics for the dashboard"""
    if national_stats is None or len(national_stats) == 0:
        return
    
    latest_data = national_stats.iloc[-1]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Kasus",
            value=f"{latest_data['total_kasus_nasional']:,}",
            delta=f"+{latest_data['total_kasus_baru_nasional']:,}"
        )
    
    with col2:
        st.metric(
            label="Total Sembuh",
            value=f"{latest_data['total_sembuh_nasional']:,}",
            delta=f"+{latest_data['total_sembuh_baru_nasional']:,}"
        )
    
    with col3:
        st.metric(
            label="Total Meninggal",
            value=f"{latest_data['total_kematian_nasional']:,}",
            delta=f"+{latest_data['total_kematian_baru_nasional']:,}"
        )
    
    with col4:
        recovery_rate = (latest_data['total_sembuh_nasional'] / latest_data['total_kasus_nasional']) * 100
        st.metric(
            label="Tingkat Kesembuhan",
            value=f"{recovery_rate:.1f}%"
        )

def create_bubble_map(latest_stats):
    """Create bubble map showing case distribution"""
    if latest_stats is None or len(latest_stats) == 0:
        st.error("No data available for map")
        return
    
    # Filter out rows with missing coordinates
    map_data = latest_stats.dropna(subset=['latitude', 'longitude'])
    
    if len(map_data) == 0:
        st.error("No location data available")
        return
    
    fig = px.scatter_mapbox(
        map_data,
        lat="latitude",
        lon="longitude",
        size="total_kasus",
        color="total_aktif",
        hover_name="nama_provinsi",
        hover_data={
            "total_kasus": ":,",
            "total_aktif": ":,",
            "total_sembuh": ":,",
            "total_kematian": ":,",
            "case_fatality_rate": ":.2f"
        },
        color_continuous_scale="Reds",
        size_max=50,
        zoom=4,
        center={"lat": -2.5, "lon": 118},
        mapbox_style="open-street-map",
        title="Peta Sebaran COVID-19 Indonesia (Ukuran = Total Kasus, Warna = Kasus Aktif)"
    )
    
    fig.update_layout(
        height=600,
        margin={"r":0,"t":50,"l":0,"b":0}
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_heatmap(latest_stats):
    """Create heatmap showing case density"""
    if latest_stats is None or len(latest_stats) == 0:
        return
    
    # Calculate cases per 100k population
    latest_stats['kasus_per_100k'] = (latest_stats['total_kasus'] / latest_stats['populasi']) * 100000
    
    map_data = latest_stats.dropna(subset=['latitude', 'longitude', 'kasus_per_100k'])
    
    fig = px.density_mapbox(
        map_data,
        lat="latitude",
        lon="longitude",
        z="kasus_per_100k",
        radius=50,
        center={"lat": -2.5, "lon": 118},
        zoom=4,
        mapbox_style="open-street-map",
        color_continuous_scale="Reds",
        title="Heatmap Kepadatan Kasus COVID-19 (per 100k penduduk)"
    )
    
    fig.update_layout(
        height=600,
        margin={"r":0,"t":50,"l":0,"b":0}
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_time_series_charts(national_stats, daily_stats):
    """Create time series analysis charts"""
    if national_stats is None or daily_stats is None:
        return
    
    # National trend
    st.subheader("📈 Tren Nasional COVID-19")
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Kasus Baru Harian', 'Kematian vs Kesembuhan', 
                       'Total Kasus Kumulatif', 'Moving Average 7 Hari'),
        specs=[[{"secondary_y": False}, {"secondary_y": True}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Chart 1: Daily new cases
    fig.add_trace(
        go.Scatter(
            x=national_stats['tanggal'],
            y=national_stats['total_kasus_baru_nasional'],
            mode='lines',
            name='Kasus Baru',
            line=dict(color='blue')
        ),
        row=1, col=1
    )
    
    # Chart 2: Deaths vs Recovered
    fig.add_trace(
        go.Scatter(
            x=national_stats['tanggal'],
            y=national_stats['total_kematian_baru_nasional'],
            mode='lines',
            name='Kematian Baru',
            line=dict(color='red')
        ),
        row=1, col=2
    )
    
    fig.add_trace(
        go.Scatter(
            x=national_stats['tanggal'],
            y=national_stats['total_sembuh_baru_nasional'],
            mode='lines',
            name='Sembuh Baru',
            line=dict(color='green')
        ),
        row=1, col=2
    )
    
    # Chart 3: Cumulative cases
    fig.add_trace(
        go.Scatter(
            x=national_stats['tanggal'],
            y=national_stats['total_kasus_nasional'],
            mode='lines',
            name='Total Kasus',
            line=dict(color='orange'),
            fill='tonexty'
        ),
        row=2, col=1
    )
    
    # Chart 4: 7-day moving average
    national_stats['ma_7'] = national_stats['total_kasus_baru_nasional'].rolling(window=7).mean()
    fig.add_trace(
        go.Scatter(
            x=national_stats['tanggal'],
            y=national_stats['ma_7'],
            mode='lines',
            name='MA 7 Hari',
            line=dict(color='purple', width=3)
        ),
        row=2, col=2
    )
    
    fig.update_layout(
        height=800,
        showlegend=True,
        title_text="Analisis Tren Waktu COVID-19 Indonesia"
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_provincial_comparison(latest_stats, daily_stats):
    """Create provincial comparison charts"""
    if latest_stats is None:
        return
    
    st.subheader("🏆 Perbandingan Antar Provinsi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top 10 provinces by total cases
        top_provinces = latest_stats.nlargest(10, 'total_kasus')
        
        fig = px.bar(
            top_provinces,
            x='total_kasus',
            y='nama_provinsi',
            orientation='h',
            title='Top 10 Provinsi dengan Kasus Tertinggi',
            color='total_kasus',
            color_continuous_scale='Reds'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Cases by island
        island_stats = latest_stats.groupby('island').agg({
            'total_kasus': 'sum',
            'total_kematian': 'sum',
            'total_sembuh': 'sum'
        }).reset_index()
        
        fig = px.pie(
            island_stats,
            values='total_kasus',
            names='island',
            title='Distribusi Kasus per Pulau'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # Population density vs cases scatter plot
    st.subheader("📊 Analisis Kepadatan Penduduk vs Penyebaran")
    
    # Calculate cases per million
    latest_stats['kasus_per_juta'] = (latest_stats['total_kasus'] / latest_stats['populasi']) * 1000000
    
    fig = px.scatter(
        latest_stats,
        x='population_density',
        y='kasus_per_juta',
        size='total_kasus',
        color='island',
        hover_name='nama_provinsi',
        title='Kepadatan Penduduk vs Kasus per Juta Penduduk',
        labels={
            'population_density': 'Kepadatan Penduduk (per km²)',
            'kasus_per_juta': 'Kasus per Juta Penduduk'
        }
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_original_visualizations(data):
    """Create original dashboard visualizations"""
    st.markdown('<div class="section-header">🗺️ Visualisasi Geospasial & Tren</div>', unsafe_allow_html=True)
    
    # Bubble Map (Original)
    if 'latest_stats' in data and len(data['latest_stats']) > 0:
        st.subheader("🗺️ Peta Sebaran COVID-19")
        
        map_data = data['latest_stats'].dropna(subset=['latitude', 'longitude'])
        
        if len(map_data) > 0:
            fig = px.scatter_mapbox(
                map_data,
                lat="latitude",
                lon="longitude",
                size="total_kasus",
                color="total_aktif",
                hover_name="nama_provinsi",
                hover_data={
                    "total_kasus": ":,",
                    "total_aktif": ":,",
                    "total_sembuh": ":,",
                    "total_kematian": ":,",
                    "case_fatality_rate": ":.2f"
                },
                color_continuous_scale="Reds",
                size_max=50,
                zoom=4,
                center={"lat": -2.5, "lon": 118},
                mapbox_style="open-street-map",
                title="Peta Sebaran COVID-19 Indonesia (Ukuran = Total Kasus, Warna = Kasus Aktif)"
            )
            fig.update_layout(height=600, margin={"r":0,"t":50,"l":0,"b":0})
            st.plotly_chart(fig, use_container_width=True)
    
    # Time Series Analysis (Original)
    if 'national_stats' in data and len(data['national_stats']) > 0:
        st.subheader("📈 Analisis Tren Waktu")
        
        national_stats = data['national_stats']
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Kasus Baru Harian', 'Kematian vs Kesembuhan', 
                           'Total Kasus Kumulatif', 'Moving Average 7 Hari'),
            specs=[[{"secondary_y": False}, {"secondary_y": True}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Chart 1: Daily new cases
        fig.add_trace(
            go.Scatter(
                x=national_stats['tanggal'],
                y=national_stats['total_kasus_baru_nasional'],
                mode='lines',
                name='Kasus Baru',
                line=dict(color='blue')
            ),
            row=1, col=1
        )
        
        # Chart 2: Deaths vs Recovered
        fig.add_trace(
            go.Scatter(
                x=national_stats['tanggal'],
                y=national_stats['total_kematian_baru_nasional'],
                mode='lines',
                name='Kematian Baru',
                line=dict(color='red')
            ),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Scatter(
                x=national_stats['tanggal'],
                y=national_stats['total_sembuh_baru_nasional'],
                mode='lines',
                name='Sembuh Baru',
                line=dict(color='green')
            ),
            row=1, col=2
        )
        
        # Chart 3: Cumulative cases
        fig.add_trace(
            go.Scatter(
                x=national_stats['tanggal'],
                y=national_stats['total_kasus_nasional'],
                mode='lines',
                name='Total Kasus',
                line=dict(color='orange'),
                fill='tonexty'
            ),
            row=2, col=1
        )
        
        # Chart 4: 7-day moving average
        national_stats['ma_7'] = national_stats['total_kasus_baru_nasional'].rolling(window=7).mean()
        fig.add_trace(
            go.Scatter(
                x=national_stats['tanggal'],
                y=national_stats['ma_7'],
                mode='lines',
                name='MA 7 Hari',
                line=dict(color='purple', width=3)
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            height=800,
            showlegend=True,
            title_text="Analisis Tren Waktu COVID-19 Indonesia"
        )
        
        st.plotly_chart(fig, use_container_width=True)

def create_healthcare_dashboard(data):
    """Create healthcare capacity dashboard"""
    st.markdown('<div class="section-header">🏥 Dashboard Kapasitas Sistem Kesehatan</div>', unsafe_allow_html=True)
    
    if 'rumah_sakit' not in data or len(data['rumah_sakit']) == 0:
        st.warning("Data rumah sakit tidak tersedia - menggunakan data dasar")
        return
    
    rs_data = data['rumah_sakit']
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Hospital distribution by type
        type_dist = rs_data.groupby('tipe_rumah_sakit').size().reset_index(name='count')
        fig = px.pie(
            type_dist,
            values='count',
            names='tipe_rumah_sakit',
            title='Distribusi Rumah Sakit berdasarkan Tipe',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # ICU capacity by province
        icu_by_province = rs_data.groupby('nama_provinsi')['icu_bed'].sum().reset_index()
        icu_by_province = icu_by_province.nlargest(10, 'icu_bed')
        
        fig = px.bar(
            icu_by_province,
            x='icu_bed',
            y='nama_provinsi',
            orientation='h',
            title='Top 10 Provinsi dengan Kapasitas ICU Tertinggi',
            color='icu_bed',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Hospital capacity vs COVID cases correlation
    if 'latest_stats' in data and len(data['latest_stats']) > 0:
        st.subheader("📊 Analisis Kapasitas vs Beban COVID-19")
        
        # Merge hospital capacity with COVID data
        capacity_summary = rs_data.groupby('nama_provinsi').agg({
            'total_bed': 'sum',
            'icu_bed': 'sum',
            'ventilator_count': 'sum'
        }).reset_index()
        
        covid_capacity = data['latest_stats'].merge(
            capacity_summary, 
            left_on='nama_provinsi', 
            right_on='nama_provinsi', 
            how='inner'
        )
        
        if len(covid_capacity) > 0:
            fig = px.scatter(
                covid_capacity,
                x='total_bed',
                y='total_aktif',
                size='icu_bed',
                color='ventilator_count',
                hover_name='nama_provinsi',
                title='Kapasitas Tempat Tidur vs Kasus Aktif (Size=ICU, Color=Ventilator)',
                labels={
                    'total_bed': 'Total Tempat Tidur',
                    'total_aktif': 'Kasus Aktif',
                    'ventilator_count': 'Jumlah Ventilator'
                }
            )
            st.plotly_chart(fig, use_container_width=True)

def create_vaccination_dashboard(data):
    """Create vaccination analytics dashboard"""
    st.markdown('<div class="section-header">💉 Dashboard Analitik Vaksinasi</div>', unsafe_allow_html=True)
    
    if 'vaksinasi' not in data or len(data['vaksinasi']) == 0:
        st.warning("Data vaksinasi tidak tersedia")
        return
    
    vaksin_data = data['vaksinasi'].copy()
    vaksin_data['tanggal'] = pd.to_datetime(vaksin_data['tanggal'])
    
    # Vaccination progress over time
    st.subheader("📈 Progress Vaksinasi Nasional")
    
    # Aggregate national vaccination data
    national_vaksin = vaksin_data.groupby('tanggal').agg({
        'dosis_1': 'sum',
        'dosis_2': 'sum', 
        'dosis_booster': 'sum',
        'vaksin_sinovac': 'sum',
        'vaksin_astrazeneca': 'sum',
        'vaksin_pfizer': 'sum',
        'vaksin_moderna': 'sum'
    }).reset_index()
    
    # Calculate cumulative
    national_vaksin['cumulative_dosis_1'] = national_vaksin['dosis_1'].cumsum()
    national_vaksin['cumulative_dosis_2'] = national_vaksin['dosis_2'].cumsum()
    national_vaksin['cumulative_booster'] = national_vaksin['dosis_booster'].cumsum()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Cumulative vaccination progress
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=national_vaksin['tanggal'],
            y=national_vaksin['cumulative_dosis_1'],
            mode='lines',
            name='Dosis 1',
            fill='tonexty',
            line=dict(color='#1f77b4')
        ))
        
        fig.add_trace(go.Scatter(
            x=national_vaksin['tanggal'],
            y=national_vaksin['cumulative_dosis_2'],
            mode='lines',
            name='Dosis 2',
            fill='tonexty',
            line=dict(color='#ff7f0e')
        ))
        
        fig.add_trace(go.Scatter(
            x=national_vaksin['tanggal'],
            y=national_vaksin['cumulative_booster'],
            mode='lines',
            name='Booster',
            fill='tonexty',
            line=dict(color='#2ca02c')
        ))
        
        fig.update_layout(
            title='Progress Kumulatif Vaksinasi',
            xaxis_title='Tanggal',
            yaxis_title='Jumlah Dosis',
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Vaccine brand distribution
        latest_brands = national_vaksin.iloc[-1]
        brand_data = {
            'Sinovac': latest_brands['vaksin_sinovac'],
            'AstraZeneca': latest_brands['vaksin_astrazeneca'],
            'Pfizer': latest_brands['vaksin_pfizer'],
            'Moderna': latest_brands['vaksin_moderna']
        }
        
        fig = px.pie(
            values=list(brand_data.values()),
            names=list(brand_data.keys()),
            title='Distribusi Jenis Vaksin (Data Terkini)',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig, use_container_width=True)

def create_policy_dashboard(data):
    """Create policy impact analysis dashboard"""
    st.markdown('<div class="section-header">📋 Dashboard Dampak Kebijakan</div>', unsafe_allow_html=True)
    
    if 'kebijakan' not in data or len(data['kebijakan']) == 0:
        st.warning("Data kebijakan tidak tersedia")
        return
    
    kebijakan_data = data['kebijakan'].copy()
    kebijakan_data['tanggal_mulai'] = pd.to_datetime(kebijakan_data['tanggal_mulai'])
    kebijakan_data['tanggal_selesai'] = pd.to_datetime(kebijakan_data['tanggal_selesai'])
    
    # Policy timeline
    st.subheader("📅 Timeline Kebijakan COVID-19")
    
    # Create Gantt chart for policies
    fig = px.timeline(
        kebijakan_data.head(20),  # Show top 20 policies
        x_start="tanggal_mulai",
        x_end="tanggal_selesai",
        y="nama_provinsi",
        color="jenis_kebijakan",
        title="Timeline Kebijakan COVID-19 per Provinsi",
        hover_data=["tingkat_keketatan", "compliance_rate"]
    )
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Policy stringency analysis
        stringency_by_type = kebijakan_data.groupby('jenis_kebijakan')['tingkat_keketatan'].mean().reset_index()
        
        fig = px.bar(
            stringency_by_type,
            x='jenis_kebijakan',
            y='tingkat_keketatan',
            title='Rata-rata Tingkat Keketatan per Jenis Kebijakan',
            color='tingkat_keketatan',
            color_continuous_scale='Reds'
        )
        fig.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Compliance rate analysis
        compliance_by_type = kebijakan_data.groupby('jenis_kebijakan')['compliance_rate'].mean().reset_index()
        
        fig = px.bar(
            compliance_by_type,
            x='jenis_kebijakan',
            y='compliance_rate',
            title='Rata-rata Tingkat Kepatuhan per Jenis Kebijakan',
            color='compliance_rate',
            color_continuous_scale='Blues'
        )
        fig.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

def create_provincial_analysis(data):
    """Create detailed provincial analysis"""
    st.markdown('<div class="section-header">🔍 Analisis Detail Provinsi</div>', unsafe_allow_html=True)
    
    if 'daily_stats' not in data or len(data['daily_stats']) == 0:
        st.warning("Data harian tidak tersedia")
        return
    
    # Province selector
    provinces = sorted(data['daily_stats']['nama_provinsi'].unique())
    selected_province = st.selectbox("Pilih Provinsi untuk Analisis Detail:", provinces)
    
    if selected_province:
        province_data = data['daily_stats'][data['daily_stats']['nama_provinsi'] == selected_province].copy()
        province_data = province_data.sort_values('tanggal')
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Provincial trend (Original)
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=province_data['tanggal'],
                y=province_data['kasus_baru'],
                mode='lines',
                name='Kasus Baru',
                line=dict(color='blue')
            ))
            
            fig.add_trace(go.Scatter(
                x=province_data['tanggal'],
                y=province_data['sembuh_baru'],
                mode='lines',
                name='Sembuh Baru',
                line=dict(color='green')
            ))
            
            fig.add_trace(go.Scatter(
                x=province_data['tanggal'],
                y=province_data['kematian_baru'],
                mode='lines',
                name='Kematian Baru',
                line=dict(color='red')
            ))
            
            fig.update_layout(
                title=f'Tren Harian {selected_province}',
                xaxis_title='Tanggal',
                yaxis_title='Jumlah Kasus',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Provincial cumulative (Original)
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=province_data['tanggal'],
                y=province_data['total_kasus'],
                mode='lines',
                name='Total Kasus',
                fill='tonexty',
                line=dict(color='orange')
            ))
            
            fig.update_layout(
                title=f'Total Kasus Kumulatif {selected_province}',
                xaxis_title='Tanggal',
                yaxis_title='Total Kasus',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Latest stats for selected province
        latest_province = province_data.iloc[-1]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Kasus", f"{latest_province['total_kasus']:,}")
        with col2:
            st.metric("Total Sembuh", f"{latest_province['total_sembuh']:,}")
        with col3:
            st.metric("Total Meninggal", f"{latest_province['total_kematian']:,}")
        with col4:
            st.metric("Kasus Aktif", f"{latest_province['total_aktif']:,}")
        
        # Additional provincial data (if available)
        if 'rumah_sakit' in data and len(data['rumah_sakit']) > 0:
            province_rs = data['rumah_sakit'][data['rumah_sakit']['nama_provinsi'] == selected_province]
            if len(province_rs) > 0:
                st.subheader(f"🏥 Infrastruktur Kesehatan {selected_province}")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Rumah Sakit", f"{len(province_rs):,}")
                with col2:
                    st.metric("Total Beds", f"{province_rs['total_bed'].sum():,}")
                with col3:
                    st.metric("ICU Beds", f"{province_rs['icu_bed'].sum():,}")
                with col4:
                    st.metric("Ventilators", f"{province_rs['ventilator_count'].sum():,}")

def main():
    """Main comprehensive application"""
    # Header
    st.markdown(f'<h1 class="main-header">🦠 {supabase_config.app_title}</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <strong>🚀 Dashboard COVID-19 Indonesia</strong><br>
        Dashboard ini menggabungkan fitur dashboard original dengan 7 tabel enhancement baru untuk analisis yang komprehensif dan lengkap.
    </div>
    """, unsafe_allow_html=True)
    
    # Display connection status in sidebar (commented out for cleaner UI)
    # connection_ok = display_connection_status()
    
    # Test connection silently without displaying in sidebar
    connection_ok, _ = supabase_config.test_connection()
    
    if not connection_ok:
        st.error("❌ Tidak dapat terhubung ke database Supabase")
        st.info("Pastikan konfigurasi Supabase sudah benar di file .env")
        
        with st.expander("📋 Panduan Setup Supabase"):
            st.markdown("""
            ### Langkah-langkah Setup:
            
            1. **Buat akun Supabase** di https://supabase.com
            2. **Buat project baru** di dashboard Supabase
            3. **Copy file template**: `cp supabase.env.template .env`
            4. **Isi konfigurasi** di file `.env` dengan data dari Supabase:
               - SUPABASE_URL (dari Settings > API)
               - SUPABASE_ANON_KEY (dari Settings > API)
               - SUPABASE_DB_HOST (dari Settings > Database)
               - SUPABASE_DB_PASSWORD (password yang Anda buat)
            5. **Jalankan schema SQL** di Supabase SQL Editor:
               - Buka file `supabase_schema.sql`
               - Copy dan paste ke SQL Editor
               - Execute
            6. **Import data** menggunakan `supabase_data_import.py`
            7. **Restart aplikasi**
            """)
        return
    
    # Load all data
    with st.spinner("Memuat semua data dari database..."):
        data = load_all_data()
    
    if not data or len(data) == 0:
        st.error("Gagal memuat data. Pastikan database sudah disetup.")
        st.info("Jalankan script berikut untuk setup:")
        st.code("""
# Setup database
python supabase_data_import.py

# Setup enhanced tables (optional)
python generate_enhanced_dummy_data.py
python import_enhanced_data.py
        """)
        return
    
    # Check data availability
    has_original = 'latest_stats' in data and len(data['latest_stats']) > 0
    has_additional_data = any(len(data.get(table, [])) > 0 for table in ['rumah_sakit', 'vaksinasi', 'kebijakan'])
    
    if has_additional_data:
        st.markdown("""
        <div class="feature-highlight">
            ✅ <strong>Fitur Lengkap Tersedia!</strong> Dashboard ini memiliki akses ke data lengkap dengan analisis komprehensif.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="feature-highlight">
            ⚠️ <strong>Mode Dasar:</strong> Hanya data dasar yang tersedia. Jalankan setup tambahan untuk fitur lengkap.
        </div>
        """, unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("📊 Dashboard Navigation")
    st.sidebar.markdown("**COVID-19 Indonesia Dashboard**")
    # st.sidebar.markdown("*Powered by Supabase*")  # Commented for cleaner UI
    
    # Dynamic menu based on available data
    menu_options = ["🏠 KPI Terpadu", "🗺️ Geospasial & Tren", "🔍 Analisis Provinsi"]
    
    if has_additional_data:
        menu_options.extend([
            "🏥 Kapasitas Kesehatan", 
            "💉 Analitik Vaksinasi",
            "📋 Dampak Kebijakan"
        ])
    
    page = st.sidebar.selectbox("Pilih Dashboard:", menu_options)
    
    # Display selected dashboard
    if page == "🏠 KPI Terpadu":
        create_unified_kpi_dashboard(data)
        
    elif page == "🗺️ Geospasial & Tren":
        create_original_visualizations(data)
        
    elif page == "🔍 Analisis Provinsi":
        create_provincial_analysis(data)
        
    elif page == "🏥 Kapasitas Kesehatan" and has_additional_data:
        create_healthcare_dashboard(data)
        
    elif page == "💉 Analitik Vaksinasi" and has_additional_data:
        create_vaccination_dashboard(data)
        
    elif page == "📋 Dampak Kebijakan" and has_additional_data:
        create_policy_dashboard(data)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        📊 COVID-19 Indonesia Dashboard | 
        🦠 Core Data • 🏥 Healthcare • 💉 Vaccination • 📋 Policy • 💰 Economy
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
