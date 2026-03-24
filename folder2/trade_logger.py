import pandas as pd


def save_paper_trade(trade_data, filename="paper_trades.csv"):
    df = pd.DataFrame([trade_data])

    try:
        old_df = pd.read_csv(filename, encoding="utf-8-sig")
        df = pd.concat([old_df, df], ignore_index=True)
    except FileNotFoundError:
        pass

    df.to_csv(filename, index=False, encoding="utf-8-sig")


def load_paper_trades(filename="paper_trades.csv"):
    try:
        return pd.read_csv(filename, encoding="utf-8-sig")
    except FileNotFoundError:
        return pd.DataFrame()


def update_paper_trades(df, filename="paper_trades.csv"):
    df.to_csv(filename, index=False, encoding="utf-8-sig")