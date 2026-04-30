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

---

## How It Works

The app is split into a Python backend and a React frontend. The backend loads pre-trained ML models and CSVs at startup, then serves predictions through a REST API. The frontend fetches from that API and renders everything as an interactive dashboard. Vite proxies all `/api` requests from the browser to Flask, so there are no cross-origin issues.

**Data pipeline:**
Raw transaction data (UCI Online Retail II) was cleaned and engineered into per-customer RFM features — Recency (days since last purchase), Frequency (number of orders), and Monetary (total spend). These features feed every model.

**Segmentation (Segments page):**
KMeans clustering on RFM scores groups all 5,878 customers into four segments — Champions, Loyal Customers, At Risk, and Lost Customers. The clusters are pre-computed and stored in `customer_features.csv`.

**Churn prediction (Churn Risk page):**
A Deep Neural Network (DNN) trained on the five RFM features outputs a churn probability (0–1) for each customer. Inputs are standardised with a `StandardScaler` before inference. Customers are ranked highest-to-lowest risk.

**Next purchase prediction (Next Purchase page):**
A GRU (Gated Recurrent Unit) model predicts each customer's average inter-purchase interval. Days remaining until the next purchase is calculated by subtracting how many days have already passed since their last order (Recency) from that predicted interval.

**Product recommendations (Recommendations page):**
Apriori association rule mining finds which products are frequently bought together. The top 20 rules by confidence are surfaced, showing antecedent → consequent product pairs with confidence % and lift score.

**Personalized Offers page:**
Combines churn probability and next-purchase timing to identify the 15 highest-risk customers. Each gets a segment-tailored offer message designed to re-engage them at the moment they are most likely to buy.
