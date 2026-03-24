import time
from datetime import datetime, time as dt_time

import pandas as pd
import yfinance as yf
from folder2.paper_engine import record_paper_entry

from config import (
    MARKET_START_HOUR,
    MARKET_START_MINUTE,
    MARKET_END_HOUR,
    MARKET_END_MINUTE,
    SCAN_INTERVAL_SECONDS,
    BUY_CANDIDATES_FILE,
    LOG_FILE
)
from indicator import calculate_ma, calculate_rsi
from strategy import check_signal
from stock_source import get_candidate_stocks


def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text = f"[{timestamp}] {message}"

    print(text)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")


def is_duplicate(ticker):
    try:
        df = pd.read_csv(BUY_CANDIDATES_FILE, encoding="utf-8-sig")

        if df.empty:
            return False

        recent = df.tail(20)

        if ticker in recent["종목코드"].values:
            return True

    except FileNotFoundError:
        return False
    except Exception as e:
        log(f"is_duplicate 확인 중 에러: {e}")
        return False

    return False


def is_market_open():
    now = datetime.now().time()
    market_start = dt_time(MARKET_START_HOUR, MARKET_START_MINUTE)
    market_end = dt_time(MARKET_END_HOUR, MARKET_END_MINUTE)

    return market_start <= now <= market_end


def run_scanner():
    buy_candidates = []
    candidate_stocks = get_candidate_stocks()

    print("\n" + "=" * 40)
    log("스캔 시작")

    for ticker, name in candidate_stocks.items():
        print("\n------------------------------")
        log(f"종목 검사: {name} ({ticker})")

        try:
            data = yf.download(
                ticker,
                period="5d",
                interval="1m",
                progress=False
            )

            if data.empty:
                log(f"데이터 없음: {name} ({ticker})")
                continue

            close_series = data["Close"].squeeze()
            volume_series = data["Volume"].squeeze()

            ma5 = calculate_ma(close_series, 5)
            ma20 = calculate_ma(close_series, 20)
            rsi = calculate_rsi(close_series, 14)

            current_price = close_series.iloc[-1]
            current_ma5 = ma5.iloc[-1]
            current_ma20 = ma20.iloc[-1]
            current_rsi = rsi.iloc[-1]
            current_volume = volume_series.iloc[-1]
            avg_volume_20 = volume_series.rolling(20).mean().iloc[-1]

            signal = check_signal(
                current_ma5,
                current_ma20,
                current_rsi,
                current_volume,
                avg_volume_20
            )

            print("현재가:", current_price)
            print("5이평:", round(current_ma5, 2))
            print("20이평:", round(current_ma20, 2))
            print("RSI:", round(current_rsi, 2))
            print("현재 거래량:", int(current_volume))
            print("20봉 평균 거래량:", round(avg_volume_20, 2))
            print("판단:", signal)

            if "매수 후보" in signal:
                if is_duplicate(ticker):
                    log(f"매수 후보이지만 중복으로 저장 생략: {name} ({ticker})")
                else:
                    log(f"매수 후보 발견: {name} ({ticker})")
                    buy_candidates.append({
                        "시간": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "종목명": name,
                        "종목코드": ticker,
                        "현재가": current_price,
                        "5이평": round(current_ma5, 2),
                        "20이평": round(current_ma20, 2),
                        "RSI": round(current_rsi, 2),
                        "현재거래량": int(current_volume),
                        "20봉평균거래량": round(avg_volume_20, 2),
                        "판단": signal
                    })
                    
                    record_paper_entry(ticker, name, current_price, signal)

        except Exception as e:
            log(f"종목 처리 중 에러 발생: {name} ({ticker}) / {e}")

    print("\n" + "=" * 40)
    log("스캔 종료 - 매수 후보 정리")

    if len(buy_candidates) == 0:
        print("이번 스캔에서 새로 저장된 매수 후보 종목: 없음")
        log("이번 스캔에서 새로 저장된 매수 후보 없음")
    else:
        print("이번 스캔에서 새로 저장된 매수 후보 종목")
        for item in buy_candidates:
            print("-", item["종목명"], f"({item['종목코드']})")

        df = pd.DataFrame(buy_candidates)

        try:
            old_df = pd.read_csv(BUY_CANDIDATES_FILE, encoding="utf-8-sig")
            df = pd.concat([old_df, df], ignore_index=True)
        except FileNotFoundError:
            pass
        except Exception as e:
            log(f"기존 CSV 읽기 중 에러: {e}")

        try:
            df.to_csv(BUY_CANDIDATES_FILE, index=False, encoding="utf-8-sig")
            log(f"{BUY_CANDIDATES_FILE} 파일에 누적 저장 완료")
        except PermissionError:
            log(f"{BUY_CANDIDATES_FILE} 저장 실패 - 파일이 열려 있는지 확인하세요")
        except Exception as e:
            log(f"CSV 저장 중 에러 발생: {e}")


while True:
    try:
        if is_market_open():
            log("장 시간 확인됨 - 스캔 실행")
            run_scanner()
            log(f"다음 스캔까지 {SCAN_INTERVAL_SECONDS}초 대기")
        else:
            log(f"장 시간이 아님 - {SCAN_INTERVAL_SECONDS}초 후 다시 확인")

        time.sleep(SCAN_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        log("사용자가 프로그램을 종료했습니다.")
        break

    except Exception as e:
        log(f"치명적 에러 발생: {e}")
        log("프로그램을 10초 후 재시도합니다.")
        time.sleep(10)