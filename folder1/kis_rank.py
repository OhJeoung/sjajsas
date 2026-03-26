import requests

from config import APP_KEY, APP_SECRET, TOP_N, MIN_PRICE, MAX_PRICE, EXCLUDE_KEYWORDS
from folder1.kis_auth import get_access_token, get_base_url


def is_excluded_stock(name):
    for keyword in EXCLUDE_KEYWORDS:
        if keyword in name:
            return True
    return False


def get_top_volume_stocks():
    token = get_access_token()

    url = f"{get_base_url()}/uapi/domestic-stock/v1/quotations/volume-rank"

    headers = {
        "content-type": "application/json; charset=utf-8",
        "authorization": f"Bearer {token}",
        "appkey": APP_KEY,
        "appsecret": APP_SECRET,
        "tr_id": "FHPST01710000"
    }

    params = {
        "FID_COND_MRKT_DIV_CODE": "J",
        "FID_COND_SCR_DIV_CODE": "20171",
        "FID_INPUT_ISCD": "0000",
        "FID_DIV_CLS_CODE": "0",
        "FID_BLNG_CLS_CODE": "0",
        "FID_TRGT_CLS_CODE": "111111111",
        "FID_TRGT_EXLS_CLS_CODE": "000000",
        "FID_INPUT_PRICE_1": "",
        "FID_INPUT_PRICE_2": "",
        "FID_VOL_CNT": "",
        "FID_INPUT_DATE_1": ""
    }

    res = requests.get(url, headers=headers, params=params, timeout=10)
    res.raise_for_status()

    data = res.json()
    output = data.get("output", [])

    result = {}

    for item in output:
        code = item.get("mksc_shrn_iscd")
        name = item.get("hts_kor_isnm")
        price = item.get("stck_prpr")

        if not code or not name or not price:
            continue

        try:
            price = int(price)
        except ValueError:
            continue

        # 이름 기반 제외
        if is_excluded_stock(name):
            continue

        # 가격 필터
        if price < MIN_PRICE:
            continue

        if price > MAX_PRICE:
            continue

        result[f"{code}.KS"] = name

        if len(result) >= TOP_N:
            break

    return result