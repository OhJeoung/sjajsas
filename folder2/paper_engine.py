from datetime import datetime

import pandas as pd
import yfinance as yf

from folder2.trade_logger import save_paper_trade, load_paper_trades, update_paper_trades

TAKE_PROFIT_PCT = 0.3   # 익절 기준 (%)
STOP_LOSS_PCT = -0.2    # 손절 기준 (%)


def record_paper_entry(ticker, name, price, signal):
    trade_data = {
        "시간": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "종목코드": ticker,
        "종목명": name,
        "진입가": price,
        "신호": signal,
        "5분후가격": None,
        "10분후가격": None,
        "5분수익률(%)": None,
        "10분수익률(%)": None,
        "최대상승률(%)": None,
        "최대하락률(%)": None,
        "시뮬결과": None,
        "시뮬수익률(%)": None
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
        "5분후가격",
        "10분후가격",
        "5분수익률(%)",
        "10분수익률(%)",
        "최대상승률(%)",
        "최대하락률(%)",
        "시뮬결과",
        "시뮬수익률(%)"
    ]

    for col in required_columns:
        if col not in df.columns:
            df[col] = None

    now = datetime.now()

    for i in range(len(df)):
        try:
            entry_time = datetime.strptime(str(df.loc[i, "시간"]), "%Y-%m-%d %H:%M:%S")
            ticker = df.loc[i, "종목코드"]
            entry_price = float(df.loc[i, "진입가"])

            minutes_passed = (now - entry_time).total_seconds() / 60

            data = yf.download(
                ticker,
                start=entry_time.strftime("%Y-%m-%d"),
                interval="1m",
                progress=False
            )

            if data.empty:
                continue

            close_series = data["Close"].squeeze()

            # yfinance 인덱스가 timezone 포함일 수 있어 문자열 비교 대신 최대한 단순 처리
            filtered = close_series

            if filtered.empty:
                continue

            max_price = filtered.max()
            min_price = filtered.min()

            max_return = ((max_price - entry_price) / entry_price) * 100
            min_return = ((min_price - entry_price) / entry_price) * 100

            df.loc[i, "최대상승률(%)"] = round(max_return, 2)
            df.loc[i, "최대하락률(%)"] = round(min_return, 2)

            latest_price = float(close_series.iloc[-1])

            if pd.isna(df.loc[i, "5분후가격"]) and minutes_passed >= 5:
                return_5 = ((latest_price - entry_price) / entry_price) * 100
                df.loc[i, "5분후가격"] = latest_price
                df.loc[i, "5분수익률(%)"] = round(return_5, 2)
                print(f"5분 결과 기록: {ticker}")

            if pd.isna(df.loc[i, "10분후가격"]) and minutes_passed >= 10:
                return_10 = ((latest_price - entry_price) / entry_price) * 100
                df.loc[i, "10분후가격"] = latest_price
                df.loc[i, "10분수익률(%)"] = round(return_10, 2)
                print(f"10분 결과 기록: {ticker}")

            # 가상 익절/손절 결과
            if pd.isna(df.loc[i, "시뮬결과"]):
                if max_return >= TAKE_PROFIT_PCT:
                    df.loc[i, "시뮬결과"] = "익절"
                    df.loc[i, "시뮬수익률(%)"] = TAKE_PROFIT_PCT
                    print(f"익절 기록: {ticker}")

                elif min_return <= STOP_LOSS_PCT:
                    df.loc[i, "시뮬결과"] = "손절"
                    df.loc[i, "시뮬수익률(%)"] = STOP_LOSS_PCT
                    print(f"손절 기록: {ticker}")

        except Exception as e:
            print(f"모의트레이드 결과 업데이트 에러: {e}")

    update_paper_trades(df)