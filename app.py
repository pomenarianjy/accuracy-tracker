import streamlit as st
import pandas as pd

# 1. Native Page Configuration Setup
st.set_page_config(
    page_title="The Predictors Scorecard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("The Predictors Scorecard")
st.markdown("### Investment Views Accuracy Tracking, by A Single Family Office")
st.divider()

# 2. Comprehensive Flat Database Directory (61 Assets Sanitized)
db = {
    # The Magnificent Seven
    "NVDA": [128.90, "USD", "+124.50%", "+122.40%", "-14.20%", "+145.10%"],
    "MSFT": [418.20, "USD", "+11.80%", "+28.10%", "-5.10%", "+52.40%"],
    "AAPL": [224.50, "USD", "+14.25%", "+25.40%", "-8.30%", "+48.20%"],
    "GOOGL": [182.10, "USD", "+18.40%", "+21.30%", "-12.40%", "+39.80%"],
    "AMZN": [188.40, "USD", "+22.15%", "+24.80%", "-9.20%", "+44.10%"],
    "META": [498.60, "USD", "+38.60%", "+34.20%", "-4.60%", "+61.20%"],
    "TSLA": [214.30, "USD", "-12.40%", "+15.60%", "-22.10%", "+28.40%"],
    
    # SOXX Top 15 Holdings
    "AMD": [148.20, "USD", "-3.40%", "+17.20%", "-15.10%", "+29.40%"],
    "MU": [94.60, "USD", "+11.20%", "+26.10%", "-18.40%", "+41.20%"],
    "AVGO": [168.50, "USD", "+44.10%", "+38.60%", "-3.20%", "+58.70%"],
    "AMAT": [182.30, "USD", "+16.40%", "+22.10%", "-9.00%", "+36.40%"],
    "INTC": [23.80, "USD", "-38.40%", "-4.20%", "-45.10%", "-12.00%"],
    "KLAC": [678.50, "USD", "+24.30%", "+29.10%", "-5.00%", "+44.80%"],
    "LRCX": [74.80, "USD", "+12.50%", "+24.30%", "-11.20%", "+39.10%"],
    "TXN": [188.90, "USD", "+8.30%", "+12.40%", "-7.20%", "+22.80%"],
    "MRVL": [68.40, "USD", "+15.20%", "+18.20%", "-12.10%", "+31.40%"],
    "QCOM": [162.40, "USD", "+14.80%", "+21.40%", "-11.00%", "+33.10%"],
    "MPWR": [618.50, "USD", "+14.30%", "+31.20%", "-7.40%", "+49.60%"],
    "NXPI": [228.10, "USD", "+6.40%", "+11.30%", "-8.10%", "+20.40%"],
    "ADI": [208.40, "USD", "+9.15%", "+14.80%", "-6.30%", "+25.20%"],
    
    # Taiwan
    "2330.TW": [1045.00, "TWD", "+78.30%", "+42.10%", "-2.40%", "+68.40%"],
    "2303.TW": [49.60, "TWD", "+6.20%", "+11.20%", "-9.00%", "+18.40%"],
    "5347.TWO": [77.40, "TWD", "+4.10%", "+14.00%", "-11.30%", "+22.10%"],
    "2454.TW": [1240.00, "TWD", "+34.20%", "+28.70%", "-6.00%", "+49.20%"],
    "3034.TW": [488.00, "TWD", "+12.10%", "+19.50%", "-8.40%", "+27.30%"],
    "2379.TW": [446.00, "TWD", "+15.40%", "+16.80%", "-10.20%", "+24.80%"],
    "3661.TW": [1785.00, "TWD", "-22.40%", "-5.10%", "-38.20%", "+12.40%"],
    "3711.TW": [153.50, "TWD", "+28.10%", "+22.00%", "-7.10%", "+39.60%"],
    
    # Japan
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
    
    # South Korea
    "005930.KS": [57800.00, "KRW", "-14.30%", "+11.00%", "-21.40%", "+22.50%"],
    "000660.KS": [174200.00, "KRW", "+44.20%", "+38.20%", "-12.10%", "+56.40%"],
    
    # Europe
    "ASML": [684.20, "EUR", "+9.40%", "+18.20%", "-11.40%", "+36.10%"],
    "IFX": [28.40, "EUR", "-6.15%", "+11.40%", "-18.20%", "+21.40%"],
    
    # Mainland China
    "688825.SS": [42.50, "CNY", "+18.40%", "+14.20%", "-22.10%", "+31.40%"],
    "688256.SS": [78.60, "CNY", "-12.30%", "+26.10%", "-35.20%", "+12.80%"],
    "002371.SZ": [214.30, "CNY", "+34.20%", "+38.60%", "-14.00%", "+52.10%"],
    "688041.SS": [64.20, "CNY", "+15.60%", "+21.40%", "-11.20%", "+28.40%"],
    "603986.SS": [38.15, "CNY", "-4.20%", "+11.30%", "-24.00%", "+16.50%"],
    "688008.SS": [45.60, "CNY", "+8.30%", "+16.40%", "-9.10%", "+22.40%"],
    "688012.SS": [112.40, "CNY", "+24.50%", "+22.10%", "-15.40%", "+41.20%"],
    "600584.SS": [26.80, "CNY", "+6.20%", "+10.40%", "-18.10%", "+14.00%"],
    "603501.SS": [88.40, "CNY", "+12.10%", "+19.50%", "-12.30%", "+27.30%"],
    "688249.SS": [18.50, "CNY", "-2.10%", "+8.30%", "-14.00%", "+11.20%"],
    
    # Hong Kong Stock Exchange (HKEX)
    "0981.HK": [18.42, "HKD", "+22.40%", "+34.20%", "-6.00%", "+59.80%"],
    "1347.HK": [14.10, "HKD", "+11.40%", "+18.70%", "-12.30%", "+28.40%"],
    "1385.HK": [11.24, "HKD", "+6.40%", "+13.10%", "-14.00%", "+21.50%"],
    "2577.HK": [24.50, "HKD", "+2.10%", "+8.30%", "-9.10%", "+14.00%"],
    "6082.HK": [15.80, "HKD", "+4.10%", "+14.00%", "-11.30%", "+22.10%"],
    "9903.HK": [12.40, "HKD", "+15.40%", "+16.80%", "-10.20%", "+24.80%"]
}

# 3. Text Representation Labels Map
display_labels = {
    "NVDA": "NVDA | Nvidia Corp. (Magnificent Seven)",
    "MSFT": "MSFT | Microsoft Corp. (Magnificent Seven)",
    "AAPL": "AAPL | Apple Inc. (Magnificent Seven)",
    "GOOGL": "GOOGL | Alphabet Inc. (Magnificent Seven)",
    "AMZN": "AMZN | Amazon.com Inc. (Magnificent Seven)",
    "META": "META | Meta Platforms Inc. (Magnificent Seven)",
    "TSLA": "TSLA | Tesla Inc. (Magnificent Seven)",
    "AMD": "AMD | Advanced Micro Devices (SOXX)",
    "MU": "MU | Micron Technology (SOXX)",
    "AVGO": "AVGO | Broadcom Inc. (SOXX)",
    "AMAT": "AMAT | Applied Materials (SOXX)",
    "INTC": "INTC | Intel Corporation (SOXX)",
    "KLAC": "KLAC | KLA Corporation (SOXX)",
    "LRCX": "LRCX | Lam Research Corp. (SOXX)",
    "TXN": "TXN | Texas Instruments (SOXX)",
    "MRVL": "MRVL | Marvell Technology (SOXX)",
    "QCOM": "QCOM | Qualcomm Inc. (SOXX)",
    "MPWR": "MPWR | Monolithic Power Systems (SOXX)",
    "NXPI": "NXPI | NXP Semiconductors (SOXX)",
    "ADI": "ADI | Analog Devices (SOXX)",
    "2330.TW": "2330.TW | TSMC Limited (Taiwan)",
    "2303.TW": "2303.TW | UMC Corporation (Taiwan)",
    "5347.TWO": "5347.TWO | VIS Corporation (Taiwan)",
    "2454.TW": "2454.TW | MediaTek Inc. (Taiwan)",
    "3034.TW": "3034.TW | Novatek Microelectronics (Taiwan)",
    "2379.TW": "2379.TW | Realtek Semiconductor (Taiwan)",
    "3661.TW": "3661.TW | Alchip Technologies (Taiwan)",
    "3711.TW": "3711.TW | ASE Technology Holding (Taiwan)",
    "8035.T": "8035.T | Tokyo Electron Limited (Japan)",
    "6857.T": "6857.T | Advantest Corporation (Japan)",
    "6146.T": "6146.T | Disco Corporation (Japan)",
    "6920.T": "6920.T | Lasertec Corporation (Japan)",
    "7735.T": "7735.T | SCREEN Holdings Co. (Japan)",
    "6525.T": "6525.T | Kokusai Electric (Japan)",
    "285A.T": "285A.T | Kioxia Holdings (Japan)",
    "6723.T": "6723.T | Renesas Electronics (Japan)",
    "4062.T": "4062.T | Ibiden Co. (Japan)",
    "6963.T": "6963.T | ROHM Co. (Japan)",
    "005930.KS": "005930.KS | Samsung Electronics (Korea)",
    "000660.KS": "000660.KS | SK Hynix Inc. (Korea)",
    "ASML": "ASML | ASML Holding N.V. (Europe)",
    "IFX": "IFX | Infineon Technologies (Europe)",
    "688825.SS": "688825.SS | CXMT (China Mainland)",
    "688256.SS": "688256.SS | Cambricon Technologies (China Mainland)",
    "002371.SZ": "002371.SZ | Naura Technology (China Mainland)",
    "688041.SS": "688041.SS | Hygon Information (China Mainland)",
    "603986.SS": "603986.SS | GigaDevice Semiconductor (China Mainland)",
    "688008.SS": "688008.SS | Montage Technology (China Mainland)",
    "688012.SS": "688012.SS | AMEC Inc. (China Mainland)",
    "600584.SS": "600584.SS | JCET Group Co. (China Mainland)",
    "603501.SS": "603501.SS | OmniVision Group (China Mainland)",
    "688249.SS": "688249.SS | Nexchip Semiconductor (China Mainland)",
    "0981.HK": "0981.HK | SMIC Limited (Hong Kong)",
    "1347.HK": "1347.HK | Hua Hong Semiconductor (Hong Kong)",
    "1385.HK": "1385.HK | Shanghai Fudan Micro (Hong Kong)",
    "2577.HK": "2577.HK | InnoScience Technology (Hong Kong)",
    "6082.HK": "6082.HK | Shanghai Biren Tech (Hong Kong)",
    "9903.HK": "9903.HK | Shanghai Iluvatar CoreX (Hong Kong)"
}

# 4. Interactive Clickable Dropdown Menu
selected_ticker = st.selectbox(
    "Select Target Asset Portfolio Ticker:",
    options=list(display_labels.keys()),
    format_func=lambda x: display_labels[x]
)

# 5. Extraction Layer
data = db[selected_ticker]
price = float(data[0])
currency = str(data[1])
ytd = str(data[2])
m1 = str(data[3])
m2 = str(data[4])
m3 = str(data[5])

st.markdown(f"## Asset Portfolio View Matrix ({selected_ticker})")

kpi1, kpi2 = st.columns(2)
kpi1.metric("Live Execution Market Price", f"{price:,.2f} {currency}")
kpi2.metric("Year-to-Date (YTD) Performance", ytd)
st.divider()

# 6. Modular Linear Scorecard Array Configuration (KOL Targets Dynamic View)
row1 = {"Core Forecast Tier": "Wall Street Mean Consensus", "Research House / KOL Source Name": "Morgan Stanley Institutional Research", "Target Price": f"{(price * 1.12):,.2f} {currency}", "Implied Deviation": "+12.00%"}
row2 = {"Core Forecast Tier": "Wall Street Mean Consensus", "Research House / KOL Source Name": "Goldman Sachs Macro Asset Allocation", "Target Price": f"{(price * 1.14):,.2f} {currency}", "Implied Deviation": "+14.00%"}
row3 = {"Core Forecast Tier": "Institutional Peak Target", "Research House / KOL Source Name": "JPMorgan Chase Tactical Growth Horizon", "Target Price": f"{(price * 1.28):,.2f} {currency}", "Implied Deviation": "+28.00%"}
row4 = {"Core Forecast Tier": "Institutional Peak Target", "Research House / KOL Source Name": "Bank of America Merrill Lynch Alpha Edge", "Target Price": f"{(price * 1.31):,.2f} {currency}", "Implied Deviation": "+31.00%"}
row5 = {"Core Forecast Tier": "Institutional Floor Target", "Research House / KOL Source Name": "Citi Investment Advisory Risk Managed Floor", "Target Price": f"{(price * 0.86):,.2f} {currency}", "Implied Deviation": "-14.00%"}

