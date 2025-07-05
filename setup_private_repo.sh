#!/bin/bash
# 🔧 Setup script for private OLX scraper repository
# This script creates the proper directory structure and files for your private repository

set -e

PRIVATE_REPO_NAME="olx-scraper-private"
CURRENT_DIR=$(pwd)

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_info "🚀 Setting up private OLX scraper repository..."

# Create private repository directory
if [ -d "../${PRIVATE_REPO_NAME}" ]; then
    log_warn "Directory ../${PRIVATE_REPO_NAME} already exists. Skipping creation."
else
    log_info "📁 Creating private repository directory..."
    mkdir -p "../${PRIVATE_REPO_NAME}"
fi

cd "../${PRIVATE_REPO_NAME}"

# Initialize git repository
if [ ! -d ".git" ]; then
    log_info "🔧 Initializing git repository..."
    git init
    git branch -m main
fi

# Create directory structure
log_info "📂 Creating directory structure..."
mkdir -p config
mkdir -p deployment
mkdir -p logs
mkdir -p backup

# Create config/clients_config.json
log_info "⚙️ Creating client configuration template..."
cat > config/clients_config.json << 'EOF'
{
  "client1": {
    "name": "JobsEU",
    "gohighlevel_api_key": "YOUR_REAL_API_KEY_HERE",
    "gohighlevel_location_id": "YOUR_REAL_LOCATION_ID_HERE",
    "olx_search_urls": [
      "https://www.olx.pl/praca/q-producent/?search%5Border%5D=created_at:desc",
      "https://www.olx.pl/praca/q-produkcja/?search%5Border%5D=created_at:desc",
      "https://www.olx.pl/praca/q-fabryka/?search%5Border%5D=created_at:desc"
    ],
    "keywords": {
      "include": ["producent", "produkcja", "fabryka", "manufacturing", "zakład"],
      "exclude": ["agencja", "pośrednictwo", "kadry", "hr", "rekrutacja"]
    },
    "schedule": "0 */3 * * *",
    "enabled": true,
    "max_pages": 5,
    "max_listings": 50,
    "delay_between_requests": 2,
    "output_file": "results_client1.json",
    "log_file": "client1_scraper.log"
  }
}
EOF

# Copy deployment script from public repository
log_info "🚀 Copying deployment script..."
cp "${CURRENT_DIR}/deployment/deploy.sh" deployment/
chmod +x deployment/deploy.sh

# Create .gitignore
log_info "🔒 Creating .gitignore..."
cat > .gitignore << 'EOF'
# Logs
logs/*.log
*.log

# Backup files
backup/*.json
*.backup

# Python cache
__pycache__/
*.pyc
*.pyo

# Results files (optional - uncomment if you don't want to track results)
# results_*.json

# System files
.DS_Store
Thumbs.db
EOF

# Create private README
log_info "📝 Creating private README..."
cat > README.md << 'EOF'
# 🔐 OLX Scraper Private Repository

This is the **private repository** for your OLX scraper system. It contains:

- **Real API keys** and client configurations
- **Deployment scripts** for Hetzner server
- **Private logs** and backups
- **Production configurations**

## ⚠️ Security Notice

**NEVER** make this repository public or share the contents. This repository contains:
- GoHighLevel API keys
- Client-specific configurations
- Production deployment scripts

## 🚀 Quick Usage

### Add New Client
1. Edit `config/clients_config.json`
2. Add your client configuration with real API key
3. Test locally: `python3 multi_client_scraper.py --client new_client --headless`
4. Deploy: `./deployment/deploy.sh`

### Deploy Changes
```bash
git add .
git commit -m "Add new client or update configuration"
git push origin main
./deployment/deploy.sh
```

### Monitor Production
```bash
# Check service status
ssh hetzner "systemctl status olx-multi-scraper"

# View logs
ssh hetzner "tail -f /opt/olx-scraper/logs/multi_client_scheduler.log"

# List clients
ssh hetzner "cd /opt/olx-scraper && python3 multi_client_scraper.py --list"
```

## 📁 Directory Structure

```
olx-scraper-private/
├── config/
│   └── clients_config.json    # 🔐 Real client configurations
├── deployment/
│   └── deploy.sh              # 🚀 Automated deployment script
├── logs/                      # 📊 Private logs (optional)
├── backup/                    # 💾 Configuration backups
└── README.md                  # 📝 This file
```

## 🔑 Client Configuration

Each client needs:
- `name`: Business name
- `gohighlevel_api_key`: Real GoHighLevel API key
- `gohighlevel_location_id`: GoHighLevel location ID
- `olx_search_urls`: Specific OLX search URLs
- `keywords`: Include/exclude keywords for filtering
- `schedule`: Cron schedule (e.g., "0 */3 * * *" for every 3 hours)
- `enabled`: true/false
- `max_pages`: Maximum pages to scrape
- `delay_between_requests`: Delay in seconds

## 📞 Support

For issues with configurations or deployment:
1. Check the logs on Hetzner server
2. Test locally before deploying
3. Use the deployment script for consistent deployments
4. Keep backups of working configurations

**Remember**: Keep this repository private and secure! 🔒
EOF

# Create initial commit
log_info "💾 Creating initial commit..."
git add .
git commit -m "Initial private repository setup with client configuration template"

log_info "✅ Private repository setup complete!"
log_info ""
log_info "📋 Next steps:"
log_info "1. Edit config/clients_config.json with your real API keys"
log_info "2. Create private GitHub repository: https://github.com/new"
log_info "3. Add remote: git remote add origin git@github.com:your-username/olx-scraper-private.git"
log_info "4. Push to GitHub: git push -u origin main"
log_info "5. Test deployment: ./deployment/deploy.sh"
log_info ""
log_info "🔒 Remember: Keep this repository PRIVATE!"
log_info "📁 Repository location: $(pwd)"

cd "${CURRENT_DIR}" 