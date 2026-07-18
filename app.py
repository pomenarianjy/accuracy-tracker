import streamlit as st
import pandas as pd

st.set_page_config(page_title="KOL & Analyst Leaderboard", layout="wide")
st.title("🎯 The Predictor Scorecard")
st.caption("Tracking the prediction accuracy of Wall Street, LinkedIn Top Voices, X Finfluencers, and Media Pundits.")

# 1. Expanded Real-World Named Mock Database
data = {
    'Predictor Name': [
        'David Kostin (Goldman Sachs)', 'Wei Li (BlackRock)', 'Marko Kolanovic (Ex-JPMorgan)',  # Institutional
        'Alfonso Peccatiello (Macro Compass)', 'Tavi Costa (Crescat)', 'Lyn Alden',             # Independent Macro
        'Matt Levine (Bloomberg)', 'David Faber (CNBC)', 'Jim Cramer (CNBC)',                  # Mainstream Media
        'Josh Brown (@Downtown)', 'Balaji Srinivasan', 'Gergely Orosz (Pragmatic Eng)'          # X / LinkedIn KOLs
    ],
    'Source / Platform': [
        'Institutional Bank', 'Institutional Bank', 'Institutional Bank',
        'LinkedIn Top Voice / Substack', 'X (Twitter) / Fund Manager', 'Independent Research',
        'Bloomberg Opinion', 'CNBC Squawk on the Street', 'CNBC Mad Money',
        'X / CNBC Halftime', 'X (Twitter)', 'LinkedIn / Newsletter'
    ],
    'Focus Sector': ['S&P 500 Equities', 'Global Allocation', 'Macro Strategy', 'Global Macro', 'Commodities/Gold', 'Macro & Crypto', 'Corporate Finance', 'M&A / Dealmaking', 'Stock Picking', 'US Equities', 'Tech & Crypto', 'Tech Industry Trends'],
    'Accuracy Rate': ['64%', '68%', '38%', '71%', '65%', '74%', '82%', '79%', '44%', '67%', '58%', '81%'],
    'Notable Last Call': [
        'S&P 500 Year-End Target @ 5,600', 'Overweight Eurozone Equities', 'Bearish on US Equities through rally',
        'Short-term Treasury Yield Drop', 'Buy Gold Mining Equities', 'Long Bitcoin structural cycle',
        'Analysis of Musk Twitter Debt restructuring', 'Predicted dynamic tech mega-merger timeline', 'Buy tech basket before minor correction',
        'Accumulate Value Stocks', 'Predicting rapid hyperinflation timeline', 'Tech hiring market bottomed out'
    ],
    'Current Status': ['✅ Met', '⏳ Pending', '❌ Failed', '✅ Success', '✅ Success', '✅ Success', '✅ Highly Accurate', '✅ Highly Accurate', '❌ Missed Timeframe', '⏳ Pending', '❌ Timelines Off', '✅ Met']
}

df = pd.DataFrame(data)

# 2. Category Tabs for Clean Scannability
tab1, tab2 = st.tabs(["🏆 Global Leaderboard", "🔍 Individual Tracker Profiles"])

with tab1:
    st.subheader("All Monitored Analysts")
    # Quick filter sidebar style inside the main page
    search_query = st.text_input("⚡ Quick Filter by Name, Platform, or Sector:", "")
    
    if search_query:
        filtered_df = df[df['Predictor Name'].str.contains(search_query, case=False) | 
                         df['Source / Platform'].str.contains(search_query, case=False)]
    else:
        filtered_df = df
        
    st.dataframe(filtered_df.sort_values(by='Accuracy Rate', ascending=False), use_container_width=True, hide_index=True)

with tab2:
    st.subheader("Analyst Breakdown")
    selected_name = st.selectbox("Choose a personality to audit:", df['Predictor Name'])
    
    # Fetch row data
    profile = df[df['Predictor Name'] == selected_name].iloc[0]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Platform Base", profile['Source / Platform'])
    col2.metric("Tracked Accuracy", profile['Accuracy Rate'])
    col3.metric("Last Action Outcome", profile['Current Status'])
    
    st.info(f"**Last Monitored Public Claim:** {profile['Notable Last Call']}")
