# RAAS Helm chart

This chart installs the RAAS API and its Qdrant StatefulSet into the `raas`
namespace. The API image repository and tag are required values; CI supplies
them when deploying.

Render the chart locally with:

```sh
helm template raas ./helm/raas \
  --namespace raas \
  --set-string image.repository=docker.io/YOUR_DOCKERHUB_USERNAME/raas-backend \
  --set-string image.tag=sha-YOUR_COMMIT_SHA
```

The deploy workflow expects these GitHub repository variables:

- `DOCKERHUB_REPO`: Docker Hub namespace or repository prefix used by the build
  workflow, such as `docker.io/YOUR_DOCKERHUB_USERNAME`.
- `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, and `AZURE_SUBSCRIPTION_ID`: the Entra
  application/workload identity details used for GitHub OIDC.
- `AKS_RESOURCE_GROUP` and `AKS_CLUSTER_NAME`: the resource group and cluster
  containing the AKS cluster.

The workflow also expects `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` as GitHub
secrets so it can push the image. Configure an Entra federated identity
credential for this repository's `main` branch, using issuer
`https://token.actions.githubusercontent.com`, subject
`repo:OWNER/REPOSITORY:ref:refs/heads/main`, and audience
`api://AzureADTokenExchange`. Grant that identity permission to retrieve AKS
credentials and deploy Kubernetes resources. Because the Terraform AKS
configuration disables local accounts, the workflow uses `kubelogin`; give the
identity the Azure Kubernetes Service Cluster User role and the required AKS
RBAC permissions to manage resources in the `raas` namespace.

For a private Docker Hub image, configure an image-pull secret in the `raas`
namespace and set `image.pullSecrets` to its name in the chart values.
