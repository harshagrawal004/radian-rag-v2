"""
Simple test endpoint to verify Vercel Python functions work.
"""

def handler(event, context):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": '{"message": "Python function works!", "event": "' + str(event.get('path', 'no path')) + '"}'
    }
