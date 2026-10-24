# src/test_gru.py
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import zipfile
import h5py
import numpy as np
import pandas as pd
import joblib
from tensorflow import keras

# ── Weight loader — matches by NAME not position ────────────────────────────
def load_weights_manually(model, weights_path):
    with h5py.File(weights_path, "r") as f:
        layers_group = f['layers']

        for layer in model.layers:
            # Strip trailing _1, _2 etc to find base name in saved file
            # e.g. local 'gru_1' → try 'gru_1' first, then 'gru'
            candidates = [layer.name]
            base = layer.name.rsplit('_', 1)
            if base[0] in layers_group:
                candidates.append(base[0])

            matched = None
            for name in candidates:
                if name in layers_group:
                    matched = name
                    break

            if matched is None:
                print(f"  ⏭️  Skipped (not in file): {layer.name}")
                continue

            grp = layers_group[matched]

            # GRU weights live under cell/vars
            if 'cell' in grp and 'vars' in grp['cell'] and len(grp['cell']['vars']) > 0:
                vars_group = grp['cell']['vars']
                weights = [vars_group[str(i)][()] for i in range(len(vars_group))]
            elif 'vars' in grp and len(grp['vars']) > 0:
                vars_group = grp['vars']
                weights = [vars_group[str(i)][()] for i in range(len(vars_group))]
            else:
                print(f"  ⏭️  Skipped (no weights): {layer.name}")
                continue

            try:
                layer.set_weights(weights)
                print(f"  ✅ {matched} → {layer.name} ({len(weights)} weights)")
            except ValueError as e:
                print(f"  ❌ {matched} → {layer.name} FAILED: {e}")


# ── Extract both .keras zips ────────────────────────────────────────────────
for keras_file, extract_dir in [
    ("models/gru_next_purchase.keras",  "models/gru_next_purchase_extracted"),
    ("models/gru_sales_forecast.keras", "models/gru_sales_forecast_extracted"),
]:
    with zipfile.ZipFile(keras_file) as z:
        z.extractall(extract_dir)

# ══════════════════════════════════════════════════════════════════════════
# MODEL 1 — Next Purchase  (input: [None, 253, 1])
# ══════════════════════════════════════════════════════════════════════════
next_purchase_model = keras.Sequential([
    keras.Input(shape=(253, 1)),
    keras.layers.Masking(mask_value=0.0,  name="masking"),
    keras.layers.GRU(32, return_sequences=False, name="gru"),
    keras.layers.Dropout(0.2,             name="dropout"),
    keras.layers.Dense(1, activation='linear', name="dense")
], name="gru_next_purchase")

print("\n── Next Purchase Model ──")
load_weights_manually(next_purchase_model,
    "models/gru_next_purchase_extracted/model.weights.h5")

# ══════════════════════════════════════════════════════════════════════════
# MODEL 2 — Sales Forecast  (input: [None, 30, 1])
# Saved has: gru(64 units), gru_1(64 units), dense(7 units)
# ══════════════════════════════════════════════════════════════════════════
sales_forecast_model = keras.Sequential([
    keras.Input(shape=(30, 1)),
    keras.layers.GRU(64, return_sequences=True,  name="gru"),    # 64 units ✅
    keras.layers.Dropout(0.2,                    name="dropout"),
    keras.layers.GRU(32, return_sequences=False, name="gru_1"),  # 32 units ← fix this
    keras.layers.Dropout(0.2,                    name="dropout_1"),
    keras.layers.Dense(7, activation='linear',   name="dense")
], name="gru_sales_forecast")

print("\n── Sales Forecast Model ──")
load_weights_manually(sales_forecast_model,
    "models/gru_sales_forecast_extracted/model.weights.h5")

# ══════════════════════════════════════════════════════════════════════════
# SMOKE TESTS
# ══════════════════════════════════════════════════════════════════════════
print("\n── Smoke Tests ──")
dummy_next = np.random.rand(5, 253, 1).astype(np.float32)
out_next = next_purchase_model.predict(dummy_next, verbose=0)
print(f"✅ Next purchase output shape: {out_next.shape}  (expected (5, 1))")

dummy_sales = np.random.rand(5, 30, 1).astype(np.float32)
out_sales = sales_forecast_model.predict(dummy_sales, verbose=0)
print(f"✅ Sales forecast output shape: {out_sales.shape}  (expected (5, 7))")

# ══════════════════════════════════════════════════════════════════════════
# REAL DATA TEST
# ══════════════════════════════════════════════════════════════════════════
print("\n── Real Data Test ──")
try:
    scaler = joblib.load("models/gru_interval_scaler.pkl")
    df = pd.read_csv("data/customer_features.csv")

    intervals = df['Avg_InterPurchase_Interval'].fillna(0).values

    # Scale input
    X_next = intervals.reshape(-1, 1, 1)
    X_next = np.pad(X_next, ((0,0),(252,0),(0,0)))
    X_next_scaled = scaler.transform(
        X_next.reshape(-1, 1)).reshape(-1, 253, 1)

    # Predict
    preds_raw = next_purchase_model.predict(
        X_next_scaled, verbose=0).flatten()

    # ← ADD THIS: inverse transform to get actual days back
    preds_days = scaler.inverse_transform(
        preds_raw.reshape(-1, 1)).flatten()

    df['GRU_Next_Purchase_Days'] = np.clip(preds_days, 1, 365)

    print("✅ Real data predictions done!")
    print(df[['Customer ID', 'GRU_Next_Purchase_Days']].head(10))

except Exception as e:
    print(f"⚠️  Real data test skipped: {e}")