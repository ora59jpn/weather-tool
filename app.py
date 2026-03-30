from flask import Flask, render_template, jsonify
import json
from weather import City, get_weather, get_multiple_weather, format_weather_output, WeatherAPIError, NetworkError

app = Flask(__name__)

# デフォルトの都市リスト
CITIES = [
    City("東京", 35.6762, 139.6503),
    City("大阪", 34.6937, 135.5023),
    City("京都", 35.0116, 135.7681),
    City("札幌", 43.0642, 141.3469),
]

@app.route('/')
def index():
    """メインページ"""
    return render_template('index.html')

@app.route('/api/weather')
def api_weather():
    """天気データAPI"""
    try:
        weather_data = get_multiple_weather(CITIES)

        # WeatherDataオブジェクトを辞書に変換
        result = []
        for weather in weather_data:
            result.append({
                'city': weather.city,
                'temperature': weather.temperature,
                'humidity': weather.humidity,
                'weather_code': weather.weather_code
            })

        return jsonify({
            'success': True,
            'data': result,
            'timestamp': __import__('datetime').datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/weather/<city_name>')
def api_weather_single(city_name):
    """指定された都市の天気データAPI"""
    try:
        # 都市を検索
        target_city = None
        for city in CITIES:
            if city.name == city_name:
                target_city = city
                break

        if not target_city:
            return jsonify({
                'success': False,
                'error': f'都市 "{city_name}" が見つかりません'
            }), 404

        weather = get_weather(target_city)

        return jsonify({
            'success': True,
            'data': {
                'city': weather.city,
                'temperature': weather.temperature,
                'humidity': weather.humidity,
                'weather_code': weather.weather_code
            },
            'timestamp': __import__('datetime').datetime.now().isoformat()
        })
    except (NetworkError, WeatherAPIError) as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 503
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
