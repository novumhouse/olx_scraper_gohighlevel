#!/bin/bash

# OLX Scraper - Quick Setup Script for Hetzner Cloud
# This is a simplified version for quick deployment
# Author: Manus AI

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}🚀 OLX Scraper Quick Setup for Hetzner Cloud${NC}"
echo "=============================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Please run as root: sudo ./quick_setup.sh${NC}"
    exit 1
fi

echo -e "${YELLOW}📦 Installing system packages...${NC}"
apt update -qq && apt upgrade -y -qq
apt install -y -qq python3 python3-pip python3-venv chromium-browser unzip curl wget nano htop cron ufw

echo -e "${YELLOW}🔧 Setting up application directory...${NC}"
mkdir -p /opt/olx-scraper
cd /opt/olx-scraper

# Check for application files
if [ ! -f "olx_scraper.py" ]; then
    echo -e "${RED}❌ Application files not found!${NC}"
    echo "Please upload and extract olx_scraper_updated.zip first:"
    echo "  scp olx_scraper_updated.zip root@YOUR_SERVER_IP:/opt/olx-scraper/"
    echo "  cd /opt/olx-scraper && unzip olx_scraper_updated.zip"
    exit 1
fi

echo -e "${YELLOW}🐍 Setting up Python environment...${NC}"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q

echo -e "${YELLOW}🌐 Installing ChromeDriver...${NC}"
wget -q "https://chromedriver.storage.googleapis.com/112.0.5615.49/chromedriver_linux64.zip"
unzip -q chromedriver_linux64.zip
mv chromedriver /usr/local/bin/
chmod +x /usr/local/bin/chromedriver
rm chromedriver_linux64.zip

echo -e "${YELLOW}⚙️ Configuring application...${NC}"
chmod +x *.py
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${YELLOW}📝 Created .env file - please edit it with your settings${NC}"
fi

echo -e "${YELLOW}🔥 Setting up firewall...${NC}"
ufw --force enable
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh

echo -e "${YELLOW}⏰ Setting up service...${NC}"
cat > /etc/systemd/system/olx-scraper.service << 'EOF'
[Unit]
Description=OLX Job Scraper
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/olx-scraper
Environment=PATH=/opt/olx-scraper/venv/bin
ExecStart=/opt/olx-scraper/venv/bin/python /opt/olx-scraper/scheduler.py --interval 24 --headless --run-now
Restart=always
RestartSec=300

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable olx-scraper

echo -e "${GREEN}✅ Quick setup completed!${NC}"
echo ""
echo "📋 Next steps:"
echo "1. Edit configuration: nano /opt/olx-scraper/.env"
echo "2. Add your GoHighLevel API key"
echo "3. Test: cd /opt/olx-scraper && source venv/bin/activate && python olx_scraper.py --headless --max-pages 1 --max-listings 3"
echo "4. Start service: systemctl start olx-scraper"
echo "5. Check status: systemctl status olx-scraper"
echo ""
echo -e "${GREEN}🎯 Your scraper will run every 24 hours automatically!${NC}"

