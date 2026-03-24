import pandas as pd


def save_paper_trade(trade_data, filename="paper_trades.csv"):
    df = pd.DataFrame([trade_data])

    try:
        old_df = pd.read_csv(filename, encoding="utf-8-sig")
        df = pd.concat([old_df, df], ignore_index=True)
    except FileNotFoundError:
        pass

    df.to_csv(filename, index=False, encoding="utf-8-sig")