# RAAS Helm chart

This chart installs the RAAS API and its Qdrant StatefulSet into the `raas`
namespace. The deployment workflow runs tests, builds and pushes the API image
tagged with the commit SHA, then installs or upgrades this chart with Helm.

## Deploy from GitHub Actions

The workflow expects these GitHub repository variables:

- `DOCKERHUB_REPO`: Docker Hub namespace or repository prefix used by the build
  workflow, for example `docker.io/YOUR_DOCKERHUB_USERNAME`.
- `AKS_CLUSTER_NAME`: the AKS cluster name.
- `AKS_RESOURCE_GROUP`: the Azure resource group containing the cluster.

It expects these GitHub Actions secrets:

- `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN`: credentials used to push the
  image to Docker Hub. Use a Docker Hub access token, not the account password.
- `AZURE_CREDENTIALS`: the Azure service principal credentials JSON consumed by
  `azure/login`. The service principal must be able to retrieve credentials for
  the AKS cluster and deploy resources to the `raas` namespace.

The current workflow uses a stored Azure credential rather than GitHub OIDC.
OIDC with a federated identity is preferable when configured, because it avoids
keeping a long-lived Azure client secret in GitHub. The AKS Terraform
configuration disables local accounts, so the Azure identity also needs the
Azure Kubernetes Service Cluster User role and suitable Kubernetes/Azure RBAC
permissions. If authentication to the cluster fails, configure `kubelogin` for
the workflow's non-admin AKS context.

Render the chart locally with:

```sh
helm template raas ./helm/raas \
  --namespace raas \
  --set-string image.repository=docker.io/YOUR_DOCKERHUB_USERNAME/raas-backend \
  --set-string image.tag=sha-YOUR_COMMIT_SHA
```

For a private Docker Hub image, configure an image-pull secret in the `raas`
namespace and set `image.pullSecrets` to its name in the chart values.
