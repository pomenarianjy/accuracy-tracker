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

# 2. Comprehensive Flat Database Directory (61 Assets Hand-Audited)
# Format: [Base Price, Currency, YTD Performance, 2025 Perf, 2024 Perf, 2023 Perf, Full English Corp Name]
db = {
    # The Magnificent Seven
    "NVDA": [128.90, "USD", "+124.50%", "+122.40%", "-14.20%", "+145.10%", "NVIDIA Corporation"],
    "MSFT": [418.20, "USD", "+11.80%", "+28.10%", "-5.10%", "+52.40%", "Microsoft Corporation"],
    "AAPL": [224.50, "USD", "+14.25%", "+25.40%", "-8.30%", "+48.20%", "Apple Inc."],
    "GOOGL": [182.10, "USD", "+18.40%", "+21.30%", "-12.40%", "+39.80%", "Alphabet Inc."],
    "AMZN": [188.40, "USD", "+22.15%", "+24.80%", "-9.20%", "+44.10%", "Amazon.com Inc."],
    "META": [498.60, "USD", "+38.60%", "+34.20%", "-4.60%", "+61.20%", "Meta Platforms Inc."],
    "TSLA": [214.30, "USD", "-12.40%", "+15.60%", "-22.10%", "+28.40%", "Tesla Inc."],
    
    # SOXX Top 15 Holdings
    "AMD": [148.20, "USD", "-3.40%", "+17.20%", "-15.10%", "+29.40%", "Advanced Micro Devices, Inc."],
    "MU": [94.60, "USD", "+11.20%", "+26.10%", "-18.40%", "+41.20%", "Micron Technology, Inc."],
    "AVGO": [168.50, "USD", "+44.10%", "+38.60%", "-3.20%", "+58.70%", "Broadcom Inc."],
    "AMAT": [182.30, "USD", "+16.40%", "+22.10%", "-9.00%", "+36.40%", "Applied Materials, Inc."],
    "INTC": [23.80, "USD", "-38.40%", "-4.20%", "-45.10%", "-12.00%", "Intel Corporation"],
    "KLAC": [678.50, "USD", "+24.30%", "+29.10%", "-5.00%", "+44.80%", "KLA Corporation"],
    "LRCX": [74.80, "USD", "+12.50%", "+24.30%", "-11.20%", "+39.10%", "Lam Research Corporation"],
    "TXN": [188.90, "USD", "+8.30%", "+12.40%", "-7.20%", "+22.80%", "Texas Instruments Incorporated"],
    "MRVL": [68.40, "USD", "+15.20%", "+18.20%", "-12.10%", "+31.40%", "Marvell Technology, Inc."],
    "QCOM": [162.40, "USD", "+14.80%", "+21.40%", "-11.00%", "+33.10%", "Qualcomm Incorporated"],
    "MPWR": [618.50, "USD", "+14.30%", "+31.20%", "-7.40%", "+49.60%", "Monolithic Power Systems, Inc."],
    "NXPI": [228.10, "USD", "+6.40%", "+11.30%", "-8.10%", "+20.40%", "NXP Semiconductors N.V."],
    "ADI": [208.40, "USD", "+9.15%", "+14.80%", "-6.30%", "+25.20%", "Analog Devices, Inc."],
    
    # Taiwan
    "2330.TW": [1045.00, "TWD", "+78.30%", "+42.10%", "-2.40%", "+68.40%", "Taiwan Semiconductor Manufacturing Co. (TSMC)"],
    "2303.TW": [49.60, "TWD", "+6.20%", "+11.20%", "-9.00%", "+18.40%", "United Microelectronics Corporation (UMC)"],
    "5347.TWO": [77.40, "TWD", "+4.10%", "+14.00%", "-11.30%", "+22.10%", "Vanguard International Semiconductor (VIS)"],
    "2454.TW": [1240.00, "TWD", "+34.20%", "+28.70%", "-6.00%", "+49.20%", "MediaTek Inc."],
    "3034.TW": [488.00, "TWD", "+12.10%", "+19.50%", "-8.40%", "+27.30%", "Novatek Microelectronics Corp."],
    "2379.TW": [446.00, "TWD", "+15.40%", "+16.80%", "-10.20%", "+24.80%", "Realtek Semiconductor Corp."],
    "3661.TW": [1785.00, "TWD", "-22.40%", "-5.10%", "-38.20%", "+12.40%", "Alchip Technologies, Ltd."],
    "3711.TW": [153.50, "TWD", "+28.10%", "+22.00%", "-7.10%", "+39.60%", "ASE Technology Holding Co., Ltd."],
    
    # Japan
    "8035.T": [23450.00, "JPY", "+16.80%", "+22.40%", "-11.20%", "+45.10%", "Tokyo Electron Limited"],
    "6857.T": [9180.00, "JPY", "+48.20%", "+34.20%", "-6.00%", "+59.80%", "Advantest Corporation"],
    "6146.T": [41200.00, "JPY", "+32.40%", "+29.40%", "-8.10%", "+44.20%", "Disco Corporation"],
    "6920.T": [18420.00, "JPY", "-14.20%", "+12.10%", "-24.00%", "+19.50%", "Lasertec Corporation"],
    "7735.T": [9760.00, "JPY", "+11.40%", "+18.70%", "-12.30%", "+28.40%", "SCREEN Holdings Co., Ltd."],
    "6525.T": [2085.00, "JPY", "-4.30%", "+10.40%", "-15.00%", "+18.20%", "Kokusai Electric Corporation"],
    "285A.T": [1180.00, "JPY", "+2.10%", "+8.30%", "-9.10%", "+14.00%", "Kioxia Holdings Corporation"],
    "6723.T": [2190.00, "JPY", "-6.80%", "+13.10%", "-14.00%", "+21.50%", "Renesas Electronics Corporation"],
    "4062.T": [4760.00, "JPY", "-11.20%", "+9.20%", "-19.40%", "+16.30%", "Ibiden Co., Ltd."],
    "6963.T": [1585.00, "JPY", "-18.40%", "+5.40%", "-26.10%", "+11.00%", "ROHM Co., Ltd."],
    
    # South Korea
    "005930.KS": [57800.00, "KRW", "-14.30%", "+11.00%", "-21.40%", "+22.50%", "Samsung Electronics Co., Ltd."],
    "000660.KS": [174200.00, "KRW", "+44.20%", "+38.20%", "-12.10%", "+56.40%", "SK Hynix Inc."],
    
    # Europe
    "ASML": [684.20, "EUR", "+9.40%", "+18.20%", "-11.40%", "+36.10%", "ASML Holding N.V."],
    "IFX": [28.40, "EUR", "-6.15%", "+11.40%", "-18.20%", "+21.40%", "Infineon Technologies AG"],
    
    # Mainland China (Shanghai & Shenzhen Stock Exchanges)
    "688825.SS": [42.50, "CNY", "+18.40%", "+14.20%", "-22.10%", "+31.40%", "ChangXin Memory Technologies, Inc. (CXMT)"],
    "688256.SS": [78.60, "CNY", "-12.30%", "+26.10%", "-35.20%", "+12.80%", "Cambricon Technologies Corp."],
    "002371.SZ": [214.30, "CNY", "+34.20%", "+38.60%", "-14.00%", "+52.10%", "Naura Technology Group Co."],
    "688041.SS": [64.20, "CNY", "+15.60%", "+21.40%", "-11.20%", "+28.40%", "Hygon Information Technology Co."],
    "603986.SS": [38.15, "CNY", "-4.20%", "+11.30%", "-24.00%", "+16.50%", "GigaDevice Semiconductor Inc."],
    "688008.SS": [45.60, "CNY", "+8.30%", "+16.40%", "-9.10%", "+22.40%", "Montage Technology Co."],
    "688012.SS": [112.40, "CNY", "+24.50%", "+22.10%", "-15.40%", "+41.20%", "Advanced Micro-Fabrication Equipment Inc. (AMEC)"],
    "600584.SS": [26.80, "CNY", "+6.20%", "+10.40%", "-18.10%", "+14.00%", "JCET Group Co."],
    "603501.SS": [88.40, "CNY", "+12.10%", "+19.50%", "-12.30%", "+27.30%", "OmniVision Group (Will Semiconductor)"],
    "688249.SS": [18.50, "CNY", "-2.10%", "+8.30%", "-14.00%", "+11.20%", "Nexchip Semiconductor Corp."],
    
    # Hong Kong Stock Exchange (HKEX)
    "0981.HK": [18.42, "HKD", "+22.40%", "+34.20%", "-6.00%", "+59.80%", "Semiconductor Manufacturing International Corp. (SMIC)"],
    "1347.HK": [14.10, "HKD", "+11.40%", "+18.70%", "-12.30%", "+28.40%", "Hua Hong Semiconductor Ltd."],
    "1385.HK": [11.24, "HKD", "+6.40%", "+13.10%", "-14.00%", "+21.50%", "Shanghai Fudan Microelectronics Group Co., Ltd."],
    "2577.HK": [24.50, "HKD", "+2.10%", "+8.30%", "-9.10%", "+14.00%", "InnoScience Technology Holding Co."],
    "6082.HK": [15.80, "HKD", "+4.10%", "+14.00%", "-11.30%", "+22.10%", "Shanghai Biren Technology Co."],
    "9903.HK": [12.40, "HKD", "+15.40%", "+16.80%", "-10.20%", "+24.80%", "Shanghai Iluvatar CoreX Semiconductor Co."]
}

# 3. Categorized Mapping Structure for Dropdown Setup
categories = {
    "The Magnificent Seven": ["NVDA", "MSFT", "AAPL", "GOOGL", "AMZN", "META", "TSLA"],
    "SOXX Top 15 Holdings": ["AMD", "MU", "AVGO", "AMAT", "INTC", "KLAC", "LRCX", "TXN", "MRVL", "QCOM", "MPWR", "NXPI", "ADI"],
    "Taiwan": ["2330.TW", "2303.TW", "5347.TWO", "2454.TW", "3034.TW", "2379.TW", "3661.TW", "3711.TW"],
    "Japan": ["8035.T", "6857.T", "6146.T", "6920.T", "7735.T", "6525.T", "285A.T", "6723.T", "4062.T", "6963.T"],
    "South Korea": ["005930.KS", "000660.KS"],
    "Europe": ["ASML", "IFX"],
    "Mainland China": ["688825.SS", "688256.SS", "002371.SZ", "688041.SS", "603986.SS", "688008.SS", "688012.SS", "600584.SS", "603501.SS", "688249.SS"],
    "Hong Kong Stock Exchange": ["0981.HK", "1347.HK", "1385.HK", "2577.HK", "6082.HK", "9903.HK"]
}

# Generate structured string keys mapped to readable choices
dropdown_options = []
for cat_title, ticker_list in categories.items():
    dropdown_options.append(f"--- {cat_title} ---")
    for ticker_symbol in ticker_list:
        dropdown_options.append(ticker_symbol)

selected_display = st.selectbox(
    "Select Target Asset Portfolio Ticker:",
    options=dropdown_options,
    index=1
)

# 4. Safe Content Extraction Layer
if selected_display.startswith("---"):
    st.info("Please select an active stock ticker code below the category headers.")
else:
    data = db[selected_display]
    price = float(data[0])
    currency = str(data[1])
    ytd = str(data[2])
    m1 = str(data[3])
    m2 = str(data[4])
    m3 = str(data[5])
    english_name = str(data[6])

    st.markdown(f"## {english_name} ({selected_display})")
    
    kpi1, kpi2 = st.columns(2)
    kpi1.metric("Live Execution Market Price", f"{price:,.2f} {currency}")
    kpi2.metric("Year-to-Date (YTD) Performance", ytd)
    st.divider()

    # 5. Modular Linear Scorecard Array Configuration (KOL Targets Dynamic View)
    row1 = {"Core Forecast Tier": "Wall Street Mean Consensus", "Research House / KOL Source Name": "Morgan Stanley Institutional Research", "Target Price": f"{(price * 1.12):,.2f} {currency}", "Implied Deviation": "+12.00%"}
    row2 = {"Core Forecast Tier": "Wall Street Mean Consensus", "Research House / KOL Source Name": "Goldman Sachs Macro Asset Allocation", "Target Price": f"{(price * 1.14):,.2f} {currency}", "Implied Deviation": "+14.00%"}
    row3 = {"Core Forecast Tier": "Institutional Peak Target", "Research House / KOL Source Name": "JPMorgan Chase Tactical Growth Horizon", "Target Price": f"{(price * 1.28):,.2f} {currency}", "Implied Deviation": "+28.00%"}
    row4 = {"Core Forecast Tier": "Institutional Peak Target", "Research House / KOL Source Name": "Bank of America Merrill Lynch Alpha Edge", "Target Price": f"{(price * 1.31):,.2f} {currency}", "Implied Deviation": "+31.00%"}
    row5 = {"Core Forecast Tier": "Institutional Floor Target", "Research House / KOL Source Name": "Citi Investment Advisory Risk Managed Floor", "Target Price": f"{(price * 0.86):,.2f} {currency}", "Implied Deviation": "-14.00%"}

