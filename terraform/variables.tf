variable "resource_group_location" {
  type        = string
  default     = "westus"
  description = "Location of the resource group."
}

variable "resource_group_name_prefix" {
  type        = string
  default     = "rg"
  description = "Prefix of the resource group name that's combined with a random ID so name is unique in your Azure subscription."
}

variable "aks_sku_tier" {
  type        = string
  description = "The SKU tier of the AKS cluster."
  default     = "Standard"
}

variable "node_sku" {
  type        = string
  description = "VM SKU of the node pool."
  default     = "Standard_D2_v2"
}

variable "node_count" {
  type        = number
  description = "The initial quantity of nodes for the node pool."
  default     = 3
}

variable "aks_admin_group_principal_type" {
  type        = string
  description = "The principal type of the AKS admin group."
  default     = "Group"
}

variable "aks_admin_group_object_id" {
  type        = string
  description = "Microsoft Entra group object ID granted AKS cluster-admin access."

  validation {
    condition     = can(regex("^[0-9a-fA-F-]{36}$", var.aks_admin_group_object_id))
    error_message = "Provide a valid Microsoft Entra group object ID."
  }
}

variable "github_actions_service_principal_object_id" {
  type        = string
  description = "Microsoft Entra service principal object ID for the GitHub Actions deployment identity."

  validation {
    condition     = can(regex("^[0-9a-fA-F-]{36}$", var.github_actions_service_principal_object_id))
    error_message = "Provide a valid Microsoft Entra service principal object ID."
  }
}

variable "vnet_address_space" {
  type        = list(string)
  description = "Address space for the AKS virtual network."
  default     = ["10.0.0.0/16"]
}

variable "aks_subnet_address_prefixes" {
  type        = list(string)
  description = "Address prefixes for the AKS node subnet."
  default     = ["10.0.1.0/24"]
}

variable "aks_pod_cidr" {
  type        = string
  description = "Non-overlapping pod address range for Azure CNI Overlay."
  default     = "10.244.0.0/16"
}

variable "aks_service_cidr" {
  type        = string
  description = "Non-overlapping Kubernetes service address range."
  default     = "10.1.0.0/16"
}

variable "aks_dns_service_ip" {
  type        = string
  description = "DNS service IP from within aks_service_cidr."
  default     = "10.1.0.10"
}

variable "msi_id" {
  type        = string
  description = "The Managed Service Identity ID. Set this value if you're running this example using Managed Identity as the authentication method."
  default     = null
}

variable "app_identity_name" {
  type        = string
  description = "Name of the user-assigned identity used by the application."
  default     = "raas-app-identity"
}

variable "app_namespace" {
  type        = string
  description = "Kubernetes namespace containing the application service account."
  default     = "raas"
}

variable "app_service_account_name" {
  type        = string
  description = "Kubernetes service account federated to the application identity."
  default     = "app-backend"
}

variable "foundry_name" {
  type        = string
  description = "Name of the existing Azure AI Foundry account to import and manage."
}

variable "foundry_resource_group_name" {
  type        = string
  description = "Resource group containing the existing Azure AI Foundry account."
}

variable "foundry_location" {
  type        = string
  description = "Azure region of the existing Azure AI Foundry account."
}

variable "foundry_kind" {
  type        = string
  description = "Kind of the existing Azure AI Foundry account."
  default     = "AIServices"
}

variable "foundry_sku_name" {
  type        = string
  description = "SKU of the existing Azure AI Foundry account."
  default     = "S0"
}

variable "foundry_custom_subdomain_name" {
  type        = string
  description = "Custom subdomain of the existing Azure AI Foundry account."
}

variable "foundry_deployment_name" {
  type        = string
  description = "Name of the existing model deployment."
}

variable "foundry_model_format" {
  type        = string
  description = "Format of the existing Foundry model deployment."
  default     = "OpenAI"
}

variable "foundry_model_name" {
  type        = string
  description = "Model name for the existing Foundry deployment."
}

variable "foundry_model_version" {
  type        = string
  description = "Model version for the existing Foundry deployment."
}

variable "foundry_deployment_sku_name" {
  type        = string
  description = "SKU name of the existing Foundry model deployment."
}

variable "foundry_deployment_capacity" {
  type        = number
  description = "Provisioned capacity of the existing Foundry model deployment."
}