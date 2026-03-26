import os
from dotenv import load_dotenv

load_dotenv()

# =========================
# 한국투자 API
# =========================

APP_KEY = os.getenv("APP_KEY")
APP_SECRET = os.getenv("APP_SECRET")
ACCOUNT_NO = os.getenv("ACCOUNT_NO")
PRODUCT_CODE = os.getenv("PRODUCT_CODE", "01")
KIS_ENV = os.getenv("KIS_ENV", "vps")

if KIS_ENV == "prod":
    BASE_URL = "https://openapi.koreainvestment.com:9443"
else:
    BASE_URL = "https://openapivts.koreainvestment.com:29443"

# =========================
# 스캐너 설정
# =========================

SCAN_INTERVAL_SECONDS = 60
TOP_N = 30


# =========================
# 종목 소스 설정
# =========================

STOCK_SOURCE_MODE = "top_volume"

MANUAL_STOCKS = {
    "005930.KS": "삼성전자",
    "000660.KS": "SK하이닉스",
    "035420.KS": "NAVER",
    "035720.KS": "카카오"
}


# =========================
# 파일 설정
# =========================

BUY_CANDIDATES_FILE = "buy_candidates.csv"
PAPER_TRADES_FILE = "paper_trades.csv"
LOG_FILE = "scanner.log"


# =========================
# 장 시간 설정
# =========================

MARKET_START_HOUR = 0
MARKET_START_MINUTE = 0

MARKET_END_HOUR = 23
MARKET_END_MINUTE = 59


# =========================
# 전략 설정
# =========================

RSI_PERIOD = 14
MA_SHORT = 5
MA_LONG = 20

VOLUME_MULTIPLIER = 1.2

# =========================
# 후보군 필터 설정
# =========================

MIN_PRICE = 1000      # 1000원 미만 제외
MAX_PRICE = 1500000    # 10만원 초과 제외 (원치 않으면 크게 올리기)

EXCLUDE_KEYWORDS = [
    "KODEX",
    "TIGER",
    "KOSEF",
    "KBSTAR",
    "HANARO",
    "ARIRANG",
    "SOL",
    "ACE",
    "PLUS",
    "ETN",
    "인버스",
    "레버리지",
    "스팩",
    "우",
    "우B"
    "선물"
]