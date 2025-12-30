"""
Vercel serverless function entry point.
This file serves as the entry point for all /api/* requests in Vercel.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to sys.path to import app
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

# Also add backend to path
backend_path = root_dir / "backend"
sys.path.insert(0, str(backend_path))

try:
    # Import the FastAPI app from the root-level app.py
    from app import app
    from mangum import Mangum

    # Wrap FastAPI app with Mangum for serverless deployment
    # api_gateway_base_path="/api" strips the /api prefix from incoming requests
    handler = Mangum(app, lifespan="off", api_gateway_base_path="/api")
except Exception as e:
    import traceback

    # Fallback handler that returns the error
    def handler(event, context):
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": f'{{"error": "Failed to load app", "details": "{str(e)}", "traceback": "{traceback.format_exc()}"}}'
        }
