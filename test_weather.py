import unittest
from unittest.mock import patch, MagicMock
import requests

from weather import (
    City, WeatherData, get_weather, format_weather_output,
    get_multiple_weather, WeatherAPIError, NetworkError
)


class TestCity(unittest.TestCase):
    """City クラスのテスト"""

    def test_city_creation(self):
        """City オブジェクトの作成テスト"""
        city = City("東京", 35.6762, 139.6503)
        self.assertEqual(city.name, "東京")
        self.assertEqual(city.latitude, 35.6762)
        self.assertEqual(city.longitude, 139.6503)


class TestWeatherData(unittest.TestCase):
    """WeatherData クラスのテスト"""

    def test_weather_data_creation(self):
        """WeatherData オブジェクトの作成テスト"""
        weather = WeatherData("東京", 25.5, 65, 0)
        self.assertEqual(weather.city, "東京")
        self.assertEqual(weather.temperature, 25.5)
        self.assertEqual(weather.humidity, 65)
        self.assertEqual(weather.weather_code, 0)


class TestGetWeather(unittest.TestCase):
    """get_weather 関数のテスト"""

    @patch('weather.requests.get')
    def test_get_weather_success(self, mock_get):
        """正常な天気データ取得のテスト"""
        # モックレスポンスを設定
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'current': {
                'temperature': 25.5,
                'humidity': 65,
                'weather_code': 0
            }
        }
        mock_get.return_value = mock_response

        city = City("東京", 35.6762, 139.6503)
        result = get_weather(city)

        self.assertIsInstance(result, WeatherData)
        self.assertEqual(result.city, "東京")
        self.assertEqual(result.temperature, 25.5)
        self.assertEqual(result.humidity, 65)

    @patch('weather.requests.get')
    def test_get_weather_timeout(self, mock_get):
        """タイムアウトエラーのテスト"""
        mock_get.side_effect = requests.exceptions.Timeout()

        city = City("東京", 35.6762, 139.6503)
        with self.assertRaises(NetworkError):
            get_weather(city)

    @patch('weather.requests.get')
    def test_get_weather_connection_error(self, mock_get):
        """接続エラーのテスト"""
        mock_get.side_effect = requests.exceptions.ConnectionError()

        city = City("東京", 35.6762, 139.6503)
        with self.assertRaises(NetworkError):
            get_weather(city)

    @patch('weather.requests.get')
    def test_get_weather_http_error(self, mock_get):
        """HTTPエラーのテスト"""
        mock_response = MagicMock()
        http_error = requests.exceptions.HTTPError()
        http_error.response = MagicMock()
        http_error.response.status_code = 404
        mock_response.raise_for_status.side_effect = http_error
        mock_get.return_value = mock_response

        city = City("東京", 35.6762, 139.6503)
        with self.assertRaises(WeatherAPIError):
            get_weather(city)

    @patch('weather.requests.get')
    def test_get_weather_invalid_response(self, mock_get):
        """不正なレスポンスのテスト"""
        mock_response = MagicMock()
        mock_response.json.return_value = {'invalid': 'data'}
        mock_get.return_value = mock_response

        city = City("東京", 35.6762, 139.6503)
        with self.assertRaises(WeatherAPIError):
            get_weather(city)


class TestFormatWeatherOutput(unittest.TestCase):
    """format_weather_output 関数のテスト"""

    def test_format_empty_list(self):
        """空リストのフォーマットテスト"""
        result = format_weather_output([])
        self.assertEqual(result, "天気データがありません")

    def test_format_single_weather(self):
        """単一天気データのフォーマットテスト"""
        weather = WeatherData("東京", 25.5, 65, 0)
        result = format_weather_output([weather])

        self.assertIn("都市名", result)
        self.assertIn("東京", result)
        self.assertIn("25.5", result)
        self.assertIn("65", result)

    def test_format_multiple_weather(self):
        """複数天気データのフォーマットテスト"""
        weather_list = [
            WeatherData("東京", 25.5, 65, 0),
            WeatherData("大阪", 26.0, 70, 0),
        ]
        result = format_weather_output(weather_list)

        self.assertIn("東京", result)
        self.assertIn("大阪", result)
        self.assertIn("25.5", result)
        self.assertIn("26.0", result)


class TestGetMultipleWeather(unittest.TestCase):
    """get_multiple_weather 関数のテスト"""

    @patch('weather.requests.get')
    def test_get_multiple_weather_success(self, mock_get):
        """複数都市の天気取得成功テスト"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'current': {
                'temperature': 25.5,
                'humidity': 65,
                'weather_code': 0
            }
        }
        mock_get.return_value = mock_response

        cities = [
            City("東京", 35.6762, 139.6503),
            City("大阪", 34.6937, 135.5023),
        ]
        result = get_multiple_weather(cities)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].city, "東京")
        self.assertEqual(result[1].city, "大阪")

    @patch('weather.get_weather')
    def test_get_multiple_weather_partial_failure(self, mock_get_weather):
        """部分的な失敗を含む複数都市取得テスト"""
        mock_get_weather.side_effect = [
            WeatherData("東京", 25.5, 65, 0),
            NetworkError("大阪: ネットワーク接続エラー"),
        ]

        cities = [
            City("東京", 35.6762, 139.6503),
            City("大阪", 34.6937, 135.5023),
        ]
        result = get_multiple_weather(cities)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].city, "東京")


if __name__ == '__main__':
    unittest.main()
