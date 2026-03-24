from config import TOP_N, MANUAL_STOCKS


def get_top_volume_stocks():
    """
    나중에 한국투자증권 API로 거래량 상위 N개를 가져올 함수
    지금은 임시로 수동 종목 반환
    """
    print(f"거래량 상위 {TOP_N}개 종목 기능 준비 중")
    return MANUAL_STOCKS