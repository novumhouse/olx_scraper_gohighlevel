#!/bin/bash

# OLX Scraper Setup Script

echo "Setting up OLX Scraper with GoHighLevel Integration..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "Please edit the .env file to configure your settings."
fi

# Make scripts executable
chmod +x olx_scraper.py
chmod +x gohighlevel_integration.py
chmod +x scheduler.py

echo "Setup complete!"
echo "To run the scraper:"
echo "  source venv/bin/activate"
echo "  python olx_scraper.py"
echo ""
echo "To schedule the scraper:"
echo "  source venv/bin/activate"
echo "  python scheduler.py --run-now"
echo ""
echo "Don't forget to edit the .env file with your GoHighLevel API key!"

