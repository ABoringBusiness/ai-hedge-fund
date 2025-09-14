# Waypoint Deployment for AI Hedge Fund

This document explains how to deploy the AI Hedge Fund application using HashiCorp Waypoint.

## Prerequisites

- [Waypoint](https://www.waypointproject.io/) installed
- Docker installed
- Kubernetes cluster configured (for Kubernetes deployment)

## Getting Started

1. Install Waypoint server (if not already installed):

```bash
waypoint server install -platform=kubernetes -accept-tos
```

2. Initialize the project:

```bash
waypoint init
```

3. Deploy the application:

```bash
waypoint up
```

This will build, deploy, and release the application according to the configuration in `waypoint.hcl`.

## Passing API Keys

You can pass API keys as variables:

```bash
waypoint up -var="api_keys={\"OPENAI_API_KEY\":\"sk-...\",\"ANTHROPIC_API_KEY\":\"sk-...\"}"
```

## Customizing Deployment

You can modify the `waypoint.hcl` file to customize the deployment:

- Change the tickers by modifying the `args` in the container configuration
- Adjust resource limits and requests
- Change the deployment target (e.g., from Kubernetes to Docker or Nomad)

## Viewing Logs

```bash
waypoint logs
```

## Destroying the Deployment

```bash
waypoint destroy
```

## Additional Resources

- [Waypoint Documentation](https://www.waypointproject.io/docs)
- [Waypoint Kubernetes Plugin](https://www.waypointproject.io/plugins/kubernetes)