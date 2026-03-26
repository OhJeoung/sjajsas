from config import STOCK_SOURCE_MODE, MANUAL_STOCKS
from folder1.kis_rank import get_top_volume_stocks


def get_candidate_stocks():
    if STOCK_SOURCE_MODE == "manual":
        return MANUAL_STOCKS

    if STOCK_SOURCE_MODE == "top_volume":
        return get_top_volume_stocks()

    return MANUAL_STOCKS