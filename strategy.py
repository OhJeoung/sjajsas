def check_buy_signal(current_ma5, current_ma20, current_rsi, current_volume, avg_volume_20):
    reasons = []

    # 단기 추세
    if current_ma5 <= current_ma20:
        reasons.append("단기 추세 약함")

    # 과열 방지
    if current_rsi >= 65:
        reasons.append("과열 구간")

    # 거래량 급증 확인
    if current_volume <= avg_volume_20 * 1.5:
        reasons.append("거래량 급증 아님")

    if not reasons:
        return "매수 후보"

    return "관망 - " + ", ".join(reasons)


def check_sell_signal(entry_price, current_price, current_ma5, current_ma20, current_rsi):
    return_pct = ((current_price - entry_price) / entry_price) * 100

    # 손절
    if return_pct <= -0.5:
        return "매도 - 손절"

    # 익절
    if return_pct >= 1.0:
        return "매도 - 익절"

    # 추세 꺾임
    if current_ma5 <= current_ma20:
        return "매도 - 추세 약화"

    # 과열 구간
    if current_rsi >= 75:
        return "매도 - 과열"

    return "보유"