#!/usr/bin/env python3
"""
LinkedIn Automation Bot - Web UI Launcher

This script launches the Streamlit web interface for the LinkedIn automation bot.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import streamlit
        import plotly
        import streamlit_authenticator
        return True
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def launch_ui():
    """Launch the Streamlit UI"""
    if not check_dependencies():
        return
    
    print("🚀 Launching LinkedIn Automation Bot Web UI...")
    print("=" * 50)
    print("📖 Access the dashboard at: http://localhost:8501")
    print("🔐 Default credentials:")
    print("   Username: admin")
    print("   Password: admin123")
    print("=" * 50)
    print("⚠️  Important: Change default credentials in production!")
    print("=" * 50)
    
    # Set up environment
    ui_path = Path(__file__).parent / "ui"
    app_path = ui_path / "app.py"
    
    if not app_path.exists():
        print(f"❌ UI app not found at {app_path}")
        return
    
    # Launch Streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            str(app_path),
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 LinkedIn Bot UI stopped")
    except Exception as e:
        print(f"❌ Error launching UI: {e}")

if __name__ == "__main__":
    launch_ui()