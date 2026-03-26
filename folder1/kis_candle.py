import time
import requests
import pandas as pd

from config import APP_KEY, APP_SECRET
from folder1.kis_auth import get_access_token, get_base_url


def get_minute_candle(stock_code, retry=1):
    token = get_access_token()

    url = f"{get_base_url()}/uapi/domestic-stock/v1/quotations/inquire-time-itemchartprice"

    headers = {
        "content-type": "application/json; charset=utf-8",
        "authorization": f"Bearer {token}",
        "appkey": APP_KEY,
        "appsecret": APP_SECRET,
        "tr_id": "FHKST03010200"
    }

    params = {
        "fid_etc_cls_code": "",
        "fid_cond_mrkt_div_code": "J",
        "fid_input_iscd": stock_code,
        "fid_input_hour_1": "",
        "fid_pw_data_incu_yn": "Y"
    }

    for attempt in range(retry + 1):
        try:
            res = requests.get(url, headers=headers, params=params, timeout=10)
            res.raise_for_status()

            data = res.json()
            output = data.get("output2", [])

            if not output:
                return None

            df = pd.DataFrame(output)

            df["stck_prpr"] = pd.to_numeric(df["stck_prpr"], errors="coerce")
            df["cntg_vol"] = pd.to_numeric(df["cntg_vol"], errors="coerce")

            df = df.rename(columns={
                "stck_prpr": "Close",
                "cntg_vol": "Volume",
                "stck_cntg_hour": "Time"
            })

            df = df[::-1].reset_index(drop=True)

            return df[["Close", "Volume", "Time"]]

        except requests.HTTPError as e:
            if attempt < retry:
                time.sleep(0.5)
                continue
            print(f"분봉 조회 실패: {stock_code} / {e}")
            return None

        except Exception as e:
            print(f"분봉 조회 예외: {stock_code} / {e}")
            return None