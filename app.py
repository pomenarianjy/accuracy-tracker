import streamlit as st
import pandas as pd

# 1. Clean Native Page Configuration
st.set_page_config(
    page_title="The Predictor Scorecard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Institutional Database: Multi-KOL Mappings per Ticker
if 'prediction_db' not in st.session_state:
    columns_list = ['Stock Code', 'Asset Description', 'Predictor Name', 'Platform Tier', 'Historic Accuracy (%)', 'Specific Prediction', 'Status']
    
    rows_data = [
        # --- TSMC (TSM) ---
        ['TSM', 'TSMC (Taiwan Semiconductor)', 'Stacy Rasgon (Bernstein)', 'Bernstein Research', 74, 'Advanced node capacity utilisation hitting 100% on structural high-performance computing (HPC) demand lines', 'Verified Metric'],
        ['TSM', 'TSMC (Taiwan Semiconductor)', 'Randy Abrams (UBS Strategy)', 'UBS Global Wealth', 66, 'Foundry expansion packaging bottlenecks clearing out faster than macro expectations', 'Live Window'],
        ['TSM', 'TSMC (Taiwan Semiconductor)', 'C.J. Muse (Evercore ISI)', 'Institutional Research', 72, 'Advanced N3 and N2 node yield metrics leading global outsourcing metrics by wide margins', 'Verified Metric'],

        # --- ASML (ASML) ---
        ['ASML', 'ASML Holding (Lithography)', 'C.J. Muse (Evercore ISI)', 'Institutional Research', 72, 'High-NA EUV machinery order backlogs maintain multi-year visibility despite macro cyclical delays', 'Verified Metric'],
        ['ASML', 'ASML Holding (Lithography)', 'Stacy Rasgon (Bernstein)', 'Bernstein Research', 74, 'System lithography memory shipment revisions bottoming out across European manufacturing tiers', 'Live Window'],

        # --- AMD (AMD) ---
        ['AMD', 'Advanced Micro Devices', 'Dan Ives (Wedbush)', 'Wedbush Securities', 48, 'Enterprise data center market share gains in AI accelerators expanding cloud software visibility parameters', 'Live Window'],
        ['AMD', 'Advanced Micro Devices', 'Josh Brown (@Downtown)', 'X / Ritholtz Wealth', 54, 'Consensus targets underestimating MI300 series scale and adoption velocities among enterprise groups', 'Live Window'],
        ['AMD', 'Advanced Micro Devices', 'Jim Cramer (CNBC)', 'CNBC Mad Money', 38, 'Buy the underlying weakness before the developer ecosystem updates launch', 'Missed Window'],

        # --- NVIDIA (NVDA) ---
        ['NVDA', 'NVIDIA Corporation', 'Josh Brown (@Downtown)', 'X / Ritholtz Wealth', 54, 'Next-generation architecture production runs facing absolute supply limits relative to baseline hyperscaler commitments', 'Live Window'],
        ['NVDA', 'NVIDIA Corporation', 'Dan Ives (Wedbush)', 'Wedbush Securities', 48, 'AI infrastructure spending cycle is still in the early stages across major hyperscalers', 'Live Window'],
        ['NVDA', 'NVIDIA Corporation', 'Toshiya Hari (Goldman Sachs)', 'Goldman Sachs Research', 70, 'Enterprise hardware market capitalization baseline multiple remains highly defensible relative to cash flow', 'Met Target'],

        # --- MICRON (MU) ---
        ['MU', 'Micron Technology', 'Tom Lee (Fundstrat)', 'Fundstrat Global Advisors', 78, 'Pricing velocity for server DRAM driving structural revenue expansion trends through the fiscal cycle', 'Met Target'],
        ['MU', 'Micron Technology', 'Timothy Arcuri (UBS)', 'UBS Investment Bank', 68, 'High-bandwidth memory memory tier shipments expanding margins past baseline industry targets', 'Verified Metric'],

        # --- BROADCOM (AVGO) ---
        ['AVGO', 'Broadcom Inc.', 'Harlan Sur (JPMorgan)', 'JPMorgan Research', 75, 'Custom application-specific integrated circuit (ASIC) pipelines scaling aggressively across multiple large internet clients', 'Met Target'],
        ['AVGO', 'Broadcom Inc.', 'Atif Malik (Citi)', 'Citi Research', 64, 'Networking infrastructure and custom silicon integration cycles creating resilient long-term contracts', 'Verified Metric'],

        # --- INTEL (INTC) ---
        ['INTC', 'Intel Corporation', 'Pat Gelsinger (CEO Insights)', 'Corporate Guidance', 45, 'External packaging and system foundry customer contract backlog verification marks long-term floor', 'Structural Drift'],
        ['INTC', 'Intel Corporation', 'Blayne Curtis (Jefferies)', 'Jefferies Strategy', 67, 'Foundry margin execution drag remains significant risk over the medium-term execution window', 'Missed Target']
    ]
    
    st.session_state.prediction_db = pd.DataFrame(rows_data, columns=columns_list)

# 3. Process Dynamic Dropdown Lists
AVAILABLE_TICKERS = sorted(list(st.session_state.prediction_db['Stock Code'].unique()))

# 4. Clean Consumer Header
st.title("🎯 The Predictor Scorecard")
st.markdown("### Track the actual performance of investment KOLs, bank analysts, and researchers.")
st.divider()

# 5. Asset Selector Search Hub
user_stock = st.selectbox(
    "Select a Stock / Index Code to view all matching analyst predictions:", 
    options=AVAILABLE_TICKERS, 
    index=AVAILABLE_TICKERS.index('NVDA') if 'NVDA' in AVAILABLE_TICKERS else 0
)

# Isolate matching stock records
filtered_df = st.session_state.prediction_db[st.session_state.prediction_db['Stock Code'] == user_stock]

if not filtered_df.empty:
    # Pull clean text description strings safely
    clean_asset_name = str(filtered_df['Asset Description'].iloc)
    st.markdown(f"#### Showing All Tracker Audits For: **{user_stock} ({clean_asset_name})**")
    
    # Sort the tracking entries so the most accurate analysts bubble to the very top automatically
    sorted_df = filtered_df.sort_values(by='Historic Accuracy (%)', ascending=False)
    
    # Display the final, polished leaderboard table
    st.dataframe(
        sorted_df[['Predictor Name', 'Platform Tier', 'Historic Accuracy (%)', 'Specific Prediction', 'Status']],
        use_container_width=True,
        hide_index=True
    )
else:
    st.error("No data records map to this choice.")

# 6. Global Master Directory Overview
st.divider()
st.markdown("#### 🌐 Complete Global Semiconductor Tracker Directory")
st.dataframe(
    st.session_state.prediction_db.sort_values(by=['Stock Code', 'Historic Accuracy (%)'], ascending=[True, False]),
    use_container_width=True,
    hide_index=True
)
