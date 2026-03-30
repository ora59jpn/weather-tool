import requests

# OpenMeteoの無料天気APIを使用
API_URL = "https://api.open-meteo.com/v1/forecast"

def get_weather(latitude, longitude, city_name):
    """
    指定された緯度経度の天気情報を取得
    
    Args:
        latitude: 緯度
        longitude: 経度
        city_name: 都市名（表示用）
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature,weather_code,humidity",
        "timezone": "Asia/Tokyo"
    }
    
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        current = data['current']
        print(f"\n{city_name}の天気")
        print(f"気温: {current['temperature']}°C")
        print(f"湿度: {current['humidity']}%")
        
    except Exception as e:
        print(f"エラー: {e}")

if __name__ == "__main__":
    # 東京の天気を取得
    get_weather(35.6762, 139.6503, "東京")
    # 大阪の天気も取得
    get_weather(34.6937, 135.5023, "大阪")
