#!/usr/bin/env python3
"""
LinkedIn Automation Bot - Simple UI Launcher

This script launches the Streamlit web interface with minimal dependencies
to avoid installation conflicts.
"""

import subprocess
import sys
import os
from pathlib import Path

def install_minimal_requirements():
    """Install minimal requirements for UI testing"""
    print("📦 Installing minimal UI dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements-minimal.txt"
        ])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def launch_ui():
    """Launch the Streamlit UI"""
    print("🚀 Launching LinkedIn Automation Bot Web UI...")
    print("=" * 50)
    print("📖 Access the dashboard at: http://localhost:8501")
    print("🔐 Default credentials:")
    print("   Username: admin")
    print("   Password: admin123")
    print("=" * 50)
    print("⚠️  Note: This is a simplified version for testing!")
    print("=" * 50)
    
    # Set up environment
    ui_path = Path(__file__).parent / "ui"
    app_path = ui_path / "app.py"
    
    if not app_path.exists():
        print(f"❌ UI app not found at {app_path}")
        return
    
    # Install minimal requirements
    if not install_minimal_requirements():
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