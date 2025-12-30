"""
Vercel serverless function handler for FastAPI backend.
This file routes all /api/* requests to the FastAPI application.
"""

import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

# Import the FastAPI app
from app.main import app as fastapi_app

# For Vercel, we need to export the ASGI app directly
# Vercel will handle the ASGI protocol
app = fastapi_app

