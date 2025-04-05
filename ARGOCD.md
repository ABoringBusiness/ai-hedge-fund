# ArgoCD Deployment for AI Hedge Fund

This document explains how to deploy the AI Hedge Fund application using ArgoCD for GitOps-based continuous delivery.

## Prerequisites

- Kubernetes cluster with ArgoCD installed
- Access to the ArgoCD UI or CLI

## Setup

1. First, ensure ArgoCD is installed in your cluster:

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

2. Access the ArgoCD UI:

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Then visit https://localhost:8080 in your browser.

3. Apply the AI Hedge Fund application manifest:

```bash
kubectl apply -f argocd/application.yaml
```

## Configuration

The ArgoCD configuration consists of:

- `application.yaml`: Defines the application, source repository, and sync policy
- `namespace.yaml`: Creates the application namespace
- `secrets.yaml`: Template for creating secrets (should be customized for production)
- `kustomization.yaml`: Kustomize configuration to apply all resources

## Managing Secrets

For production, you should use a secure method to manage secrets:

1. Using Sealed Secrets:
```bash
# Install kubeseal
kubectl apply -f https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.19.5/controller.yaml

# Create a sealed secret
kubeseal -o yaml < argocd/secrets.yaml > argocd/sealed-secrets.yaml
```

2. Using Vault:
```bash
# Configure Vault integration with ArgoCD
# See: https://argo-cd.readthedocs.io/en/stable/operator-manual/secret-management/vault/
```

## Syncing the Application

ArgoCD will automatically sync the application based on the sync policy defined in `application.yaml`. You can also manually sync from the ArgoCD UI or using the CLI:

```bash
argocd app sync ai-hedge-fund
```

## Monitoring Deployment Status

```bash
argocd app get ai-hedge-fund
```

## Additional Resources

- [ArgoCD Documentation](https://argo-cd.readthedocs.io/en/stable/)
- [Kustomize Documentation](https://kubectl.docs.kubernetes.io/guides/introduction/kustomize/)