"""
Vercel serverless function entry point.
This file serves as the entry point for all /api/* requests in Vercel.
"""

import sys
from pathlib import Path

# Add the parent directory to sys.path to import app
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

# Import the FastAPI app from the root-level app.py
from app import app
from mangum import Mangum

# Wrap FastAPI app with Mangum for serverless deployment
handler = Mangum(app, lifespan="off")
