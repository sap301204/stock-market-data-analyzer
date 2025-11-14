import datetime as dt
from src.db_utils import get_conn

def fire_alert(text: str):
    # Replace this with SMTP / Telegram / Slack integration
    print("ALERT:", text)

def evaluate_alerts(db_path: str = None):
    conn = get_conn(db_path)
    cur = conn.cursor()
    alerts = cur.execute("SELECT id,ticker,rule,threshold,last_fired FROM alerts WHERE active=1").fetchall()
    for aid, ticker, rule, thresh, last_fired in alerts:
        row = cur.execute("""SELECT i.rsi14, i.bb_lower, c.close, c.date
                             FROM indicators_daily i JOIN candles_daily c
                             ON c.ticker=i.ticker AND c.date=i.date
                             WHERE i.ticker=? ORDER BY c.date DESC LIMIT 1""", (ticker,)).fetchone()
        if not row:
            continue
        rsi, bb_lower, close, date = row
        ok = False
        if rule == "RSI_LT" and rsi is not None and rsi < thresh:
            ok = True
        if rule == "CLOSE_LT_BBLOWER" and bb_lower is not None and close < bb_lower:
            ok = True
        if ok:
            fire_alert(f"{ticker} {rule} triggered at {date}: close={close:.2f}, rsi={rsi:.1f}")
            cur.execute("UPDATE alerts SET last_fired=? WHERE id=?", (dt.datetime.utcnow().isoformat(), aid))
    conn.commit()
    conn.close()
