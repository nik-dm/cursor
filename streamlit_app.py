import streamlit as st
import sys
from pathlib import Path

# Add ui directory to path
sys.path.insert(0, str(Path(__file__).parent / "ui"))

# Import and run the main app
from app import main

if __name__ == "__main__":
    main()