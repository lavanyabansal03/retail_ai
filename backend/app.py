from flask import Flask, jsonify
import pandas as pd
import numpy as np
import joblib
import re
import os

app = Flask(__name__)

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, "data")
MODELS_DIR = os.path.join(BASE, "models")

_models = {}
_scalers = {}


def _data(name):
    return pd.read_csv(os.path.join(DATA_DIR, name))


def _scaler(name):
    if name not in _scalers:
        _scalers[name] = joblib.load(os.path.join(MODELS_DIR, name))
    return _scalers[name]


def _model(name):
    if name not in _models:
        import tensorflow as tf
        _models[name] = tf.keras.models.load_model(os.path.join(MODELS_DIR, name))
    return _models[name]


def parse_frozenset(s):
    return re.findall(r"'([^']+)'", str(s))


SEGMENT_ACTIONS = {
    "Champions": "Send loyalty reward — they deserve it",
    "Loyal Customers": "Give early access to new products",
    "At Risk": "Send win-back offer before they leave",
    "Lost Customers": "Re-engagement campaign with big discount",
}


# ── Dashboard ────────────────────────────────────────────────────────────────

@app.route("/api/dashboard")
def dashboard():
    df = _data("customer_features.csv")
    total = len(df)
    total_revenue = float(df["Monetary"].sum())
    churn_rate = float((df["Churn"] == 1).sum() / total * 100)
    avg_order_value = float((df["Monetary"] / df["Frequency"]).mean())
    segment_counts = df["Segment"].value_counts().to_dict()

    return jsonify({
        "total_customers": total,
        "total_revenue": round(total_revenue, 2),
        "churn_rate": round(churn_rate, 1),
        "avg_order_value": round(avg_order_value, 2),
        "segment_counts": segment_counts,
    })


# ── Segments ─────────────────────────────────────────────────────────────────

@app.route("/api/segments")
def segments():
    df = _data("customer_features.csv").reset_index(drop=True)
    rfm = _data("rfm_scores.csv").reset_index(drop=True)
    total = len(df)

    result = []
    for seg in df["Segment"].unique():
        mask = df["Segment"] == seg
        seg_df = df[mask]
        seg_rfm = rfm[mask]

        result.append({
            "segment": seg,
            "count": int(len(seg_df)),
            "pct_of_total": round(len(seg_df) / total * 100, 1),
            "avg_recency": round(float(seg_df["Recency"].mean()), 1),
            "avg_monetary": round(float(seg_df["Monetary"].mean()), 2),
            "avg_r_score": round(float(seg_rfm["R_Score"].mean()), 2) if "R_Score" in rfm.columns else None,
            "avg_f_score": round(float(seg_rfm["F_Score"].mean()), 2) if "F_Score" in rfm.columns else None,
            "avg_m_score": round(float(seg_rfm["M_Score"].mean()), 2) if "M_Score" in rfm.columns else None,
            "recommended_action": SEGMENT_ACTIONS.get(seg, ""),
        })

    return jsonify(result)


# ── Churn ─────────────────────────────────────────────────────────────────────

@app.route("/api/churn")
def churn():
    df = _data("customer_features.csv")
    features = ["Recency", "Frequency", "Monetary", "Avg_InterPurchase_Interval", "Is_OneTimeBuyer"]

    scaler = _scaler("dnn_scaler.pkl")
    model = _model("dnn_churn.keras")

    X_scaled = scaler.transform(df[features].values)
    probs = model.predict(X_scaled, verbose=0).flatten()

    def risk(p):
        if p > 0.7:
            return "High"
        if p >= 0.4:
            return "Medium"
        return "Low"

    records = []
    for i, (_, row) in enumerate(df.iterrows()):
        p = float(probs[i])
        records.append({
            "customer_id": str(row["Customer ID"]),
            "segment": row["Segment"],
            "recency": f"{int(row['Recency'])} days ago",
            "churn_probability": round(p, 3),
            "risk_level": risk(p),
        })

    records.sort(key=lambda x: x["churn_probability"], reverse=True)

    return jsonify({
        "customers": records,
        "summary": {
            "high_count": sum(1 for r in records if r["risk_level"] == "High"),
            "medium_count": sum(1 for r in records if r["risk_level"] == "Medium"),
            "low_count": sum(1 for r in records if r["risk_level"] == "Low"),
        },
    })


# ── Next Purchase ─────────────────────────────────────────────────────────────

@app.route("/api/next-purchase")
def next_purchase():
    df = _data("customer_features.csv")
    scaler = _scaler("gru_interval_scaler.pkl")
    model = _model("gru_next_purchase.keras")

    intervals = df["Avg_InterPurchase_Interval"].values.reshape(-1, 1)
    scaled = scaler.transform(intervals).reshape(-1, 1, 1)
    raw_preds = model.predict(scaled, verbose=0).flatten()

    # Model predicts the next full interval; subtract days already elapsed
    # (Recency) to get days remaining until next purchase
    predicted_interval = scaler.inverse_transform(raw_preds.reshape(-1, 1)).flatten()
    days_remaining = predicted_interval - df["Recency"].values
    days_remaining = np.clip(days_remaining, 0, None)

    records = []
    for i, (_, row) in enumerate(df.iterrows()):
        records.append({
            "customer_id": str(row["Customer ID"]),
            "segment": row["Segment"],
            "avg_interval": round(float(row["Avg_InterPurchase_Interval"]), 1),
            "predicted_days": round(float(days_remaining[i]), 1),
        })

    records.sort(key=lambda x: x["predicted_days"])
    # Show customers whose predicted next purchase is within 30 days
    # Fall back to top 25 soonest if none qualify
    upcoming = [r for r in records if r["predicted_days"] <= 30]
    if not upcoming:
        upcoming = records[:25]

    return jsonify({
        "upcoming": upcoming,
        "within_7_days": sum(1 for r in records if r["predicted_days"] <= 7),
        "all_count": len(records),
    })


# ── Recommendations ───────────────────────────────────────────────────────────

@app.route("/api/recommendations")
def recommendations():
    df = pd.read_csv(os.path.join(DATA_DIR, "association_rules.csv"))
    df = df.sort_values("confidence", ascending=False).head(20)

    result = [
        {
            "antecedents": parse_frozenset(row["antecedents"]),
            "consequents": parse_frozenset(row["consequents"]),
            "confidence": round(float(row["confidence"]) * 100, 1),
            "lift": round(float(row["lift"]), 2),
            "support": round(float(row["support"]), 4),
        }
        for _, row in df.iterrows()
    ]
    return jsonify(result)


# ── RFM ───────────────────────────────────────────────────────────────────────

@app.route("/api/rfm")
def rfm():
    df = _data("rfm_scores.csv")
    return jsonify({
        "r_score_dist": {str(k): int(v) for k, v in df["R_Score"].value_counts().sort_index().items()},
        "f_score_dist": {str(k): int(v) for k, v in df["F_Score"].value_counts().sort_index().items()},
        "m_score_dist": {str(k): int(v) for k, v in df["M_Score"].value_counts().sort_index().items()},
        "total_score_dist": {str(k): int(v) for k, v in df["Total_Score"].value_counts().sort_index().items()},
    })


if __name__ == "__main__":
    app.run(debug=True, port=5001)
