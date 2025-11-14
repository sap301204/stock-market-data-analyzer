import dash
from dash import html, dcc, Input, Output, State
import plotly.graph_objs as go
import requests
import pandas as pd

API_BASE = "http://127.0.0.1:8000"

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H2("Stock Market Data Analyzer — Dashboard"),
    html.Div([
        dcc.Input(id="ticker-input", value="AAPL", type="text"),
        html.Button("Refresh", id="refresh-btn"),
        html.Button("Backtest SMA", id="bt-btn"),
        html.Div(id="bt-output")
    ], style={"display":"flex","gap":"8px","alignItems":"center"}),
    dcc.Graph(id="price-chart"),
    dcc.Store(id="rows-store")
])

@app.callback(Output("rows-store","data"),
              Input("refresh-btn","n_clicks"),
              State("ticker-input","value"))
def refresh(n, ticker):
    if not ticker:
        return []
    resp = requests.get(f"{API_BASE}/chart/{ticker}")
    if resp.status_code != 200:
        return []
    return resp.json()

@app.callback(Output("price-chart","figure"),
              Input("rows-store","data"))
def update_chart(rows):
    if not rows:
        return go.Figure()
    df = pd.DataFrame(rows)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.date, y=df.close, name="Close"))
    if "sma20" in df.columns:
        fig.add_trace(go.Scatter(x=df.date, y=df.sma20, name="SMA20"))
    if "sma50" in df.columns:
        fig.add_trace(go.Scatter(x=df.date, y=df.sma50, name="SMA50"))
    fig.update_layout(height=480, xaxis_title="Date", yaxis_title="Price")
    return fig

@app.callback(Output("bt-output","children"),
              Input("bt-btn","n_clicks"),
              State("ticker-input","value"))
def run_bt(n, ticker):
    if not n:
        return ""
    r = requests.post(f"{API_BASE}/backtest/sma", json={"ticker": ticker})
    if r.status_code != 200:
        return html.Div("Backtest failed")
    stats = r.json()["stats"]
    return html.Div([
        html.Div(f"PnL: {(stats['pnl']*100):.2f}%"),
        html.Div(f"MaxDD: {(stats['max_dd']*100):.2f}%"),
        html.Div(f"Sharpe: {stats['sharpe']:.2f}"),
        html.Div(f"Trades: {stats['trades']}, Win%: {(stats['win_rate']*100):.1f}%")
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
