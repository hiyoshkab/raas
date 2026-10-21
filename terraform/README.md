# Terraform

Terraform grants the GitHub Actions deployment service principal:

- `Azure Kubernetes Service Cluster User Role` at the AKS cluster scope, to retrieve non-admin cluster credentials.
- `Azure Kubernetes Service RBAC Writer` at the `raas` namespace scope, to deploy the Helm release.

Set `github_actions_service_principal_object_id` to the service principal's
Microsoft Entra **object ID** (not its application/client ID) in
`terraform.tfvars` or via the `TF_VAR_github_actions_service_principal_object_id`
environment variable before running Terraform.

The `raas` namespace must already exist in the cluster. If it does not, the
workflow's `--create-namespace` option requires cluster-wide namespace-creation
permission, which the namespace-scoped Writer assignment does not grant.
