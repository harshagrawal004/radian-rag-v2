"""
Vercel serverless function handler for FastAPI backend.
This file routes all /api/* requests to the FastAPI application.
"""

import sys
import traceback
from pathlib import Path

# Add the backend directory to the Python path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

# Try to import and provide detailed error if it fails
try:
    # Import the FastAPI app
    from app.main import app

    # Import Mangum to convert ASGI (FastAPI) to AWS Lambda/Vercel format
    from mangum import Mangum

    # Create the handler instance
    # lifespan="auto" allows Mangum to handle startup/shutdown appropriately
    handler = Mangum(app, lifespan="auto")
except Exception as e:
    # If import fails, create a simple error handler
    print(f"CRITICAL ERROR during import: {e}", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)

    # Create a fallback handler that returns the error
    def handler(event, context):
        return {
            'statusCode': 500,
            'body': f'Import Error: {str(e)}\n\nTraceback:\n{traceback.format_exc()}'
        }

