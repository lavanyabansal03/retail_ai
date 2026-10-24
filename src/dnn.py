import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import zipfile
import h5py
import joblib
import tensorflow as tf
from tensorflow import keras

KERAS_FILE  = "models/dnn_churn(3).keras"
EXTRACT_DIR = "models/dnn_churn_extracted"
SCALER_FILE = "models/dnn_scaler(4).pkl"
FEATURES    = ['Recency', 'Frequency', 'Monetary',
                'Avg_InterPurchase_Interval', 'Is_OneTimeBuyer']


def _load_weights_manually(model, weights_path):
    with h5py.File(weights_path, "r") as f:
        for layer in model.layers:
            name = layer.name
            if name in f['layers'] and 'vars' in f['layers'][name]:
                vars_group = f['layers'][name]['vars']
                weights = [vars_group[str(i)][()] for i in range(len(vars_group))]
                layer.set_weights(weights)


def load_dnn():
    """Load DNN model and scaler. Returns (model, scaler)."""
    with zipfile.ZipFile(KERAS_FILE) as z:
        z.extractall(EXTRACT_DIR)

    model = keras.Sequential([
        keras.layers.Dense(64, activation='relu', input_shape=(5,)),
        keras.layers.BatchNormalization(momentum=0.99, epsilon=0.001),
        keras.layers.Dropout(0.3),
        keras.layers.Dense(32, activation='relu'),
        keras.layers.BatchNormalization(momentum=0.99, epsilon=0.001),
        keras.layers.Dropout(0.3),
        keras.layers.Dense(16, activation='relu'),
        keras.layers.Dense(1,  activation='sigmoid')
    ], name="sequential")
    model.build(input_shape=(None, 5))
    _load_weights_manually(model, f"{EXTRACT_DIR}/model.weights.h5")

    scaler = joblib.load(SCALER_FILE)
    return model, scaler


def predict_dnn(df, model, scaler):
    """
    Run DNN churn prediction.
    Adds DNN_Churn_Prob and DNN_Churn columns to a copy of df.
    Returns updated DataFrame.
    """
    df_copy = df.copy()
    X = df_copy[FEATURES].fillna(0)
    X_scaled = scaler.transform(X)
    probs = model.predict(X_scaled, verbose=0).flatten()
    df_copy['DNN_Churn_Prob'] = probs
    df_copy['DNN_Churn']      = (probs > 0.5).astype(int)
    return df_copy






if __name__ == "__main__":
    print("Testing pipeline...")

    model, scaler = load_dnn()

    import pandas as pd
    sample = pd.DataFrame([{
        'Recency': 10,
        'Frequency': 5,
        'Monetary': 200,
        'Avg_InterPurchase_Interval': 7,
        'Is_OneTimeBuyer': 0
    }])

    print(predict_dnn(sample, model, scaler))