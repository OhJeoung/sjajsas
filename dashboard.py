import json
from pathlib import Path

import pandas as pd
import streamlit as st

# =========================
# 경로 고정
# =========================
BASE_DIR = Path(__file__).resolve().parent
STATUS_FILE = BASE_DIR / "status.json"
TRADE_FILE = BASE_DIR / "paper_trades.csv"

st.set_page_config(
    page_title="자동매매 대시보드",
    layout="wide"
)

st.title("📈 자동매매 모니터링 대시보드")

# =========================
# 상태 정보
# =========================
st.subheader("엔진 상태")

try:
    with open(STATUS_FILE, "r", encoding="utf-8") as f:
        status = json.load(f)
except Exception:
    status = {}

col1, col2, col3, col4 = st.columns(4)

col1.metric("엔진 상태", status.get("engine_status", "unknown"))
col2.metric("장 상태", status.get("market_status", "unknown"))
col3.metric("마지막 스캔", status.get("last_scan_time", "-"))
col4.metric("열린 포지션", status.get("open_positions", "-"))

st.write("마지막 신호:", status.get("last_signal", "-"))
st.write("마지막 에러:", status.get("last_error", "-"))

st.divider()

# =========================
# 거래 데이터 로드
# =========================
try:
    df = pd.read_csv(TRADE_FILE, encoding="utf-8-sig")
except Exception:
    st.warning("paper_trades.csv 없음")
    st.stop()

if df.empty:
    st.warning("거래 기록 없음")
    st.stop()

# 숫자 변환
for col in [
    "실현수익률(%)",
    "5분수익률(%)",
    "10분수익률(%)",
    "시뮬수익률(%)"
]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# =========================
# 기본 통계
# =========================
closed_df = df[df["상태"] == "청산"] if "상태" in df.columns else pd.DataFrame()
open_df = df[df["상태"] == "보유"] if "상태" in df.columns else pd.DataFrame()

total_trades = len(df)
closed_count = len(closed_df)
open_count = len(open_df)

if closed_count > 0 and "실현수익률(%)" in closed_df.columns:
    avg_return = closed_df["실현수익률(%)"].mean()
    total_return = closed_df["실현수익률(%)"].sum()
    win_rate = (closed_df["실현수익률(%)"] > 0).mean() * 100
else:
    avg_return = 0
    total_return = 0
    win_rate = 0

# =========================
# KPI
# =========================
st.subheader("성과 요약")

c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric("총 거래", total_trades)
c2.metric("청산 거래", closed_count)
c3.metric("보유 중", open_count)
c4.metric("총 수익률", f"{total_return:.2f}%")
c5.metric("평균 수익률", f"{avg_return:.2f}%")
c6.metric("승률", f"{win_rate:.2f}%")

st.divider()

# =========================
# 종목별 성과
# =========================
st.subheader("종목별 성과")

if closed_count > 0:
    group = (
        closed_df.groupby("종목명")
        .agg(
            거래횟수=("종목코드", "count"),
            평균수익률=("실현수익률(%)", "mean"),
            총수익률=("실현수익률(%)", "sum"),
            승률=("실현수익률(%)", lambda x: (x > 0).mean() * 100)
        )
        .sort_values("총수익률", ascending=False)
        .round(2)
    )

    st.dataframe(group, width="stretch")
else:
    st.info("청산 거래 없음")

st.divider()

# =========================
# 최근 거래
# =========================
st.subheader("최근 거래")

show_cols = [
    "시간",
    "종목명",
    "종목코드",
    "진입가",
    "청산가",
    "청산사유",
    "실현수익률(%)",
    "상태",
]

show_cols = [c for c in show_cols if c in df.columns]

st.dataframe(
    df[show_cols].tail(30),
    width="stretch"
)

st.divider()

# =========================
# 전체 데이터
# =========================
with st.expander("전체 데이터 보기"):
    st.dataframe(df, width="stretch")