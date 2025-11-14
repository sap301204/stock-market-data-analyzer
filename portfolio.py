import pandas as pd
from src.db_utils import get_conn

def current_positions(db_path: str = None):
    conn = get_conn(db_path)
    tx = pd.read_sql_query("SELECT * FROM portfolio_tx ORDER BY ts", conn, parse_dates=["ts"])
    conn.close()
    if tx.empty:
        return pd.DataFrame(columns=["ticker", "qty", "avg_cost"])
    tx["signed_qty"] = tx.apply(lambda r: r["qty"] if r["side"].upper() == "BUY" else -r["qty"], axis=1)
    agg = tx.groupby("ticker").agg(qty=("signed_qty", "sum"), avg_cost=("price", "mean")).reset_index()
    return agg
