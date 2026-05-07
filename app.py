import streamlit as st
from fetcher import get_fundamentals, ENERGY_TICKERS
from scorer import calculate_score
from recommender import get_recommendation
import pandas as pd

st.title("Energy Sector Stock Scorer")
st.write("Fundamental scoring model for major energy stocks. Scores each company across 5 factors and outputs a BUY, HOLD, or SELL signal.")

if st.button("Run Screener"):
    with st.spinner("Fetching data..."):
        results = []
        for ticker in ENERGY_TICKERS:
            data = get_fundamentals(ticker)
            score = calculate_score(data)
            recommendation = get_recommendation(score)
            results.append({
                'Ticker': ticker,
                'P/E Ratio': round(data['pe_ratio'], 2) if data['pe_ratio'] else 'N/A',
                'EPS Growth': f"{round(data['eps_growth']*100, 1)}%" if data['eps_growth'] else 'N/A',
                'Revenue Growth': f"{round(data['revenue_growth']*100, 1)}%" if data['revenue_growth'] else 'N/A',
                'ROE': f"{round(data['roe']*100, 1)}%" if data['roe'] else 'N/A',
                'Debt/Equity': round(data['debt_to_equity'], 1) if data['debt_to_equity'] else 'N/A',
                'Score': score,
                'Signal': recommendation
            })

        df = pd.DataFrame(results)

        def color_signal(val):
            if val == "BUY":
                return 'background-color: #d4edda; color: #155724'
            elif val == "SELL":
                return 'background-color: #f8d7da; color: #721c24'
            else:
                return 'background-color: #fff3cd; color: #856404'

        styled = df.style.map(color_signal, subset=['Signal'])
        st.dataframe(styled, use_container_width=True)