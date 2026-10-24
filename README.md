# retail_ai

Customer behaviour analytics dashboard for a UK online retailer, built on the
UCI Online Retail II dataset (2009–2011, 5,878 customers). A Streamlit web app
brings together customer segmentation, churn prediction, product
recommendations and personalised offers.

**Team:** Lavanya Bansal · Ridwan Shakoor · Harshita Yangalasetty · Jiya Yadav · Kevin Philip
(GDSC · Machine Learning Track)

📊 Project presentation: [docs/Customer_Behavior_Analyzer_presentation.pdf](docs/Customer_Behavior_Analyzer_presentation.pdf)

🤝 Earlier work by teammates, including Kevin's React + Flask version of the dashboard: [contributions/](contributions/)

## Running the app

Requires Python 3.10–3.12.

```bash
git clone https://github.com/lavanyabansal03/retail_ai.git
cd retail_ai
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\streamlit run app.py
```

Mac / Linux:

```bash
.venv/bin/pip install -r requirements.txt
.venv/bin/streamlit run app.py
```

The app opens at http://localhost:8501.

## Pages

| Page | What it shows |
|---|---|
| Overview | KPIs (customers, churn rate, spend, one-time buyers) and top product rules |
| Customer Segments | Filter customers by segment / churn / buyer type, look up a customer |
| RFM Analysis | Recency · Frequency · Monetary scores per segment and per customer |
| Market Basket | Apriori association rules, filterable by confidence, lift and support |
| Churn Prediction | Churn risk from the trained DNN and XGBoost models (averaged) |
| Sales Forecasting | Next-purchase estimate per customer; revenue forecast is demo data for now |
| Offers & Recs | Segment-based offer plus personalised product recommendations |
| Model Monitor | Which model files are present and the training curves |

Try customer ID `12347` in the lookup boxes.

## Project structure

```
retail_ai/
├── app.py                      ← Streamlit dashboard
├── requirements.txt
├── data/
│   ├── cleaned_retail_data.csv   cleaned transactions
│   ├── customer_features.csv     RFM features, segment and churn label per customer
│   ├── rfm_scores.csv            R/F/M scores (1–5) and total score
│   └── association_rules.csv     Apriori rules
├── models/
│   ├── dnn_churn(3).keras        DNN churn model (+ dnn_scaler(4).pkl)
│   ├── xgboost_churn.pkl         XGBoost churn model (+ xgboost_label_encoder.pkl)
│   ├── gru_next_purchase.keras   GRU next-purchase model (+ gru_interval_scaler.pkl)
│   ├── gru_sales_forecast.keras  GRU sales forecast model
│   └── *_extracted/              unpacked weights used by src/ loaders
└── src/
    ├── data_cleaning_ridwan.py   data cleaning (from the Colab notebook)
    ├── dnn.py                    load DNN + predict churn
    ├── xgboost_model.py          load XGBoost + predict churn
    ├── gru.py                    GRU loading / test script
    ├── recommendation.py         per-customer recommendations from association rules
    ├── offers.py                 offer message generation
    ├── segmentation.py
    └── data_processing.py
```

## Notes

- The `.keras` model files were saved with Keras 3.13, which can't be loaded
  directly on Python 3.10. `src/dnn.py` therefore rebuilds the network and loads
  the weights from `models/*_extracted/`.
- Don't commit `.venv/`. Each person creates their own environment from
  `requirements.txt` (it's in `.gitignore`).
