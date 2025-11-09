from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Your GROK API key - using environment variable for security
GROK_API_KEY = os.environ.get('GROK_API_KEY', 'YOUR_API_KEY_HERE')

@app.route('/api/grok-proxy', methods=['POST'])
def grok_proxy():
    try:
        # Get the request data from the frontend
        data = request.get_json()
        
        # Forward the request to GROK API
        headers = {
            'Authorization': f'Bearer {GROK_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            'https://api.x.ai/v1/chat/completions',
            headers=headers,
            json=data,
            timeout=30
        )
        
        # Return the response from GROK API
        return jsonify(response.json()), response.status_code
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/grok-models', methods=['GET'])
def grok_models():
    try:
        # Forward the request to GROK API models endpoint
        headers = {
            'Authorization': f'Bearer {GROK_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(
            'https://api.x.ai/v1/models',
            headers=headers,
            timeout=30
        )
        
        # Return the response from GROK API
        return jsonify(response.json()), response.status_code
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)