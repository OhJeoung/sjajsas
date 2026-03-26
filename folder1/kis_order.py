import requests

from folder1.kis_auth import get_access_token
from config import (
    APP_KEY,
    APP_SECRET,
    ACCOUNT_NO,
    PRODUCT_CODE,
    BASE_URL
)


def buy_market(stock_code, qty=1):
    """
    시장가 매수
    """

    url = f"{BASE_URL}/uapi/domestic-stock/v1/trading/order-cash"

    token = get_access_token()

    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {token}",
        "appKey": APP_KEY,
        "appSecret": APP_SECRET,
        "tr_id": "VTTC0802U"
    }

    body = {
        "CANO": ACCOUNT_NO,
        "ACNT_PRDT_CD": PRODUCT_CODE,
        "PDNO": stock_code,
        "ORD_DVSN": "01",   # 시장가
        "ORD_QTY": str(qty),
        "ORD_UNPR": "0"
    }

    res = requests.post(url, headers=headers, json=body)

    return res.json()

def sell_market(stock_code, qty=1):
    """
    시장가 매도
    """

    url = f"{BASE_URL}/uapi/domestic-stock/v1/trading/order-cash"

    token = get_access_token()

    headers = {
        "Content-Type": "application/json",
        "authorization": f"Bearer {token}",
        "appKey": APP_KEY,
        "appSecret": APP_SECRET,
        "tr_id": "VTTC0801U"
    }

    body = {
        "CANO": ACCOUNT_NO,
        "ACNT_PRDT_CD": PRODUCT_CODE,
        "PDNO": stock_code,
        "ORD_DVSN": "01",
        "ORD_QTY": str(qty),
        "ORD_UNPR": "0"
    }

    res = requests.post(url, headers=headers, json=body)

    return res.json()