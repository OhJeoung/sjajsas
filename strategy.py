def check_signal(current_ma5, current_ma20, current_rsi, current_volume, avg_volume_20):
    reasons = []

    # 단기 추세 확인
    if current_ma5 <= current_ma20:
        reasons.append("단기 추세 약함")

    # 과열 여부 확인
    if current_rsi >= 70:
        reasons.append("과열 구간")

    # 거래량 확인
    if current_volume <= avg_volume_20:
        reasons.append("거래량 부족")

    if not reasons:
        return "매수 후보"

    return "관망 - " + ", ".join(reasons)