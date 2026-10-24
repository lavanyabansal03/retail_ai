import joblib
import pandas as pd


MODEL_FILE    = "models/xgboost_churn.pkl"
ENCODER_FILE  = "models/xgboost_label_encoder.pkl"
FEATURES      = ['Recency', 'Frequency', 'Monetary',
                  'Avg_InterPurchase_Interval', 'Is_OneTimeBuyer', 'Segment']


def load_xgb():
    """Load XGBoost model and the Segment label encoder. Returns (model, encoder)."""
    return joblib.load(MODEL_FILE), joblib.load(ENCODER_FILE)


def predict_xgb(df, model, encoder):
    """
    Run XGBoost churn prediction.
    Adds XGB_Churn_Prob and XGB_Churn columns to a copy of df.
    Returns updated DataFrame.
    """
    df_copy = df.copy()
    X = df_copy[FEATURES].copy()

    # Encode Segment with the same LabelEncoder used in training
    X['Segment'] = encoder.transform(X['Segment'])

    df_copy['XGB_Churn_Prob'] = model.predict_proba(X)[:, 1]
    df_copy['XGB_Churn'] = (df_copy['XGB_Churn_Prob'] > 0.5).astype(int)
    return df_copy
