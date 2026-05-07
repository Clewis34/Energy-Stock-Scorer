def score_pe(pe, sector_avg=15):
    if pe is None:
        return 5
    if pe < sector_avg * 0.7:
        return 10
    elif pe < sector_avg * 0.9:
        return 8
    elif pe < sector_avg * 1.1:
        return 6
    elif pe < sector_avg * 1.3:
        return 4
    else:
        return 2

def score_growth(growth):
    if growth is None:
        return 5
    growth = growth * 100
    if growth > 20:
        return 10
    elif growth > 10:
        return 8
    elif growth > 0:
        return 6
    elif growth > -10:
        return 4
    else:
        return 2

def score_roe(roe):
    if roe is None:
        return 5
    roe = roe * 100
    if roe > 20:
        return 10
    elif roe > 15:
        return 8
    elif roe > 10:
        return 6
    elif roe > 5:
        return 4
    else:
        return 2

def score_debt(de):
    if de is None:
        return 5
    if de < 30:
        return 10
    elif de < 60:
        return 8
    elif de < 100:
        return 6
    elif de < 150:
        return 4
    else:
        return 2

def calculate_score(data):
    pe_score = score_pe(data['pe_ratio'])
    eps_score = score_growth(data['eps_growth'])
    rev_score = score_growth(data['revenue_growth'])
    roe_score = score_roe(data['roe'])
    debt_score = score_debt(data['debt_to_equity'])

    final_score = (
        pe_score * 0.25 +
        eps_score * 0.20 +
        rev_score * 0.15 +
        roe_score * 0.20 +
        debt_score * 0.20
    )
    return round(final_score, 2)