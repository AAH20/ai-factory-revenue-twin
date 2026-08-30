param location string = resourceGroup().location
param suffix string = uniqueString(resourceGroup().id)

var tags = {
  project: 'AI Factory Revenue Twin'
  purpose: 'evidence-control-plane'
  website: 'a2zsoc.com'
}

resource logs 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: 'aifactory-law-${suffix}'
  location: location
  tags: tags
  properties: {
    retentionInDays: 30
    sku: {
      name: 'PerGB2018'
    }
  }
}

resource storage 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: 'aifactory${suffix}'
  location: location
  tags: tags
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    allowBlobPublicAccess: false
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
  }
}

resource receipts 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = {
  name: '${storage.name}/default/readiness-receipts'
  properties: {
    publicAccess: 'None'
  }
}

resource insights 'Microsoft.Insights/components@2020-02-02' = {
  name: 'aifactory-ai-${suffix}'
  location: location
  kind: 'web'
  tags: tags
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logs.id
  }
}

output logAnalyticsWorkspace string = logs.name
output storageAccount string = storage.name
output applicationInsights string = insights.name
