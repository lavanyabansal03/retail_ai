def get_recommendations(customer_id, df, rules, top_n=5):
    """
    Return top_n product recommendations for a customer
    based on association rules and their purchase history.
    Returns list of (product, lift) tuples.
    """

    def parse_frozenset(val):
        if isinstance(val, (set, frozenset, list, tuple)):
            return list(val)

        if isinstance(val, str):
            return val.replace("frozenset({", "") \
                      .replace("})", "") \
                      .replace("'", "") \
                      .replace('"', "") \
                      .split(",")

        return []

    purchased = (
        df[df['Customer ID'] == customer_id]['Description'].unique().tolist()
        if 'Customer ID' in df.columns else []
    )

    recs = {}

    for _, rule in rules.iterrows():
        ants = parse_frozenset(rule['antecedents'])
        cons = parse_frozenset(rule['consequents'])

        if any(item in purchased for item in ants):
            for product in cons:
                product = product.strip()
                if product and product not in purchased:
                    recs[product] = rule.get('lift', 1.0)

    sorted_recs = sorted(recs.items(), key=lambda x: x[1], reverse=True)[:top_n]

    return sorted_recs if sorted_recs else [("No recommendations found", 0)]