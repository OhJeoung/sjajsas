import yfinance as yf
import pandas as pd

# 삼성전자 (한국 주식은 .KS 붙임)
ticker = "005930.KS"

data = yf.download(ticker, period="5d", interval="1m")

print(data.tail())

ticker = "005930.KS"
data = yf.download(ticker, period="5d", interval="1m")

# 종가만 사용
close_series = data["Close"].squeeze()

# 이동평균선 계산
ma5 = close_series.rolling(5).mean()
ma20 = close_series.rolling(20).mean()

# 마지막 값 가져오기
current_price = close_series.iloc[-1]
current_ma5 = ma5.iloc[-1]
current_ma20 = ma20.iloc[-1]

print("현재가:", current_price)
print("5이평:", round(current_ma5, 2))
print("20이평:", round(current_ma20, 2))

# 간단한 판단
if current_ma5 > current_ma20:
    print("판단: 단기 상승 흐름")
else:
    print("판단: 아직 강한 상승 흐름 아님")

    ticker = "005930.KS"
data = yf.download(ticker, period="5d", interval="1m")

# 종가만 사용
close_series = data["Close"].squeeze()

# 이동평균선 계산
ma5 = close_series.rolling(5).mean()
ma20 = close_series.rolling(20).mean()

# RSI 계산
delta = close_series.diff()
gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)

avg_gain = gain.rolling(14).mean()
avg_loss = loss.rolling(14).mean()

rs = avg_gain / avg_loss
rsi = 100 - (100 / (1 + rs))

# 마지막 값 가져오기
current_price = close_series.iloc[-1]
current_ma5 = ma5.iloc[-1]
current_ma20 = ma20.iloc[-1]
current_rsi = rsi.iloc[-1]

print("현재가:", current_price)
print("5이평:", round(current_ma5, 2))
print("20이평:", round(current_ma20, 2))
print("RSI:", round(current_rsi, 2))

# 간단한 판단
if current_ma5 > current_ma20 and current_rsi < 70:
    print("판단: 매수 후보")
elif current_rsi >= 70:
    print("판단: 과열 가능성 있음")
else:
    print("판단: 관망")