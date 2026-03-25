@description('Azure Container App')
param name string
param location string = resourceGroup().location
param tags object = {}

param environmentId string
param containerImage string
param containerPort int
param acrLoginServer string

@description('User-assigned managed identity resource ID for ACR pull')
param identityId string


param cpu string = '0.5'
param memory string = '1Gi'
param minReplicas int = 1
param maxReplicas int = 2

param envVars array = []
param secrets array = []

@description('Whether the app is reachable from the public internet')
param external bool = true
param targetPort int = containerPort

param probeEnabled bool = true
param probePath string = '/health'



resource app 'Microsoft.App/containerApps@2024-03-01' = {
  name: name
  location: location
  tags: tags
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${identityId}': {}
    }
  }
  properties: {
    managedEnvironmentId: environmentId
    configuration: {
      activeRevisionsMode: 'Single'
      ingress: {
        external: external
        targetPort: targetPort
        transport: 'http'
        allowInsecure: false
      }
      registries: [
        {
          server: acrLoginServer
          identity: identityId
        }
      ]
      secrets: secrets
    }
    template: {
      containers: [
        {
          name: name
          image: containerImage
          resources: {
            cpu: json(cpu)
            memory: memory
          }
          env: envVars
          probes: probeEnabled ? [
            {
              type: 'Liveness'
              httpGet: {
                path: probePath
                port: containerPort
              }
              initialDelaySeconds: 30
              periodSeconds: 30
            }
            {
              type: 'Readiness'
              httpGet: {
                path: probePath
                port: containerPort
              }
              initialDelaySeconds: 10
              periodSeconds: 10
            }
          ] : []
        }
      ]
      scale: {
        minReplicas: minReplicas
        maxReplicas: maxReplicas
      }
    }
  }
}

output id string = app.id
output name string = app.name
output fqdn string = app.properties.configuration.ingress.fqdn
output url string = 'https://${app.properties.configuration.ingress.fqdn}'
