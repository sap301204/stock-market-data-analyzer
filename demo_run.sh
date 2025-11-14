#!/bin/bash
python scripts/init_db.py
python - <<'PY'
from src.ingest import upsert_daily
from src.indicators import compute_indicators_for_ticker
upsert_daily(ticker='AAPL', start='2018-01-01')
compute_indicators_for_ticker('AAPL')
print('Demo data loaded.')
PY
echo "Start API: uvicorn api.app:app --reload --port 8000"
echo "Start Dashboard: python -m dashboard.app"
