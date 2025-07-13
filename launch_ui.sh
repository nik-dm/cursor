#!/bin/bash

# LinkedIn Automation Bot - Web UI Launcher (Shell Script)

echo "🚀 LinkedIn Automation Bot - Web UI"
echo "=================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed."
    exit 1
fi

# Check if Streamlit is installed
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "❌ Streamlit not installed. Installing dependencies..."
    pip3 install -r requirements.txt
fi

echo "📖 Starting LinkedIn Bot Dashboard..."
echo "🌐 Access at: http://localhost:8501"
echo "🔐 Login: admin / admin123"
echo "=================================="
echo "Press Ctrl+C to stop the server"
echo "=================================="

# Launch the Streamlit app
python3 -m streamlit run ui/app.py \
    --server.port 8501 \
    --server.address localhost \
    --browser.gatherUsageStats false