import pandas as pd
import numpy as np
import json
import uuid
import datetime as dt
from src.db_utils import get_conn

def run_sma_backtest(ticker: str, fee_bps: float = 5.0, start: str | None = None, end: str | None = None, db_path: str = None):
    conn = get_conn(db_path)
    df = pd.read_sql_query("""
      SELECT c.date, c.close, i.sma20, i.sma50
      FROM candles_daily c JOIN indicators_daily i ON c.ticker=i.ticker AND c.date=i.date
      WHERE c.ticker=? ORDER BY c.date
    """, conn, params=(ticker,))
    conn.close()
    if start:
        df = df[df["date"] >= start]
    if end:
        df = df[df["date"] <= end]
    df = df.dropna().reset_index(drop=True)
    if df.empty:
        return {}
    signal = (df["sma20"] > df["sma50"]).astype(int)
    pos = signal.shift(1).fillna(0)
    ret = df["close"].pct_change().fillna(0.0)
    gross = pos * ret
    turns = (pos.diff().abs().fillna(0) > 0).astype(int)
    cost = turns * (fee_bps / 10000.0)
    net = gross - cost
    equity = (1 + net).cumprod()
    pnl = float(equity.iloc[-1] - 1)
    roll = equity.pct_change().fillna(0.0)
    sharpe = float(np.sqrt(252) * (roll.mean() / (roll.std() + 1e-9)))
    peak = equity.cummax()
    dd = (equity / peak - 1).min()
    trades = int(turns.sum())
    win_rate = float((net[turns == 1] > 0).mean()) if trades else 0.0
    return {
        "pnl": pnl,
        "max_dd": float(dd),
        "sharpe": sharpe,
        "trades": trades,
        "win_rate": win_rate,
        "curve": equity.tolist(),
        "dates": df["date"].tolist()
    }

def save_backtest_to_db(stats: dict, name: str, params: dict, ticker: str, db_path: str = None):
    conn = get_conn(db_path)
    cur = conn.cursor()
    bid = str(uuid.uuid4())
    start = stats["dates"][0] if stats.get("dates") else None
    end = stats["dates"][-1] if stats.get("dates") else None
    cur.execute("""INSERT INTO backtests(id,name,params_json,start,end,ticker,pnl,max_dd,sharpe,trades,win_rate,created_at)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
                (bid, name, json.dumps(params), start, end, ticker,
                 stats.get("pnl"), stats.get("max_dd"), stats.get("sharpe"),
                 stats.get("trades"), stats.get("win_rate"), dt.datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()
    return bid
