from datetime import datetime

from folder2.trade_logger import save_paper_trade


def record_paper_entry(ticker, name, price, signal):
    trade_data = {
        "시간": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "종목코드": ticker,
        "종목명": name,
        "진입가": price,
        "신호": signal
    }

    save_paper_trade(trade_data)
    print(f"모의진입 기록 완료: {name} ({ticker})")