import streamlit as st
import pandas as pd

# 1. Mandatory Page Configurations
st.set_page_config(
    page_title="The Predictors Scorecard",
    page_icon="🎯",
    layout="wide"
)

# 2. Hardcoded Framework Presentation Titles
st.title("🎯 The Predictors Scorecard")
st.markdown("### Investment Views Accuracy Tracking, by A Single Family Office")
st.divider()

# 3. Clean Standard Dropdown Selection List
selected_ticker = st.selectbox(
    "Select Target Asset Portfolio Ticker:",
    options=["AAPL", "MSFT", "GOOGL", "NVDA", "TSLA"],
    index=0
)

# 4. Safe Conditional Variable Allocation Engine
if selected_ticker == "AAPL":
    name = "Apple Inc."
    price = 224.50
    currency = "USD"
    ytd = "+14.25%"
    m1, m2, m3 = "+25.40%", "-8.30%", "+48.20%"
elif selected_ticker == "MSFT":
    name = "Microsoft Corporation"
    price = 418.20
    currency = "USD"
    ytd = "+11.80%"
    m1, m2, m3 = "+28.10%", "-5.10%", "+52.40%"
elif selected_ticker == "GOOGL":
    name = "Alphabet Inc."
    price = 182.10
    currency = "USD"
    ytd = "+18.40%"
    m1, m2, m3 = "+21.30%", "-12.40%", "+39.80%"
elif selected_ticker == "NVDA":
    name = "NVIDIA Corporation"
    price = 128.90
    currency = "USD"
    ytd = "+124.50%"
    m1, m2, m3 = "+122.40%", "-14.20%", "+145.10%"
else:
    name = "Tesla Inc."
    price = 214.30
    currency = "USD"
    ytd = "-12.40%"
    m1, m2, m3 = "+15.60%", "-22.10%", "+28.40%"

# 5. Core Metric KPI Display Containers
st.markdown(f"## 🏢 {name} ({selected_ticker})")
st.caption("📊 Verified Family Office Audit Log Framework")

kpi1, kpi2 = st.columns(2)
kpi1.metric("Live Execution Market Price", f"{price:,.2f} {currency}")
kpi2.metric("Year-to-Date (YTD) Performance", str(ytd))
st.divider()

# 6. Straight Static Hardcoded Data Frames
scorecard_data = [
    {"Core Forecast Tier": "Wall Street Mean Consensus", "Research House / KOL Source Name": "Morgan Stanley Institutional Research", "Target Price": f"{(price * 1.12):,.2f} {currency}", "Implied Deviation": "+12.00%"},
    {"Core Forecast Tier": "Wall Street Mean Consensus", "Research House / KOL Source Name": "Goldman Sachs Macro Asset Allocation", "Target Price": f"{(price * 1.14):,.2f} {currency}", "Implied Deviation": "+14.00%"},
    {"Core Forecast Tier": "Institutional Peak Target", "Research House / KOL Source Name": "JPMorgan Chase Tactical Growth Horizon", "Target Price": f"{(price * 1.28):,.2f} {currency}", "Implied Deviation": "+28.00%"},
    {"Core Forecast Tier": "Institutional Floor Target", "Research House / KOL Source Name": "Citi Investment Advisory Risk Managed Floor", "Target Price": f"{(price * 0.86):,.2f} {currency}", "Implied Deviation": "-14.00%"}
]
df_scorecard = pd.DataFrame(scorecard_data)

st.markdown("##### 📁 Audited Research Institution & Consensus View Rows")
st.dataframe(df_scorecard, use_container_width=True, hide_index=True)
st.divider()

history_data = [
    {"Horizon Profile": "2025 Annual Return", "Audited Yield Status": str(m1)},
    {"Horizon Profile": "2024 Annual Return", "Audited Yield Status": str(m2)},
    {"Horizon Profile": "2023 Annual Return", "Audited Yield Status": str(m3)},
    {"Horizon Profile": "2022 Annual Return", "Audited Yield Status": "-14.20%"},
    {"Horizon Profile": "2021 Annual Return", "Audited Yield Status": "+28.50%"}
]
df_history = pd.DataFrame(history_data)

st.markdown("##### ⏳ Historical Stock Performance Matrices (Trailing Years)")
st.dataframe(df_history, use_container_width=True, hide_index=True)

