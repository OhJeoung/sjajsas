def check_signal(
    current_ma5,
    current_ma20,
    current_rsi,
    current_volume,
    avg_volume_20,
    prev_ma5=None,
    prev_ma20=None
):

    reasons = []

    # 골든크로스 조건
    if prev_ma5 is not None and prev_ma20 is not None:
        golden_cross = prev_ma5 <= prev_ma20 and current_ma5 > current_ma20
    else:
        golden_cross = False

    if not golden_cross:
        reasons.append("골든크로스 아님")

    # RSI 과열
    if current_rsi >= 70:
        reasons.append("과열 구간")

    # 거래량 증가
    if current_volume <= avg_volume_20:
        reasons.append("거래량 부족")

    if not reasons:
        return "매수 후보"

    return "관망 - " + ", ".join(reasons)