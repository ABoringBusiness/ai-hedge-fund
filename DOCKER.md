# Docker Setup for AI Hedge Fund

This document explains how to run the AI Hedge Fund application using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose installed on your system

## Quick Start

1. Create a `.env` file with your API keys (copy from `.env.example` and fill in your values)

2. Build and run the application using Docker Compose:

```bash
docker-compose up --build
```

This will start the application with default parameters (analyzing AAPL, MSFT, and GOOGL stocks).

## Customizing Parameters

You can modify the `docker-compose.yml` file to change the command-line arguments:

```yaml
command: ["--tickers", "AAPL,MSFT,GOOGL", "--show-reasoning"]
```

Available parameters:
- `--tickers`: Comma-separated list of stock ticker symbols
- `--start-date`: Start date (YYYY-MM-DD)
- `--end-date`: End date (YYYY-MM-DD)
- `--initial-cash`: Initial cash position (default: 100000.0)
- `--margin-requirement`: Initial margin requirement (default: 0.0)
- `--show-reasoning`: Show reasoning from each agent
- `--show-agent-graph`: Show the agent graph

## Running with Custom Parameters

You can also run the Docker container directly with custom parameters:

```bash
docker build -t ai-hedge-fund .
docker run -it --env-file .env ai-hedge-fund --tickers TSLA,AMZN --start-date 2023-01-01 --end-date 2023-12-31
```

## Development with Docker

For development, you can mount your local code into the container:

```bash
docker run -it --env-file .env -v $(pwd):/app ai-hedge-fund --tickers AAPL
```

This allows you to make changes to the code and see them reflected immediately in the container.