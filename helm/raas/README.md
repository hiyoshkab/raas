# RAAS Helm chart

This chart installs the RAAS frontend, API, and Qdrant StatefulSet into the
`raas` namespace. The app pipeline runs tests, builds and pushes the API image
tagged with the commit SHA, then calls the reusable Helm workflow to deploy it.
Changes under `helm/` trigger the same reusable workflow directly, reusing the
image repository and tag from the currently installed Helm release instead of
rebuilding the image.

## Deploy from GitHub Actions

The workflow expects these GitHub repository variables:

- `DOCKERHUB_REPO`: Docker Hub namespace or repository prefix used by the build
  workflow, for example `docker.io/YOUR_DOCKERHUB_USERNAME`.
- `AKS_CLUSTER_NAME`: the AKS cluster name.
- `AKS_RESOURCE_GROUP`: the Azure resource group containing the cluster.
- `AZURE_OPENAI_ENDPOINT`: endpoint provided to the app's ConfigMap at deploy
  time.
- `AZURE_APP_CLIENT_ID`: client ID from Terraform's `app_identity_client_id`
  output. It configures the app's Kubernetes service account for Azure
  Workload Identity.
- `FRONTEND_IMAGE_REPOSITORY` and `FRONTEND_IMAGE_TAG`: repository and tag for
  the separately built frontend image.

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
permissions. The deploy workflow installs `kubelogin` and configures the AKS
context to use it for Entra authentication. The app uses a separate
user-assigned identity federated to its Kubernetes service account; it does not
inherit the node identity's Azure permissions.

Render the chart locally with:

```sh
helm template raas ./helm/raas \
  --namespace raas \
  --set-string backendImage.repository=docker.io/YOUR_DOCKERHUB_USERNAME/raas-backend \
  --set-string backendImage.tag=sha-YOUR_COMMIT_SHA \
  --set-string frontendImage.repository=docker.io/YOUR_DOCKERHUB_USERNAME/raas-frontend \
  --set-string frontendImage.tag=YOUR_FRONTEND_TAG \
  --set-string azureWorkloadIdentity.clientId=YOUR_APP_IDENTITY_CLIENT_ID
```

For private Docker Hub images, configure an image-pull secret in the `raas`
namespace and set `backendImage.pullSecrets` and/or `frontendImage.pullSecrets`
to its name in the chart values.
