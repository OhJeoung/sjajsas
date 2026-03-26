import requests
from datetime import datetime, timedelta

from config import APP_KEY, APP_SECRET, KIS_ENV

ACCESS_TOKEN = None
TOKEN_EXPIRED_AT = None


def get_base_url():
    if KIS_ENV == "prod":
        return "https://openapi.koreainvestment.com:9443"
    return "https://openapivts.koreainvestment.com:29443"


def request_new_token():
    url = f"{get_base_url()}/oauth2/tokenP"

    headers = {
        "content-type": "application/json"
    }

    body = {
        "grant_type": "client_credentials",
        "appkey": APP_KEY,
        "appsecret": APP_SECRET
    }

    res = requests.post(url, headers=headers, json=body, timeout=10)
    res.raise_for_status()

    data = res.json()

    if "access_token" not in data:
        raise ValueError(f"토큰 발급 실패: {data}")

    access_token = data["access_token"]

    # KIS 토큰은 보통 24시간 유효라 여유 두고 23시간 후 만료로 처리
    expired_at = datetime.now() + timedelta(hours=23)

    return access_token, expired_at


def get_access_token():
    global ACCESS_TOKEN, TOKEN_EXPIRED_AT

    if ACCESS_TOKEN and TOKEN_EXPIRED_AT:
        if datetime.now() < TOKEN_EXPIRED_AT:
            return ACCESS_TOKEN

    ACCESS_TOKEN, TOKEN_EXPIRED_AT = request_new_token()
    return ACCESS_TOKEN