import pandas as pd
from src.db_utils import get_conn

def compute_sma_cross_signals(ticker: str, db_path: str = None):
    conn = get_conn(db_path)
    df = pd.read_sql_query("""
      SELECT c.date, c.close, i.sma20, i.sma50
      FROM candles_daily c JOIN indicators_daily i ON c.ticker = i.ticker AND c.date = i.date
      WHERE c.ticker = ? ORDER BY c.date
    """, conn, params=(ticker,))
    conn.close()
    if df.empty:
        return []
    df = df.dropna().reset_index(drop=True)
    signals = []
    for i in range(1, len(df)):
        prev = df.iloc[i-1]
        now = df.iloc[i]
        buy = (prev["sma20"] < prev["sma50"]) and (now["sma20"] >= now["sma50"])
        sell = (prev["sma20"] > prev["sma50"]) and (now["sma20"] <= now["sma50"])
        sig = {"date": now["date"], "ticker": ticker, "signal": "BUY" if buy else "SELL" if sell else "HOLD"}
        signals.append(sig)
    return signals
