# Team contributions

Work by team members that shaped the project but isn't part of the final
Streamlit app. It's kept here, with its original commit history, so everyone's
contribution is visible. Nothing in this folder is used by `app.py`.

## harshita-early-models/ — Harshita Yangalasetty

Early versions of the pipeline, built while learning the workflow:

- `models/dnn_churn_model.h5` — first DNN churn model
- `models/xgboost_model.pkl` — first XGBoost churn model
- `data/rfm_data.csv`, `data/customer_segments.csv` — early RFM features and segments
- `loss_curve.png` — DNN training loss curve

The final models in `/models` were developed from this groundwork.

## kevin-react-app/ — Kevin Philip

A complete alternative version of the dashboard: a **React (Vite) frontend**
with charts and a **Flask REST API** backend, with pages for the dashboard,
segments, churn risk, next purchase, recommendations and personalised offers.
See [kevin-react-app/README.md](kevin-react-app/README.md) for how to run it.

It wasn't used for the final demo because of model-version conflicts and lack
of time. Things to know if you pick it up:

- The `.keras` models were saved with Keras 3.13, which needs **Python 3.11+**.
  On Python 3.10 the Churn Risk and Next Purchase endpoints fail to load them
  (the Streamlit app works around this in `src/dnn.py` by rebuilding the model
  and loading only the weights).
- `start.sh` targets Mac/Linux (`venv/bin/python`); on Windows use
  `venv\Scripts\python app.py` in `backend/` and `npm run dev` in `frontend/`.
