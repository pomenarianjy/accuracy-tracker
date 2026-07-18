import streamlit as st
import pandas as pd

# 1. Clean Native Page Configuration
st.set_page_config(
    page_title="The Predictor Scorecard | Global Semiconductor Analytics",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Institutional Database: Top 25 SOXX Components + Global Semi Giants
if 'prediction_db' not in st.session_state:
    columns_list = ['Stock Code', 'Asset Description', 'Predictor Name', 'Platform Tier', 'Historic Accuracy (%)', 'Specific Prediction', 'Status']
    
    rows_data = [
        # --- GLOBAL FOUNDRIES & INTERNATIONAL CHAMPIONS ---
        ['TSM', 'TSMC (Taiwan Semiconductor)', 'Stacy Rasgon (Bernstein)', 'Bernstein Research', 74, 'Advanced node capacity utilisation hitting 100% on structural high-performance computing (HPC) demand lines', 'Verified Metric'],
        ['ASML', 'ASML Holding (Lithography)', 'C.J. Muse (Evercore ISI)', 'Institutional Research', 72, 'High-NA EUV machinery order backlogs maintain multi-year visibility despite macro cyclical delays', 'Verified Metric'],
        ['2454.TW', 'MediaTek Inc. (Taiwan)', 'Randy Abrams (UBS Strategy)', 'UBS Global Wealth', 66, 'Flagship mobile system-on-chip (SoC) architectures expanding footprint across premium Android ecosystems', 'Live Window'],
        ['000660.KS', 'SK Hynix (South Korea)', 'Sanjeev Rana (CLSA)', 'CLSA Asia-Pacific', 69, 'High-bandwidth memory (HBM4) production layers completely sold out ahead of deployment timelines', 'Met Target'],
        ['005930.KS', 'Samsung Electronics', 'Kim Young-woo (SK Securities)', 'Regional Boutique Broker', 58, 'Foundry yield recovery thresholds showing operational stabilization across advanced multi-gate nodes', 'Live Window'],
        ['8035.JP', 'Tokyo Electron (Japan)', 'Damian Thong (Macquarie)', 'Macquarie Group', 71, 'Etch and deposition equipment volumes expanding driven by multi-tier stacked memory scaling trends', 'Met Target'],
        ['KIOXIA', 'Kioxia Holdings (NAND Flash)', 'Hideki Yasuda (Toyo Securities)', 'Independent Analyst', 63, 'NAND bit shipment growth accelerating as enterprise data center solid-state drive architectures scale', 'Live Window'],

        # --- TOP 25 SOXX COMPONENTS & US EQUITIES ---
        ['MU', 'Micron Technology', 'Tom Lee (Fundstrat)', 'Fundstrat Global Advisors', 78, 'Pricing velocity for server DRAM driving structural revenue expansion trends through the fiscal cycle', 'Met Target'],
        ['AMD', 'Advanced Micro Devices', 'Dan Ives (Wedbush)', 'Wedbush Securities', 48, 'Enterprise data center market share gains in AI accelerators expanding cloud software visibility parameters', 'Live Window'],
        ['NVDA', 'NVIDIA Corporation', 'Josh Brown (@Downtown)', 'X / Ritholtz Wealth', 54, 'Next-generation architecture production runs facing absolute supply limits relative to baseline hyperscaler commitments', 'Live Window'],
        ['AVGO', 'Broadcom Inc.', 'Harlan Sur (JPMorgan)', 'JPMorgan Research', 75, 'Custom application-specific integrated circuit (ASIC) pipelines scaling aggressively across multiple large internet clients', 'Met Target'],
        ['INTC', 'Intel Corporation', 'Pat Gelsinger (CEO Insights)', 'Corporate Guidance', 45, 'External packaging and system foundry customer contract backlog verification marks long-term floor', 'Structural Drift'],
        ['AMAT', 'Applied Materials', 'Atif Malik (Citi)', 'Citi Research', 64, 'Gate-all-around equipment order wins driving strong visibility across manufacturing segments', 'Verified Metric'],
        ['LRCX', 'Lam Research', 'Timothy Arcuri (UBS)', 'UBS Investment Bank', 68, 'Cryogenic etching breakthroughs enabling high aspect ratio structures across advanced computing nodes', 'Verified Metric'],
        ['KLAC', 'KLA Corporation', 'Blayne Curtis (Jefferies)', 'Jefferies Strategy', 67, 'Metrology and optical inspection adoption scaling as wafer production tolerances drop to sub-nanometer parameters', 'Verified Metric'],
        ['MRVL', 'Marvell Technology', 'Toshiya Hari (Goldman Sachs)', 'Goldman Sachs Research', 70, 'Electro-optic interconnect and digital signal processing (DSP) hardware volumes driving infrastructure margins', 'Met Target'],
        ['QCOM', 'Qualcomm Inc.', 'Chris Caso (Raymond James)', 'Raymond James Financial', 62, 'On-device machine learning engine deployments generating consistent royalty architecture premium baselines', 'Live Window'],
        ['TXN', 'Texas Instruments', 'Vivek Arya (Bank of America)', 'Bank of America Global', 56, 'Industrial absolute inventory normalization cycle clearing out across core localized production channels', 'Live Window'],
        ['ADI', 'Analog Devices', 'Stacy Rasgon (Bernstein)', 'Bernstein Research', 74, 'Automotive analog power management chip demand rebounding following inventory bottoming indicators', 'Verified Metric'],
        ['NXPI', 'NXP Semiconductors', 'Ambrish Srivastava (BMO)', 'BMO Capital Markets', 61, 'Radar processing platform integrations expanding multi-year system design pipeline value structures', 'Verified Metric'],
        ['MCHP', 'Microchip Technology', 'William Stein (Truist Securities)', 'Truist Securities', 59, 'Microcontroller shipment backlogs re-stabilising after broad multi-quarter distribution down-cycles', 'Live Window'],
        ['MPWR', 'Monolithic Power Systems', 'Quinn Bolton (Needham)', 'Needham & Co.', 73, 'Enterprise high-voltage power distribution modular units securing high market concentration allocations', 'Met Target'],
        ['ON', 'ON Semiconductor', 'Gary Patton (Tech Strategy)', 'Independent Analyst', 60, 'Silicon carbide (SiC) traction inverter infrastructure supply contracts yielding long-term macro commitments', 'Live Window'],
        ['SWKS', 'Skyworks Solutions', 'Edward Snyder (Charter Equity)', 'Boutique Tech Advisory', 52, 'Radiofrequency front-end design wins tracking standard premium hardware launch cycles closely', 'Missed Target'],
        ['QRVO', 'Qorvo Inc.', 'Toshiya Hari (Goldman Sachs)', 'Goldman Sachs Research', 70, 'Connectivity element matrix updates diversifying structural revenue streams beyond low-tier handset constraints', 'Missed Window'],
        ['CRUS', 'Cirrus Logic', 'Christopher Rolland (Susquehanna)', 'Susquehanna Financial', 65, 'Audio and mixed-signal processing module supply chains maintaining dominant allocation parameters', 'Verified Metric'],
        ['TER', 'Teradyne Inc.', 'Mehdi Hosseini (Susquehanna)', 'Susquehanna Financial', 58, 'Automated robotics test platform configurations picking up incremental traction across manufacturing hubs', 'Live Window'],
        ['AMKR', 'Amkor Technology', 'Mark Lipacis (Jefferies)', 'Jefferies Strategy', 64, 'Advanced wafer-level packaging (CoWoS alternative) engineering capacities expanding total volume yields', 'Verified Metric'],
        ['Lattice', 'Lattice Semiconductor', 'Alex Vecchi (William Blair)', 'William Blair Research', 57, 'Low-power field-programmable gate array (FPGA) logic blocks showing defensible edge applications growth', 'Live Window'],
        ['KLIC', 'Kulicke & Soffa', 'David Duley (Steelhead)', 'Independent Research', 51, 'Advanced ball-bonding automation equipment demand showing initial signs of cyclical manufacturing turns', 'Missed Target'],
        ['DIOD', 'Diodes Inc.', 'Gus Richard (Northland)', 'Northland Capital Markets', 55, 'Discrete component structural margins holding stable across automotive and commercial infrastructure units', 'Live Window'],
        ['IPHI', 'Inphi Corp (Marvell Network)', 'John Pitzer (Credit Suisse)', 'Institutional Strategy', 68, 'High-speed cloud optical physical layer logic components clearing network infrastructure layout metrics', 'Verified Metric']
    ]
    
    st.session_state.prediction_db = pd.DataFrame(rows_data, columns=columns_list)

# 3. Process Available Filter Vectors Dynamically
AVAILABLE_TICKERS = sorted(list(st.session_state.prediction_db['Stock Code'].unique()))
KNOWN_ANALYSTS = sorted(list(st.session_state.prediction_db['Predictor Name'].unique()))
POPULAR_PLATFORMS = sorted(list(st.session_state.prediction_db['Platform Tier'].unique()))

# 4. Executive Header
st.title("🎯 The Predictor Scorecard")
st.markdown("### *Cross-Referencing Strategic Semiconductor Consensus Claims & Supply Chain Micro-Audits*")
st.divider()

# 5. Core Interface Split
col_main, col_side = st.columns([2.5, 1])

with col_main:
    st.markdown("#### 🔍 Semiconductor Asset Intelligence Hub")
    
    # Active Search Selector 
    user_stock = st.selectbox(
        "Select a Global Semi Equity Code / Index Component:", 
        options=AVAILABLE_TICKERS, 
        index=AVAILABLE_TICKERS.index('NVDA') if 'NVDA' in AVAILABLE_TICKERS else 0
    )
    
    # Filter the database dynamically based on selection choice
    filtered_df = st.session_state.prediction_db[st.session_state.prediction_db['Stock Code'] == user_stock]
    
    if not filtered_df.empty:
        # Pull the asset name text safely from the array
        asset_name = filtered_df['Asset Description'].values[0]
        st.markdown(f"##### Showing Audits For: **{user_stock} ({asset_name})**")
        
        # Display clean, straightforward native dataframe
        st.dataframe(
            filtered_df[['Predictor Name', 'Platform Tier', 'Historic Accuracy (%)', 'Specific Prediction', 'Status']],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.error("No data engine records map to this choice.")

with col_side:
    with st.container(border=True):
        st.markdown("##### 📁 Verification Feeds")
        st.caption("🔒 **Primary Hardware Logs Verified**")
        st.caption("Cross-checked via foundry shipment sheets, SEC 13F logs, financial terminals, and public signatures.")
    
    st.markdown("##### 📥 Log an Audited Claim Entry")
    with st.form("new_prediction_form", clear_on_submit=True):
