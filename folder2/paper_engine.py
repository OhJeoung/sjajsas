from datetime import datetime

import pandas as pd

from indicator import calculate_ma, calculate_rsi
from strategy import check_sell_signal
from folder1.kis_candle import get_minute_candle
from folder2.trade_logger import (
    save_paper_trade,
    load_paper_trades,
    update_paper_trades,
)

TAKE_PROFIT_PCT = 0.3
STOP_LOSS_PCT = -0.2


def has_open_position(ticker):
    df = load_paper_trades()

    if df.empty:
        return False

    if "상태" not in df.columns:
        return False

    open_rows = df[(df["종목코드"] == ticker) & (df["상태"] == "보유")]
    return len(open_rows) > 0


def record_paper_entry(ticker, name, price, signal):
    if has_open_position(ticker):
        print(f"이미 보유 중이라 신규 모의진입 생략: {name} ({ticker})")
        return

    trade_data = {
        "시간": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "종목코드": ticker,
        "종목명": name,
        "진입가": price,
        "신호": signal,
        "상태": "보유",
        "청산시간": None,
        "청산가": None,
        "청산사유": None,
        "실현수익률(%)": None,
        "5분후가격": None,
        "10분후가격": None,
        "5분수익률(%)": None,
        "10분수익률(%)": None,
        "최대상승률(%)": None,
        "최대하락률(%)": None,
        "시뮬결과": None,
        "시뮬수익률(%)": None,
    }

    save_paper_trade(trade_data)
    print(f"모의진입 기록 완료: {name} ({ticker})")


def update_paper_trade_results():
    df = load_paper_trades()

    if df.empty:
        return

    required_columns = [
        "시간",
        "종목코드",
        "종목명",
        "진입가",
        "신호",
        "상태",
        "청산시간",
        "청산가",
        "청산사유",
        "실현수익률(%)",
        "5분후가격",
        "10분후가격",
        "5분수익률(%)",
        "10분수익률(%)",
        "최대상승률(%)",
        "최대하락률(%)",
        "시뮬결과",
        "시뮬수익률(%)",
    ]

    for col in required_columns:
        if col not in df.columns:
            df[col] = None

    df["신호"] = df["신호"].astype("object")
    df["상태"] = df["상태"].astype("object")
    df["청산사유"] = df["청산사유"].astype("object")
    df["시뮬결과"] = df["시뮬결과"].astype("object")

    now = datetime.now()

    for i in range(len(df)):
        try:
            status = df.loc[i, "상태"]

            # 이미 청산된 건 건너뜀
            if status == "청산":
                continue

            entry_time = datetime.strptime(str(df.loc[i, "시간"]), "%Y-%m-%d %H:%M:%S")
            ticker = str(df.loc[i, "종목코드"])
            stock_code = ticker.replace(".KS", "")
            entry_price = float(df.loc[i, "진입가"])

            # 당일 기록만 추적
            if entry_time.date() != now.date():
                continue

            candle_df = get_minute_candle(stock_code)

            if candle_df is None or candle_df.empty:
                continue

            candle_df["Time"] = candle_df["Time"].astype(str).str.zfill(6)
            candle_df["TimeInt"] = candle_df["Time"].astype(int)

            entry_time_int = int(entry_time.strftime("%H%M%S"))
            filtered = candle_df[candle_df["TimeInt"] >= entry_time_int].copy()

            if filtered.empty:
                continue

            close_series = filtered["Close"].reset_index(drop=True)
            volume_series = filtered["Volume"].reset_index(drop=True)

            ma5 = calculate_ma(close_series, 5)
            ma20 = calculate_ma(close_series, 20)
            rsi = calculate_rsi(close_series, 14)

            current_price = float(close_series.iloc[-1])
            max_price = float(close_series.max())
            min_price = float(close_series.min())

            max_return = ((max_price - entry_price) / entry_price) * 100
            min_return = ((min_price - entry_price) / entry_price) * 100

            df.loc[i, "최대상승률(%)"] = round(max_return, 2)
            df.loc[i, "최대하락률(%)"] = round(min_return, 2)

            minutes_passed = (now - entry_time).total_seconds() / 60

            # 5분 후 결과
            if pd.isna(df.loc[i, "5분후가격"]) and minutes_passed >= 5:
                return_5 = ((current_price - entry_price) / entry_price) * 100
                df.loc[i, "5분후가격"] = current_price
                df.loc[i, "5분수익률(%)"] = round(return_5, 2)
                print(f"5분 결과 기록: {ticker}")

            # 10분 후 결과
            if pd.isna(df.loc[i, "10분후가격"]) and minutes_passed >= 10:
                return_10 = ((current_price - entry_price) / entry_price) * 100
                df.loc[i, "10분후가격"] = current_price
                df.loc[i, "10분수익률(%)"] = round(return_10, 2)
                print(f"10분 결과 기록: {ticker}")

            # 기존 익절/손절 시뮬 기록
            if pd.isna(df.loc[i, "시뮬결과"]):
                if max_return >= TAKE_PROFIT_PCT:
                    df.loc[i, "시뮬결과"] = "익절"
                    df.loc[i, "시뮬수익률(%)"] = TAKE_PROFIT_PCT
                elif min_return <= STOP_LOSS_PCT:
                    df.loc[i, "시뮬결과"] = "손절"
                    df.loc[i, "시뮬수익률(%)"] = STOP_LOSS_PCT

            # 조건 기반 매도 판단
            if len(close_series) >= 20:
                current_ma5 = ma5.iloc[-1]
                current_ma20 = ma20.iloc[-1]
                current_rsi = rsi.iloc[-1]

                sell_signal = check_sell_signal(
                    entry_price,
                    current_price,
                    current_ma5,
                    current_ma20,
                    current_rsi
                )

                if sell_signal != "보유":
                    realized_return = ((current_price - entry_price) / entry_price) * 100

                    df.loc[i, "상태"] = "청산"
                    df.loc[i, "청산시간"] = now.strftime("%Y-%m-%d %H:%M:%S")
                    df.loc[i, "청산가"] = current_price
                    df.loc[i, "청산사유"] = sell_signal
                    df.loc[i, "실현수익률(%)"] = round(realized_return, 2)

                    print(f"모의청산 기록: {ticker} / {sell_signal}")

        except Exception as e:
            print(f"모의트레이드 결과 업데이트 에러: {e}")

    update_paper_trades(df)