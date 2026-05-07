import csv
from fetcher import get_fundamentals, ENERGY_TICKERS
from scorer import calculate_score
from recommender import get_recommendation

results = []

for ticker in ENERGY_TICKERS:
    data = get_fundamentals(ticker)
    score = calculate_score(data)
    recommendation = get_recommendation(score)
    results.append({
        'ticker': ticker,
        'pe_ratio': data['pe_ratio'],
        'eps_growth': data['eps_growth'],
        'revenue_growth': data['revenue_growth'],
        'roe': data['roe'],
        'debt_to_equity': data['debt_to_equity'],
        'score': score,
        'recommendation': recommendation
    })

print(f"\n{'Ticker':<8} {'P/E':>8} {'EPS Gr':>8} {'Rev Gr':>8} {'ROE':>8} {'D/E':>8} {'Score':>8} {'Signal':>8}")
print("-" * 70)
for r in results:
    print(f"{r['ticker']:<8} {str(r['pe_ratio'] or 'N/A'):>8} {str(r['eps_growth'] or 'N/A'):>8} {str(r['revenue_growth'] or 'N/A'):>8} {str(r['roe'] or 'N/A'):>8} {str(r['debt_to_equity'] or 'N/A'):>8} {r['score']:>8} {r['recommendation']:>8}")

with open("scoring_results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("\nResults saved to scoring_results.csv")