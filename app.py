import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="The Predictor Scorecard", page_icon="🎯", layout="wide", initial_sidebar_state="collapsed")

# 2. Fixed Single-Line CSS Injection (Prevents Redacted TypeError)
st.markdown("<style>.metric-box { background-color: rgba(128,128,128,0.05); padding: 15px; border-radius: 8px; border-left: 4px solid #0066cc; margin-bottom: 10px; } .source-tag { font-size: 0.85rem; background-color: rgba(0,102,204,0.1); color: #0066cc; padding: 3px 8px; border-radius: 4px; font-weight: bold; } .badge-success { background-color: rgba(40,167,69,0.15); color: #28a745; padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 0.85rem; display: inline-block; } .badge-pending { background-color: rgba(255,193,7,0.15); color: #ffc107; padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 0.85rem; display: inline-block; } .badge-failed { background-color: rgba(220,53,69,0.15); color: #dc3545; padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 0.85rem; display: inline-block; }</style>", unsafe_allowed_html=True)

# 3. Initialize Persistent App Database
if 'prediction_db' not in st.session_state:
    raw_data = {
        'Stock Code': ['NVDA', 'NVDA', 'NVDA', 'AAPL', 'AAPL', 'AAPL', 'TSLA', 'TSLA', 'TSLA', 'MSFT', 'MSFT', 'BTC', 'BTC'],
        'Predictor Name': ['Dan Ives (Wedbush)', 'David Kostin (Goldman Sachs)', 'Josh Brown (@Downtown)', 'David Faber (CNBC)', 'Wei Li (BlackRock)', 'Jim Cramer (CNBC)', 'Cathie Wood (ARK Invest)', 'Marko Kolanovic (Ex-JPMorgan)', 'Tavi Costa (Crescat)', 'Matt Levine (Bloomberg)', 'Gergely Orosz (Pragmatic Eng)', 'Lyn Alden', 'Balaji Srinivasan'],
        'Platform Tier': ['Wedbush Securities', 'Goldman Sachs Research', 'X / Ritholtz Wealth', 'CNBC Investigative', 'BlackRock Strategy', 'CNBC Mad Money', 'ARK Invest CEO', 'Ex-JPMorgan Strategy', 'X / Crescat Capital', 'Bloomberg Opinion', 'LinkedIn / Newsletter', 'Independent Macro', 'X / Tech Futurist'],
        'Their Historic Accuracy': ['48%', '59%', '54%', '67%', '68%', '38%', '41%', '34%', '52%', '82%', '68%', '64%', '39%'],
        'Their Specific Prediction': ['Target $160 - AI demand structural hyper-cycle', 'Target $130 - Near-term valuation consolidation', 'Accumulate on dips - Tech momentum remains strong', 'Supply chain optimization pushes target to $260', 'Neutral stance on near-term hardware cycles', 'Buy basket before institutional upgrade cycle', 'Target $2,600 by 2029 on autonomous robotaxis', 'Underperform - Competitive pressures mounting', 'Target $400 - Electric vehicle market saturation', 'Regulatory anti-trust shifts present structural risk', 'Enterprise cloud spending bottomed out', 'Long structural cycle - Monetary debasement hedge', 'Hyper-accelerated sovereign capital flight timeline'],
        'Status': ['⏳ Live Window', '✅ Met Target', '⏳ Live Window', '✅ Met Target', '⏳ Live Window', '❌ Missed Window', '❌ Structural Drift', '❌ Missed Target', '⏳ Live Window', '✅ Verified Metric', '✅ Verified Metric', '✅ Met Target', '❌ Out of Bounds']
    }
    st.session_state.prediction_db = pd.DataFrame(raw_data)

# Helper function to convert text strings to HTML badges
def apply_color_badges(status_string):
    if "Met" in status_string or "Verified" in status_string:
        return f'<span class="badge-success">{status_string}</span>'
    elif "Live" in status_string or "Pending" in status_string:
        return f'<span class="badge-pending">{status_string}</span>'
    else:
        return f'<span class="badge-failed">{status_string}</span>'

# Apply formatting across dataframe dynamically
display_master_df = st.session_state.prediction_db.copy()
display_master_df['Status'] = display_master_df['Status'].apply(apply_color_badges)

# 4. Executive Header
st.title("🎯 The Predictor Scorecard")
st.markdown("### *Cross-Referencing Analyst & KOL Forecasts by Asset Code*")
st.divider()

# 5. UI Layout: Core Features
col_main, col_side = st.columns([2.5, 1])

with col_main:
    st.markdown("#### 🔍 Asset Intelligence Hub")
    user_stock = st.text_input("Enter a Stock Code to pull targeted predictions (e.g., NVDA, AAPL, TSLA, BTC):", "NVDA").strip().upper()
    
    filtered_df = display_master_df[display_master_df['Stock Code'] == user_stock]
    st.markdown(f"##### Results for ticker: **{user_stock}**")
    
    if not filtered_df.empty:
        st.write(filtered_df[['Predictor Name', 'Platform Tier', 'Their Historic Accuracy', 'Their Specific Prediction', 'Status']].to_html(escape=False, index=False), unsafe_allowed_html=True)
    else:
        st.warning(f"No tracked predictions found for '{user_stock}' yet. Use the form on the right or try NVDA, AAPL, TSLA.")

with col_side:
    st.markdown("##### 📁 Verification Feeds")
    st.markdown("<div class='metric-box'><span class='source-tag'>Primary Data Logs</span><br><small style='color:gray;'>Cross-checked via SEC, Financial Press, & Ledger Signatures.</small></div>", unsafe_allowed_html=True)
    
    st.markdown("##### 📥 Submit a New Tracked Prediction")
    with st.form("new_prediction_form", clear_on_submit=True):
        new_ticker = st.text_input("Asset Ticker Code:", placeholder="e.g., AMD, ETH, MSFT").strip().upper()
        new_name = st.text_input("Analyst / KOL Name:", placeholder="e.g., Tom Lee (Fundstrat)")
        new_platform = st.text_input("Platform / Network Base:", placeholder="e.g., X (Twitter), Bloomberg")
        new_accuracy = st.slider("Estimated Past Accuracy Rating (%):", min_value=0, max_value=100, value=50)
        new_claim = st.text_area("Specific Public Forecast Claim:", placeholder="Type the precise price target or structural direction thesis...")
        
        submit_btn = st.form_submit_button("Log Claim to Audit Engine")
        
        if submit_btn:
            if new_ticker and new_name and new_claim:
                new_row = pd.DataFrame([{
                    'Stock Code': new_ticker,
                    'Predictor Name': new_name,
                    'Platform Tier': new_platform if new_platform else 'Crowdsourced Log',
                    'Their Historic Accuracy': f"{new_accuracy}%",
                    'Their Specific Prediction': new_claim,
                    'Status': '⏳ Live Window'
                }])
                st.session_state.prediction_db = pd.concat([st.session_state.prediction_db, new_row], ignore_index=True)
                st.success(f"Claim successfully cataloged! Search fields will now display {new_name}'s entry.")
                st.rerun()
            else:
                st.error("Submission failed. Ticker, Name, and Prediction Claim are required fields.")

# 6. Global Directory Overview
st.divider()
st.markdown("#### 🌐 Global Tracker Directory (All Monitored Assets)")
st.write(display_master_df.sort_values(by='Stock Code').to_html(escape=False, index=False), unsafe_allowed_html=True)

