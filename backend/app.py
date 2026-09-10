from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Get API key from environment variable.
# No default placeholder. If the env var is missing, this becomes None.
WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY')
WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint for Kubernetes probes"""
    return jsonify({'status': 'healthy'}), 200

@app.route('/weather', methods=['GET'])
def get_weather():
    """Fetch weather data for a given city"""
    city = request.args.get('city')
    
    # Validate city parameter
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400
    
    # Validate that the API key is actually set
    if not WEATHER_API_KEY:
        return jsonify({'error': 'WEATHER_API_KEY environment variable is not set'}), 500
    
    params = {
        'q': city,
        'appid': WEATHER_API_KEY,
        'units': 'metric'  # Celsius
    }
    
    try:
        response = requests.get(WEATHER_API_URL, params=params, timeout=10)
        
        # Explicitly handle invalid API key (401 Unauthorized)
        if response.status_code == 401:
            return jsonify({'error': 'Invalid API Key. Please check your credentials.'}), 401
        
        response.raise_for_status()
        data = response.json()
        
        return jsonify({
            'city': data['name'],
            'country': data['sys']['country'],
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon']
        })
    
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to fetch weather: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)