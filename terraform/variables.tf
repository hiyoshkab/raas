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
