import requests
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

# OpenMeteoの無料天気APIを使用
API_URL = "https://api.open-meteo.com/v1/forecast"
API_TIMEOUT = 5

class WeatherCode(Enum):
    """天気コードのマッピング"""
    CLEAR = 0
    MAINLY_CLEAR = (1, 2)
    PARTLY_CLOUDY = 3
    OVERCAST = 45
    FOGGY = 48
    LIGHT_DRIZZLE = (51, 53, 55)
    RAIN = (61, 63, 65)
    SNOW = (71, 73, 75)
    HEAVY_RAIN = 80
    THUNDERSTORM = (80, 82, 85, 86)

@dataclass
class City:
    """都市の地理情報"""
    name: str
    latitude: float
    longitude: float

@dataclass
class WeatherData:
    """天気データ"""
    city: str
    temperature: float
    humidity: int
    weather_code: int

class WeatherAPIError(Exception):
    """天気API固有のエラー"""
    pass

class NetworkError(Exception):
    """ネットワークエラー"""
    pass

def get_weather(city: City) -> Optional[WeatherData]:
    """
    指定された都市の天気情報を取得

    Args:
        city: City オブジェクト

    Returns:
        WeatherData オブジェクト、またはエラー時は None

    Raises:
        NetworkError: ネットワーク接続エラー
        WeatherAPIError: API固有のエラー
    """
    params = {
        "latitude": city.latitude,
        "longitude": city.longitude,
        "current": "temperature,weather_code,humidity",
        "timezone": "Asia/Tokyo"
    }

    try:
        response = requests.get(API_URL, params=params, timeout=API_TIMEOUT)
        response.raise_for_status()
        data = response.json()

        current = data['current']
        return WeatherData(
            city=city.name,
            temperature=current['temperature'],
            humidity=current['humidity'],
            weather_code=current['weather_code']
        )

    except requests.exceptions.Timeout:
        raise NetworkError(f"{city.name}: リクエストがタイムアウトしました")
    except requests.exceptions.ConnectionError:
        raise NetworkError(f"{city.name}: ネットワーク接続エラー")
    except requests.exceptions.HTTPError as e:
        raise WeatherAPIError(f"{city.name}: HTTPエラー {e.response.status_code}")
    except (KeyError, ValueError) as e:
        raise WeatherAPIError(f"{city.name}: レスポンスデータが不正です: {e}")

def format_weather_output(weather_list: List[WeatherData]) -> str:
    """
    天気データをテーブル形式でフォーマット

    Args:
        weather_list: WeatherData のリスト

    Returns:
        フォーマット済みの文字列
    """
    if not weather_list:
        return "天気データがありません"

    # ヘッダー
    header = f"{'都市名':<10} | {'気温 (°C)':<8} | {'湿度 (%)':<8}"
    separator = "-" * len(header)

    lines = ["\n" + header, separator]

    for weather in weather_list:
        line = f"{weather.city:<10} | {weather.temperature:>6.1f}  | {weather.humidity:>6}  "
        lines.append(line)

    return "\n".join(lines) + "\n"

def get_multiple_weather(cities: List[City]) -> List[WeatherData]:
    """
    複数都市の天気情報を取得

    Args:
        cities: City オブジェクトのリスト

    Returns:
        WeatherData オブジェクトのリスト
    """
    results = []
    errors = []

    for city in cities:
        try:
            weather = get_weather(city)
            results.append(weather)
        except (NetworkError, WeatherAPIError) as e:
            errors.append(str(e))

    if errors:
        print("エラーが発生しました:")
        for error in errors:
            print(f"  ✗ {error}")

    return results

if __name__ == "__main__":
    # 複数都市の定義
    cities = [
        City("東京", 35.6762, 139.6503),
        City("大阪", 34.6937, 135.5023),
        City("京都", 35.0116, 135.7681),
        City("札幌", 43.0642, 141.3469),
    ]

    # 天気情報を取得して表示
    weather_data = get_multiple_weather(cities)
    print(format_weather_output(weather_data))
