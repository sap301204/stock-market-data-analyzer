import yfinance as yf
import pandas as pd
from src.db_utils import get_conn
from typing import Optional
import datetime as dt

def fetch_daily(ticker: str, start: str = "2015-01-01", end: Optional[str] = None) -> pd.DataFrame:
    end = end or dt.date.today().isoformat()
    df = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=False)
    if df.empty:
        return pd.DataFrame()
    df = df.reset_index()
    df.columns = [c.lower().replace(" ", "_") for c in df.columns]
    if "adj_close" not in df.columns and "adj close" in df.columns:
        df["adj_close"] = df["adj close"]
    df["date"] = pd.to_datetime(df["date"]).dt.date.astype(str)
    return df[["date", "open", "high", "low", "close", "adj_close", "volume"]]

def upsert_daily(db_path: str = None, ticker: str = "AAPL", start: str = "2015-01-01", end: str | None = None):
    df = fetch_daily(ticker, start=start, end=end)
    if df.empty:
        print("No data fetched for", ticker)
        return 0
    conn = get_conn(db_path)
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO symbols(ticker) VALUES(?)", (ticker,))
    rows = [
        (ticker, r.date, float(r.open), float(r.high), float(r.low),
         float(r.close), float(r.adj_close), int(r.volume))
        for r in df.itertuples(index=False)
    ]
    cur.executemany("""INSERT OR REPLACE INTO candles_daily
      (ticker,date,open,high,low,close,adj_close,volume) VALUES (?,?,?,?,?,?,?,?)""", rows)
    conn.commit()
    conn.close()
    print(f"Upserted {len(rows)} rows for {ticker}")
    return len(rows)
