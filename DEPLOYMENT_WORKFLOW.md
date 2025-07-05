# 🚀 OLX Scraper Deployment Workflow Guide

## Overview

This guide explains the complete workflow for managing your OLX scraper system, from adding new clients to deploying changes to production.

## 📋 Repository Structure

```
🔧 Local Development
├── olx_scraper_gohighlevel/          # Public repo (application code)
│   ├── multi_client_scraper.py       # Core application
│   ├── gohighlevel_integration.py    # API integration
│   ├── clients_config.json.example   # Template config
│   └── README.md                     # Public documentation
│
└── olx-scraper-private/              # Private repo (real credentials)
    ├── config/
    │   └── clients_config.json       # 🔐 REAL API keys
    ├── deployment/
    │   └── deploy.sh                 # Deployment script
    └── README.md                     # Private documentation

🌐 GitHub
├── novumhouse/olx_scraper_gohighlevel     # Public repository
└── novumhouse/olx-scraper-private         # Private repository

☁️ Hetzner Server
└── /opt/olx-scraper/                      # Connected to private repo
```

## 🔄 Complete Workflow: Adding New Clients

### Step 1: Add Client Configuration Locally

1. **Edit the private configuration file:**
   ```bash
   cd olx-scraper-private
   nano config/clients_config.json
   ```

2. **Add your new client:**
   ```json
   {
     "client1": {
       "name": "JobsEU",
       "gohighlevel_api_key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
       "gohighlevel_location_id": "qiFnT0rj80EEsruBVTTs",
       "olx_search_urls": [
         "https://www.olx.pl/praca/q-producent/?search%5Border%5D=created_at:desc"
       ],
       "keywords": {
         "include": ["producent", "produkcja", "fabryka"],
         "exclude": ["agencja", "pośrednictwo", "hr"]
       },
       "schedule": "0 */3 * * *",
       "enabled": true,
       "max_pages": 5,
       "delay_between_requests": 2
     },
     "client2": {
       "name": "Manufacturing Corp",
       "gohighlevel_api_key": "YOUR_NEW_CLIENT_API_KEY",
       "gohighlevel_location_id": "YOUR_NEW_CLIENT_LOCATION_ID",
       "olx_search_urls": [
         "https://www.olx.pl/praca/q-automotive/?search%5Border%5D=created_at:desc"
       ],
       "keywords": {
         "include": ["automotive", "samochodowy", "motoryzacja"],
         "exclude": ["agencja", "pośrednictwo", "hr"]
       },
       "schedule": "0 */6 * * *",
       "enabled": true,
       "max_pages": 3,
       "delay_between_requests": 2
     }
   }
   ```

### Step 2: Test Locally

```bash
# Test the new client configuration
cd olx-scraper-private
python3 multi_client_scraper.py --list
python3 multi_client_scraper.py --client client2 --headless
```

### Step 3: Commit to Private Repository

```bash
cd olx-scraper-private
git add config/clients_config.json
git commit -m "Add new client: Manufacturing Corp with automotive keywords"
git push origin master
```

### Step 4: Deploy to Hetzner Server

**Option A: Manual Deployment (Current)**
```bash
# Pull changes on server
ssh hetzner "cd /opt/olx-scraper && git pull origin master"

# Restart service to apply changes
ssh hetzner "systemctl restart olx-multi-scraper"

# Verify deployment
ssh hetzner "cd /opt/olx-scraper && python3 multi_client_scraper.py --list"
```

**Option B: Automated Deployment (Recommended)**
```bash
# Run deployment script
cd olx-scraper-private
./deployment/deploy.sh
```

### Step 5: Monitor New Client

```bash
# Check service status
ssh hetzner "systemctl status olx-multi-scraper"

# Monitor logs
ssh hetzner "tail -f /opt/olx-scraper/logs/multi_client_scheduler.log"

# Check client-specific logs
ssh hetzner "tail -f /opt/olx-scraper/logs/client2_scraper.log"
```

## 🔧 Workflow: Updating Application Code

### Step 1: Update Public Repository

1. **Make changes to application code:**
   ```bash
   cd olx_scraper_gohighlevel
   # Edit multi_client_scraper.py, gohighlevel_integration.py, etc.
   ```

2. **Test changes locally:**
   ```bash
   python3 multi_client_scraper.py --client client1 --headless
   ```

3. **Commit and push to public repository:**
   ```bash
   git add .
   git commit -m "Improve error handling and add new features"
   git push origin main
   ```

### Step 2: Update Private Repository

1. **Pull application code changes:**
   ```bash
   cd olx-scraper-private
   git submodule update --remote  # If using submodules
   # OR copy updated files manually
   ```

2. **Test with real configurations:**
   ```bash
   python3 multi_client_scraper.py --client client1 --headless
   ```

3. **Commit and push:**
   ```bash
   git add .
   git commit -m "Update application code with latest features"
   git push origin master
   ```

### Step 3: Deploy to Production

```bash
# Deploy using automated script
./deployment/deploy.sh

# OR manual deployment
ssh hetzner "cd /opt/olx-scraper && git pull origin master && systemctl restart olx-multi-scraper"
```

## 🚀 Automated Deployment Script

Create `/deployment/deploy.sh` in your private repository:

```bash
#!/bin/bash
# Auto-deployment script for Hetzner server

set -e

HETZNER_IP="188.245.58.182"
HETZNER_USER="root"
SERVICE_NAME="olx-multi-scraper"
DEPLOY_PATH="/opt/olx-scraper"

echo "🚀 Starting deployment to Hetzner server..."

# 1. Pull latest changes on server
echo "📥 Pulling latest changes..."
ssh ${HETZNER_USER}@${HETZNER_IP} "cd ${DEPLOY_PATH} && git pull origin master"

# 2. Install any new dependencies
echo "📦 Installing dependencies..."
ssh ${HETZNER_USER}@${HETZNER_IP} "cd ${DEPLOY_PATH} && source venv/bin/activate && pip install -r requirements.txt"

# 3. Restart service
echo "🔄 Restarting service..."
ssh ${HETZNER_USER}@${HETZNER_IP} "systemctl restart ${SERVICE_NAME}"

# 4. Verify deployment
echo "✅ Verifying deployment..."
ssh ${HETZNER_USER}@${HETZNER_IP} "systemctl status ${SERVICE_NAME} --no-pager"

# 5. Test client list
echo "📋 Testing client configuration..."
ssh ${HETZNER_USER}@${HETZNER_IP} "cd ${DEPLOY_PATH} && source venv/bin/activate && python3 multi_client_scraper.py --list"

echo "🎉 Deployment completed successfully!"
echo "📊 Monitor logs: ssh ${HETZNER_USER}@${HETZNER_IP} 'tail -f ${DEPLOY_PATH}/logs/multi_client_scheduler.log'"
```

## 📋 Quick Reference Commands

### Adding New Clients
```bash
# 1. Edit config
nano olx-scraper-private/config/clients_config.json

# 2. Test locally
python3 multi_client_scraper.py --client new_client --headless

# 3. Deploy
cd olx-scraper-private
git add . && git commit -m "Add new client" && git push
./deployment/deploy.sh
```

### Updating Application Code
```bash
# 1. Update public repo
cd olx_scraper_gohighlevel
git add . && git commit -m "New features" && git push

# 2. Update private repo
cd olx-scraper-private
git add . && git commit -m "Update app code" && git push

# 3. Deploy
./deployment/deploy.sh
```

### Monitoring
```bash
# Service status
ssh hetzner "systemctl status olx-multi-scraper"

# Live logs
ssh hetzner "tail -f /opt/olx-scraper/logs/multi_client_scheduler.log"

# Client results
ssh hetzner "ls -la /opt/olx-scraper/results_*.json"
```

## 🔒 Security Best Practices

1. **Never commit real API keys to public repository**
2. **Use SSH keys for GitHub authentication**
3. **Regularly rotate API keys**
4. **Monitor access logs**
5. **Keep private repository access restricted**

## 🚨 Emergency Procedures

### Rollback Deployment
```bash
# Rollback to previous version
ssh hetzner "cd /opt/olx-scraper && git reset --hard HEAD~1"
ssh hetzner "systemctl restart olx-multi-scraper"
```

### Service Recovery
```bash
# Restart service
ssh hetzner "systemctl restart olx-multi-scraper"

# Check service logs
ssh hetzner "journalctl -u olx-multi-scraper -f"

# Manual service recovery
ssh hetzner "cd /opt/olx-scraper && source venv/bin/activate && python3 multi_client_scheduler.py"
```

## 📈 Scaling Considerations

- **Server Resources**: Monitor CPU/memory usage when adding clients
- **API Rate Limits**: Stagger client schedules to avoid GoHighLevel limits
- **Storage**: Implement log rotation and result file cleanup
- **Backup**: Regular configuration backups to prevent data loss

## 🎯 Summary

This workflow provides:
- ✅ **Secure credential management** (private repository)
- ✅ **Easy client addition** (JSON configuration)
- ✅ **Automated deployment** (deployment script)
- ✅ **Production monitoring** (logs and status)
- ✅ **Rollback capability** (git-based versioning)

**Next Steps:**
1. Set up the deployment script
2. Test the workflow with a new client
3. Monitor production performance
4. Scale as needed 