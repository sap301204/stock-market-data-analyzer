'use client'
import { useEffect, useState } from 'react'

export default function Home(){
  const [ticker,setTicker]=useState('AAPL')
  const [rows,setRows]=useState<any[]>([])
  const [bt,setBt]=useState<any|null>(null)

  async function load(){ const r = await fetch(`/api/chart/${ticker}`); setRows(await r.json()) }
  async function runBt(){ const r = await fetch(`/api/backtest/sma`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({ticker})}); setBt((await r.json()).stats) }

  useEffect(()=>{ load() },[ticker])

  return (
    <div style={{maxWidth: '900px', margin: '2rem auto', padding: '1rem'}}>
      <h1 style={{fontSize: '1.5rem'}}>Stock Market Data Analyzer</h1>
      <div style={{display:'flex', gap:8, alignItems:'center'}}>
        <input value={ticker} onChange={e=>setTicker(e.target.value.toUpperCase())}/>
        <button onClick={load}>Refresh</button>
        <button onClick={runBt}>Backtest SMA</button>
      </div>
      <div style={{marginTop:16, padding:12, border:'1px solid #ddd', borderRadius:8}}>
        <div style={{fontWeight:600}}>{ticker} — Close, SMA20, SMA50</div>
        <pre style={{height:240, overflow:'auto'}}>{JSON.stringify(rows.slice(-60),null,2)}</pre>
      </div>
      {bt && <div style={{marginTop:12, padding:12, border:'1px solid #eee', borderRadius:8}}>
        <div style={{fontWeight:600}}>Backtest (SMA20>50)</div>
        <div>PnL: {(bt.pnl*100).toFixed(1)}% • MaxDD: {(bt.max_dd*100).toFixed(1)}% • Sharpe: {bt.sharpe.toFixed(2)} • Trades: {bt.trades} • Win%: {(bt.win_rate*100).toFixed(1)}%</div>
      </div>}
    </div>
  )
}
