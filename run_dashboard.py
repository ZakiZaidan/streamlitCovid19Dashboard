#!/usr/bin/env python3
"""
Simple launcher for COVID-19 Indonesia Dashboard
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Launch the Streamlit dashboard"""
    print("🦠 COVID-19 Indonesia Dashboard")
    print("=" * 40)
    
    # Check if .env file exists
    if not Path(".env").exists():
        print("❌ File .env tidak ditemukan!")
        print("📋 Silakan copy supabase.env.template ke .env dan isi konfigurasi Supabase")
        print("   cp supabase.env.template .env")
        return
    
    # Check if main dashboard file exists
    if not Path("streamlit_supabase_app.py").exists():
        print("❌ File streamlit_supabase_app.py tidak ditemukan!")
        return
    
    print("🚀 Meluncurkan dashboard...")
    print("📱 Dashboard akan terbuka di browser pada http://localhost:8501")
    print("⏹️  Tekan Ctrl+C untuk menghentikan dashboard")
    print()
    
    try:
        # Run Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "streamlit_supabase_app.py",
            "--server.headless", "true",
            "--server.address", "localhost",
            "--server.port", "8501"
        ])
    except KeyboardInterrupt:
        print("\n👋 Dashboard dihentikan. Terima kasih!")
    except FileNotFoundError:
        print("❌ Streamlit tidak terinstall!")
        print("📦 Install dengan: pip install -r requirements_supabase.txt")

if __name__ == "__main__":
    main()
