import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# 1. Clean Native Page Configuration
st.set_page_config(
    page_title="The Predictor Scorecard | Automated Institutional Consensus",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Executive Consumer Header
st.title("🎯 The Automated Predictor Scorecard")
st.markdown("### Real-Time Wall Street Consensus Targets & Forecast Auditing Engine")
st.caption("⚡ Powered by live financial data. Automatically fetching, parsing, and structured forward-looking targets.")
st.divider()

# 3. Expanded Universal Ticker List (Mag 7 + Complete Top 25 SOXX Holdings + Global Giants)
TICKER_DIRECTORY = [
    "SOXX", "NVDA", "AVGO", "AMD", "QCOM", "TXN", "MU", "AMAT", "LRCX", "ADI", 
    "KLAC", "MRVL", "NXPI", "MCHP", "MPWR", "ON", "SWKS", "QRVO", "CRUS", "TER", 
    "AMKR", "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "INTC", "TSM", "ASML"
]

# 4. Interactive Dropdown Asset Selector
user_stock = st.selectbox(
    "Select a Stock Ticker or Index Component to audit live consensus forecasts:",
    options=sorted(TICKER_DIRECTORY),
    index=sorted(TICKER_DIRECTORY).index("META") if "META" in TICKER_DIRECTORY else 0
)

# 5. Live Data Fetching & Scraping Engine
@st.cache_data(ttl=3600)  # Caches data for 1 hour to keep the app blazing fast
def fetch_live_analyst_data(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        
        # Pull live baseline market points
        current_price = info.get('currentPrice', info.get('previousClose', 0.0))
        company_name = info.get('longName', ticker_symbol)
        
        # Pull Wall Street Forward Price Targets
        targets = ticker.analyst_price_targets
        mean_target = targets.get('mean', None)
        high_target = targets.get('high', None)
        low_target = targets.get('low', None)
        num_analysts = info.get('numberOfAnalystOpinions', 0)
        
        if not mean_target:
            return None, company_name, current_price
            
        # Structure automated forward-looking data points
        consensus_rows = [
            {
                "Predictor Tier": "Wall Street Consensus (Average)",
                "Forecast Target Price": f"${mean_target:,.2f}",
                "Implied Return (%)": f"{((mean_target / current_price) - 1) * 100:.2f}%",
                "Thesis / Context Vector": f"Aggregated view of {num_analysts} institutional analysts tracking structural sector margins.",
                "Status/Window": "⏳ Active 12-Month Target"
            },
            {
                "Predictor Tier": "Institutional Bull Case (Highest)",
                "Forecast Target Price": f"${high_target:,.2f}",
                "Implied Return (%)": f"{((high_target / current_price) - 1) * 100:.2f}%",
                "Thesis / Context Vector": "Top-tier valuation models mapping optimal growth expansion curves.",
                "Status/Window": "⏳ Active 12-Month Target"
            },
            {
                "Predictor Tier": "Institutional Bear Case (Lowest)",
                "Forecast Target Price": f"${low_target:,.2f}",
                "Implied Return (%)": f"{((low_target / current_price) - 1) * 100:.2f}%",
                "Thesis / Context Vector": "Conservative valuation models mapping margin contraction or structural cyclical risks.",
                "Status/Window": "⏳ Active 12-Month Target"
            }
        ]
        return pd.DataFrame(consensus_rows), company_name, current_price
    except Exception as e:
        return None, ticker_symbol, 0.0

# 6. Execution & Rendering
with st.spinner(f"Querying live global data endpoints for {user_stock}..."):
    forecast_df, asset_fullname, live_price = fetch_live_analyst_data(user_stock)

# Display targeted layout metrics
if forecast_df is not None:
    st.markdown(f"#### Showing Automated Consensus Audits For: **{user_stock} ({asset_fullname})**")
    
    # Visual KPI Blocks
    kpi1, kpi2 = st.columns(2)
    kpi1.metric("Live Market Price", f"${live_price:,.2f}")
    kpi2.metric("Total Institutional Coverage", f"{yf.Ticker(user_stock).info.get('numberOfAnalystOpinions', 'N/A')} Banks/Firms")
    st.write("")
    
    # Render the automated structured analytics table
    st.dataframe(forecast_df, use_container_width=True, hide_index=True)
else:
    st.markdown(f"#### Showing Automated Consensus Audits For: **{user_stock} ({asset_fullname})**")
    st.warning(f"Live forward price target data is currently restricted or unavailable for ticker: {user_stock}. General info summary is displayed below.")
    try:
        st.json({
            "Ticker": user_stock,
            "Company Name": asset_fullname,
            "Current Stock Price": f"${live_price:,.2f}"
        })
    except Exception:
        st.error("Data tracking timeout. Please choose another ticker from the selector panel.")

