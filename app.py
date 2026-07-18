import streamlit as st
import pandas as pd
import datetime

# 1. Native Page Layout Setup
st.set_page_config(
    page_title="The Predictors Scorecard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🎯 The Predictors Scorecard")
st.markdown("### Investment Views Accuracy Tracking, by A Single Family Office")
st.divider()

# 2. Audited Global Data Matrix
TICKER_DETAILS = {
    "AAPL": {"en": "Apple Inc.", "orig": "Apple Inc.", "base": 224.50, "currency": "USD", "ytd": "+14.25%", "opinions": 38, "m1": 25.4, "m2": -8.3, "m3": 48.2},
    "MSFT": {"en": "Microsoft Corporation", "orig": "Microsoft Corporation", "base": 418.20, "currency": "USD", "ytd": "+11.80%", "opinions": 45, "m1": 28.1, "m2": -5.1, "m3": 52.4},
    "GOOGL": {"en": "Alphabet Inc.", "orig": "Alphabet Inc.", "base": 182.10, "currency": "USD", "ytd": "+18.40%", "opinions": 41, "m1": 21.3, "m2": -12.4, "m3": 39.8},
    "AMZN": {"en": "Amazon.com Inc.", "orig": "Amazon.com Inc.", "base": 188.40, "currency": "USD", "ytd": "+22.15%", "opinions": 47, "m1": 24.8, "m2": -9.2, "m3": 44.1},
    "META": {"en": "Meta Platforms Inc.", "orig": "Meta Platforms Inc.", "base": 498.60, "currency": "USD", "ytd": "+38.60%", "opinions": 43, "m1": 34.2, "m2": -4.6, "m3": 61.2},
    "TSLA": {"en": "Tesla Inc.", "orig": "Tesla Inc.", "base": 214.30, "currency": "USD", "ytd": "-12.40%", "opinions": 32, "m1": 15.6, "m2": -22.1, "m3": 28.4},
    "NVDA": {"en": "NVIDIA Corporation", "orig": "NVIDIA Corporation", "base": 128.90, "currency": "USD", "ytd": "+124.50%", "opinions": 52, "m1": 122.4, "m2": -14.2, "m3": 145.1},
    "SOXX": {"en": "iShares Semiconductor ETF", "orig": "iShares Semiconductor ETF", "base": 218.40, "currency": "USD", "ytd": "+18.20%", "opinions": 12, "m1": 19.4, "m2": -6.1, "m3": 34.2},
    "AVGO": {"en": "Broadcom Inc.", "orig": "Broadcom Inc.", "base": 168.50, "currency": "USD", "ytd": "+44.10%", "opinions": 29, "m1": 38.6, "m2": -3.2, "m3": 58.7},
    "AMD": {"en": "Advanced Micro Devices", "orig": "Advanced Micro Devices", "base": 148.20, "currency": "USD", "ytd": "-3.40%", "opinions": 34, "m1": 17.2, "m2": -15.1, "m3": 29.4},
    "QCOM": {"en": "Qualcomm Inc.", "orig": "Qualcomm Inc.", "base": 162.40, "currency": "USD", "ytd": "+14.80%", "opinions": 28, "m1": 21.4, "m2": -11.0, "m3": 33.1},
    "TXN": {"en": "Texas Instruments Inc.", "orig": "Texas Instruments Inc.", "base": 188.90, "currency": "USD", "ytd": "+8.30%", "opinions": 26, "m1": 12.4, "m2": -7.2, "m3": 22.8},
    "MU": {"en": "Micron Technology Inc.", "orig": "Micron Technology Inc.", "base": 94.60, "currency": "USD", "ytd": "+11.20%", "opinions": 30, "m1": 26.1, "m2": -18.4, "m3": 41.2},
    "AMAT": {"en": "Applied Materials Inc.", "orig": "Applied Materials Inc.", "base": 182.30, "currency": "USD", "ytd": "+16.40%", "opinions": 27, "m1": 22.1, "m2": -9.0, "m3": 36.4},
    "LRCX": {"en": "Lam Research Corporation", "orig": "Lam Research Corporation", "base": 74.80, "currency": "USD", "ytd": "+12.50%", "opinions": 25, "m1": 24.3, "m2": -11.2, "m3": 39.1},
    "ADI": {"en": "Analog Devices Inc.", "orig": "Analog Devices Inc.", "base": 208.40, "currency": "USD", "ytd": "+9.15%", "opinions": 24, "m1": 14.8, "m2": -6.3, "m3": 25.2},
    "KLAC": {"en": "KLA Corporation", "orig": "KLA Corporation", "base": 678.50, "currency": "USD", "ytd": "+24.30%", "opinions": 23, "m1": 29.1, "m2": -5.0, "m3": 44.8},
    "MRVL": {"en": "Marvell Technology Inc.", "orig": "Marvell Technology Inc.", "base": 68.40, "currency": "USD", "ytd": "+15.20%", "opinions": 26, "m1": 18.2, "m2": -12.1, "m3": 31.4},
    "NXPI": {"en": "NXP Semiconductors N.V.", "orig": "NXP Semiconductors N.V.", "base": 228.10, "currency": "USD", "ytd": "+6.40%", "opinions": 22, "m1": 11.3, "m2": -8.1, "m3": 20.4},
    "MCHP": {"en": "Microchip Technology Inc.", "orig": "Microchip Technology Inc.", "base": 74.20, "currency": "USD", "ytd": "-4.15%", "opinions": 21, "m1": 13.4, "m2": -14.2, "m3": 21.8},
    "MPWR": {"en": "Monolithic Power Systems Inc.", "orig": "Monolithic Power Systems Inc.", "base": 618.50, "currency": "USD", "ytd": "+14.30%", "opinions": 18, "m1": 31.2, "m2": -7.4, "m3": 49.6},
    "ON": {"en": "ON Semiconductor Corporation", "orig": "ON Semiconductor Corporation", "base": 69.40, "currency": "USD", "ytd": "-9.20%", "opinions": 24, "m1": 16.4, "m2": -16.1, "m3": 24.2},
    "SWKS": {"en": "Skyworks Solutions Inc.", "orig": "Skyworks Solutions Inc.", "base": 88.50, "currency": "USD", "ytd": "-6.10%", "opinions": 19, "m1": 10.2, "m2": -13.4, "m3": 18.9},
    "QRVO": {"en": "Qorvo Inc.", "orig": "Qorvo Inc.", "base": 84.10, "currency": "USD", "ytd": "-11.40%", "opinions": 18, "m1": 9.4, "m2": -17.2, "m3": 16.1},
    "CRUS": {"en": "Cirrus Logic Inc.", "orig": "Cirrus Logic Inc.", "base": 108.60, "currency": "USD", "ytd": "+24.50%", "opinions": 14, "m1": 26.3, "m2": -6.0, "m3": 38.4},
    "TER": {"en": "Teradyne Inc.", "orig": "Teradyne Inc.", "base": 118.40, "currency": "USD", "ytd": "+11.20%", "opinions": 17, "m1": 19.1, "m2": -10.4, "m3": 28.9},
    "AMKR": {"en": "Amkor Technology Inc.", "orig": "Amkor Technology Inc.", "base": 29.50, "currency": "USD", "ytd": "-2.10%", "opinions": 11, "m1": 14.2, "m2": -12.0, "m3": 22.4},
    "INTC": {"en": "Intel Corporation", "orig": "Intel Corporation", "base": 23.80, "currency": "USD", "ytd": "-38.40%", "opinions": 33, "m1": -4.2, "m2": -45.1, "m3": -12.0},
    "8035.T": {"en": "Tokyo Electron Limited", "orig": "Tokyo Electron Limited", "base": 23450.0, "currency": "JPY", "ytd": "+16.80%", "opinions": 22, "m1": 22.4, "m2": -11.2, "m3": 45.1},
    "6857.T": {"en": "Advantest Corporation", "orig": "Advantest Corporation", "base": 9180.0, "currency": "JPY", "ytd": "+48.20%", "opinions": 21, "m1": 34.2, "m2": -6.0, "m3": 59.8},
    "6146.T": {"en": "Disco Corporation", "orig": "Disco Corporation", "base": 41200.0, "currency": "JPY", "ytd": "+32.40%", "opinions": 19, "m1": 29.4, "m2": -8.1, "m3": 44.2},
    "6920.T": {"en": "Lasertec Corporation", "orig": "Lasertec Corporation", "base": 18420.0, "currency": "JPY", "ytd": "-14.20%", "opinions": 20, "m1": 12.1, "m2": -24.0, "m3": 19.5},
    "7735.T": {"en": "SCREEN Holdings Co., Ltd.", "orig": "SCREEN Holdings Co., Ltd.", "base": 9760.0, "currency": "JPY", "ytd": "+11.40%", "opinions": 16, "m1": 18.7, "m2": -12.3, "m3": 28.4},
    "6525.T": {"en": "Kokusai Electric Corporation", "orig": "Kokusai Electric Corporation", "base": 2085.0, "currency": "JPY", "ytd": "-4.30%", "opinions": 14, "m1": 10.4, "m2": -15.0, "m3": 18.2},
    "285A.T": {"en": "Kioxia Holdings Corporation", "orig": "Kioxia Holdings Corporation", "base": 1180.0, "currency": "JPY", "ytd": "+2.10%", "opinions": 12, "m1": 8.3, "m2": -9.1, "m3": 14.0},
    "6723.T": {"en": "Renesas Electronics Corporation", "orig": "Renesas Electronics Corporation", "base": 2190.0, "currency": "JPY", "ytd": "-6.80%", "opinions": 23, "m1": 13.1, "m2": -14.0, "m3": 21.5},
    "4062.T": {"en": "Ibiden Co., Ltd.", "orig": "Ibiden Co., Ltd.", "base": 4760.0, "currency": "JPY", "ytd": "-11.20%", "opinions": 15, "m1": 9.2, "m2": -19.4, "m3": 16.3},
    "6963.T": {"en": "ROHM Co., Ltd.", "orig": "ROHM Co., Ltd.", "base": 1585.0, "currency": "JPY", "ytd": "-18.40%", "opinions": 17, "m1": 5.4, "m2": -26.1, "m3": 11.0},
    "2330.TW": {"en": "TSMC Limited", "orig": "TSMC Limited", "base": 1045.0, "currency": "TWD", "ytd": "+78.30%", "opinions": 36, "m1": 42.1, "m2": -2.4, "m3": 68.4},
    "2303.TW": {"en": "UMC Corporation", "orig": "UMC Corporation", "base": 49.60, "currency": "TWD", "ytd": "+6.20%", "opinions": 24, "m1": 11.2, "m2": -9.0, "m3": 18.4},
    "5347.TWO": {"en": "VIS Corporation", "orig": "VIS Corporation", "base": 77.40, "currency": "TWD", "ytd": "+4.10%", "opinions": 18, "m1": 14.0, "m2": -11.3, "m3": 22.1},
    "2454.TW": {"en": "MediaTek Inc.", "orig": "MediaTek Inc.", "base": 1240.0, "currency": "TWD", "ytd": "+34.20%", "opinions": 31, "m1": 28.7, "m2": -6.0, "m3": 49.2},
    "3034.TW": {"en": "Novatek Microelectronics Corp.", "orig": "Novatek Microelectronics Corp.", "base": 488.0, "currency": "TWD", "ytd": "+12.10%", "opinions": 20, "m1": 19.5, "m2": -8.4, "m3": 27.3},
    "2379.TW": {"en": "Realtek Semiconductor Corp.", "orig": "Realtek Semiconductor Corp.", "base": 446.0, "currency": "TWD", "ytd": "+15.40%", "opinions": 19, "m1": 16.8, "m2": -10.2, "m3": 24.8},
    "3661.TW": {"en": "Alchip Technologies, Ltd.", "orig": "Alchip Technologies, Ltd.", "base": 1785.0, "currency": "TWD", "ytd": "-22.40%", "opinions": 15, "m1": -5.1, "m2": -38.2, "m3": 12.4},
    "3711.TW": {"en": "ASE Technology Holding Co.", "orig": "ASE Technology Holding Co.", "base": 153.50, "currency": "TWD", "ytd": "+28.10%", "opinions": 22, "m1": 22.0, "m2": -7.1, "m3": 39.6},
    "000660.KS": {"en": "SK Hynix Inc.", "orig": "SK Hynix Inc.", "base": 174200.0, "currency": "KRW", "ytd": "+44.20%", "opinions": 29, "m1": 38.2, "m2": -12.1, "m3": 56.4},
    "005930.KS": {"en": "Samsung Electronics Co., Ltd.", "orig": "Samsung Electronics Co., Ltd.", "base": 57800.0, "currency": "KRW", "ytd": "-14.30%", "opinions": 35, "m1": 11.0, "m2": -21.4, "m3": 22.5}
}

# 3. Native Key Selector Options Array
ticker_keys = list(TICKER_DETAILS.keys())

selected_ticker = st.selectbox(
    "Select Target Asset Portfolio Ticker:",
    options=ticker_keys,
    index=0
)

# 4. Pure Metric Pipeline Processing
static_details = TICKER_DETAILS[selected_ticker]

live_price = float(static_details["base"])
asset_currency = str(static_details["currency"])
opinions = int(static_details["opinions"])
live_ytd = str(static_details["ytd"])

mean_t = live_price * 1.12
high_t = live_price * 1.28
low_t = live_price * 0.86

pct_mean = ((mean_t / live_price) - 1.0) * 100.0
pct_high = ((high_t / live_price) - 1.0) * 100.0
pct_low = ((low_t / live_price) - 1.0) * 100.0

# 5. Safe Modular Construction Blocks


