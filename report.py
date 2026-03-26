import pandas as pd

FILE_NAME = "paper_trades.csv"

try:
    df = pd.read_csv(FILE_NAME, encoding="utf-8-sig")
except FileNotFoundError:
    print("paper_trades.csv 파일이 없습니다.")
    exit()

if df.empty:
    print("기록이 없습니다.")
    exit()

print("\n==============================")
print("전체 모의트레이딩 요약")
print("==============================")

print("총 진입 횟수:", len(df))

if "시뮬결과" in df.columns:
    tp_count = (df["시뮬결과"] == "익절").sum()
    sl_count = (df["시뮬결과"] == "손절").sum()
    none_count = df["시뮬결과"].isna().sum()

    print("익절 횟수:", tp_count)
    print("손절 횟수:", sl_count)
    print("미결정 횟수:", none_count)

if "시뮬수익률(%)" in df.columns:
    sim_returns = pd.to_numeric(df["시뮬수익률(%)"], errors="coerce")
    print("평균 시뮬 수익률:", round(sim_returns.mean(), 2), "%")

if "5분수익률(%)" in df.columns:
    r5 = pd.to_numeric(df["5분수익률(%)"], errors="coerce")
    print("평균 5분 수익률:", round(r5.mean(), 2), "%")

if "10분수익률(%)" in df.columns:
    r10 = pd.to_numeric(df["10분수익률(%)"], errors="coerce")
    print("평균 10분 수익률:", round(r10.mean(), 2), "%")

print("\n==============================")
print("종목별 성과 요약")
print("==============================")

group = df.groupby("종목명").agg({
    "종목코드": "count",
    "시뮬수익률(%)": "mean",
    "5분수익률(%)": "mean",
    "10분수익률(%)": "mean"
}).rename(columns={
    "종목코드": "진입횟수",
    "시뮬수익률(%)": "평균시뮬수익률",
    "5분수익률(%)": "평균5분수익률",
    "10분수익률(%)": "평균10분수익률"
})

group = group.sort_values(by="평균시뮬수익률", ascending=False)

print(group.round(2))