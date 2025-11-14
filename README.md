# Stock Market Data Analyzer

Full end-to-end project: ingest → store → indicators → signals → backtest → API → dashboard → alerts.
See `sql/schema.sql` and `scripts/init_db.py` to initialize.

Run demo:
1. python -m venv venv && source venv/bin/activate
2. pip install -r requirements.txt
3. python scripts/init_db.py
4. python -c "from src.ingest import upsert_daily; upsert_daily('AAPL','2018-01-01')"
5. python -c "from src.indicators import compute_indicators_for_ticker; compute_indicators_for_ticker('AAPL')"
6. uvicorn api.app:app --reload --port 8000
7. python -m dashboard.app
