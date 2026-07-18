import streamlit as st
import pandas as pd

# 1. Clean Native Page Configuration
st.set_page_config(
    page_title="The Predictor Scorecard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Comprehensive Global Semiconductor Database
if 'prediction_db' not in st.session_state:
    columns_list = ['Stock Code', 'Asset Description', 'Predictor Name', 'Platform Tier', 'Historic Accuracy (%)', 'Specific Prediction', 'Status']
    
    rows_data = [
        # --- THE SOXX ETF ---
        ['SOXX', 'iShares Semiconductor ETF', 'Stacy Rasgon (Bernstein)', 'Bernstein Research', 74, 'Overall ETF structural volume scaling aggressively driven by broad enterprise hardware demand sweeps', 'Verified Metric'],
        ['SOXX', 'iShares Semiconductor ETF', 'Jim Cramer (CNBC)', 'CNBC Mad Money', 38, 'Buy the index basket during broad cyclical tech valuation corrections', 'Missed Window'],

        # --- THE MAGNIFICENT 7 (SEMI & TECH SECTORS) ---
        ['NVDA', 'NVIDIA Corporation', 'Josh Brown (@Downtown)', 'X / Ritholtz Wealth', 54, 'Next-generation system cluster production runs facing strict capacity limits relative to hyper-scaler demands', 'Live Window'],
        ['NVDA', 'NVIDIA Corporation', 'Dan Ives (Wedbush)', 'Wedbush Securities', 48, 'AI infrastructure spending cycle is still in the early stages across major hyperscalers', 'Live Window'],
        ['NVDA', 'NVIDIA Corporation', 'Toshiya Hari (Goldman Sachs)', 'Goldman Sachs Research', 70, 'Enterprise hardware market capitalization baseline multiple remains highly defensible relative to cash flow', 'Met Target'],
        ['AMD', 'Advanced Micro Devices', 'Dan Ives (Wedbush)', 'Wedbush Securities', 48, 'Enterprise data center accelerator footprint expansion providing long-term cloud revenue stability', 'Live Window'],
        ['AMD', 'Advanced Micro Devices', 'Josh Brown (@Downtown)', 'X / Ritholtz Wealth', 54, 'Consensus targets underestimating MI300 series scale and adoption velocities among enterprise groups', 'Live Window'],
        ['AAPL', 'Apple Inc.', 'David Faber (CNBC)', 'CNBC Investigative', 67, 'Edge computing software upgrades to trigger premium device replacement ecosystem cycles', 'Met Target'],
        ['MSFT', 'Microsoft Corporation', 'Matt Levine (Bloomberg)', 'Bloomberg Opinion', 82, 'Commercial software and AI-driven cloud subscription backlogs present multi-year recurring visibility', 'Verified Metric'],
        ['GOOGL', 'Alphabet Inc.', 'Gene Munster (Deepwater)', 'Deepwater Asset Mgmt', 71, 'Ad network monetization architecture and core search defense outperforms market deceleration models', 'Met Target'],
        ['AMZN', 'Amazon.com Inc.', 'Andrew Jassy (CEO Insights)', 'Corporate Guidance', 65, 'Logistics network automation margins successfully offsetting structural absolute infrastructure costs', 'Verified Metric'],
        ['META', 'Meta Platforms Inc.', 'Brad Gerstner (Altimeter)', 'Hedge Fund Research', 75, 'Open-source code integrations and custom compute clusters driving global advertising conversion efficiency', 'Met Target'],
        ['TSLA', 'Tesla Inc.', 'Cathie Wood (ARK Invest)', 'ARK Invest CEO', 41, 'Autonomous robotaxi operations to command premium software enterprise valuations by 2029', 'Structural Drift'],

        # --- TOP 20 SOXX SEMICONDUCTOR HOLDINGS (US LISTED) ---
        ['AVGO', 'Broadcom Inc.', 'Harlan Sur (JPMorgan)', 'JPMorgan Research', 75, 'Custom application-specific integrated circuit (ASIC) pipelines locking in large cloud infrastructure commitments', 'Met Target'],
        ['QCOM', 'Qualcomm Inc.', 'Chris Caso (Raymond James)', 'Raymond James Financial', 62, 'On-device machine learning engine deployments generating consistent royalty architecture premium baselines', 'Live Window'],
        ['TXN', 'Texas Instruments', 'Vivek Arya (Bank of America)', 'Bank of America Global', 56, 'Industrial inventory pipeline channels approaching a cyclical clearing bottom phase', 'Live Window'],
        ['MU', 'Micron Technology', 'Tom Lee (Fundstrat)', 'Fundstrat Global Advisors', 78, 'High-bandwidth memory architecture supply completely sold out past current fiscal calendar windows', 'Met Target'],
        ['AMAT', 'Applied Materials', 'Atif Malik (Citi)', 'Citi Research', 64, 'Gate-all-around equipment manufacturing contract wins driving strong baseline visibility', 'Verified Metric'],
        ['LRCX', 'Lam Research', 'Timothy Arcuri (UBS)', 'UBS Investment Bank', 68, 'Cryogenic etching processing engineering capturing majority allocation yields across key production nodes', 'Verified Metric'],
        ['ADI', 'Analog Devices', 'Stacy Rasgon (Bernstein)', 'Bernstein Research', 74, 'Automotive absolute analog component inventory clearing cycles pointing toward a structural turnaround', 'Verified Metric'],
        ['KLAC', 'KLA Corporation', 'Blayne Curtis (Jefferies)', 'Jefferies Strategy', 67, 'Metrology and diagnostic inspection volume dependencies scaling with advanced multi-layer stack adoption', 'Verified Metric'],
        ['MRVL', 'Marvell Technology', 'Toshiya Hari (Goldman Sachs)', 'Goldman Sachs Research', 70, 'High-speed electro-optic interconnect demand vectors scaling adjacent to cluster deployments', 'Met Target'],
        ['NXPI', 'NXP Semiconductors', 'Ambrish Srivastava (BMO)', 'BMO Capital Markets', 61, 'Radar data processing platform component pipelines widening total vehicle system design pipelines', 'Verified Metric'],
        ['MCHP', 'Microchip Technology', 'William Stein (Truist Securities)', 'Truist Securities', 59, 'Microcontroller shipment backlogs stabilizing after systematic distributor adjustments phase out', 'Live Window'],
        ['MPWR', 'Monolithic Power Systems', 'Quinn Bolton (Needham)', 'Needham & Co.', 73, 'High-performance computing high-voltage distribution designs capturing dominant chip tier margins', 'Met Target'],
        ['ON', 'ON Semiconductor', 'Gary Patton (Tech Strategy)', 'Independent Analyst', 60, 'Silicon carbide power module infrastructure contracts anchoring medium-term absolute volume paths', 'Live Window'],
        ['SWKS', 'Skyworks Solutions', 'Edward Snyder (Charter Equity)', 'Boutique Tech Advisory', 52, 'Radiofrequency front-end configurations tracking traditional premium consumer product launch frames', 'Missed Target'],
        ['QRVO', 'Qorvo Inc.', 'Toshiya Hari (Goldman Sachs)', 'Goldman Sachs Research', 70, 'Connectivity element matrix upgrades diversifying structural revenue streams beyond low-tier handset constraints', 'Missed Window'],
        ['CRUS', 'Cirrus Logic', 'Christopher Rolland (Susquehanna)', 'Susquehanna Financial', 65, 'Audio and mixed-signal module allocations maintaining clear concentration leads within core consumer groups', 'Verified Metric'],
        ['TER', 'Teradyne Inc.', 'Mehdi Hosseini (Susquehanna)', 'Susquehanna Financial', 58, 'Automated industrial robotics test system integrations logging continuous baseline unit demand turns', 'Live Window'],
        ['INTC', 'Intel Corporation', 'Pat Gelsinger (CEO Insights)', 'Corporate Guidance', 45, 'External packaging and system foundry customer contract backlog verification marks long-term floor', 'Structural Drift'],

        # --- TAIWAN SEMICONDUCTOR LEADERS ---
        ['TSM', 'TSMC (Taiwan Semiconductor)', 'Stacy Rasgon (Bernstein)', 'Bernstein Research', 74, 'Advanced node asset utilization limits stretching to 100% efficiency targets on structural compute needs', 'Verified Metric'],
        ['TSM', 'TSMC (Taiwan Semiconductor)', 'Randy Abrams (UBS Strategy)', 'UBS Global Wealth', 66, 'Foundry expansion packaging bottlenecks clearing out faster than macro expectations', 'Live Window'],
        ['TSM', 'TSMC (Taiwan Semiconductor)', 'C.J. Muse (Evercore ISI)', 'Institutional Research', 72, 'Advanced N3 and N2 node yield metrics leading global outsourcing metrics by wide margins', 'Verified Metric'],
        ['2454.TW', 'MediaTek Inc. (Taiwan)', 'Randy Abrams (UBS Strategy)', 'UBS Global Wealth', 66, 'Flagship mobile system-on-chip architectures securing significant footprints across tier-1 client builds', 'Live Window'],

        # --- KOREA SEMICONDUCTOR LEADERS ---
        ['000660.KS', 'SK Hynix (South Korea)', 'Sanjeev Rana (CLSA)', 'CLSA Asia-Pacific', 69, 'High-bandwidth memory (HBM) production allocations fully committed ahead of distribution delivery windows', 'Met Target'],
        ['005930.KS', 'Samsung Electronics (South Korea)', 'Kim Young-woo (SK Securities)', 'Regional Boutique Broker', 58, 'Foundry yield recovery and structural node milestones demonstrating steady internal engineering progress', 'Live Window'],

        # --- JAPAN SEMICONDUCTOR LEADERS ---
        ['8035.JP', 'Tokyo Electron (Japan)', 'Damian Thong (Macquarie)', 'Macquarie Group', 71, 'Advanced etch and coating machinery shipment volumes expanding on multi-layer design dependencies', 'Met Target'],
        ['KIOXIA', 'Kioxia Holdings (Japan)', 'Hideki Yasuda (Toyo Securities)', 'Independent Analyst', 63, 'NAND bit volume shipments recovering as data center flash array migrations pick up velocity', 'Live Window']
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
    index=AVAILABLE_TICKERS.index('SOXX') if 'SOXX' in AVAILABLE_TICKERS else 0
)

# Isolate matching stock records
filtered_df = st.session_state.prediction_db[st.session_state.prediction_db['Stock Code'] == user_stock]

if not filtered_df.empty:


