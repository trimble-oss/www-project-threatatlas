// ---------------------------------------------------------------------------
// ThreatAtlas – Main Infrastructure Orchestration
// Deploys all resources for a given environment (e.g., lista-preprod).
// Network-hardened: PostgreSQL is VNet-only, backend is internal,
// only the frontend is internet-facing.
// ---------------------------------------------------------------------------
targetScope = 'resourceGroup'

@description('Environment name (e.g., preprod, prod)')
param environmentName string

@description('Azure region')
param location string = resourceGroup().location

@description('PostgreSQL administrator login')
param dbAdminLogin string

@secure()
@description('PostgreSQL administrator password')
param dbAdminPassword string

@secure()
@description('Application JWT secret key')
param appSecretKey string

@description('Container image tag')
param imageTag string = 'latest'

@description('SMTP configuration')
param smtpHost string = ''
param smtpPort int = 587
param smtpUsername string = ''
@secure()
param smtpPassword string = ''
param smtpFromEmail string = 'noreply@threatatlas.com'
param smtpFromName string = 'ThreatAtlas'

// ---------------------------------------------------------------------------
// Naming convention
// ---------------------------------------------------------------------------
var prefix = 'ta-${environmentName}'
var acrName = replace('ta${environmentName}acr', '-', '')
var kvName = 'ta-${environmentName}-kv'

var tags = {
  project: 'threatatlas'
  environment: environmentName
  managedBy: 'bicep'
}

// ---------------------------------------------------------------------------
// Virtual Network (isolation backbone)
// ---------------------------------------------------------------------------
module vnet 'modules/vnet.bicep' = {
  name: 'vnet'
  params: {
    name: '${prefix}-vnet'
    location: location
    tags: tags
  }
}

// ---------------------------------------------------------------------------
// Managed Identity (shared by Container Apps for ACR pull & Key Vault)
// ---------------------------------------------------------------------------
module identity 'modules/managed-identity.bicep' = {
  name: 'identity'
  params: {
    name: '${prefix}-identity'
    location: location
    tags: tags
  }
}

// ---------------------------------------------------------------------------
// Azure Container Registry
// ---------------------------------------------------------------------------
module acr 'modules/acr.bicep' = {
  name: 'acr'
  params: {
    name: acrName
    location: location
    tags: tags
  }
}

// Grant AcrPull role to the managed identity
resource acrPullRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(resourceGroup().id, acrName, '${prefix}-identity', '7f951dda-4ed3-4680-a7ca-43fe172d538d')
  scope: resourceGroup()
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d')
    principalId: identity.outputs.principalId
    principalType: 'ServicePrincipal'
  }
  dependsOn: [acr, identity]
}

// ---------------------------------------------------------------------------
// Key Vault
// ---------------------------------------------------------------------------
module keyvault 'modules/keyvault.bicep' = {
  name: 'keyvault'
  params: {
    name: kvName
    location: location
    tags: tags
    identityPrincipalId: identity.outputs.principalId
  }
}

// ---------------------------------------------------------------------------
// PostgreSQL Flexible Server – VNet-integrated, NO public access
// ---------------------------------------------------------------------------
module postgres 'modules/postgresql.bicep' = {
  name: 'postgres'
  params: {
    name: '${prefix}-pg'
    location: location
    tags: tags
    administratorLogin: dbAdminLogin
    administratorPassword: dbAdminPassword
    databaseName: 'threatatlas'
    delegatedSubnetId: vnet.outputs.postgresSubnetId
    privateDnsZoneId: vnet.outputs.privateDnsZoneId
  }
}

// ---------------------------------------------------------------------------
// Container Apps Environment – VNet-integrated (same VNet as PostgreSQL)
// ---------------------------------------------------------------------------
module appEnvironment 'modules/container-app-environment.bicep' = {
  name: 'app-environment'
  params: {
    name: '${prefix}-env'
    location: location
    tags: tags
    logAnalyticsWorkspaceName: '${prefix}-logs'
    infrastructureSubnetId: vnet.outputs.containerAppsSubnetId
  }
}

// ---------------------------------------------------------------------------
// Backend Container App – INTERNAL only (not internet-facing)
// Reachable by the frontend via the Container Apps Environment internal FQDN.
// ---------------------------------------------------------------------------
var databaseUrl = 'postgresql://${dbAdminLogin}:${dbAdminPassword}@${postgres.outputs.fqdn}:5432/${postgres.outputs.databaseName}?sslmode=require'

module backend 'modules/container-app.bicep' = {
  name: 'backend'
  params: {
    name: '${prefix}-backend'
    location: location
    tags: tags
    environmentId: appEnvironment.outputs.id
    containerImage: '${acr.outputs.loginServer}/threatatlas-backend:${imageTag}'
    containerPort: 8000
    acrLoginServer: acr.outputs.loginServer
    identityId: identity.outputs.id
    external: true   // Must be external so browser JS can call /api/* directly
    cpu: '0.5'
    memory: '1Gi'
    minReplicas: 1
    maxReplicas: 3
    probePath: '/health'
    secrets: [
      { name: 'database-url', value: databaseUrl }
      { name: 'secret-key', value: appSecretKey }
      { name: 'smtp-password', value: smtpPassword }
    ]
    envVars: [
      { name: 'DATABASE_URL', secretRef: 'database-url' }
      { name: 'SECRET_KEY', secretRef: 'secret-key' }
      { name: 'API_TITLE', value: 'ThreatAtlas API' }
      { name: 'API_VERSION', value: '1.0.0' }
      { name: 'DEBUG', value: 'False' }
      { name: 'SMTP_HOST', value: smtpHost }
      { name: 'SMTP_PORT', value: string(smtpPort) }
      { name: 'SMTP_USERNAME', value: smtpUsername }
      { name: 'SMTP_PASSWORD', secretRef: 'smtp-password' }
      { name: 'SMTP_FROM_EMAIL', value: smtpFromEmail }
      { name: 'SMTP_FROM_NAME', value: smtpFromName }
      { name: 'SMTP_TLS', value: 'True' }
      { name: 'INVITATION_EXPIRE_HOURS', value: '168' }
      // FRONTEND_URL is set after frontend deploys; update via az CLI
      { name: 'FRONTEND_URL', value: 'https://placeholder.azurecontainerapps.io' }
      // CORS_ORIGINS will be patched after frontend URL is known
      { name: 'CORS_ORIGINS', value: '["https://placeholder.azurecontainerapps.io"]' }
    ]
  }
  dependsOn: [acrPullRole]
}

// ---------------------------------------------------------------------------
// Frontend Container App – the ONLY internet-facing resource
// ---------------------------------------------------------------------------
module frontend 'modules/container-app.bicep' = {
  name: 'frontend'
  params: {
    name: '${prefix}-frontend'
    location: location
    tags: tags
    environmentId: appEnvironment.outputs.id
    containerImage: '${acr.outputs.loginServer}/threatatlas-frontend:${imageTag}'
    containerPort: 8080
    acrLoginServer: acr.outputs.loginServer
    identityId: identity.outputs.id
    external: true    // Internet-facing – serves the SPA to browsers
    cpu: '0.25'
    memory: '0.5Gi'
    minReplicas: 1
    maxReplicas: 2
    probeEnabled: false
    envVars: []
    secrets: []
  }
  dependsOn: [acrPullRole]
}

// ---------------------------------------------------------------------------
// Outputs
// ---------------------------------------------------------------------------
output acrLoginServer string = acr.outputs.loginServer
output backendUrl string = backend.outputs.url
output frontendUrl string = frontend.outputs.url
output postgresqlFqdn string = postgres.outputs.fqdn
output keyVaultUri string = keyvault.outputs.uri
output vnetName string = vnet.outputs.vnetName
