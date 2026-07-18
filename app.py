import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

# 1. Clean Native Page Configuration
st.set_page_config(
    page_title="The Predictors Scorecard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Executive Title (Customised Family Office Branding)
st.title("🎯 The Predictors Scorecard")
st.markdown("### Investment Views Accuracy Tracking, by A Single Family Office")
st.divider()

# 3. Explicitly Categorised Stocks Structure with Full Names
TICKER_DETAILS = {
    # Magnificent 7
    "AAPL": {"en": "Apple Inc.", "orig": "Apple Inc.", "symbol": "AAPL"},
    "MSFT": {"en": "Microsoft Corporation", "orig": "Microsoft Corporation", "symbol": "MSFT"},
    "GOOGL": {"en": "Alphabet Inc.", "orig": "Alphabet Inc.", "symbol": "GOOGL"},
    "AMZN": {"en": "Amazon.com Inc.", "orig": "Amazon.com Inc.", "symbol": "AMZN"},
    "META": {"en": "Meta Platforms Inc.", "orig": "Meta Platforms Inc.", "symbol": "META"},
    "TSLA": {"en": "Tesla Inc.", "orig": "Tesla Inc.", "symbol": "TSLA"},
    "NVDA": {"en": "NVIDIA Corporation", "orig": "NVIDIA Corporation", "symbol": "NVDA"},
    
    # SOXX & Top Semiconductor Holdings
    "SOXX": {"en": "iShares Semiconductor ETF", "orig": "iShares Semiconductor ETF", "symbol": "SOXX"},
    "AVGO": {"en": "Broadcom Inc.", "orig": "Broadcom Inc.", "symbol": "AVGO"},
    "AMD": {"en": "Advanced Micro Devices", "orig": "Advanced Micro Devices", "symbol": "AMD"},
    "QCOM": {"en": "Qualcomm Inc.", "orig": "Qualcomm Inc.", "symbol": "QCOM"},
    "TXN": {"en": "Texas Instruments Inc.", "orig": "Texas Instruments Inc.", "symbol": "TXN"},
    "MU": {"en": "Micron Technology Inc.", "orig": "Micron Technology Inc.", "symbol": "MU"},
    "AMAT": {"en": "Applied Materials Inc.", "orig": "Applied Materials Inc.", "symbol": "AMAT"},
    "LRCX": {"en": "Lam Research Corporation", "orig": "Lam Research Corporation", "symbol": "LRCX"},
    "ADI": {"en": "Analog Devices Inc.", "orig": "Analog Devices Inc.", "symbol": "ADI"},
    "KLAC": {"en": "KLA Corporation", "orig": "KLA Corporation", "symbol": "KLAC"},
    "MRVL": {"en": "Marvell Technology Inc.", "orig": "Marvell Technology Inc.", "symbol": "MRVL"},
    "NXPI": {"en": "NXP Semiconductors N.V.", "orig": "NXP Semiconductors N.V.", "symbol": "NXPI"},
    "MCHP": {"en": "Microchip Technology Inc.", "orig": "Microchip Technology Inc.", "symbol": "MCHP"},
    "MPWR": {"en": "Monolithic Power Systems Inc.", "orig": "Monolithic Power Systems Inc.", "symbol": "MPWR"},
    "ON": {"en": "ON Semiconductor Corporation", "orig": "ON Semiconductor Corporation", "symbol": "ON"},
    "SWKS": {"en": "Skyworks Solutions Inc.", "orig": "Skyworks Solutions Inc.", "symbol": "SWKS"},
    "QRVO": {"en": "Qorvo Inc.", "orig": "Qorvo Inc.", "symbol": "QRVO"},
    "CRUS": {"en": "Cirrus Logic Inc.", "orig": "Cirrus Logic Inc.", "symbol": "CRUS"},
    "TER": {"en": "Teradyne Inc.", "orig": "Teradyne Inc.", "symbol": "TER"},
    "AMKR": {"en": "Amkor Technology Inc.", "orig": "Amkor Technology Inc.", "symbol": "AMKR"},
    "INTC": {"en": "Intel Corporation", "orig": "Intel Corporation", "symbol": "INTC"},
    
    # Japan Semiconductor Leaders
    "8035.T": {"en": "Tokyo Electron Limited", "orig": "東京エレクトロン株式会社 (TYO: 8035)", "symbol": "8035.T"},
    "6857.T": {"en": "Advantest Corporation", "orig": "株式会社アドバンテスト (TYO: 6857)", "symbol": "6857.T"},
    "6146.T": {"en": "Disco Corporation", "orig": "株式会社ディスコ (TYO: 6146)", "symbol": "6146.T"},
    "6920.T": {"en": "Lasertec Corporation", "orig": "レーザーテック株式会社 (TYO: 6920)", "symbol": "6920.T"},
    "7735.T": {"en": "SCREEN Holdings Co., Ltd.", "orig": "SCREENホールディングス (TYO: 7735)", "symbol": "7735.T"},
    "6525.T": {"en": "Kokusai Electric Corporation", "orig": "株式会社KOKUSAI ELECTRIC (TYO: 6525)", "symbol": "6525.T"},
    "285A.T": {"en": "Kioxia Holdings Corporation", "orig": "キオクシアホールディングス株式会社 (TYO: 285A)", "symbol": "285A.T"},
    "6723.T": {"en": "Renesas Electronics Corporation", "orig": "ルネサスエレクトロニクス株式会社 (TYO: 6723)", "symbol": "6723.T"},
    "4062.T": {"en": "Ibiden Co., Ltd.", "orig": "イビデン株式会社 (TYO: 4062)", "symbol": "4062.T"},
    "6963.T": {"en": "ROHM Co., Ltd.", "orig": "ローム株式会社 (TYO: 6963)", "symbol": "6963.T"},
    
    # Taiwan Semiconductor Leaders
    "2330.TW": {"en": "Taiwan Semiconductor Manufacturing Co., Ltd. (TSMC)", "orig": "台灣積體電路製造股份有限公司 (TWSE: 2330 / NYSE: TSM)", "symbol": "2330.TW"},
    "2303.TW": {"en": "United Microelectronics Corporation (UMC)", "orig": "聯華電子股份有限公司 (TWSE: 2303 / NYSE: UMC)", "symbol": "2303.TW"},
    "5347.TWO": {"en": "Vanguard International Semiconductor Corporation (VIS)", "orig": "世界先進積體電路股份有限公司 (TWSE: 5347)", "symbol": "5347.TWO"},
    "2454.TW": {"en": "MediaTek Inc.", "orig": "聯發科技股份有限公司 (TWSE: 2454)", "symbol": "2454.TW"},
    "3034.TW": {"en": "Novatek Microelectronics Corp.", "orig": "聯詠科技股份有限公司 (TWSE: 3034)", "symbol": "3034.TW"},
    "2379.TW": {"en": "Realtek Semiconductor Corp.", "orig": "瑞昱半導體股份有限公司 (TWSE: 2379)", "symbol": "2379.TW"},
    "3661.TW": {"en": "Alchip Technologies, Ltd.", "orig": "世芯電子股份有限公司 (TWSE: 3661)", "symbol": "3661.TW"},
    "3711.TW": {"en": "ASE Technology Holding Co., Ltd.", "orig": "日月光投資控股股份有限公司 (TWSE: 3711 / NYSE: ASX)", "symbol": "3711.TW"},
    
    # Korea Semiconductor Leaders
    "000660.KS": {"en": "SK Hynix Inc.", "orig": "SK하이닉스 주식회사", "symbol": "000660.KS"},
    "005930.KS": {"en": "Samsung Electronics Co., Ltd.", "orig": "삼성전자주식회사", "symbol": "005930.KS"}
}

CATEGORIZED_TICKERS = {
    "🌟 Magnificent 7": ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA"],
    "🔌 SOXX ETF & Top Semiconductor Holdings": ["SOXX", "AVGO", "AMD", "QCOM", "TXN", "MU", "AMAT", "LRCX", "ADI", "KLAC", "MRVL", "NXPI", "MCHP", "MPWR", "ON", "SWKS", "QRVO", "CRUS", "TER", "AMKR", "INTC"],
    "🇯🇵 Japan Semiconductor Leaders": ["8035.T", "6857.T", "6146.T", "6920.T", "7735.T", "6525.T", "285A.T", "6723.T", "4062.T", "6963.T"],
    "🇹🇼 Taiwan Semiconductor Leaders": ["2330.TW", "2303.TW", "5347.TWO", "2454.TW", "3034.TW", "2379.TW", "3661.TW", "3711.TW"],
    "🇰🇷 Korea Semiconductor Leaders": ["000660.KS", "005930.KS"]
}

# Helper Functions for Data Streams
def get_options_signal(ticker_obj):
    try:
        expirations = ticker_obj.options
        if expirations:
            opt_chain = ticker_obj.option_chain(expirations[0])
            calls_vol = opt_chain.calls['volume'].sum()
            puts_vol = opt_chain.puts['volume'].sum()
            ratio = calls_vol / puts_vol if puts_vol > 0 else 1.0
            return f"Bullish (Ratio: {ratio:.2f}x)" if ratio > 1.2 else f"Bearish/Neutral (Ratio: {ratio:.2f}x)"
    except:
        pass
    return "Neutral / Data Stream Delayed"

def get_insider_signal(ticker_obj):
    try:
        insiders = ticker_obj.insider_transactions
        if insiders is not None and not insiders.empty:
            text_col = insiders['Text'].astype(str).str.lower()
            buy_count = sum(text_col.str.contains('purchase'))
            sell_count = sum(text_col.str.contains('sale'))
            if buy_count > sell_count:
                return f"Net Buying Accumulation (+{buy_count} trades logged)"
            if sell_count > buy_count:
                return f"Net Selling Liquidation (-{sell_count} trades logged)"
    except:
        pass
    return "Neutral (No recent executive transactions filed)"

def get_media_signal(ticker_obj):
    try:
        news = ticker_obj.news
        if news:
            headlines = [n.get('title', '') for n in news]
            bull_words = ['buy', 'growth', 'surge', 'beat', 'upgrade', 'higher', 'positive']
            bear_words = ['sell', 'drop', 'risk', 'miss', 'downgrade', 'lower', 'negative']
            text_blob = " ".join(headlines).lower()
            b_score = sum(text_blob.count(w) for w in bull_words)
            r_score = sum(text_blob.count(w) for w in bear_words)
            if b_score > r_score:
                return f"Positive Sentiment (Score: +{b_score - r_score})"
            if r_score > b_score:
                return f"Negative Sentiment (Score: {b_score - r_score})"
    except:
        pass
    return "Neutral Media Coverage Profile"

# 5. Build Dropdown Layout Map
dropdown_options = []
label_to_ticker = {}

for category, tickers in CATEGORIZED_TICKERS.items():
    dropdown_options.append(f"--- {category} ---")
    for ticker in tickers:
        details = TICKER_DETAILS.get(ticker, {"en": ticker})
        display_label = f"   {ticker} | {details['en']}"
        dropdown_options.append(display_label)
        label_to_ticker[display_label] = ticker

selected_display = st.selectbox(
    "Select an Asset Code to compile all multi-source records & audited historical yields:",
    options=dropdown_options,
    index=dropdown_options.index("   META | Meta Platforms Inc.") if "   META | Meta Platforms Inc." in dropdown_options else 1
)

# 6. Core Multi-Source Pipeline Execution
@st.cache_data(ttl=1800)
def compile_all_sources(ticker_symbol):
    try:
        t = yf.Ticker(ticker_symbol)
        info = t.info
        current_price = float(info.get('currentPrice', info.get('previousClose', 1.0)))
        currency = str(info.get('currency', 'USD'))
        market_cap = float(info.get('marketCap', 0.0))
        
        targets = t.analyst_price_targets
        mean_t = float(targets.get('mean', current_price))
        high_t = float(targets.get('high', current_price))
        low_t = float(targets.get('low', current_price))
        num_opinions = int(info.get('numberOfAnalystOpinions', 0))
        
        opt_signal = get_options_signal(t)
        insider_signal = get_insider_signal(t)
        media_signal = get_media_signal(t)

        scorecard_rows = [
            ["1. Wall Street Consensus (Mean Target)", f"{mean_t:,.2f} {currency}", f"{((mean_t/current_price)-1)*100:+.2f}%", f"Aggregated baseline target from {num_opinions} registered research institutions."],
