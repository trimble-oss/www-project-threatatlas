#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# deploy.sh – Build, push, and deploy ThreatAtlas to Azure
#
# Usage:
#   ./deploy.sh --env lista-preprod --tag v1.0.0
#   ./deploy.sh --env lista-preprod               # defaults to 'latest'
# ---------------------------------------------------------------------------
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── Defaults ──────────────────────────────────────────────────────────────
ENV_NAME=""
IMAGE_TAG="latest"
RESOURCE_GROUP=""
SKIP_BUILD=false

usage() {
  echo "Usage: $0 --env <environment> [--tag <image-tag>] [--rg <resource-group>] [--skip-build]"
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --env)       ENV_NAME="$2"; shift 2 ;;
    --tag)       IMAGE_TAG="$2"; shift 2 ;;
    --rg)        RESOURCE_GROUP="$2"; shift 2 ;;
    --skip-build) SKIP_BUILD=true; shift ;;
    *)           usage ;;
  esac
done

[[ -z "$ENV_NAME" ]] && usage

RESOURCE_GROUP="${RESOURCE_GROUP:-threatatlas-${ENV_NAME}-rg}"
ACR_NAME="$(echo "ta${ENV_NAME}acr" | tr -d '-')"
PARAMS_FILE="${SCRIPT_DIR}/parameters/${ENV_NAME}.parameters.json"

if [[ ! -f "$PARAMS_FILE" ]]; then
  echo "❌ Parameter file not found: $PARAMS_FILE"
  exit 1
fi

echo "═══════════════════════════════════════════════════════════"
echo "  ThreatAtlas Deployment"
echo "  Environment : $ENV_NAME"
echo "  Image Tag   : $IMAGE_TAG"
echo "  Resource Grp: $RESOURCE_GROUP"
echo "═══════════════════════════════════════════════════════════"

# ── 1. Ensure resource group ──────────────────────────────────────────────
echo "▶ Ensuring resource group: $RESOURCE_GROUP"
az group create \
  --name "$RESOURCE_GROUP" \
  --location "$(jq -r '.parameters.location.value' "$PARAMS_FILE")" \
  --output none

# ── 2. Deploy ACR first (so we can push images before Container Apps need them)
echo "▶ Deploying ACR..."
az acr create \
  --name "$ACR_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --sku Basic \
  --admin-enabled false \
  --output none 2>/dev/null || true

ACR_LOGIN_SERVER=$(az acr show --name "$ACR_NAME" --query loginServer -o tsv)

# ── 3. Build & push container images ─────────────────────────────────────
if [[ "$SKIP_BUILD" == false ]]; then
  echo "▶ Logging in to ACR: $ACR_LOGIN_SERVER"
  az acr login --name "$ACR_NAME"

  BACKEND_DIR="${SCRIPT_DIR}/../backend"
  FRONTEND_DIR="${SCRIPT_DIR}/../frontend"

  echo "▶ Building backend image..."
  docker build --platform linux/amd64 -t "${ACR_LOGIN_SERVER}/threatatlas-backend:${IMAGE_TAG}" "$BACKEND_DIR"

  echo "▶ Building frontend image (VITE_API_URL will be patched post-deploy)..."
  docker build --platform linux/amd64 \
    --build-arg "VITE_API_URL=https://placeholder.azurecontainerapps.io" \
    -t "${ACR_LOGIN_SERVER}/threatatlas-frontend:${IMAGE_TAG}" "$FRONTEND_DIR"

  echo "▶ Pushing images to ACR..."
  docker push "${ACR_LOGIN_SERVER}/threatatlas-backend:${IMAGE_TAG}"
  docker push "${ACR_LOGIN_SERVER}/threatatlas-frontend:${IMAGE_TAG}"
fi

# ── 4. Deploy full infrastructure via Bicep ───────────────────────────────
echo "▶ Deploying Bicep infrastructure..."
az deployment group create \
  --resource-group "$RESOURCE_GROUP" \
  --template-file "${SCRIPT_DIR}/main.bicep" \
  --parameters "@${PARAMS_FILE}" \
  --parameters imageTag="$IMAGE_TAG" \
  --name "threatatlas-${ENV_NAME}-$(date +%Y%m%d%H%M%S)" \
  --output none

# ── 5. Resolve URLs and rebuild frontend with correct API URL ─────────────
BACKEND_FQDN=$(az containerapp show \
  --name "ta-${ENV_NAME}-backend" \
  --resource-group "$RESOURCE_GROUP" \
  --query 'properties.configuration.ingress.fqdn' -o tsv 2>/dev/null || echo "")

if [[ "$SKIP_BUILD" == false && -n "$BACKEND_FQDN" ]]; then
  VITE_API_URL="https://${BACKEND_FQDN}"
  FRONTEND_DIR="${SCRIPT_DIR}/../frontend"

  echo "▶ Rebuilding frontend with VITE_API_URL=${VITE_API_URL}..."
  docker build --platform linux/amd64 \
    --build-arg "VITE_API_URL=${VITE_API_URL}" \
    -t "${ACR_LOGIN_SERVER}/threatatlas-frontend:${IMAGE_TAG}" "$FRONTEND_DIR"
  docker push "${ACR_LOGIN_SERVER}/threatatlas-frontend:${IMAGE_TAG}"

  echo "▶ Updating frontend container app with correct API URL..."
  az containerapp update \
    --name "ta-${ENV_NAME}-frontend" \
    --resource-group "$RESOURCE_GROUP" \
    --image "${ACR_LOGIN_SERVER}/threatatlas-frontend:${IMAGE_TAG}" \
    --output none
fi

# ── 6. Update FRONTEND_URL + CORS_ORIGINS on backend (circular dep resolution)
FRONTEND_FQDN=$(az containerapp show \
  --name "ta-${ENV_NAME}-frontend" \
  --resource-group "$RESOURCE_GROUP" \
  --query 'properties.configuration.ingress.fqdn' -o tsv)

echo "▶ Setting FRONTEND_URL and CORS_ORIGINS on backend → https://${FRONTEND_FQDN}"
az containerapp update \
  --name "ta-${ENV_NAME}-backend" \
  --resource-group "$RESOURCE_GROUP" \
  --set-env-vars \
    "FRONTEND_URL=https://${FRONTEND_FQDN}" \
    "CORS_ORIGINS=[\"https://${FRONTEND_FQDN}\"]" \
  --output none

# ── 6. Summary ────────────────────────────────────────────────────────────
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  ✅ Deployment complete!"
echo ""
echo "  Frontend : https://${FRONTEND_FQDN}"
echo "  Backend  : https://${BACKEND_FQDN:-$(az containerapp show --name "ta-${ENV_NAME}-backend" --resource-group "$RESOURCE_GROUP" --query 'properties.configuration.ingress.fqdn' -o tsv)}"
echo "  API Docs : https://${BACKEND_FQDN:-}/docs"
echo "═══════════════════════════════════════════════════════════"
