import joblib
import pandas as pd


MODEL_FILE    = "models/xgboost_churn.pkl"
SEGMENT_ORDER = ['Champions', 'Loyal Customers', 'At Risk', 'Lost Customers']
FEATURES      = ['Recency', 'Frequency', 'Monetary',
                  'Avg_InterPurchase_Interval', 'Is_OneTimeBuyer', 'Segment']


def load_xgb():
    """Load XGBoost model. Returns model."""
    return joblib.load(MODEL_FILE)


def predict_xgb(df, model):
    """
    Run XGBoost churn prediction.
    Adds XGB_Churn_Prob and XGB_Churn columns to a copy of df.
    Returns updated DataFrame.
    """
    df_copy = df.copy()

    # Stable category encoding — must match training order
    df_copy['Segment'] = pd.Categorical(
    df_copy['Segment'],
    categories=SEGMENT_ORDER
     ).codes

    X = df_copy[FEATURES]
    df_copy['XGB_Churn_Prob'] = model.predict_proba(X)[:, 1]
    df_copy['XGB_Churn'] = (df_copy['XGB_Churn_Prob'] > 0.5).astype(int)
    return df_copy