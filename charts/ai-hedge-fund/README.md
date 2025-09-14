# AI Hedge Fund Helm Chart

This Helm chart deploys the AI Hedge Fund application on a Kubernetes cluster.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.2.0+

## Installing the Chart

To install the chart with the release name `my-release`:

```bash
# First, build and push the Docker image to your registry
docker build -t your-registry/ai-hedge-fund:latest .
docker push your-registry/ai-hedge-fund:latest

# Then install the Helm chart
helm install my-release ./charts/ai-hedge-fund \
  --set image.repository=your-registry/ai-hedge-fund \
  --set image.tag=latest \
  --set secrets.data.OPENAI_API_KEY=your-openai-api-key
```

## Uninstalling the Chart

To uninstall/delete the `my-release` deployment:

```bash
helm delete my-release
```

## Parameters

### Global parameters

| Name                      | Description                                     | Value |
| ------------------------- | ----------------------------------------------- | ----- |
| `replicaCount`            | Number of replicas to deploy                    | `1`   |
| `image.repository`        | Image repository                                | `ai-hedge-fund` |
| `image.tag`               | Image tag                                       | `latest` |
| `image.pullPolicy`        | Image pull policy                               | `IfNotPresent` |

### Application parameters

| Name                           | Description                                | Value |
| ------------------------------ | ------------------------------------------ | ----- |
| `application.tickers`          | Comma-separated list of stock tickers      | `AAPL,MSFT,GOOGL` |
| `application.initialCash`      | Initial cash position                      | `100000.0` |
| `application.marginRequirement`| Initial margin requirement                 | `0.0` |
| `application.showReasoning`    | Show reasoning from each agent             | `true` |
| `application.showAgentGraph`   | Show the agent graph                       | `false` |

### Secret parameters

| Name                      | Description                                     | Value |
| ------------------------- | ----------------------------------------------- | ----- |
| `secrets.enabled`         | Enable secrets                                  | `true` |
| `secrets.create`          | Create the secret                               | `true` |
| `secrets.name`            | Name of the secret                              | `ai-hedge-fund-secrets` |
| `secrets.data`            | Secret data to add                              | `{}` |

## Example: Setting API Keys

You can set your API keys in the `values.yaml` file:

```yaml
secrets:
  enabled: true
  create: true
  data:
    OPENAI_API_KEY: "your-openai-api-key"
    ANTHROPIC_API_KEY: "your-anthropic-api-key"
```

Or you can pass them as command-line arguments:

```bash
helm install my-release ./charts/ai-hedge-fund \
  --set secrets.data.OPENAI_API_KEY=your-openai-api-key \
  --set secrets.data.ANTHROPIC_API_KEY=your-anthropic-api-key
```