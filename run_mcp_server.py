#!/usr/bin/env python3
"""
Script to run the Model Control Panel (MCP) server.
"""

import argparse
import logging
from src.mcp import start_server

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Model Control Panel (MCP) server")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to run the server on")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on")
    
    args = parser.parse_args()
    
    logger.info(f"Starting MCP server on {args.host}:{args.port}")
    start_server(host=args.host, port=args.port)