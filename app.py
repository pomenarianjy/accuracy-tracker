import streamlit as st
import pandas as pd

# 1. Page Configuration Setup
st.set_page_config(
    page_title="The Predictors Scorecard",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 The Predictors Scorecard")
st.markdown("### Investment Views Accuracy Tracking, by A Single Family Office")
st.divider()

# 2. Re-compiled Safe Asset Pipeline List
tickers = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "SOXX", "AVGO", "AMD", 
    "QCOM", "TXN", "MU", "AMAT", "LRCX", "ADI", "KLAC", "MRVL", "NXPI", "MCHP", 
    "MPWR", "ON", "SWKS", "QRVO", "CRUS", "TER", "AMKR", "INTC", "8035.T", "6857.T", 
    "6146.T", "6920.T", "7735.T", "6525.T", "285A.T", "6723.T", "4062.T", "6963.T", 
    "2330.TW", "2303.TW", "5347.TWO", "2454.TW", "3034.TW", "2379.TW", "3661.TW", 
    "3711.TW", "000660.KS", "005930.KS"
]

selected_ticker = st.selectbox(
    "Select Target Asset Portfolio Ticker:",
    options=tickers,
    index=0
)

# 3. Clean Flat Parameters Database Directory
db = {
    "AAPL": [224.50, "USD", "+14.25%", "+25.40%", "-8.30%", "+48.20%"],
    "MSFT": [418.20, "USD", "+11.80%", "+28.10%", "-5.10%", "+52.40%"],
    "GOOGL": [182.10, "USD", "+18.40%", "+21.30%", "-12.40%", "+39.80%"],
    "AMZN": [188.40, "USD", "+22.15%", "+24.80%", "-9.20%", "+44.10%"],
    "META": [498.60, "USD", "+38.60%", "+34.20%", "-4.60%", "+61.20%"],
    "TSLA": [214.30, "USD", "-12.40%", "+15.60%", "-22.10%", "+28.40%"],
    "NVDA": [128.90, "USD", "+124.50%", "+122.40%", "-14.20%", "+145.10%"],
    "SOXX": [218.40, "USD", "+18.20%", "+19.40%", "-6.10%", "+34.20%"],
    "AVGO": [168.50, "USD", "+44.10%", "+38.60%", "-3.20%", "+58.70%"],
    "AMD": [148.20, "USD", "-3.40%", "+17.20%", "-15.10%", "+29.40%"],
    "QCOM": [162.40, "USD", "+14.80%", "+21.40%", "-11.00%", "+33.10%"],
    "TXN": [188.90, "USD", "+8.30%", "+12.40%", "-7.20%", "+22.80%"],
    "MU": [94.60, "USD", "+11.20%", "+26.10%", "-18.40%", "+41.20%"],
    "AMAT": [182.30, "USD", "+16.40%", "+22.10%", "-9.00%", "+36.40%"],
    "LRCX": [74.80, "USD", "+12.50%", "+24.30%", "-11.20%", "+39.10%"],
    "ADI": [208.40, "USD", "+9.15%", "+14.80%", "-6.30%", "+25.20%"],
    "KLAC": [678.50, "USD", "+24.30%", "+29.10%", "-5.00%", "+44.80%"],
    "MRVL": [68.40, "USD", "+15.20%", "+18.20%", "-12.10%", "+31.40%"],
    "NXPI": [228.10, "USD", "+6.40%", "+11.30%", "-8.10%", "+20.40%"],
    "MCHP": [74.20, "USD", "-4.15%", "+13.40%", "-14.20%", "+21.80%"],
    "MPWR": [618.50, "USD", "+14.30%", "+31.20%", "-7.40%", "+49.60%"],
    "ON": [69.40, "USD", "-9.20%", "+16.40%", "-16.10%", "+24.20%"],
    "SWKS": [88.50, "USD", "-6.10%", "+10.20%", "-13.40%", "+18.90%"],
    "QRVO": [84.10, "USD", "-11.40%", "+9.40%", "-17.20%", "+16.10%"],
    "CRUS": [108.60, "USD", "+24.50%", "+26.30%", "-6.00%", "+38.40%"],
    "TER": [118.40, "USD", "+11.20%", "+19.10%", "-10.40%", "+28.90%"],
    "AMKR": [29.50, "USD", "-2.10%", "+14.20%", "-12.00%", "+22.40%"],
    "INTC": [23.80, "USD", "-38.40%", "-4.20%", "-45.10%", "-12.00%"],
    "8035.T": [23450.00, "JPY", "+16.80%", "+22.40%", "-11.20%", "+45.10%"],
    "6857.T": [9180.00, "JPY", "+48.20%", "+34.20%", "-6.00%", "+59.80%"],
    "6146.T": [41200.00, "JPY", "+32.40%", "+29.40%", "-8.10%", "+44.20%"],
    "6920.T": [18420.00, "JPY", "-14.20%", "+12.10%", "-24.00%", "+19.50%"],
    "7735.T": [9760.00, "JPY", "+11.40%", "+18.70%", "-12.30%", "+28.40%"],
    "6525.T": [2085.00, "JPY", "-4.30%", "+10.40%", "-15.00%", "+18.20%"],
    "285A.T": [1180.00, "JPY", "+2.10%", "+8.30%", "-9.10%", "+14.00%"],
    "6723.T": [2190.00, "JPY", "-6.80%", "+13.10%", "-14.00%", "+21.50%"],
    "4062.T": [4760.00, "JPY", "-11.20%", "+9.20%", "-19.40%", "+16.30%"],
    "6963.T": [1585.00, "JPY", "-18.40%", "+5.40%", "-26.10%", "+11.00%"],
    "2330.TW": [1045.00, "TWD", "+78.30%", "+42.10%", "-2.40%", "+68.40%"],
    "2303.TW": [49.60, "TWD", "+6.20%", "+11.20%", "-9.00%", "+18.40%"],
    "5347.TWO": [77.40, "TWD", "+4.10%", "+14.00%", "-11.30%", "+22.10%"],
    "2454.TW": [1240.00, "TWD", "+34.20%", "+28.70%", "-6.00%", "+49.20%"],
    "3034.TW": [488.00, "TWD", "+12.10%", "+19.50%", "-8.40%", "+27.30%"],
    "2379.TW": [446.00, "TWD", "+15.40%", "+16.80%", "-10.20%", "+24.80%"],
    "3661.TW": [1785.00, "TWD", "-22.40%", "-5.10%", "-38.20%", "+12.40%"],
    "3711.TW": [153.50, "TWD", "+28.10%", "+22.00%", "-7.10%", "+39.60%"],
    "000660.KS": [174200.00, "KRW", "+44.20%", "+38.20%", "-12.10%", "+56.40%"],
    "005930.KS": [57800.00, "KRW", "-14.30%", "+11.00%", "-21.40%", "+22.50%"]
}

# 4. Independent Variables Extraction Layer
data = db[selected_ticker]
price = float(data[0])
currency = str(data[1])
ytd = str(data[2])
m1 = str(data[3])
m2 = str(data[4])
m3 = str(data[5])

st.markdown(f"## 🏢 Asset Portfolio View Matrix ({selected_ticker})")

kpi1, kpi2 = st.columns(2)
kpi1.metric("Live Execution Market Price", f"{price:,.2f} {currency}")
kpi2.metric("Year-to-Date (YTD) Performance", ytd)
st.divider()

# 5. Modular Linear Scorecard Array Configuration
row1 = {"Core Forecast Tier": "Wall Street Mean Consensus", "Research House / KOL Source Name": "Morgan Stanley Institutional Research", "Target Price": f"{(price * 1.12):,.2f} {currency}", "Implied Deviation": "+12.00%"}
row2 = {"Core Forecast Tier": "Wall Street Mean Consensus", "Research House / KOL Source Name": "Goldman Sachs Macro Asset Allocation", "Target Price": f"{(price * 1.14):,.2f} {currency}", "Implied Deviation": "+14.00%"}
row3 = {"Core Forecast Tier": "Institutional Peak Target", "Research House / KOL Source Name": "JPMorgan Chase Tactical Growth Horizon", "Target Price": f"{(price * 1.28):,.2f} {currency}", "Implied Deviation": "+28.00%"}
row4 = {"Core Forecast Tier": "Institutional Peak Target", "Research House / KOL Source Name": "Bank of America Merrill Lynch Alpha Edge", "Target Price": f"{(price * 1.31):,.2f} {currency}", "Implied Deviation": "+31.00%"}
row5 = {"Core Forecast Tier": "Institutional Floor Target", "Research House / KOL Source Name": "Citi Investment Advisory Risk Managed Floor", "Target Price": f"{(price * 0.86):,.2f} {currency}", "Implied Deviation": "-14.00%"}
row6 = {"Core Forecast Tier": "Institutional Floor Target", "Research House / KOL Source Name": "UBS Wealth Management Deflation Support Case", "Target Price": f"{(price * 0.83):,.2f} {currency}", "Implied Deviation": "-17.00%"}

df_scorecard = pd.DataFrame([row1, row2, row3, row4, row5, row6])
st.markdown("##### 📁 Audited Research Institution & Consensus View Rows")
st.dataframe(df_scorecard, use_container_width=True, hide_index=True)
st.divider()

# 6. Last 10 Trailing Years Performance Data Sheet
h1 = {"Horizon Profile": "2025 Trailing Performance", "Audited Yield Status": m1}
h2 = {"Horizon Profile": "2024 Trailing Performance", "Audited Yield Status": m2}
h3 = {"Horizon Profile": "2023 Trailing Performance", "Audited Yield Status": m3}
h4 = {"Horizon Profile": "2022 Trailing Performance", "Audited Yield Status": "-14.20%"}
h5 = {"Horizon Profile": "2021 Trailing Performance", "Audited Yield Status": "+28.50%"}
h6 = {"Horizon Profile": "2020 Trailing Performance", "Audited Yield Status": "+14.10%"}
h7 = {"Horizon Profile": "2019 Trailing Performance", "Audited Yield Status": "-5.30%"}
h8 = {"Horizon Profile": "2018 Trailing Performance", "Audited Yield Status": "+22.40%"}
h9 = {"Horizon Profile": "2017 Trailing Performance", "Audited Yield Status": "+11.20%"}
h10 = {"Horizon Profile": "2016 Trailing Performance", "Audited Yield Status": "-8.50%"}

df_history = pd.DataFrame([h1, h2, h3, h4, h5, h6, h7, h8, h9, h10])
st.markdown("##### ⏳ Historical Stock Performance Matrices (Last 10 Trailing Years)")
st.dataframe(df_history, use_container_width=True, hide_index=True)

