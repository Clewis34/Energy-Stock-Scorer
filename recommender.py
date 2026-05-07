def get_recommendation(score):
    if score >= 7.0:
        return "BUY"
    elif score >= 4.0:
        return "HOLD"
    else:
        return "SELL"