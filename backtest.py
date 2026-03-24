import yfinance as yf

from indicator import calculate_ma, calculate_rsi
from strategy import check_signal
from stock_source import get_candidate_stocks


def backtest_stock(ticker, name):

    data = yf.download(ticker, period="5d", interval="1m", progress=False)

    if data.empty:
        print(f"{name} 데이터 없음")
        return None

    close_series = data["Close"].squeeze()
    volume_series = data["Volume"].squeeze()

    ma5 = calculate_ma(close_series, 5)
    ma20 = calculate_ma(close_series, 20)
    rsi = calculate_rsi(close_series, 14)
    avg_volume_20 = volume_series.rolling(20).mean()

    buy_count = 0
    win_count = 0
    total_return = 0

    cooldown_until = -1

    for i in range(len(data)):

        if i < 20:
            continue

        if i + 5 >= len(data):
            continue

        if i < cooldown_until:
            continue

        current_price = close_series.iloc[i]
        current_ma5 = ma5.iloc[i]
        current_ma20 = ma20.iloc[i]
        current_rsi = rsi.iloc[i]
        current_volume = volume_series.iloc[i]
        current_avg_volume_20 = avg_volume_20.iloc[i]

        signal = check_signal(
            current_ma5,
            current_ma20,
            current_rsi,
            current_volume,
            current_avg_volume_20
        )

        if "매수 후보" in signal:

            buy_count += 1

            future_price = close_series.iloc[i + 5]
            return_pct = ((future_price - current_price) / current_price) * 100

            total_return += return_pct

            if return_pct > 0:
                win_count += 1

            cooldown_until = i + 5

    if buy_count == 0:
        return {
            "ticker": ticker,
            "name": name,
            "count": 0,
            "avg": 0,
            "win": 0
        }

    avg_return = total_return / buy_count
    win_rate = (win_count / buy_count) * 100

    return {
        "ticker": ticker,
        "name": name,
        "count": buy_count,
        "avg": avg_return,
        "win": win_rate
    }


print("여러 종목 백테스트 시작\n")

stocks = get_candidate_stocks()

results = []

for ticker, name in stocks.items():

    print(f"{name} 테스트 중...")

    result = backtest_stock(ticker, name)

    if result:
        results.append(result)


print("\n==============================")
print("백테스트 결과 정리")
print("==============================\n")

# 평균 수익률 기준 정렬
results = sorted(results, key=lambda x: x["avg"], reverse=True)

for r in results:

    print(
        f"{r['name']} ({r['ticker']}) | "
        f"신호: {r['count']} | "
        f"평균수익률: {round(r['avg'], 2)}% | "
        f"승률: {round(r['win'], 2)}%"
    )