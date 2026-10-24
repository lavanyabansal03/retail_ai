import numpy as np

def is_valid_days(days):
    try:
        return days is not None and not np.isnan(float(days))
    except:
        return False


def generate_offer(row):

    seg  = row.get('Segment', '')
    prob = row.get('DNN_Churn_Prob') or row.get('Churn_Prob') or 0
    days = row.get('Days_Until_Next_Purchase')
    prod = row.get('Top_Recommendation', 'your favourite products')

    timing = (
        f"Valid for {int(days)} days"
        if is_valid_days(days)
        else "Limited time offer"
    )

    if prob > 0.8 or seg == 'Lost Customers':
        return (
            f"We miss you! Come back and enjoy buy 2 get 1 FREE on {prod}. "
            f"{timing} — we'd love to have you back!",
            "lost"
        )

    elif seg == 'At Risk' or prob > 0.5:
        return (
            f"We noticed you haven't visited in a while. "
            f"Here's 50% off {prod} — just for you. {timing}!",
            "atrisk"
        )

    elif seg == 'Champions':
        return (
            f"Thank you for being one of our top customers! "
            f"Enjoy an exclusive 20% loyalty reward on {prod}. {timing}.",
            "champion"
        )

    else:
        return (
            f"Hi! Here's an early access deal — 15% off {prod}. "
            f"{timing}. Thank you for your loyalty!",
            "loyal"
        )