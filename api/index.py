"""
Vercel serverless function handler for FastAPI backend.
This file routes all /api/* requests to the FastAPI application.
"""

import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

# Import required modules
from mangum import Mangum
from app.main import app as fastapi_app

# Create Mangum handler - Vercel requires this specific pattern
def handler(event, context):
    # Debug logging
    import json
    print(f"[DEBUG] Event: {json.dumps(event, indent=2)}")
    print(f"[DEBUG] Context: {context}")

    asgi_handler = Mangum(fastapi_app, lifespan="off")
    response = asgi_handler(event, context)

    print(f"[DEBUG] Response: {response}")
    return response

