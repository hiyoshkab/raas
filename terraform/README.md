# Terraform

Terraform grants the GitHub Actions deployment service principal:

- `Azure Kubernetes Service Cluster User Role` at the AKS cluster scope, to retrieve non-admin cluster credentials.
- `Azure Kubernetes Service RBAC Writer` at the `raas` namespace scope, to deploy the Helm release.

Set `github_actions_service_principal_object_id` to the service principal's
Microsoft Entra **object ID** (not its application/client ID) in
`terraform.tfvars` or via the `TF_VAR_github_actions_service_principal_object_id`
environment variable before running Terraform.

The `raas` namespace must exist before the Helm workflow deploys the chart.

## Existing Foundry account and app identity

Copy `terraform.tfvars.example` to `terraform.tfvars` and set the account and
deployment values. The Foundry account and model deployment are declared as
Terraform resources and must be imported before planning, since they already
exist:

```sh
FOUNDRY_RESOURCE_ID=$(az cognitiveservices account show \
  --name "$FOUNDRY_NAME" \
  --resource-group "$FOUNDRY_RESOURCE_GROUP" \
  --query id -o tsv)

terraform import azurerm_cognitive_account.foundry "$FOUNDRY_RESOURCE_ID"

terraform import azurerm_cognitive_deployment.foundry_model \
  "$FOUNDRY_RESOURCE_ID/deployments/$FOUNDRY_DEPLOYMENT_NAME"
```

Populate the `foundry_*` variables with the existing account and deployment
settings, then run `terraform plan` and resolve any differences before
applying. Do not apply until the imported resources show no unexpected
replacement or deletion.

Terraform creates a dedicated user-assigned identity for the API, enables AKS
Workload Identity, federates that identity to the `raas/app-backend` service
account, and grants it `Cognitive Services OpenAI User` on the Foundry account.
Set the GitHub repository variable `AZURE_APP_CLIENT_ID` to the Terraform
`app_identity_client_id` output. The app must be deployed after this identity
configuration is applied.
