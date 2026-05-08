import streamlit as st
import yfinance as yf
import ta
import pandas as pd
from openai import OpenAI
import streamlit.components.v1 as components

# הגדרות עמוד
st.set_page_config(page_title="סורק מניות AI מתקדם", layout="wide")

# עיצוב RTL לעברית
st.markdown("""
    <style>
    .main { direction: rtl; text-align: right; }
    div[data-testid="stSidebar"] { direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

def get_ai_analysis(api_key, symbol, price, rsi, action):
    if not api_key: return "הכנס מפתח API בתפריט הצד."
    try:
        client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
        response = client.chat.completions.create(
            model="grok-beta",
            messages=[{"role": "user", "content": f"נתח את מניית {symbol}. מחיר: {price}, RSI: {rsi}. המלצה: {action}. כתוב בעברית סיכום קצר."}]
        )
        return response.choices[0].message.content
    except: return "שגיאה בחיבור ל-AI."

def analyze_stock(symbol):
    try:
        data = yf.Ticker(symbol).history(period="1mo")
        if data.empty: return None
        price = data['Close'].iloc[-1]
        rsi = ta.momentum.RSIIndicator(data["Close"]).rsi().iloc[-1]
        action = "קנייה" if rsi < 35 else "מכירה" if rsi > 65 else "המתנה"
        return {"מניה": symbol, "מחיר": round(price, 2), "RSI": round(rsi, 2), "פעולה": action}
    except: return None

st.title("🔥 סורק מניות GOD MODE - AI")

with st.sidebar:
    api_key = st.text_input("מפתח Grok API:", type="password")
    watchlist = st.text_area("מניות (מופרדות בפסיק):", "NVDA, TSLA, AAPL")
    run_btn = st.button("🚀 הרץ סריקה")

if run_btn:
    results = []
    for sym in [s.strip() for s in watchlist.split(",")]:
        res = analyze_stock(sym)
        if res: results.append(res)
    
    if results:
        st.table(pd.DataFrame(results))
        for s in results:
            with st.expander(f"ניתוח {s['מניה']}"):
                st.write(get_ai_analysis(api_key, s['מניה'], s['מחיר'], s['RSI'], s['פעולה']))
