from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Backend service URL (Kubernetes Service name in cluster)
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://backend-service:5001')

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/weather', methods=['GET'])
def weather():
    """Proxy request to backend API"""
    city = request.args.get('city')
    
    if not city:
        return jsonify({'error': 'City is required'}), 400
    
    try:
        response = requests.get(f"{BACKEND_URL}/weather", params={'city': city}, timeout=10)
        response.raise_for_status()
        return jsonify(response.json())
    
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Backend service unavailable'}), 503
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
