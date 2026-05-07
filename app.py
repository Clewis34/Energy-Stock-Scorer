import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from fetcher import get_fundamentals, ENERGY_TICKERS
from scorer import calculate_score
from recommender import get_recommendation

st.set_page_config(page_title="Energy Stock Scorer", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #0f172a; }
    h1 { color: #0f172a !important; font-size: 24px !important; font-weight: 700 !important; letter-spacing: -0.5px; }
    h2, h3 { color: #1e3a5f !important; font-size: 13px !important; font-weight: 600 !important; text-transform: uppercase; letter-spacing: 1.2px; }
    .stApp p { color: #475569; }
    hr { border-color: #e2e8f0 !important; }
    [data-testid="stMetricValue"] { color: #0f172a !important; font-size: 28px !important; font-weight: 700 !important; }
    [data-testid="stMetricLabel"] { color: #64748b !important; font-size: 11px !important; text-transform: uppercase; letter-spacing: 1px; }
    [data-testid="metric-container"] { background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; }
    .stDataFrame { border: 1px solid #e2e8f0; border-radius: 8px; }
    div.stButton button { background-color: #1e3a5f !important; color: #ffffff !important; border: none !important; border-radius: 6px !important; padding: 10px 28px !important; font-size: 14px !important; font-weight: 600 !important; width: auto !important; }
    div.stButton button:hover { background-color: #162d4a !important; color: #ffffff !important; }
    div.stButton button p { color: #ffffff !important; }
    </style>
""", unsafe_allow_html=True)

st.title("Energy Sector Stock Scorer")
st.markdown("Fundamental scoring model for major energy stocks. Scored across five weighted factors with BUY, HOLD, or SELL output.")
st.divider()

if st.button("Run Screener"):
    with st.spinner("Fetching live data..."):
        results = []
        for ticker in ENERGY_TICKERS:
            data = get_fundamentals(ticker)
            score = calculate_score(data)
            recommendation = get_recommendation(score)
            results.append({
                'Ticker': ticker,
                'P/E Ratio': round(data['pe_ratio'], 2) if data['pe_ratio'] else None,
                'EPS Growth': round(data['eps_growth']*100, 1) if data['eps_growth'] else None,
                'Revenue Growth': round(data['revenue_growth']*100, 1) if data['revenue_growth'] else None,
                'ROE': round(data['roe']*100, 1) if data['roe'] else None,
                'Debt/Equity': round(data['debt_to_equity'], 1) if data['debt_to_equity'] else None,
                'Score': score,
                'Signal': recommendation
            })

        df = pd.DataFrame(results)
        buys = len(df[df['Signal'] == 'BUY'])
        holds = len(df[df['Signal'] == 'HOLD'])
        sells = len(df[df['Signal'] == 'SELL'])
        top_stock = df.loc[df['Score'].idxmax(), 'Ticker']

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Buy Signals", buys)
        col2.metric("Hold Signals", holds)
        col3.metric("Sell Signals", sells)
        col4.metric("Top Ranked", top_stock)

        st.divider()
        st.subheader("Score by Stock")

        fig = go.Figure(go.Bar(
            x=df['Ticker'],
            y=df['Score'],
            marker_color='#1e3a5f',
            marker_line_color='#162d4a',
            marker_line_width=1,
            text=df['Score'],
            textposition='outside',
            textfont=dict(color='#0f172a', size=13)
        ))
        fig.update_layout(
            yaxis=dict(range=[0, 11], title='Score', color='#64748b', gridcolor='#e2e8f0', zerolinecolor='#e2e8f0'),
            xaxis=dict(title='', color='#64748b', tickfont=dict(color='#0f172a', size=13)),
            height=380,
            paper_bgcolor='#ffffff',
            plot_bgcolor='#ffffff',
            font=dict(color='#64748b'),
            margin=dict(t=30, b=20)
        )
        fig.add_hline(y=7, line_dash="dot", line_color="#1e3a5f", line_width=1, annotation_text="BUY", annotation_font_color="#1e3a5f", annotation_font_size=11)
        fig.add_hline(y=4, line_dash="dot", line_color="#94a3b8", line_width=1, annotation_text="SELL", annotation_font_color="#94a3b8", annotation_font_size=11)
        st.plotly_chart(fig, width='stretch')

        st.divider()
        st.subheader("Full Breakdown")

        def color_signal(val):
            if val == "BUY":
                return 'background-color: #dbeafe; color: #1e3a5f; font-weight: 600'
            elif val == "SELL":
                return 'background-color: #fee2e2; color: #991b1b; font-weight: 600'
            else:
                return 'background-color: #f1f5f9; color: #475569; font-weight: 600'

        styled = df.style.map(color_signal, subset=['Signal'])
        st.dataframe(styled, width='stretch')

        st.divider()
        st.subheader("Factor Comparison")

        factors = ['P/E Ratio', 'EPS Growth', 'Revenue Growth', 'ROE', 'Debt/Equity']
        fig2 = px.bar(
            df.melt(id_vars='Ticker', value_vars=factors),
            x='Ticker',
            y='value',
            color='variable',
            barmode='group',
            height=420,
            color_discrete_sequence=['#0f172a', '#1e3a5f', '#1d4ed8', '#3b82f6', '#93c5fd']
        )
        fig2.update_layout(
            xaxis=dict(title='', color='#64748b', tickfont=dict(color='#0f172a')),
            yaxis=dict(title='Value', color='#64748b', gridcolor='#e2e8f0', zerolinecolor='#e2e8f0'),
            legend_title=dict(text='Factor', font=dict(color='#64748b')),
            legend=dict(font=dict(color='#0f172a')),
            paper_bgcolor='#ffffff',
            plot_bgcolor='#ffffff',
            font=dict(color='#64748b'),
            margin=dict(t=30, b=20)
        )
        st.plotly_chart(fig2, width='stretch')