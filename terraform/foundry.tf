resource "azurerm_cognitive_account" "foundry" {
  name                          = var.foundry_name
  resource_group_name           = var.foundry_resource_group_name
  location                      = var.foundry_location
  kind                          = var.foundry_kind
  sku_name                      = var.foundry_sku_name
  custom_subdomain_name         = var.foundry_custom_subdomain_name
  local_auth_enabled            = false
  public_network_access_enabled = true
  project_management_enabled    = true

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_cognitive_deployment" "foundry_model" {
  name                 = var.foundry_deployment_name
  cognitive_account_id = azurerm_cognitive_account.foundry.id

  model {
    format  = var.foundry_model_format
    name    = var.foundry_model_name
    version = var.foundry_model_version
  }

  sku {
    name     = var.foundry_deployment_sku_name
    capacity = var.foundry_deployment_capacity
  }
}

resource "azurerm_role_assignment" "app_foundry_user" {
  name                 = random_uuid.app_foundry_role_assignment.result
  scope                = azurerm_cognitive_account.foundry.id
  role_definition_name = "Cognitive Services OpenAI User"
  principal_id         = azurerm_user_assigned_identity.app.principal_id
  principal_type       = "ServicePrincipal"
}

resource "random_uuid" "app_foundry_role_assignment" {}
