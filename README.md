# retail_ai

````retail_ai_project/
│
├── data/
│   ├── cleaned_data.csv
│   ├── rfm_features.csv
│   ├── customer_segments.csv
│   └── association_rules.csv
│
├── models/
│   ├── xgboost_model.pkl
│   ├── dnn_model.h5
│   ├── gru_sales.h5
│   └── autoencoder.h5
│
├── src/
│   ├── data_processing.py
│   ├── segmentation.py
│   ├── recommendation.py
│   ├── churn_model.py
│   ├── dnn_model.py
│   ├── forecasting.py
│   ├── offers.py
│
├── app.py   ← Streamlit dashboard
└── README.md
```