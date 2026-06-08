#!/bin/bash

# XT Shipping Governance Demo - Fixed Version
# This version implements proper governance controls and security measures

echo "🚢 Starting XT Shipping Management System (Fixed Version)..."
echo "✅ This version implements proper governance and security controls"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Initialize database
echo "Initializing database..."
cd database
python3 init_db_fixed.py
cd ..

# Start the application
echo ""
echo "✅ Application starting on http://localhost:5001"
echo "📝 Login credentials: admin / 0000"
echo ""
python3 app.py

# Made with Bob
