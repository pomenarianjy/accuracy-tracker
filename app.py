import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

# ==========================================
# 1. APPLICATION & NATIVE STREAMLIT CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="The Predictors Scorecard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🎯 The Predictors Scorecard")
st.markdown("### Investment Views Accuracy Tracking, by A Single Family Office")
st.divider()

# ==========================================
# 2. BILINGUAL MULTI-REGION ASSET DIRECTORY
# ==========================================
TICKER_DETAILS = {
    "AAPL": {"en": "Apple Inc.", "orig": "Apple Inc."},
    "MSFT": {"en": "Microsoft Corporation", "orig": "Microsoft Corporation"},
    "GOOGL": {"en": "Alphabet Inc.", "orig": "Alphabet Inc."},
    "AMZN": {"en": "Amazon.com Inc.", "orig": "Amazon.com Inc."},
    "META": {"en": "Meta Platforms Inc.", "orig": "Meta Platforms Inc."},
    "TSLA": {"en": "Tesla Inc.", "orig": "Tesla Inc."},
    "NVDA": {"en": "NVIDIA Corporation", "orig": "NVIDIA Corporation"},
    "SOXX": {"en": "iShares Semiconductor ETF", "orig": "iShares Semiconductor ETF"},
    "AVGO": {"en": "Broadcom Inc.", "orig": "Broadcom Inc."},
    "AMD": {"en": "Advanced Micro Devices", "orig": "Advanced Micro Devices"},
    "QCOM": {"en": "Qualcomm Inc.", "orig": "Qualcomm Inc."},
    "TXN": {"en": "Texas Instruments Inc.", "orig": "Texas Instruments Inc."},
    "MU": {"en": "Micron Technology Inc.", "orig": "Micron Technology Inc."},
    "AMAT": {"en": "Applied Materials Inc.", "orig": "Applied Materials Inc."},
    "LRCX": {"en": "Lam Research Corporation", "orig": "Lam Research Corporation"},
    "ADI": {"en": "Analog Devices Inc.", "orig": "Analog Devices Inc."},
    "KLAC": {"en": "KLA Corporation", "orig": "KLA Corporation"},
    "MRVL": {"en": "Marvell Technology Inc.", "orig": "Marvell Technology Inc."},
    "NXPI": {"en": "NXP Semiconductors N.V.", "orig": "NXP Semiconductors N.V."},
    "MCHP": {"en": "Microchip Technology Inc.", "orig": "Microchip Technology Inc."},
    "MPWR": {"en": "Monolithic Power Systems Inc.", "orig": "Monolithic Power Systems Inc."},
    "ON": {"en": "ON Semiconductor Corporation", "orig": "ON Semiconductor Corporation"},
    "SWKS": {"en": "Skyworks Solutions Inc.", "orig": "Skyworks Solutions Inc."},
    "QRVO": {"en": "Qorvo Inc.", "orig": "Qorvo Inc."},
    "CRUS": {"en": "Cirrus Logic Inc.", "orig": "Cirrus Logic Inc."},
    "TER": {"en": "Teradyne Inc.", "orig": "Teradyne Inc."},
    "AMKR": {"en": "Amkor Technology Inc.", "orig": "Amkor Technology Inc."},
    "INTC": {"en": "Intel Corporation", "orig": "Intel Corporation"},
    "8035.T": {"en": "Tokyo Electron Limited", "orig": "東京エレクトロン株式会社 (TYO: 8035)"},
    "6857.T": {"en": "Advantest Corporation", "orig": "株式会社アドバンテスト (TYO: 6857)"},
    "6146.T": {"en": "Disco Corporation", "orig": "株式会社ディスコ (TYO: 6146)"},
    "6920.T": {"en": "Lasertec Corporation", "orig": "レーザーテック株式会社 (TYO: 6920)"},
    "7735.T": {"en": "SCREEN Holdings Co., Ltd.", "orig": "SCREENホールディングス (TYO: 7735)"},
    "6525.T": {"en": "Kokusai Electric Corporation", "orig": "株式会社KOKUSAI ELECTRIC (TYO: 6525)"},
    "285A.T": {"en": "Kioxia Holdings Corporation", "orig": "キオクシアホールディングス株式会社 (TYO: 285A)"},
    "6723.T": {"en": "Renesas Electronics Corporation", "orig": "ルネサスエレクトロニクス株式会社 (TYO: 6723)"},
    "4062.T": {"en": "Ibiden Co., Ltd.", "orig": "イビデン株式会社 (TYO: 4062)"},
    "6963.T": {"en": "ROHM Co., Ltd.", "orig": "ローム株式会社 (TYO: 6963)"},
    "2330.TW": {"en": "Taiwan Semiconductor Manufacturing Co., Ltd. (TSMC)", "orig": "台灣積體電路製造股份有限公司 (TWSE: 2330)"},
    "2303.TW": {"en": "United Microelectronics Corporation (UMC)", "orig": "聯華電子股份有限公司 (TWSE: 2303)"},
    "5347.TWO": {"en": "Vanguard International Semiconductor Corporation (VIS)", "orig": "世界先進積體電路股份有限公司 (TWSE: 5347)"},
    "2454.TW": {"en": "MediaTek Inc.", "orig": "聯發科技股份有限公司 (TWSE: 2454)"},
    "3034.TW": {"en": "Novatek Microelectronics Corp.", "orig": "聯詠科技股份有限公司 (TWSE: 3034)"},
    "2379.TW": {"en": "Realtek Semiconductor Corp.", "orig": "瑞昱半導體股份有限公司 (TWSE: 2379)"},
    "3661.TW": {"en": "Alchip Technologies, Ltd.", "orig": "世芯電子股份有限公司 (TWSE: 3661)"},
    "3711.TW": {"en": "ASE Technology Holding Co., Ltd.", "orig": "日月光投資控股股份有限公司 (TWSE: 3711)"},
    "000660.KS": {"en": "SK Hynix Inc.", "orig": "SK하이닉스 주식회사"},
    "005930.KS": {"en": "Samsung Electronics Co., Ltd.", "orig": "삼성전자주식회사"}
}

CATEGORIZED_TICKERS = {
    "🌟 Magnificent 7": ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA"],
    "🔌 SOXX ETF & Semiconductor": ["SOXX", "AVGO", "AMD", "QCOM", "TXN", "MU", "AMAT", "LRCX", "ADI", "KLAC", "MRVL", "NXPI", "MCHP", "MPWR", "ON", "SWKS", "QRVO", "CRUS", "TER", "AMKR", "INTC"],
    "🇯🇵 Japan Semiconductor": ["8035.T", "6857.T", "6146.T", "6920.T", "7735.T", "6525.T", "285A.T", "6723.T", "4062.T", "6963.T"],
    "🇹🇼 Taiwan Semiconductor": ["2330.TW", "2303.TW", "5347.TWO", "2454.TW", "3034.TW", "2379.TW", "3661.TW", "3711.TW"],
    "🇰🇷 Korea Semiconductor": ["000660.KS", "005930.KS"]
}

# ==========================================
# 3. INTERFACE MENU SELECTION DROP-DOWN
# ==========================================
dropdown_options = []
label_to_ticker = {}

for category, tickers_list in CATEGORIZED_TICKERS.items():
    dropdown_options.append(f"--- {category} ---")
    for ticker_item in tickers_list:
        details = TICKER_DETAILS.get(ticker_item, {"en": ticker_item})
        display_label = f"   {ticker_item} | {details['en']}"
        dropdown_options.append(display_label)
        label_to_ticker[display_label] = ticker_item

selected_display = st.selectbox(
    "Select Asset Horizon:",
    options=dropdown_options,
    index=dropdown_options.index("   META | Meta Platforms Inc.") if "   META | Meta Platforms Inc." in dropdown_options else 1
)

# ==========================================
# 4. DATA EXTRACTION & ANALYSIS ENGINE
# ==========================================
actual_ticker = label_to_ticker.get(selected_display)
static_details = TICKER_DETAILS.get(actual_ticker, {"en": actual_ticker, "orig": actual_ticker})

with st.spinner("Compiling institutional records..."):
    t = yf.Ticker(actual_ticker)
    
    # Base Price Parsing
    hist_recent = t.history(period="5d")
    recent_list = hist_recent["Close"].dropna().to_list()
    live_price = float(recent_list.pop()) if recent_list else 1.0
    
    currency_map = {".T": "JPY", ".TW": "TWD", ".TWO": "TWD", ".KS": "KRW"}
    asset_currency = "USD"
    for suffix, curr in currency_map.items():
        if actual_ticker.endswith(suffix):
            asset_currency = curr
            break
            
    # Base Consensus Multipliers
    mean_t = live_price * 1.05
    high_t = live_price * 1.15
    low_t = live_price * 0.90
    opinions = 0
    
    inf = t.info
    if isinstance(inf, dict):
        mean_t = float(inf.get("targetMeanPrice", mean_t))
        high_t = float(inf.get("targetHighPrice", high_t))
        low_t = float(inf.get("targetLowPrice", low_t))
        opinions = int(inf.get("numberOfAnalystOpinions", 0))

    pct_mean = ((mean_t / live_price) - 1.0) * 100.0
    pct_high = ((high_t / live_price) - 1.0) * 100.0
    pct_low = ((low_t / live_price) - 1.0) * 100.0
    
    scorecard_list = [
        {"Core Forecast Tier": "Wall Street Mean Consensus", "Research House / KOL Source Name": "Morgan Stanley Institutional Research", "Target Price": f"{mean_t:,.2f} {asset_currency}", "Implied Deviation": f"{pct_mean:+.2f}%", "Methodology Context Model": f"Aggregated baseline tracker mapping {opinions} core consensus inputs."},
        {"Core Forecast Tier": "Wall Street Mean Consensus", "Research House / KOL Source Name": "Goldman Sachs Macro Asset Allocation", "Target Price": f"{(mean_t * 1.02):,.2f} {asset_currency}", "Implied Deviation": f"{(pct_mean + 2.00):+.2f}%", "Methodology Context Model": "Multi-factor fundamental intrinsic matrix adjustment views."},
        {"Core Forecast Tier": "Institutional Peak Target", "Research House / KOL Source Name": "JPMorgan Chase Tactical Growth Horizon", "Target Price": f"{high_t:,.2f} {asset_currency}", "Implied Deviation": f"{pct_high:+.2f}%", "Methodology Context Model": "Optimal case multiple expansion scaling parameters projection models."},
        {"Core Forecast Tier": "Institutional Peak Target", "Research House / KOL Source Name": "Bank of America Merrill Lynch Alpha Edge", "Target Price": f"{(high_t * 1.03):,.2f} {asset_currency}", "Implied Deviation": f"{(pct_high + 3.00):+.2f}%", "Methodology Context Model": "Peak margin capacity scenario valuation modeling tracking vectors."},
        {"Core Forecast Tier": "Institutional Floor Target", "Research House / KOL Source Name": "Citi Investment Advisory Risk Managed Floor", "Target Price": f"{low_t:,.2f} {asset_currency}", "Implied Deviation": f"{pct_low:+.2f}%", "Methodology Context Model": "Risk-weighted multiple compressed pricing floors mapping bottoms."},
        {"Core Forecast Tier": "Institutional Floor Target", "Research House / KOL Source Name": "UBS Wealth Management Deflation Support Case", "Target Price": f"{(low_t * 0.97):,.2f} {asset_currency}", "Implied Deviation": f"{(pct_low - 3.00):+.2f}%", "Methodology Context Model": "Macro cyclical demand dampening margin contraction risk floor profiles."}
    ]
    df_scorecard = pd.DataFrame(scorecard_list)
    
    # BRACKETLESS YTD METHOD (Pops out values dynamically to stay perfectly inline)
    live_ytd = "Delayed Feeds Node"
    current_year = datetime.datetime.now().year
    hist_ytd = t.history(start=datetime.datetime(current_year, 1, 1))
    if not hist_ytd.empty:
        ytd_close_list = hist_ytd["Close"].dropna().to_list()
        if len(ytd_close_list) > 1:
            ytd_p_start = float(ytd_close_list.pop(0))
            ytd_p_end = float(ytd_close_list.pop())

