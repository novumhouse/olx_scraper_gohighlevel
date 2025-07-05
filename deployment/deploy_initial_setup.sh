#!/bin/bash
# OLX Multi-Client Scraper - Initial Setup Deployment Script
# This script sets up everything from scratch on a Hetzner server

set -e

echo "🚀 Initial Setup - OLX Multi-Client Scraper on Hetzner"
echo "======================================================="

# Configuration
SERVER_IP="${HETZNER_IP:-188.245.58.182}"
SERVER_USER="${HETZNER_USER:-root}"
PUBLIC_REPO="https://github.com/novumhouse/olx_scraper_gohighlevel.git"
INSTALL_DIR="/opt/olx-scraper"

echo "🖥️  Server: $SERVER_USER@$SERVER_IP"
echo "🔗 Repository: $PUBLIC_REPO"
echo "📁 Install Directory: $INSTALL_DIR"

# Test SSH connection
echo "🔍 Testing SSH connection..."
ssh -o ConnectTimeout=10 $SERVER_USER@$SERVER_IP "echo 'SSH connection successful!'"

# Deploy to server
ssh $SERVER_USER@$SERVER_IP << 'ENDSSH'
    set -e
    
    echo "📦 Updating system packages..."
    apt update && apt upgrade -y
    
    echo "🐍 Installing Python and dependencies..."
    apt install -y python3 python3-pip python3-venv git curl wget unzip
    
    echo "🌐 Installing Google Chrome and ChromeDriver..."
    # Install Chrome
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
    apt update
    apt install -y google-chrome-stable
    
    # Install ChromeDriver
    CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+')
    echo "Chrome version: $CHROME_VERSION"
    
    echo "📁 Setting up application directory..."
    mkdir -p /opt/olx-scraper
    cd /opt/olx-scraper
    
    echo "🔗 Cloning repository..."
    if [ -d ".git" ]; then
        git pull origin main
    else
        git clone https://github.com/novumhouse/olx_scraper_gohighlevel.git .
    fi
    
    echo "🔧 Setting up Python virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    
    echo "📦 Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    echo "📁 Creating directories..."
    mkdir -p logs backup config
    
    echo "🔧 Setting permissions..."
    chown -R root:root /opt/olx-scraper
    chmod +x *.py
    
    echo "⚙️  Creating systemd service..."
    cat > /etc/systemd/system/olx-multi-scraper.service << EOF
[Unit]
Description=OLX Multi-Client Scraper Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/olx-scraper
Environment=PATH=/opt/olx-scraper/venv/bin
ExecStart=/opt/olx-scraper/venv/bin/python multi_client_scheduler.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    
    echo "🔄 Enabling systemd service..."
    systemctl daemon-reload
    systemctl enable olx-multi-scraper
    
    echo "✅ Initial setup complete!"
    echo "📍 Application installed in: /opt/olx-scraper"
    echo "🔧 Service created: olx-multi-scraper"
    echo "📝 Next steps:"
    echo "   1. Add configuration file: /opt/olx-scraper/clients_config.json"
    echo "   2. Start service: systemctl start olx-multi-scraper"
    echo "   3. Check status: systemctl status olx-multi-scraper"
    echo "   4. View logs: journalctl -u olx-multi-scraper -f"
ENDSSH

echo ""
echo "🎉 Initial deployment completed successfully!"
echo ""
echo "📋 Next Steps:"
echo "1. Update config/clients_config.json with your real API credentials"
echo "2. Copy configuration to server"
echo "3. Start the service"
echo ""
echo "🔧 Commands to finish setup:"
echo "   scp config/clients_config.json $SERVER_USER@$SERVER_IP:$INSTALL_DIR/"
echo "   ssh $SERVER_USER@$SERVER_IP 'systemctl start olx-multi-scraper'"
echo "   ssh $SERVER_USER@$SERVER_IP 'systemctl status olx-multi-scraper'" 