# =========================
# 실행 설정
# =========================
SCAN_INTERVAL_SECONDS = 60

# =========================
# 장 시간 설정
# =========================
MARKET_START_HOUR = 9
MARKET_START_MINUTE = 0

MARKET_END_HOUR = 15
MARKET_END_MINUTE = 20

# =========================
# 파일 설정
# =========================
BUY_CANDIDATES_FILE = "buy_candidates.csv"
LOG_FILE = "scanner.log"

# =========================
# 종목 공급 방식 설정
# manual: 내가 직접 지정한 종목 목록 사용
# top_volume: 나중에 API로 거래량 상위 종목 사용
# =========================
STOCK_SOURCE_MODE = "manual"

# 거래량 상위 몇 개를 볼지
TOP_N = 30

# =========================
# 수동 종목 목록
# STOCK_SOURCE_MODE가 "manual"일 때 사용
# =========================
MANUAL_STOCKS = {
    "005930.KS": "삼성전자",
    "000660.KS": "SK하이닉스",
    "035420.KS": "NAVER",
    "035720.KS": "카카오"
}