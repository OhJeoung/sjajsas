import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STATUS_FILE = BASE_DIR / "status.json"


def update_status(
    engine_status=None,
    market_status=None,
    last_scan_time=None,
    last_signal=None,
    last_error=None,
    open_positions=None,
):
    try:
        try:
            with open(STATUS_FILE, "r", encoding="utf-8") as f:
                status = json.load(f)
        except Exception:
            status = {}

        if engine_status is not None:
            status["engine_status"] = engine_status

        if market_status is not None:
            status["market_status"] = market_status

        if last_scan_time is not None:
            status["last_scan_time"] = last_scan_time

        if last_signal is not None:
            status["last_signal"] = last_signal

        if last_error is not None:
            status["last_error"] = last_error

        if open_positions is not None:
            status["open_positions"] = open_positions

        status["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(STATUS_FILE, "w", encoding="utf-8") as f:
            json.dump(status, f, ensure_ascii=False, indent=2)

    except Exception as e:
        print("status 업데이트 실패:", e)