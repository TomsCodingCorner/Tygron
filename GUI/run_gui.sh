#!/bin/bash

# Activeer Python environment (indien nodig)
# source venv/bin/activate

echo "Starting Tygron AI Object Detection GUI..."
echo "Make sure you have:"
echo "1. Installed requirements: pip install -r requirements.txt"
echo "2. .pt model files in ../Models/ directory"
echo "3. Test images ready for upload"
echo ""
echo "Opening GUI in browser..."

# Start Streamlit app
streamlit run GUI.py --server.port 8501 --server.address localhost

echo "GUI has been stopped."
