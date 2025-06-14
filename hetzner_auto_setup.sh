#!/bin/bash

# OLX Scraper - Hetzner Cloud Automated Setup Script
# This script automates the complete deployment process on a fresh Ubuntu 22.04 server
# Author: Manus AI
# Version: 1.0

set -e  # Exit on any error

# Color codes for output formatting
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration variables
APP_DIR="/opt/olx-scraper"
APP_USER="olxuser"
PYTHON_VERSION="3.11"
CHROME_DRIVER_VERSION="112.0.5615.49"
SERVICE_NAME="olx-scraper"

# Function to print colored output with timestamps
print_status() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] [INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] [WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] [ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] [STEP]${NC} $1"
}

print_success() {
    echo -e "${PURPLE}[$(date '+%Y-%m-%d %H:%M:%S')] [SUCCESS]${NC} $1"
}

# Function to check if running as root
check_root() {
    if [ "$EUID" -ne 0 ]; then
        print_error "This script must be run as root. Please use 'sudo' or run as root user."
        exit 1
    fi
}

# Function to detect OS and version
detect_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$NAME
        VERSION=$VERSION_ID
    else
        print_error "Cannot detect operating system. This script requires Ubuntu 22.04 or later."
        exit 1
    fi
    
    if [[ "$OS" != *"Ubuntu"* ]] || [[ "$VERSION" < "22.04" ]]; then
        print_warning "This script is optimized for Ubuntu 22.04. Your system: $OS $VERSION"
        read -p "Do you want to continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# Function to update system packages
update_system() {
    print_step "Updating system packages..."
    
    # Update package lists
    apt update -qq
    
    # Upgrade existing packages
    DEBIAN_FRONTEND=noninteractive apt upgrade -y -qq
    
    # Install essential packages
    apt install -y -qq \
        curl \
        wget \
        unzip \
        git \
        nano \
        htop \
        jq \
        cron \
        logrotate \
        ufw \
        fail2ban \
        software-properties-common \
        apt-transport-https \
        ca-certificates \
        gnupg \
        lsb-release
    
    print_success "System packages updated successfully"
}

# Function to install Python and dependencies
install_python() {
    print_step "Installing Python and dependencies..."
    
    # Install Python 3 and related packages
    apt install -y -qq \
        python3 \
        python3-pip \
        python3-venv \
        python3-dev \
        python3-setuptools \
        python3-wheel \
        build-essential
    
    # Upgrade pip to latest version
    python3 -m pip install --upgrade pip
    
    # Verify Python installation
    PYTHON_VER=$(python3 --version | cut -d' ' -f2)
    print_success "Python $PYTHON_VER installed successfully"
}

# Function to install Chrome/Chromium and ChromeDriver
install_chrome() {
    print_step "Installing Chrome/Chromium browser and ChromeDriver..."
    
    # Install Chromium browser
    apt install -y -qq chromium-browser
    
    # Get installed Chrome version
    CHROME_VERSION=$(chromium-browser --version | grep -oP '\d+\.\d+\.\d+\.\d+' | head -1)
    print_status "Detected Chrome version: $CHROME_VERSION"
    
    # Download and install compatible ChromeDriver
    print_status "Downloading ChromeDriver version $CHROME_DRIVER_VERSION..."
    
    cd /tmp
    wget -q "https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip" -O chromedriver.zip
    
    if [ $? -eq 0 ]; then
        unzip -q chromedriver.zip
        mv chromedriver /usr/local/bin/
        chmod +x /usr/local/bin/chromedriver
        rm chromedriver.zip LICENSE.chromedriver 2>/dev/null || true
        print_success "ChromeDriver installed successfully"
    else
        print_warning "Failed to download ChromeDriver $CHROME_DRIVER_VERSION, trying alternative..."
        # Try to use webdriver-manager as fallback
        python3 -m pip install webdriver-manager
        print_status "Installed webdriver-manager as fallback"
    fi
    
    # Verify ChromeDriver installation
    if command -v chromedriver &> /dev/null; then
        DRIVER_VERSION=$(chromedriver --version | cut -d' ' -f2)
        print_success "ChromeDriver $DRIVER_VERSION is ready"
    fi
}

# Function to create application user
create_app_user() {
    print_step "Creating application user..."
    
    # Create user if it doesn't exist
    if ! id "$APP_USER" &>/dev/null; then
        useradd -r -m -s /bin/bash "$APP_USER"
        usermod -aG sudo "$APP_USER"
        print_success "Created user: $APP_USER"
    else
        print_status "User $APP_USER already exists"
    fi
}

# Function to setup application directory
setup_app_directory() {
    print_step "Setting up application directory..."
    
    # Create application directory
    mkdir -p "$APP_DIR"
    mkdir -p "$APP_DIR/logs"
    mkdir -p "$APP_DIR/data"
    mkdir -p "$APP_DIR/backups"
    
    # Set ownership and permissions
    chown -R "$APP_USER:$APP_USER" "$APP_DIR"
    chmod 755 "$APP_DIR"
    chmod 755 "$APP_DIR/logs"
    chmod 755 "$APP_DIR/data"
    chmod 700 "$APP_DIR/backups"
    
    print_success "Application directory created: $APP_DIR"
}

# Function to check for application files
check_app_files() {
    print_step "Checking for application files..."
    
    REQUIRED_FILES=(
        "olx_scraper.py"
        "gohighlevel_integration.py"
        "scheduler.py"
        "requirements.txt"
        ".env.example"
    )
    
    MISSING_FILES=()
    
    for file in "${REQUIRED_FILES[@]}"; do
        if [ ! -f "$APP_DIR/$file" ]; then
            MISSING_FILES+=("$file")
        fi
    done
    
    if [ ${#MISSING_FILES[@]} -gt 0 ]; then
        print_error "Missing required application files:"
        for file in "${MISSING_FILES[@]}"; do
            echo "  - $file"
        done
        print_error "Please upload the application files to $APP_DIR before running this script"
        print_status "You can upload files using: scp olx_scraper_updated.zip root@YOUR_SERVER_IP:$APP_DIR/"
        print_status "Then extract: cd $APP_DIR && unzip olx_scraper_updated.zip"
        exit 1
    fi
    
    print_success "All required application files found"
}

# Function to install Python dependencies
install_python_deps() {
    print_step "Installing Python dependencies..."
    
    cd "$APP_DIR"
    
    # Create virtual environment
    sudo -u "$APP_USER" python3 -m venv venv
    
    # Activate virtual environment and install dependencies
    sudo -u "$APP_USER" bash -c "
        source venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt
    "
    
    print_success "Python dependencies installed in virtual environment"
}

# Function to configure application
configure_app() {
    print_step "Configuring application..."
    
    cd "$APP_DIR"
    
    # Make scripts executable
    chmod +x *.py
    
    # Create .env file if it doesn't exist
    if [ ! -f ".env" ]; then
        cp .env.example .env
        chown "$APP_USER:$APP_USER" .env
        chmod 600 .env
        print_warning "Created .env file from template. Please edit it with your settings."
    fi
    
    # Set proper ownership
    chown -R "$APP_USER:$APP_USER" "$APP_DIR"
    
    print_success "Application configured successfully"
}

# Function to create systemd service
create_systemd_service() {
    print_step "Creating systemd service..."
    
    cat > "/etc/systemd/system/${SERVICE_NAME}.service" << EOF
[Unit]
Description=OLX Job Scraper
Documentation=https://github.com/your-repo/olx-scraper
After=network.target network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$APP_USER
Group=$APP_USER
WorkingDirectory=$APP_DIR
Environment=PATH=$APP_DIR/venv/bin
ExecStart=$APP_DIR/venv/bin/python $APP_DIR/scheduler.py --interval 24 --headless --run-now
ExecReload=/bin/kill -HUP \$MAINPID
Restart=always
RestartSec=300
TimeoutStopSec=30
KillMode=mixed
StandardOutput=journal
StandardError=journal
SyslogIdentifier=olx-scraper

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=$APP_DIR
ProtectKernelTunables=true
ProtectKernelModules=true
ProtectControlGroups=true

[Install]
WantedBy=multi-user.target
EOF
    
    # Reload systemd and enable service
    systemctl daemon-reload
    systemctl enable "$SERVICE_NAME"
    
    print_success "Systemd service created and enabled"
}

# Function to setup log rotation
setup_log_rotation() {
    print_step "Setting up log rotation..."
    
    cat > "/etc/logrotate.d/olx-scraper" << EOF
$APP_DIR/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    copytruncate
    create 644 $APP_USER $APP_USER
}

$APP_DIR/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    copytruncate
    create 644 $APP_USER $APP_USER
}
EOF
    
    print_success "Log rotation configured"
}

# Function to create monitoring script
create_monitoring() {
    print_step "Creating monitoring and maintenance scripts..."
    
    cat > "$APP_DIR/monitor.sh" << 'EOF'
#!/bin/bash

# OLX Scraper Monitoring Script
# This script monitors the health of the OLX scraper service

APP_DIR="/opt/olx-scraper"
SERVICE_NAME="olx-scraper"
LOG_FILE="$APP_DIR/logs/monitor.log"
MAX_DISK_USAGE=80
MAX_HOURS_WITHOUT_UPDATE=48

# Ensure log directory exists
mkdir -p "$APP_DIR/logs"

# Function to log messages
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Check if service is running
if ! systemctl is-active --quiet "$SERVICE_NAME"; then
    log_message "ERROR: $SERVICE_NAME service is down, attempting restart..."
    systemctl restart "$SERVICE_NAME"
    if systemctl is-active --quiet "$SERVICE_NAME"; then
        log_message "SUCCESS: $SERVICE_NAME service restarted successfully"
    else
        log_message "CRITICAL: Failed to restart $SERVICE_NAME service"
    fi
fi

# Check disk usage
DISK_USAGE=$(df "$APP_DIR" | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt "$MAX_DISK_USAGE" ]; then
    log_message "WARNING: Disk usage is ${DISK_USAGE}%, cleaning old logs..."
    find "$APP_DIR" -name "*.log" -mtime +7 -delete
    find "$APP_DIR/logs" -name "*.log.gz" -mtime +30 -delete
    log_message "INFO: Log cleanup completed"
fi

# Check if results file is being updated
if [ -f "$APP_DIR/olx_results.json" ]; then
    LAST_MODIFIED=$(stat -c %Y "$APP_DIR/olx_results.json" 2>/dev/null || echo 0)
    CURRENT_TIME=$(date +%s)
    HOURS_SINCE_UPDATE=$(( (CURRENT_TIME - LAST_MODIFIED) / 3600 ))
    
    if [ "$HOURS_SINCE_UPDATE" -gt "$MAX_HOURS_WITHOUT_UPDATE" ]; then
        log_message "WARNING: Results file not updated for ${HOURS_SINCE_UPDATE} hours"
    fi
fi

# Check memory usage
MEMORY_USAGE=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100.0}')
if [ "$MEMORY_USAGE" -gt 90 ]; then
    log_message "WARNING: High memory usage: ${MEMORY_USAGE}%"
fi

# Check if Chrome processes are accumulating
CHROME_PROCESSES=$(pgrep -c chromium || echo 0)
if [ "$CHROME_PROCESSES" -gt 5 ]; then
    log_message "WARNING: Multiple Chrome processes detected: $CHROME_PROCESSES"
    # Kill orphaned Chrome processes
    pkill -f chromium || true
    log_message "INFO: Cleaned up Chrome processes"
fi

# Rotate monitor log if it gets too large
if [ -f "$LOG_FILE" ] && [ $(stat -c%s "$LOG_FILE") -gt 10485760 ]; then  # 10MB
    mv "$LOG_FILE" "${LOG_FILE}.old"
    log_message "INFO: Monitor log rotated"
fi
EOF
    
    chmod +x "$APP_DIR/monitor.sh"
    chown "$APP_USER:$APP_USER" "$APP_DIR/monitor.sh"
    
    # Create backup script
    cat > "$APP_DIR/backup.sh" << 'EOF'
#!/bin/bash

# OLX Scraper Backup Script
# This script creates backups of important data and configuration

APP_DIR="/opt/olx-scraper"
BACKUP_DIR="$APP_DIR/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="olx_scraper_backup_$DATE.tar.gz"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Create backup
tar -czf "$BACKUP_DIR/$BACKUP_FILE" \
    --exclude="$APP_DIR/venv" \
    --exclude="$APP_DIR/logs" \
    --exclude="$APP_DIR/backups" \
    --exclude="$APP_DIR/__pycache__" \
    -C "$(dirname "$APP_DIR")" \
    "$(basename "$APP_DIR")"

# Keep only last 7 backups
cd "$BACKUP_DIR"
ls -t olx_scraper_backup_*.tar.gz | tail -n +8 | xargs -r rm

echo "Backup created: $BACKUP_DIR/$BACKUP_FILE"
EOF
    
    chmod +x "$APP_DIR/backup.sh"
    chown "$APP_USER:$APP_USER" "$APP_DIR/backup.sh"
    
    print_success "Monitoring and backup scripts created"
}

# Function to setup cron jobs
setup_cron() {
    print_step "Setting up cron jobs..."
    
    # Create cron jobs for the app user
    sudo -u "$APP_USER" bash -c "
        (crontab -l 2>/dev/null || echo '') | grep -v 'olx-scraper' > /tmp/crontab_temp
        echo '# OLX Scraper monitoring - every 30 minutes' >> /tmp/crontab_temp
        echo '*/30 * * * * $APP_DIR/monitor.sh' >> /tmp/crontab_temp
        echo '# OLX Scraper backup - daily at 2 AM' >> /tmp/crontab_temp
        echo '0 2 * * * $APP_DIR/backup.sh' >> /tmp/crontab_temp
        crontab /tmp/crontab_temp
        rm /tmp/crontab_temp
    "
    
    # Ensure cron service is running
    systemctl enable cron
    systemctl start cron
    
    print_success "Cron jobs configured"
}

# Function to configure firewall
configure_firewall() {
    print_step "Configuring firewall..."
    
    # Reset UFW to defaults
    ufw --force reset
    
    # Set default policies
    ufw default deny incoming
    ufw default allow outgoing
    
    # Allow SSH
    ufw allow ssh
    ufw allow 22/tcp
    
    # Allow HTTP and HTTPS for scraping
    ufw allow out 80/tcp
    ufw allow out 443/tcp
    
    # Allow DNS
    ufw allow out 53
    
    # Enable firewall
    ufw --force enable
    
    print_success "Firewall configured"
}

# Function to configure fail2ban
configure_fail2ban() {
    print_step "Configuring fail2ban..."
    
    # Create jail configuration
    cat > "/etc/fail2ban/jail.local" << EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
EOF
    
    # Start and enable fail2ban
    systemctl enable fail2ban
    systemctl start fail2ban
    
    print_success "Fail2ban configured"
}

# Function to run initial tests
run_tests() {
    print_step "Running initial tests..."
    
    cd "$APP_DIR"
    
    # Test Python environment
    sudo -u "$APP_USER" bash -c "
        source venv/bin/activate
        python -c 'import selenium, requests, schedule; print(\"Python dependencies OK\")'
    "
    
    # Test Chrome/ChromeDriver
    if command -v chromedriver &> /dev/null; then
        print_status "ChromeDriver test: OK"
    else
        print_warning "ChromeDriver not found in PATH"
    fi
    
    # Test application import
    sudo -u "$APP_USER" bash -c "
        source venv/bin/activate
        cd '$APP_DIR'
        python -c 'import olx_scraper; print(\"Application import: OK\")'
    " 2>/dev/null || print_warning "Application import test failed - check configuration"
    
    print_success "Initial tests completed"
}

# Function to display final instructions
show_final_instructions() {
    print_success "🎉 OLX Scraper installation completed successfully!"
    echo
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${CYAN}📋 NEXT STEPS:${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo
    echo -e "${YELLOW}1. Configure your settings:${NC}"
    echo "   nano $APP_DIR/.env"
    echo "   # Add your GoHighLevel API key and adjust settings"
    echo
    echo -e "${YELLOW}2. Test the scraper:${NC}"
    echo "   cd $APP_DIR"
    echo "   sudo -u $APP_USER bash -c 'source venv/bin/activate && python olx_scraper.py --headless --max-pages 1 --max-listings 3'"
    echo
    echo -e "${YELLOW}3. Start the service:${NC}"
    echo "   systemctl start $SERVICE_NAME"
    echo "   systemctl status $SERVICE_NAME"
    echo
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${CYAN}📊 MONITORING COMMANDS:${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo
    echo "• View service logs:     journalctl -u $SERVICE_NAME -f"
    echo "• Check service status:  systemctl status $SERVICE_NAME"
    echo "• View scraper results:  cat $APP_DIR/olx_results.json | jq"
    echo "• Monitor system:        htop"
    echo "• Check disk usage:      df -h"
    echo "• View monitor logs:     tail -f $APP_DIR/logs/monitor.log"
    echo
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${CYAN}🔧 MANAGEMENT COMMANDS:${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo
    echo "• Start service:         systemctl start $SERVICE_NAME"
    echo "• Stop service:          systemctl stop $SERVICE_NAME"
    echo "• Restart service:       systemctl restart $SERVICE_NAME"
    echo "• Disable service:       systemctl disable $SERVICE_NAME"
    echo "• Run manual backup:     $APP_DIR/backup.sh"
    echo "• Run monitor check:     $APP_DIR/monitor.sh"
    echo
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${CYAN}💰 COST INFORMATION:${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo
    echo "• Hetzner CX11 Server:   €3.29/month"
    echo "• Traffic included:      20TB/month"
    echo "• Backups (optional):    €1.31/month"
    echo "• Total estimated:       ~€4.60/month"
    echo
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${GREEN}🚀 Your OLX scraper will run automatically every 24 hours!${NC}"
    echo -e "${GREEN}📞 It will find manufacturing companies and send them to GoHighLevel!${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# Main execution function
main() {
    echo -e "${PURPLE}"
    echo "╔══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                    OLX Scraper - Hetzner Cloud Setup                        ║"
    echo "║                           Automated Installation                            ║"
    echo "║                              Version 1.0                                    ║"
    echo "╚══════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo
    
    # Pre-flight checks
    check_root
    detect_os
    
    # Main installation steps
    update_system
    install_python
    install_chrome
    create_app_user
    setup_app_directory
    check_app_files
    install_python_deps
    configure_app
    create_systemd_service
    setup_log_rotation
    create_monitoring
    setup_cron
    configure_firewall
    configure_fail2ban
    run_tests
    
    # Show final instructions
    show_final_instructions
}

# Execute main function
main "$@"

