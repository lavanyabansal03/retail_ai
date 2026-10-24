def generate_offer(row):
    churn = row.get('Churn_Prob', 0)
    seg = row.get('Segment', '')

    if churn > 0.8 or seg == 'Lost Customers':
        return "20% Discount + Free Shipping"

    elif seg == 'At Risk' or churn > 0.5:
        return "Win-back Offer"

    elif seg == 'Champions':
        return "Loyalty Reward + Early Access"

    else:
        return "Standard Offer"