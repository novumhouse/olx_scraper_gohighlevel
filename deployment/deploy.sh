#!/bin/bash
# 🚀 Auto-deployment script for Hetzner server
# This script deploys the latest changes to your OLX scraper on Hetzner

set -e

# Configuration
HETZNER_IP="188.245.58.182"
HETZNER_USER="root"
SERVICE_NAME="olx-multi-scraper"
DEPLOY_PATH="/opt/olx-scraper"
SSH_ALIAS="hetzner"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if SSH alias exists
if ! ssh -o ConnectTimeout=5 -o BatchMode=yes ${SSH_ALIAS} exit 2>/dev/null; then
    log_error "Cannot connect to Hetzner server using SSH alias '${SSH_ALIAS}'"
    log_info "Please ensure SSH is configured with: ssh ${SSH_ALIAS}"
    exit 1
fi

log_info "🚀 Starting deployment to Hetzner server (${HETZNER_IP})..."

# 1. Check current service status
log_info "📊 Checking current service status..."
ssh ${SSH_ALIAS} "systemctl is-active ${SERVICE_NAME} || echo 'Service is not running'"

# 2. Create backup of current configuration
log_info "💾 Creating backup of current configuration..."
ssh ${SSH_ALIAS} "cd ${DEPLOY_PATH} && cp clients_config.json clients_config.json.backup-$(date +%Y%m%d-%H%M%S)"

# 3. Pull latest changes from private repository
log_info "📥 Pulling latest changes from private repository..."
ssh ${SSH_ALIAS} "cd ${DEPLOY_PATH} && git pull origin master"

# 4. Install/update dependencies
log_info "📦 Installing/updating dependencies..."
ssh ${SSH_ALIAS} "cd ${DEPLOY_PATH} && source venv/bin/activate && pip install -r requirements.txt --quiet"

# 5. Validate configuration
log_info "✅ Validating client configuration..."
ssh ${SSH_ALIAS} "cd ${DEPLOY_PATH} && source venv/bin/activate && python3 multi_client_scraper.py --list" || {
    log_error "Configuration validation failed!"
    log_warn "Restoring backup..."
    ssh ${SSH_ALIAS} "cd ${DEPLOY_PATH} && cp clients_config.json.backup-* clients_config.json"
    exit 1
}

# 6. Restart service
log_info "🔄 Restarting OLX scraper service..."
ssh ${SSH_ALIAS} "systemctl restart ${SERVICE_NAME}"

# 7. Wait for service to start
log_info "⏳ Waiting for service to start..."
sleep 5

# 8. Verify deployment
log_info "🔍 Verifying deployment..."
if ssh ${SSH_ALIAS} "systemctl is-active ${SERVICE_NAME} --quiet"; then
    log_info "✅ Service is running successfully!"
else
    log_error "❌ Service failed to start!"
    ssh ${SSH_ALIAS} "systemctl status ${SERVICE_NAME} --no-pager"
    exit 1
fi

# 9. Display service status
log_info "📊 Service status:"
ssh ${SSH_ALIAS} "systemctl status ${SERVICE_NAME} --no-pager -l"

# 10. Test client configuration
log_info "📋 Testing client configuration..."
ssh ${SSH_ALIAS} "cd ${DEPLOY_PATH} && source venv/bin/activate && python3 multi_client_scraper.py --list"

# 11. Show recent logs
log_info "📝 Recent service logs:"
ssh ${SSH_ALIAS} "journalctl -u ${SERVICE_NAME} --no-pager -n 10"

# 12. Cleanup old backups (keep last 5)
log_info "🧹 Cleaning up old backups..."
ssh ${SSH_ALIAS} "cd ${DEPLOY_PATH} && ls -t clients_config.json.backup-* 2>/dev/null | tail -n +6 | xargs rm -f"

log_info "🎉 Deployment completed successfully!"
log_info ""
log_info "📊 Monitor your deployment:"
log_info "   Service status: ssh ${SSH_ALIAS} 'systemctl status ${SERVICE_NAME}'"
log_info "   Live logs:      ssh ${SSH_ALIAS} 'tail -f ${DEPLOY_PATH}/logs/multi_client_scheduler.log'"
log_info "   Client results: ssh ${SSH_ALIAS} 'ls -la ${DEPLOY_PATH}/results_*.json'"
log_info ""
log_info "🚀 Your OLX scraper is now running with the latest configuration!" 