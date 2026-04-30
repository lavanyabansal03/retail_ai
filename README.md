# Customer Analyzer

AI-powered customer behavior dashboard for UK Retail. Built on the UCI Online Retail II dataset (2009–2011), 5,878 customers.

## Project Structure

```
CustomerBehaviorAnalyzer/
├── backend/
│   ├── app.py              ← Flask REST API
│   ├── data/               ← Put CSV files here
│   │   ├── customer_features.csv
│   │   ├── rfm_scores.csv
│   │   └── association_rules.csv
│   └── models/             ← Put model files here
│       ├── dnn_churn.keras
│       ├── dnn_scaler.pkl
│       ├── xgboost_churn.pkl
│       ├── xgboost_label_encoder.pkl
│       ├── gru_next_purchase.keras
│       ├── gru_interval_scaler.pkl
│       └── gru_sales_forecast.keras
├── frontend/               ← Vite React app
├── requirements.txt        ← Python dependencies
├── start.sh                ← Runs both servers together
└── README.md
```

## Prerequisites

- Python 3.10+
- Node.js 18+
- npm

## Setup

### 1. Place your data and model files

Copy your CSV files into `backend/data/` and your `.keras` / `.pkl` model files into `backend/models/` before running.

### 2. Install Python dependencies (virtual environment)

```bash
cd backend
python3 -m venv venv
venv/bin/pip install -r ../requirements.txt
cd ..
```

### 3. Install frontend dependencies

```bash
cd frontend
npm install
cd ..
```

## Running the App

From the project root, one command starts both servers:

```bash
./start.sh
```

| Server         | URL                   |
| -------------- | --------------------- |
| Flask API      | http://localhost:5001 |
| React frontend | http://localhost:5173 |

Press **Ctrl+C** to stop both servers.

## API Endpoints

| Endpoint                   | Description                                    |
| -------------------------- | ---------------------------------------------- |
| `GET /api/dashboard`       | KPI stats and segment counts                   |
| `GET /api/segments`        | RFM segment breakdown with recommended actions |
| `GET /api/churn`           | DNN churn probabilities ranked by risk         |
| `GET /api/next-purchase`   | GRU predicted days until next purchase         |
| `GET /api/recommendations` | Top 20 Apriori association rules               |
| `GET /api/rfm`             | RFM score distributions                        |

## Pages

- **Dashboard** — KPI cards, segment donut chart, RFM score distribution
- **Segments** — Segment cards with stats and recommended actions
- **Churn Risk** — Leaderboard of customers most likely to churn
- **Next Purchase** — GRU-predicted upcoming purchases + 8-week forecast
- **Recommendations** — Apriori product association rules
- **Personalized Offers** — AI-generated offers for highest-risk customers
