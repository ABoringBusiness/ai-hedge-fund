"""
Model Control Panel (MCP) server for managing and monitoring LLM models.
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any, Union
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request, HTTPException, Depends, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from src.llm.models import LLM_ORDER, get_model_info, get_llm_model, ModelInfo, ModelProvider

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="AI Hedge Fund - Model Control Panel")

# Get the directory of the current file
current_dir = Path(__file__).parent

# Mount static files
app.mount("/static", StaticFiles(directory=str(current_dir / "static")), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory=str(current_dir / "templates"))

# Model configuration storage
model_configs = {}
active_model = {"name": "gpt-4o", "provider": "OpenAI"}
model_usage = {}


class ModelConfig(BaseModel):
    """Model configuration settings."""
    name: str
    provider: str
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    stop_sequences: Optional[List[str]] = None


class ModelUsage(BaseModel):
    """Model usage statistics."""
    name: str
    provider: str
    total_calls: int = 0
    total_tokens: int = 0
    average_latency: float = 0.0


@app.get("/", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    """Render the main dashboard."""
    # Get all available models
    available_models = [{"display": display, "name": name, "provider": provider} 
                       for display, name, provider in LLM_ORDER]
    
    # Get active model
    active = active_model
    
    # Get model configurations
    configs = model_configs
    
    # Get model usage statistics
    usage = model_usage
    
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "available_models": available_models,
            "active_model": active,
            "model_configs": configs,
            "model_usage": usage,
        }
    )


@app.get("/api/models", response_class=JSONResponse)
async def get_models():
    """Get all available models."""
    models = [{"display": display, "name": name, "provider": provider} 
             for display, name, provider in LLM_ORDER]
    return {"models": models}


@app.get("/api/models/active", response_class=JSONResponse)
async def get_active_model():
    """Get the currently active model."""
    return active_model


@app.post("/api/models/active", response_class=JSONResponse)
async def set_active_model(model: ModelConfig):
    """Set the active model."""
    global active_model
    
    # Validate that the model exists
    model_exists = False
    for _, name, provider in LLM_ORDER:
        if name == model.name and provider.value == model.provider:
            model_exists = True
            break
    
    if not model_exists:
        raise HTTPException(status_code=404, detail=f"Model {model.name} with provider {model.provider} not found")
    
    # Update active model
    active_model = {"name": model.name, "provider": model.provider}
    
    # Save model configuration if it doesn't exist
    config_key = f"{model.name}_{model.provider}"
    if config_key not in model_configs:
        model_configs[config_key] = {
            "temperature": model.temperature,
            "max_tokens": model.max_tokens,
            "top_p": model.top_p,
            "frequency_penalty": model.frequency_penalty,
            "presence_penalty": model.presence_penalty,
            "stop_sequences": model.stop_sequences or [],
        }
    
    return {"status": "success", "active_model": active_model}


@app.get("/api/models/{model_name}/config", response_class=JSONResponse)
async def get_model_config(model_name: str, provider: str):
    """Get configuration for a specific model."""
    config_key = f"{model_name}_{provider}"
    
    if config_key not in model_configs:
        # Create default configuration
        model_configs[config_key] = {
            "temperature": 0.7,
            "max_tokens": None,
            "top_p": 1.0,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
            "stop_sequences": [],
        }
    
    return {"model": model_name, "provider": provider, "config": model_configs[config_key]}


@app.post("/api/models/{model_name}/config", response_class=JSONResponse)
async def update_model_config(model_name: str, provider: str, config: dict):
    """Update configuration for a specific model."""
    config_key = f"{model_name}_{provider}"
    
    # Update configuration
    model_configs[config_key] = {
        "temperature": config.get("temperature", 0.7),
        "max_tokens": config.get("max_tokens"),
        "top_p": config.get("top_p", 1.0),
        "frequency_penalty": config.get("frequency_penalty", 0.0),
        "presence_penalty": config.get("presence_penalty", 0.0),
        "stop_sequences": config.get("stop_sequences", []),
    }
    
    return {"status": "success", "model": model_name, "provider": provider, "config": model_configs[config_key]}


@app.get("/api/models/usage", response_class=JSONResponse)
async def get_model_usage():
    """Get usage statistics for all models."""
    return {"usage": model_usage}


@app.post("/api/models/test", response_class=JSONResponse)
async def test_model(model_name: str, provider: str, prompt: str):
    """Test a model with a prompt."""
    try:
        # Get model
        model_provider = ModelProvider(provider)
        model = get_llm_model(model_name=model_name, model_provider=model_provider)
        
        # Apply configuration if available
        config_key = f"{model_name}_{provider}"
        if config_key in model_configs:
            config = model_configs[config_key]
            # Apply configuration to model (implementation depends on the model type)
            # This is a simplified example
            if hasattr(model, "temperature"):
                model.temperature = config["temperature"]
        
        # Generate response
        response = model.invoke(prompt)
        
        # Update usage statistics
        if config_key not in model_usage:
            model_usage[config_key] = {
                "name": model_name,
                "provider": provider,
                "total_calls": 0,
                "total_tokens": 0,
                "average_latency": 0.0,
            }
        
        model_usage[config_key]["total_calls"] += 1
        
        return {"status": "success", "response": response}
    
    except Exception as e:
        logger.error(f"Error testing model: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/dashboard/set-active-model", response_class=RedirectResponse)
async def dashboard_set_active_model(
    model_name: str = Form(...),
    provider: str = Form(...),
):
    """Set active model from dashboard form."""
    global active_model
    active_model = {"name": model_name, "provider": provider}
    return RedirectResponse(url="/", status_code=303)


@app.post("/dashboard/update-config", response_class=RedirectResponse)
async def dashboard_update_config(
    model_name: str = Form(...),
    provider: str = Form(...),
    temperature: float = Form(0.7),
    max_tokens: Optional[int] = Form(None),
    top_p: float = Form(1.0),
    frequency_penalty: float = Form(0.0),
    presence_penalty: float = Form(0.0),
):
    """Update model configuration from dashboard form."""
    config_key = f"{model_name}_{provider}"
    
    # Update configuration
    model_configs[config_key] = {
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_p": top_p,
        "frequency_penalty": frequency_penalty,
        "presence_penalty": presence_penalty,
        "stop_sequences": [],
    }
    
    return RedirectResponse(url="/", status_code=303)


def start_server(host: str = "0.0.0.0", port: int = 8000):
    """Start the MCP server."""
    uvicorn.run("src.mcp.server:app", host=host, port=port, reload=True)


if __name__ == "__main__":
    start_server()