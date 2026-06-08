#!/bin/bash

# XT Shipping Governance Demo - Broken Version
# This version contains intentional governance and security issues for demonstration

echo "🚢 Starting XT Shipping Management System (Broken Version)..."
echo "⚠️  This version contains intentional governance and security issues"
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
pip install --index-url https://pypi.org/simple/ Flask==3.0.0 python-dotenv==1.0.0

# Initialize database
echo "Initializing database..."
cd database
python3 init_db.py
cd ..

# Start the application
echo ""
echo "✅ Application starting on http://localhost:5000"
echo "📝 Login credentials: admin / admin123"
echo ""
python3 app.py

# Made with Bob
