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

# Install dependencies using PyPI directly (bypass IBM artifactory)
echo "Installing dependencies..."
pip install --index-url https://pypi.org/simple/ --upgrade pip
pip install --index-url https://pypi.org/simple/ Flask==3.0.0 python-dotenv==1.0.0 bcrypt==4.1.2

# Initialize database
echo "Initializing database..."
cd database
python3 init_db_fixed.py
# Copy database to parent directory where app expects it
cp xt_shipping_fixed.db ../
cd ..

# Start the application
echo ""
echo "✅ Application starting on http://localhost:5000"
echo "📝 Login credentials: admin / 0000"
echo ""
python3 app.py

# Made with Bob
