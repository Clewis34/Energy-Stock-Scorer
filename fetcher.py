import yfinance as yf

ENERGY_TICKERS = [
    "XOM", "CVX", "COP", "SLB", "EOG",
    "MPC", "PSX", "VLO", "HAL", "OXY"
]

def get_fundamentals(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        'ticker': ticker,
        'pe_ratio': info.get('trailingPE', None),
        'eps_growth': info.get('earningsGrowth', None),
        'revenue_growth': info.get('revenueGrowth', None),
        'roe': info.get('returnOnEquity', None),
        'debt_to_equity': info.get('debtToEquity', None)
    }

if __name__ == "__main__":
    for ticker in ENERGY_TICKERS:
        data = get_fundamentals(ticker)
        print(data)