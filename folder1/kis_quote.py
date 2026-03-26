import requests

from config import APP_KEY, APP_SECRET
from folder1.kis_auth import get_access_token, get_base_url


def get_current_price(stock_code):
    """
    국내주식 현재가 조회
    stock_code 예: '005930'
    """
    token = get_access_token()

    url = f"{get_base_url()}/uapi/domestic-stock/v1/quotations/inquire-price"

    headers = {
        "content-type": "application/json; charset=utf-8",
        "authorization": f"Bearer {token}",
        "appkey": APP_KEY,
        "appsecret": APP_SECRET,
        "tr_id": "FHKST01010100"
    }

    params = {
        "fid_cond_mrkt_div_code": "J",
        "fid_input_iscd": stock_code
    }

    res = requests.get(url, headers=headers, params=params, timeout=10)
    res.raise_for_status()

    data = res.json()

    output = data.get("output", {})
    price = output.get("stck_prpr")

    if not price:
        raise ValueError(f"현재가 조회 실패: {data}")

    return int(price)