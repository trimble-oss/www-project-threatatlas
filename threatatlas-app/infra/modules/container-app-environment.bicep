@description('Azure Container Apps Environment – VNet-integrated')
param name string
param location string = resourceGroup().location
param tags object = {}

param logAnalyticsWorkspaceName string

@description('Subnet ID for Container Apps infrastructure (snet-container-apps)')
param infrastructureSubnetId string

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: logAnalyticsWorkspaceName
  location: location
  tags: tags
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

resource environment 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: name
  location: location
  tags: tags
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalytics.properties.customerId
        sharedKey: logAnalytics.listKeys().primarySharedKey
      }
    }
    // VNet integration – apps run inside the VNet and can reach PostgreSQL
    vnetConfiguration: {
      infrastructureSubnetId: infrastructureSubnetId
      internal: false // ingress is still reachable from the internet
    }
  }
}

output id string = environment.id
output name string = environment.name
output defaultDomain string = environment.properties.defaultDomain
