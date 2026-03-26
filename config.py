import os
from dotenv import load_dotenv

load_dotenv()

# =========================
# 한국투자 API
# =========================

APP_KEY = os.getenv("APP_KEY")
APP_SECRET = os.getenv("APP_SECRET")
KIS_ENV = os.getenv("KIS_ENV", "vps")


# =========================
# 기타 설정
# =========================

TOP_N = 30
SCAN_INTERVAL_SECONDS = 60