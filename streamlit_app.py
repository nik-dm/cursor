# Streamlit Cloud Entry Point
# This file serves as the main entry point for Streamlit Cloud deployment

import sys
from pathlib import Path

# Ensure the ui directory is in the path
ui_path = Path(__file__).parent / "ui"
sys.path.insert(0, str(ui_path))

# Import and run the main app
from app import main

if __name__ == "__main__":
    main()