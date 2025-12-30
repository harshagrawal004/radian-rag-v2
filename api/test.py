"""
Simple test endpoint to verify Vercel deployment
"""

def handler(event, context):
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': '{"status": "ok", "message": "Test endpoint working"}'
    }
