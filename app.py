import streamlit as st
import yfinance as yf
import ta
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(page_title="GOD MODE AI", layout="wide")

def render_tradingview(symbol):
    tv_html = f"""
    <div id="tradingview_chart" style="height: 400px;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({{
      "autosize": true, "symbol": "{symbol}", "interval": "5",
      "timezone": "Etc/UTC", "theme": "dark", "style": "1",
      "locale": "en", "container_id": "tradingview_chart"
    }});
    </script>
    """
    components.html(tv_html, height=410)

def analyze_stock(symbol):
    try:
        data = yf.Ticker(symbol).history(period="2d", interval="5m")
        if data.empty: return None
        price = data['Close'].iloc[-1]
        rsi = ta.momentum.RSIIndicator(data["Close"]).rsi().iloc[-1]
        score = 50
        if rsi < 30: score += 20
        elif rsi > 70: score -= 20
        action = "BUY 📈" if score > 65 else "SHORT 📉" if score < 35 else "WAIT"
        return {"Symbol": symbol, "Price": round(price, 2), "Score": score, "Action": action}
    except: return None

st.title("🔥 GOD MODE AI TERMINAL")
watchlist = st.multiselect("Watchlist", ["AAPL", "TSLA", "NVDA", "PLTR"], default=["AAPL", "NVDA"])

if st.button("🚀 SCAN"):
    results = [analyze_stock(s) for s in watchlist if analyze_stock(s)]
    if results:
        st.dataframe(pd.DataFrame(results).sort_values(by="Score", ascending=False), use_container_width=True)
        for stock in results:
            with st.expander(f"Chart: {stock['Symbol']}"):
                render_tradingview(stock['Symbol'])
