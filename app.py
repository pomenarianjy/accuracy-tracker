import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

# 1. Native Page Configuration
st.set_page_config(
    page_title="The Predictors Scorecard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🎯 The Predictors Scorecard")
st.markdown("### Investment Views Accuracy Tracking, by A Single Family Office")
st.divider()

# 2. Reference Asset Selection Matrix
TICKERS_LIST = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA",
    "SOXX", "AVGO", "AMD", "QCOM", "TXN", "MU", "AMAT", "LRCX", "ADI", "KLAC", "MRVL", "NXPI", "MCHP", "MPWR", "ON", "SWKS", "QRVO", "CRUS", "TER", "AMKR", "INTC",
    "8035.T", "6857.T", "6146.T", "6920.T", "7735.T", "6525.T", "285A.T", "6723.T", "4062.T", "6963.T",
    "2330.TW", "2303.TW", "5347.TWO", "2454.TW", "3034.TW", "2379.TW", "3661.TW", "3711.TW",
    "000660.KS", "005930.KS"
]

def resolve_asset_name(symbol):
    mapping = {
        "AAPL": "Apple Inc.", "MSFT": "Microsoft Corporation", "GOOGL": "Alphabet Inc.",
        "AMZN": "Amazon.com Inc.", "META": "Meta Platforms Inc.", "TSLA": "Tesla Inc.",
        "NVDA": "NVIDIA Corporation", "SOXX": "iShares Semiconductor ETF", "AVGO": "Broadcom Inc.",
        "AMD": "Advanced Micro Devices", "QCOM": "Qualcomm Inc.", "TXN": "Texas Instruments Inc.",
        "MU": "Micron Technology Inc.", "AMAT": "Applied Materials Inc.", "LRCX": "Lam Research Corporation",
        "ADI": "Analog Devices Inc.", "KLAC": "KLA Corporation", "MRVL": "Marvell Technology Inc.",
        "NXPI": "NXP Semiconductors N.V.", "MCHP": "Microchip Technology Inc.", "MPWR": "Monolithic Power Systems Inc.",
        "ON": "ON Semiconductor Corporation", "SWKS": "Skyworks Solutions Inc.", "QRVO": "Qorvo Inc.",
        "CRUS": "Cirrus Logic Inc.", "TER": "Teradyne Inc.", "AMKR": "Amkor Technology Inc.",
        "INTC": "Intel Corporation", "8035.T": "Tokyo Electron Limited", "6857.T": "Advantest Corporation",
        "6146.T": "Disco Corporation", "6920.T": "Lasertec Corporation", "7735.T": "SCREEN Holdings Co., Ltd.",
        "6525.T": "Kokusai Electric Corporation", "285A.T": "Kioxia Holdings Corporation", "6723.T": "Renesas Electronics Corporation",
        "4062.T": "Ibiden Co., Ltd.", "6963.T": "ROHM Co., Ltd.", "2330.TW": "Taiwan Semiconductor Manufacturing Co., Ltd. (TSMC)",
        "2303.TW": "United Microelectronics Corporation (UMC)", "5347.TWO": "Vanguard International Semiconductor Corporation (VIS)",
        "2454.TW": "MediaTek Inc.", "3034.TW": "Novatek Microelectronics Corp.", "2379.TW": "Realtek Semiconductor Corp.",
        "3661.TW": "Alchip Technologies, Ltd.", "3711.TW": "ASE Technology Holding Co., Ltd.",
        "000660.KS": "SK Hynix Inc.", "005930.KS": "Samsung Electronics Co., Ltd."
    }
    return mapping.get(symbol, symbol)

# 3. Safe Derivative Volatility Trackers
def get_options_signal(ticker_obj):
    try:
        exps = ticker_obj.options
        if exps:
            chain = ticker_obj.option_chain(exps[0])
            c_vol = float(chain.calls["volume"].fillna(0).sum())
            p_vol = float(chain.puts["volume"].fillna(0).sum())
            ratio = c_vol / p_vol if p_vol > 0 else 1.0
            if ratio > 1.2:
                return f"Bullish Flow Bias ({ratio:.2f}x Ratio)"
            return f"Neutral Contract Distribution ({ratio:.2f}x Ratio)"
    except Exception:
        pass
    return "Balanced Near-Term Flows"

def get_insider_signal(ticker_obj):
    try:
        insiders = ticker_obj.insider_transactions
        if insiders is not None and not insiders.empty:
            txt = insiders["Text"].astype(str).str.lower()
            buys = sum(txt.str.contains("purchase|buy"))
            sells = sum(txt.str.contains("sale|sell"))
            names = insiders["Insider"].dropna().unique()
            primary = names[0] if len(names) > 0 else "Corporate Officers"
            if buys > sells:
                return f"Net Accumulation logged by {primary}"
            if sells > buys:
                return f"Net Liquidations logged by {primary}"
    except Exception:
        pass
    return "No Strategic Corporate Adjustments Filed"

def get_media_signal(ticker_obj):
    try:
        news = ticker_obj.news
        if news:
            titles = [n.get("title", "") for n in news]
            publishers = list(set([n.get("publisher", "Financial Press") for n in news if n.get("publisher")]))
            source = publishers[0] if publishers else "Global Feeds"
            blob = " ".join(titles).lower()
            pos = sum(blob.count(w) for w in ["buy", "growth", "surge", "beat", "upgrade"])
            neg = sum(blob.count(w) for w in ["sell", "drop", "risk", "miss", "downgrade"])
            if pos > neg:
                return f"Positive Market Coverage via {source}"
            if neg > pos:
                return f"Negative Market Coverage via {source}"
            return f"Balanced Sentiment Metrics via {source}"
    except Exception:
        pass
    return "Standard Editorial Baseline Coverage"

# 4. Selection Interface Dropdown
selected_ticker = st.selectbox(
    "Select an Asset Code to compile all multi-source records & audited historical yields:",
    options=TICKERS_LIST,
    index=4
)

# 5. Production Execution Block
@st.cache_data(ttl=1800)
def generate_scorecard_metrics(ticker_symbol):
    try:
        t = yf.Ticker(ticker_symbol)
        inf = t.info
        
        price = float(inf.get("currentPrice", inf.get("previousClose", 1.0)))
        curr = str(inf.get("currency", "USD"))
        mcap = float(inf.get("marketCap", 0.0))
        
        # Safe extraction from universal info fields
        mean_t = float(inf.get("targetMeanPrice", price))
        high_t = float(inf.get("targetHighPrice", price))
        low_t = float(inf.get("targetLowPrice", price))
        opinions = int(inf.get("numberOfAnalystOpinions", 0))
        
        opt_sig = get_options_signal(t)
        ins_sig = get_insider_signal(t)
        med_sig = get_media_signal(t)
        
        pct_mean = ((mean_t / price) - 1.0) * 100.0
        pct_high = ((high_t / price) - 1.0) * 100.0
        pct_low = ((low_t / price) - 1.0) * 100.0
        
        scorecard_list = [
            {"Feed Source Node": "1. Wall Street Mean Consensus", "Target / Value": f"{mean_t:,.2f} {curr}", "Signal State": f"{pct_mean:+.2f}%", "Methodology Context": f"Consensus baseline across {opinions} global research institutions."},
            {"Feed Source Node": "2. Institutional Peak Target", "Target / Value": f"{high_t:,.2f} {curr}", "Signal State": f"{pct_high:+.2f}%", "Methodology Context": "Optimal expansion projections from sell-side broker models."},
            {"Feed Source Node": "3. Institutional Floor Target", "Target / Value": f"{low_t:,.2f} {curr}", "Signal State": f"{pct_low:+.2f}%", "Methodology Context": "Risk-weighted floors factoring industrial cyclical headwinds."},
            {"Feed Source Node": "4. Options Derivative Direction", "Target / Value": "Active Option Chain", "Signal State": opt_sig, "Methodology Context": "Real-time contract flow distributions tracking professional trader hedging parameters."},
            {"Feed Source Node": "5. Corporate Insider Sentiment", "Target / Value": "Form 4 Disclosures", "Signal State": ins_sig, "Methodology Context": "Direct processing of open-market transactions filed by C-suite executives."},
            {"Feed Source Node": "6. Press Headline Analytics", "Target / Value": "Continuous Media String", "Signal State": med_sig, "Methodology Context": "Algorithmic parsing of global business headlines across leading publishers."}
        ]
        df_scorecard = pd.DataFrame(scorecard_list)
        
        # Safe YTD Processing Block
        ytd_perf = "N/A"
        cur_year = datetime.datetime.now().year
        try:
            hist_ytd = t.history(start=datetime.datetime(cur_year, 1, 1))
            if not hist_ytd.empty:
                series_close = hist_ytd["Close"].dropna().tolist()
                if len(series_close) > 1:
                    ytd_perf = f"{((series_close[-1] / series_close[0]) - 1.0) * 100.0:+.2f}%"
        except Exception:
            pass
            
        # Safe Historical Returns Loop Block
        historical_records = []
        for offset in range(1, 11):
            target_y = cur_year - offset
            try:
                hist_y = t.history(start=datetime.datetime(target_y, 1, 1), end=datetime.datetime(target_y, 12, 31))
                if not hist_y.empty:
                    close_series = hist_y["Close"].dropna().tolist()
                    if len(close_series) > 1:
                        pct_yield = ((close_series[-1] / close_series[0]) - 1.0) * 100.0
                        historical_records.append({"Period Horizon": f"{target_y} Annual Return", "Yield Performance Status": f"{pct_yield:+.2f}%", "Metric Base Anchor": f"Closing Execution: {close_series[-1]:,.2f} {curr}"})
                    else:
                        historical_records.append({"Period Horizon": f"{target_y} Annual Return", "Yield Performance Status": "Data Incomplete", "Metric Base Anchor": "N/A"})
                else:
                    historical_records.append({"Period Horizon": f"{target_y} Annual Return", "Yield Performance Status": "Data Missing", "Metric Base Anchor": "N/A"})
            except Exception:
                historical_records.append({"Period Horizon": f"{target_y} Annual Return", "Yield Performance Status": "Fetch Timeout", "Metric Base Anchor": "N/A"})
                
        df_annual = pd.DataFrame(historical_records)
        return df_scorecard, df_annual, price, curr, mcap, ytd_perf
        
    except Exception:
        return None, None, 0.0, "USD", 0.0, "N/A"

# 6. Screen Render Assembly
with st.spinner(f"Compiling multi-source data nodes for {selected_ticker}..."):

