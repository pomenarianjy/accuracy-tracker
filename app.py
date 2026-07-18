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
# 2. BILINGUAL MULTI-REGION ASSET MATRIX DIRECTORY
# ==========================================
TICKER_DETAILS = {
    # Magnificent 7
    "AAPL": {"en": "Apple Inc.", "orig": "Apple Inc."},
    "MSFT": {"en": "Microsoft Corporation", "orig": "Microsoft Corporation"},
    "GOOGL": {"en": "Alphabet Inc.", "orig": "Alphabet Inc."},
    "AMZN": {"en": "Amazon.com Inc.", "orig": "Amazon.com Inc."},
    "META": {"en": "Meta Platforms Inc.", "orig": "Meta Platforms Inc."},
    "TSLA": {"en": "Tesla Inc.", "orig": "Tesla Inc."},
    "NVDA": {"en": "NVIDIA Corporation", "orig": "NVIDIA Corporation"},
    
    # SOXX & Top Semiconductor Holdings
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
    
    # Japan Semiconductor Leaders
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
    
    # Taiwan Semiconductor Leaders
    "2330.TW": {"en": "Taiwan Semiconductor Manufacturing Co., Ltd. (TSMC)", "orig": "台灣積體電路製造股份有限公司 (TWSE: 2330)"},
    "2303.TW": {"en": "United Microelectronics Corporation (UMC)", "orig": "聯華電子股份有限公司 (TWSE: 2303)"},
    "5347.TWO": {"en": "Vanguard International Semiconductor Corporation (VIS)", "orig": "世界先進積體電路股份有限公司 (TWSE: 5347)"},
    "2454.TW": {"en": "MediaTek Inc.", "orig": "聯發科技股份有限公司 (TWSE: 2454)"},
    "3034.TW": {"en": "Novatek Microelectronics Corp.", "orig": "聯詠科技股份有限公司 (TWSE: 3034)"},
    "2379.TW": {"en": "Realtek Semiconductor Corp.", "orig": "瑞昱半導體股份有限公司 (TWSE: 2379)"},
    "3661.TW": {"en": "Alchip Technologies, Ltd.", "orig": "世芯電子股份有限公司 (TWSE: 3661)"},
    "3711.TW": {"en": "ASE Technology Holding Co., Ltd.", "orig": "日月光投資控股股份有限公司 (TWSE: 3711)"},
    
    # Korea Semiconductor Leaders
    "000660.KS": {"en": "SK Hynix Inc.", "orig": "SK하이닉스 주식회사"},
    "005930.KS": {"en": "Samsung Electronics Co., Ltd.", "orig": "삼성전자주식회사"}
}

CATEGORIZED_TICKERS = {
    "🌟 Magnificent 7": ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA"],
    "🔌 SOXX ETF & Top Semiconductor Holdings": ["SOXX", "AVGO", "AMD", "QCOM", "TXN", "MU", "AMAT", "LRCX", "ADI", "KLAC", "MRVL", "NXPI", "MCHP", "MPWR", "ON", "SWKS", "QRVO", "CRUS", "TER", "AMKR", "INTC"],
    "🇯🇵 Japan Semiconductor Leaders": ["8035.T", "6857.T", "6146.T", "6920.T", "7735.T", "6525.T", "285A.T", "6723.T", "4062.T", "6963.T"],
    "🇹🇼 Taiwan Semiconductor Leaders": ["2330.TW", "2303.TW", "5347.TWO", "2454.TW", "3034.TW", "2379.TW", "3661.TW", "3711.TW"],
    "🇰🇷 Korea Semiconductor Leaders": ["000660.KS", "005930.KS"]
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
    "Select an Asset Code to compile all multi-source records & audited historical yields:",
    options=dropdown_options,
    index=dropdown_options.index("   META | Meta Platforms Inc.") if "   META | Meta Platforms Inc." in dropdown_options else 1
)

# ==========================================
# 4. FAIL-SAFE RAW API DATA EVALUATORS
# ==========================================
def get_options_signal(ticker_obj):
    try:
        exps = ticker_obj.options
        if exps:
            chain = ticker_obj.option_chain(exps[0])
            c_vol = float(chain.calls.volume.fillna(0).sum())
            p_vol = float(chain.puts.volume.fillna(0).sum())
            if c_vol == 0 and p_vol == 0:
                c_vol = float(chain.calls.openInterest.fillna(0).sum())
                p_vol = float(chain.puts.openInterest.fillna(0).sum())
            ratio = c_vol / p_vol if p_vol > 0 else 1.0
            if ratio > 1.2:
                return f"Bullish Flow Bias (Ratio: {ratio:.2f}x)"
            elif ratio < 0.8:
                return f"Bearish Flow Bias (Ratio: {ratio:.2f}x)"
            return f"Balanced Flow (Ratio: {ratio:.2f}x)"
    except Exception:
        pass
    return "Balanced Near-Term Option Flow Volume"

def get_insider_signal(ticker_obj):
    try:
        insiders = ticker_obj.insider_transactions
        if insiders is not None and not insiders.empty:
            txt = insiders.Text.astype(str).str.lower()
            buys = sum(txt.str.contains("purchase|buy|acquisition"))
            sells = sum(txt.str.contains("sale|sell|disposition"))
            names = insiders.Insider.dropna().unique()
            primary = names[0] if len(names) > 0 else "Corporate Officers"
            if buys > sells:
                return f"Net Accumulation via Form 4 filings ({primary})"
            if sells > buys:
                return f"Net Liquidation via Form 4 filings ({primary})"
    except Exception:
        pass
    return "No Strategic Executive Multi-Trades Filed"

def get_media_signal(ticker_obj):
    try:
        news = ticker_obj.news
        if news:
            titles = [n.get("title", "") for n in news]
            publishers = list(set([n.get("publisher", "Financial Press") for n in news if n.get("publisher")]))
            source = publishers[0] if publishers else "Global Feeds"
            blob = " ".join(titles).lower()
            pos = sum(blob.count(w) for w in ["buy", "growth", "surge", "beat", "upgrade", "positive"])
            neg = sum(blob.count(w) for w in ["sell", "drop", "risk", "miss", "downgrade", "negative"])
            if pos > neg:
                return f"Positive Sentiment via {source} News Feed"
            if neg > pos:
                return f"Negative Sentiment via {source} News Feed"
            return f"Balanced Market Coverage via {source}"
    except Exception:
        pass
    return "Standard Baseline Press Coverage Profiles"

# ==========================================
# 5. HIGH-STABILITY MULTI-SOURCE PIPELINE
# ==========================================
@st.cache_data(ttl=1800)
def fetch_robust_market_data(ticker_symbol):
    try:
        t = yf.Ticker(ticker_symbol)
        
        # 1. Resilient Price Discovery Engine via History Frames
        hist_recent = t.history(period="5d")
        if hist_recent.empty:
            return None, None, 0.0, "N/A", "USD", 0.0
            
        live_price = float(hist_recent.Close.iloc[-1])
        
        # 2. Currency Determination Base Mapping
        currency_map = {".T": "JPY", ".TW": "TWD", ".TWO": "TWD", ".KS": "KRW"}
        asset_currency = "USD"
        for suffix, curr in currency_map.items():
            if ticker_symbol.endswith(suffix):
                asset_currency = curr
                break
                
        # 3. Native Financial Fallbacks for info endpoints
        mcap = 0.0
        mean_t = live_price * 1.05
        high_t = live_price * 1.15
        low_t = live_price * 0.90
        opinions = 0
        
        try:
            inf = t.info

