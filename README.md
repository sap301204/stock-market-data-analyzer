📈 Stock Market Data Analyzer — End-to-End FinTech Project (Python)

A production-style, industry-ready Stock Market Data Analyzer built with Python.
This project simulates how a real FinTech/Quant team builds:

⚙ Data pipelines (ingestion → indicators → signals)

📊 Vectorized backtesting engine
💼 Portfolio accounting
🚀 FastAPI service for live data
🔔 Alert engine with scheduler
🖥 Next.js dashboard
This is built for resume-ready, portfolio-ready, interview-ready presentation.

🚀 Features

Fetches OHLCV data (Yahoo Finance)
Computes SMA, RSI, MACD, Bollinger Bands
Generates buy/sell signals
Runs a vectorized SMA crossover backtest
Tracks trades, PnL, drawdown, Sharpe ratio
FastAPI backend for:
Prices
Indicators
Alerts
Backtest results
Alerts via rule engine (SMA cross, RSI oversold, price breakouts)
Next.js dashboard for charts + watchlist
CI workflow + Docker-ready

📦 Project Structure

project/
│── api/
│   └── app.py
│── src/
│   ├── ingest.py
│   ├── indicators.py
│   ├── signals.py
│   ├── backtest.py
│   ├── portfolio.py
│   ├── db_utils.py
│   └── jobs/
│       └── alerts.py
│── dashboard/ (Next.js)
│── sql/
│   └── schema.sql
│── scripts/
│   └── init_db.py
│── .github/workflows/ci.yml
│── requirements.txt
│── LICENSE
│── README.md

🛠 Installation & Setup
git clone https://github.com/your-username/stock-market-data-analyzer
cd stock-market-data-analyzer

pip install -r requirements.txt
python scripts/init_db.py

▶ Running Components
Start FastAPI
uvicorn api.app:app --reload

Run Ingestion
python src/ingest.py --ticker AAPL

Run Indicators
python src/indicators.py --ticker AAPL

Run Backtest
python src/backtest.py --ticker AAPL

Run Alerts Scheduler
python src/jobs/alerts.py

📊 Dashboard

Dashboard lives in /dashboard — start it using:

npm install
npm run dev

📚 License

MIT License — free to use and modify.

💼 Resume Points (Copy-Paste)

Built a complete Python-based Stock Market Data Analyzer replicating real-world FinTech workflows.
Developed data ingestion, transformation, signal generation, and vectorized backtesting pipelines.
Designed and deployed a FastAPI microservice exposing analytical endpoints.
Implemented a scheduler-driven alert system with rule-based triggers.
Created a Next.js analytics dashboard for visualizing price, indicators, and backtest results.
