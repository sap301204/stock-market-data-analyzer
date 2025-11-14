import pandas as pd
from src.db_utils import get_conn
from ta.trend import SMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands

def compute_indicators_for_ticker(ticker: str, db_path: str = None):
    conn = get_conn(db_path)
    df = pd.read_sql_query("SELECT date, close FROM candles_daily WHERE ticker=? ORDER BY date",
                           conn, params=(ticker,))
    conn.close()
    if df.empty:
        return 0
    s = df["close"].astype(float)
    sma20 = SMAIndicator(s, window=20).sma_indicator()
    sma50 = SMAIndicator(s, window=50).sma_indicator()
    rsi14 = RSIIndicator(s, window=14).rsi()
    macd_obj = MACD(s)
    macd = macd_obj.macd()
    macd_signal = macd_obj.macd_signal()
    macd_hist = macd_obj.macd_diff()
    bb = BollingerBands(s, window=20, window_dev=2)
    out = pd.DataFrame({
        "date": df["date"],
        "sma20": sma20,
        "sma50": sma50,
        "rsi14": rsi14,
        "macd": macd,
        "macd_signal": macd_signal,
        "macd_hist": macd_hist,
        "bb_upper": bb.bollinger_hband(),
        "bb_mid": bb.bollinger_mavg(),
        "bb_lower": bb.bollinger_lband()
    }).dropna()
    conn = get_conn(db_path)
    cur = conn.cursor()
    rows = [(ticker, r.date, float(r.sma20), float(r.sma50), float(r.rsi14),
             float(r.macd), float(r.macd_signal), float(r.macd_hist),
             float(r.bb_upper), float(r.bb_mid), float(r.bb_lower))
            for r in out.itertuples(index=False)]
    cur.executemany("""INSERT OR REPLACE INTO indicators_daily
      (ticker,date,sma20,sma50,rsi14,macd,macd_signal,macd_hist,bb_upper,bb_mid,bb_lower)
      VALUES (?,?,?,?,?,?,?,?,?,?,?)""", rows)
    conn.commit()
    conn.close()
    print(f"Computed and stored {len(rows)} indicator rows for {ticker}")
    return len(rows)
