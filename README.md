# Energy Sector Stock Scorer

A Python-based fundamental scoring model for major energy sector stocks.
Scores each stock across 5 key factors and outputs a BUY, HOLD, or SELL signal.

## Scoring Factors & Weights
- P/E Ratio vs Sector Average (25%) — valuation relative to peers
- EPS Growth (20%) — earnings trajectory
- Revenue Growth (15%) — business momentum
- Return on Equity / ROE (20%) — capital efficiency
- Debt/Equity Ratio (20%) — leverage risk

## Scoring Logic
- 7.0 and above = BUY
- 4.0 to 6.9 = HOLD
- Below 4.0 = SELL

## Sample Output
Ticker      P/E   EPS Gr   Rev Gr     ROE     D/E   Score  Signal
EOG       12.87    0.396    0.156   0.182   26.87     8.8     BUY
OXY       72.89    3.156   -0.083   0.041   41.99     5.1    HOLD

## Files
- fetcher.py — pulls fundamental data from Yahoo Finance
- scorer.py — scores each factor 1-10 and calculates weighted final score
- recommender.py — converts final score to BUY/HOLD/SELL
- main.py — runs full model and exports results to CSV

## Libraries
pandas, yfinance

## How to run
python3 main.py