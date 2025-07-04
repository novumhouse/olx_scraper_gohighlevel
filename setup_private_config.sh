#!/bin/bash

# OLX Multi-Client Scraper - Private Configuration Setup
# This script helps you set up a private repository for sensitive client data

echo "🔐 OLX Multi-Client Scraper - Private Configuration Setup"
echo "========================================================"

# Check if git is available
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Get private repository details
echo "📁 Setting up private configuration repository..."
read -p "Enter your private repository URL (e.g., git@github.com:yourusername/olx-scraper-private.git): " PRIVATE_REPO

if [ -z "$PRIVATE_REPO" ]; then
    echo "❌ Private repository URL is required."
    exit 1
fi

# Create private config directory
PRIVATE_DIR="../olx-scraper-private"
echo "📂 Creating private configuration directory: $PRIVATE_DIR"

if [ -d "$PRIVATE_DIR" ]; then
    echo "⚠️  Directory $PRIVATE_DIR already exists. Do you want to continue? (y/n)"
    read -p "> " continue_setup
    if [[ $continue_setup != "y" && $continue_setup != "Y" ]]; then
        echo "❌ Setup cancelled."
        exit 1
    fi
else
    mkdir -p "$PRIVATE_DIR"
fi

cd "$PRIVATE_DIR"

# Initialize git repository
if [ ! -d ".git" ]; then
    echo "🔧 Initializing Git repository..."
    git init
    git remote add origin "$PRIVATE_REPO"
fi

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p config
mkdir -p logs
mkdir -p backup
mkdir -p deployment

# Create private configuration file
echo "⚙️  Creating private configuration file..."
cat > config/clients_config.json << 'EOF'
{
  "client1": {
    "name": "JobsEU",
    "gohighlevel_api_key": "YOUR_REAL_API_KEY_HERE",
    "gohighlevel_location_id": "YOUR_REAL_LOCATION_ID_HERE",
    "olx_search_urls": [
      "https://www.olx.pl/praca/q-producent/?search%5Border%5D=created_at:desc",
      "https://www.olx.pl/praca/q-produkcja/?search%5Border%5D=created_at:desc"
    ],
    "keywords": {
      "include": ["producent", "produkcja", "fabryka", "manufacturing"],
      "exclude": ["agencja", "pośrednictwo", "kadry", "hr"]
    },
    "schedule": "0 9 * * 1-5",
    "enabled": true,
    "max_pages": 5,
    "delay_between_requests": 2
  }
}
EOF

# Create deployment script
echo "🚀 Creating deployment script..."
cat > deployment/deploy_to_hetzner.sh << 'EOF'
#!/bin/bash

# OLX Multi-Client Scraper - Private Deployment Script
# This script deploys both the public app and private configuration to Hetzner

set -e

echo "🚀 Deploying OLX Multi-Client Scraper to Hetzner"
echo "================================================"

# Configuration
SERVER_IP="${HETZNER_IP:-your_server_ip}"
SERVER_USER="${HETZNER_USER:-root}"
PUBLIC_REPO="https://github.com/novumhouse/olx_scraper_gohighlevel.git"
PRIVATE_REPO="$1"

if [ -z "$PRIVATE_REPO" ]; then
    echo "❌ Usage: $0 <private_repo_url>"
    echo "Example: $0 git@github.com:yourusername/olx-scraper-private.git"
    exit 1
fi

echo "🔗 Public Repository: $PUBLIC_REPO"
echo "🔐 Private Repository: $PRIVATE_REPO"
echo "🖥️  Server: $SERVER_USER@$SERVER_IP"

# Deploy to server
ssh $SERVER_USER@$SERVER_IP << ENDSSH
    echo "📦 Updating public repository..."
    cd /opt/olx-scraper
    git pull origin main
    
    echo "🔐 Updating private configuration..."
    cd /opt/olx-scraper-private
    git pull origin main
    
    echo "⚙️  Copying configuration..."
    cp config/clients_config.json /opt/olx-scraper/clients_config.json
    
    echo "🔄 Restarting services..."
    systemctl restart olx-multi-scraper
    systemctl enable olx-multi-scraper
    
    echo "✅ Deployment complete!"
ENDSSH

echo "🎉 Deployment finished successfully!"
EOF

chmod +x deployment/deploy_to_hetzner.sh

# Create README for private repo
echo "📝 Creating private repository README..."
cat > README.md << 'EOF'
# OLX Multi-Client Scraper - Private Configuration

🔐 **This is the private configuration repository containing sensitive client data.**

## ⚠️ SECURITY WARNING
- **NEVER** make this repository public
- **NEVER** commit real API keys to public repositories
- Keep this repository private and secure

## 📁 Repository Structure

```
olx-scraper-private/
├── config/
│   └── clients_config.json     # Real client configurations with API keys
├── logs/                       # Private log files (optional)
├── backup/                     # Configuration backups
├── deployment/
│   └── deploy_to_hetzner.sh   # Private deployment script
└── README.md
```

## 🔧 Configuration

Edit `config/clients_config.json` with your real client data:

```json
{
  "client1": {
    "name": "Your Real Client Name",
    "gohighlevel_api_key": "pk_live_xxxxxxxxxxxxx",
    "gohighlevel_location_id": "xxxxxxxxxxxxxxx",
    "olx_search_urls": ["your_real_search_urls"],
    "keywords": {
      "include": ["your", "real", "keywords"],
      "exclude": ["unwanted", "terms"]
    },
    "schedule": "0 9 * * 1-5",
    "enabled": true
  }
}
```

## 🚀 Deployment

1. Update configuration: `git add . && git commit -m "Update config" && git push`
2. Deploy to Hetzner: `./deployment/deploy_to_hetzner.sh YOUR_PRIVATE_REPO_URL`

## 🔄 Sync with Public Repository

The public repository contains the application code. This private repository contains only sensitive configuration data.

- **Public repo**: https://github.com/novumhouse/olx_scraper_gohighlevel
- **Private repo**: This repository (keep URL private)
EOF

# Create .gitignore for private repo
cat > .gitignore << 'EOF'
# Logs
*.log
logs/*.log

# Backup files
*.bak
*~

# Environment
.env
.venv/
venv/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Python
__pycache__/
*.pyc
EOF

# Initial commit
echo "📤 Creating initial commit..."
git add .
git commit -m "🔐 Initial private configuration setup

✅ Private client configurations
✅ Deployment scripts
✅ Security documentation
✅ Directory structure"

echo ""
echo "✅ Private configuration repository setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit config/clients_config.json with your real API keys"
echo "2. Push to your private repository: git push -u origin main"
echo "3. Update deployment/deploy_to_hetzner.sh with your server details"
echo "4. Deploy using: ./deployment/deploy_to_hetzner.sh $PRIVATE_REPO"
echo ""
echo "🔐 Repository location: $PRIVATE_DIR"
echo "🔗 Private repository: $PRIVATE_REPO"
EOF 