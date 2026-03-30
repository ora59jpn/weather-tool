# weather-tool

天気予報の小型ツール。複数都市の気象データをリアルタイムで取得・表示できるツールです。

## 機能

- 🌍 複数都市の天気情報取得
- 🌐 Flask Webアプリケーション
- 📊 リアルタイム天気表示
- 🔄 30秒自動更新
- 📱 レスポンシブデザイン
- ✅ 包括的なユニットテスト（12テスト、全てパス）

## セットアップ

### 必要な環境
- Python 3.7以上
- pip

### インストール

```bash
# 依存ライブラリをインストール
pip install -r requirements.txt
```

## 使い方

### Webアプリケーション（推奨）

```bash
# Flaskアプリケーションを起動
python app.py
```

起動後、ブラウザで以下のURLにアクセス：
- **http://localhost:5000** - メインページ（天気情報表示）

#### API エンドポイント

- `GET /` - メインページ（HTML）
- `GET /api/weather` - 全都市の天気データ（JSON）
- `GET /api/weather/<city_name>` - 指定都市の天気データ（JSON）

### コマンドラインツール

```bash
# 直接実行
python weather.py
```

## テスト実行

```bash
# ユニットテストを実行
python -m unittest test_weather -v
```

テスト結果：
- ✅ 12テスト全てパス
- 実行時間：約0.005秒
- カバレッジ：City、WeatherData、get_weather、format_weather_output、get_multiple_weather

## プロジェクト構造

```
weather-tool/
├── app.py                 # Flask Webアプリケーション
├── weather.py             # 天気データ取得モジュール
├── test_weather.py        # ユニットテスト
├── requirements.txt       # 依存ライブラリ
├── README.md              # このファイル
└── templates/
    └── index.html         # Webアプリケーション UI
```

## 機能詳細

### weather.py

主要なクラスと関数：

- **City**: 都市の地理情報（名前、緯度、経度）
- **WeatherData**: 天気データ（気温、湿度、天気コード）
- **get_weather(city)**: 単一都市の天気を取得
- **get_multiple_weather(cities)**: 複数都市の天気を一括取得
- **format_weather_output(weather_list)**: テーブル形式でフォーマット

### Webアプリケーション（app.py）

Flaskを使用したWebインターフェース：

- レスポンシブなモダンUI
- 30秒自動更新機能
- エラーハンドリング
- JSONベースのAPI

## サポートされている都市

デフォルトでは以下の都市に対応：

- 🏙️ 東京 (35.6762°N, 139.6503°E)
- 🏙️ 大阪 (34.6937°N, 135.5023°E)
- 🏙️ 京都 (35.0116°N, 135.7681°E)
- ❄️ 札幌 (43.0642°N, 141.3469°E)

都市を追加するには、`app.py` の `CITIES` リストを編集してください。

## 天気 API

Open-Meteo無料天気APIを使用しています。

- API: https://api.open-meteo.com/v1/forecast
- ドキュメント: https://open-meteo.com/

## ライセンス

MITライセンス
