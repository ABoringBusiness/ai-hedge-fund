# Model Control Panel (MCP)

The Model Control Panel (MCP) is a web-based interface for managing and monitoring the LLM models used by the AI Hedge Fund. It provides a user-friendly way to configure model parameters, switch between different models, and test model responses.

## Features

- **Model Selection**: Easily switch between different LLM models (OpenAI, Anthropic, Google, etc.)
- **Parameter Configuration**: Adjust temperature, top_p, max tokens, and other parameters for each model
- **Model Testing**: Test models with custom prompts and see responses in real-time
- **Usage Monitoring**: Track model usage statistics including call count and token usage

## Getting Started

### Prerequisites

- Python 3.9 or higher
- AI Hedge Fund dependencies installed

### Running the MCP Server

You can start the MCP server using the provided script:

```bash
python run_mcp_server.py
```

By default, the server runs on `http://0.0.0.0:8000`. You can specify a different host or port:

```bash
python run_mcp_server.py --host 127.0.0.1 --port 8080
```

### Accessing the Dashboard

Once the server is running, open your web browser and navigate to:

```
http://localhost:8000
```

## Using the MCP

### Selecting a Model

1. Browse the list of available models in the left panel
2. Click on a model to select it
3. Click "Set as Active Model" to make it the default model for the AI Hedge Fund

### Configuring Model Parameters

1. Select a model to configure
2. Adjust the parameters in the configuration form:
   - **Temperature**: Controls randomness (0 = deterministic, 1 = creative)
   - **Top P**: Controls diversity of token selection
   - **Max Tokens**: Maximum number of tokens to generate
   - **Frequency Penalty**: Reduces repetition of token sequences
   - **Presence Penalty**: Reduces repetition of topics
3. Click "Save Configuration" to apply the changes

### Testing a Model

1. Select the model you want to test
2. Enter a prompt in the test area
3. Click "Test Model" to generate a response
4. View the model's response in the response area

## Integration with AI Hedge Fund

The MCP is integrated with the AI Hedge Fund application and affects how the LLM models are used by the various analyst agents. When you change the active model or adjust parameters in the MCP, these changes will be reflected in the behavior of the AI Hedge Fund.

## Technical Details

The MCP is built using:

- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for running the FastAPI application
- **Jinja2**: Template engine for rendering the HTML dashboard
- **Bootstrap**: Front-end framework for responsive design

The server exposes both a web interface and a REST API that can be used programmatically.