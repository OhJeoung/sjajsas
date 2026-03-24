from config import STOCK_SOURCE_MODE, MANUAL_STOCKS, TOP_N


def get_candidate_stocks():
    if STOCK_SOURCE_MODE == "manual":
        return MANUAL_STOCKS

    elif STOCK_SOURCE_MODE == "top_volume":
        # 나중에 한국투자증권 API 연결 시 이 부분 구현
        print(f"거래량 상위 {TOP_N}개 종목 기능은 아직 준비 중입니다.")
        return MANUAL_STOCKS

    else:
        print("알 수 없는 STOCK_SOURCE_MODE입니다. manual 모드로 진행합니다.")
        return MANUAL_STOCKS