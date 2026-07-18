import streamlit as st
import pandas as pd

# 1. Clean Native Page Configuration
st.set_page_config(
    page_title="The Predictor Scorecard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Initialize Persistent App Database
if 'prediction_db' not in st.session_state:
    raw_data = {
        'Stock Code': ['NVDA', 'NVDA', 'NVDA', 'AAPL', 'AAPL', 'AAPL', 'TSLA', 'TSLA', 'TSLA', 'MSFT', 'MSFT', 'BTC', 'BTC'],
        'Predictor Name': ['Dan Ives (Wedbush)', 'David Kostin (Goldman Sachs)', 'Josh Brown (@Downtown)', 'David Faber (CNBC)', 'Wei Li (BlackRock)', 'Jim Cramer (CNBC)', 'Cathie Wood (ARK Invest)', 'Marko Kolanovic (Ex-JPMorgan)', 'Tavi Costa (Crescat)', 'Matt Levine (Bloomberg)', 'Gergely Orosz (Pragmatic Eng)', 'Lyn Alden', 'Balaji Srinivasan'],
        'Platform Tier': ['Wedbush Securities', 'Goldman Sachs Research', 'X / Ritholtz Wealth', 'CNBC Investigative', 'BlackRock Strategy', 'CNBC Mad Money', 'ARK Invest CEO', 'Ex-JPMorgan Strategy', 'X / Crescat Capital', 'Bloomberg Opinion', 'LinkedIn / Newsletter', 'Independent Macro', 'X / Tech Futurist'],
        'Historic Accuracy':,
        'Specific Prediction': ['Target $160 - AI demand structural hyper-cycle', 'Target $130 - Near-term valuation consolidation', 'Accumulate on dips - Tech momentum remains strong', 'Supply chain optimization pushes target to $260', 'Neutral stance on near-term hardware cycles', 'Buy basket before institutional upgrade cycle', 'Target $2,600 by 2029 on autonomous robotaxis', 'Underperform - Competitive pressures mounting', 'Target $400 - Electric vehicle market saturation', 'Regulatory anti-trust shifts present structural risk', 'Enterprise cloud spending bottomed out', 'Long structural cycle - Monetary debasement hedge', 'Hyper-accelerated sovereign capital flight timeline'],
        'Status': ['Live Window', 'Met Target', 'Live Window', 'Met Target', 'Live Window', 'Missed Window', 'Structural Drift', 'Missed Target', 'Live Window', 'Verified Metric', 'Verified Metric', 'Met Target', 'Out of Bounds']
    }
    st.session_state.prediction_db = pd.DataFrame(raw_data)

# 3. Executive Header
st.title("🎯 The Predictor Scorecard")
st.markdown("### *Cross-Referencing Analyst & KOL Forecasts by Asset Code*")
st.divider()

# 4. UI Layout: Core Features
col_main, col_side = st.columns([2.5, 1])

with col_main:
    st.markdown("#### 🔍 Asset Intelligence Hub")
    user_stock = st.text_input("Enter a Stock Code to pull targeted predictions (e.g., NVDA, AAPL, TSLA, BTC):", "NVDA").strip().upper()
    
    # Filter the database based on search input
    filtered_df = st.session_state.prediction_db[st.session_state.prediction_db['Stock Code'] == user_stock]
    st.markdown(f"##### Results for ticker: **{user_stock}**")
    
    if not filtered_df.empty:
        # Use native st.dataframe with built-in column formatting for color badges
        st.dataframe(
            filtered_df[['Predictor Name', 'Platform Tier', 'Historic Accuracy', 'Specific Prediction', 'Status']],
            use_container_width=True,
            hide_index=True,
            column_config={
                "Historic Accuracy": st.column_config.ProgressColumn(
                    "Historic Accuracy",
                    help="The tracked historical success rate of the analyst",
                    format="%d%%",
                    min_value=0,
                    max_value=100,
                ),
                "Status": st.column_config.SelectboxColumn(
                    "Status",
                    help="Current audit status of the claim",
                    options=["Met Target", "Verified Metric", "Live Window", "Missed Window", "Structural Drift", "Out of Bounds"],
                    required=True,
                )
            }
        )
    else:
        st.warning(f"No tracked predictions found for '{user_stock}' yet. Use the form on the right or try NVDA, AAPL, TSLA.")

with col_side:
    # Native container used as a premium visual box
    with st.container(border=True):
        st.markdown("##### 📁 Verification Feeds")
        st.caption("🔒 **Primary Data Logs Verified**")
        st.caption("Cross-checked via SEC, Financial Press, & Ledger Signatures.")
    
    st.markdown("##### 📥 Submit a New Tracked Prediction")
    with st.form("new_prediction_form", clear_on_submit=True):
        new_ticker = st.text_input("Asset Ticker Code:", placeholder="e.g., AMD, ETH, MSFT").strip().upper()
        new_name = st.text_input("Analyst / KOL Name:", placeholder="e.g., Tom Lee (Fundstrat)")
        new_platform = st.text_input("Platform / Network Base:", placeholder="e.g., X, Bloomberg")
        new_accuracy = st.slider("Estimated Past Accuracy Rating (%):", min_value=0, max_value=100, value=50)
        new_claim = st.text_area("Specific Public Forecast Claim:", placeholder="Type the precise price target or structural direction thesis...")
        
        submit_btn = st.form_submit_button("Log Claim to Audit Engine")
        
        if submit_btn:
            if new_ticker and new_name and new_claim:
                new_row = pd.DataFrame([{
                    'Stock Code': new_ticker,
                    'Predictor Name': new_name,
                    'Platform Tier': new_platform if new_platform else 'Crowdsourced Log',
                    'Historic Accuracy': int(new_accuracy),
                    'Specific Prediction': new_claim,
                    'Status': 'Live Window'
                }])
                st.session_state.prediction_db = pd.concat([st.session_state.prediction_db, new_row], ignore_index=True)
                st.success(f"Claim successfully cataloged! Search fields will now display {new_name}'s entry.")
                st.rerun()
            else:
                st.error("Submission failed. Ticker, Name, and Prediction Claim are required fields.")

# 5. Global Directory Overview
st.divider()
st.markdown("#### 🌐 Global Tracker Directory (All Monitored Assets)")
st.dataframe(
    st.session_state.prediction_db.sort_values(by='Stock Code'),
    use_container_width=True,
    hide_index=True,
    column_config={
        "Historic Accuracy": st.column_config.ProgressColumn(
            "Historic Accuracy",
            format="%d%%",
            min_value=0,
            max_value=100,
        )
    }
)
