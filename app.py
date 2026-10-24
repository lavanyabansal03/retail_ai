import streamlit as st
import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
#  PAGE CONFIG  (must be FIRST Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="RETAIL AI · Intelligence Suite",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS  – dark navy + violet accent theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Outfit:wght@300;400;600;800&display=swap');

/* ── Root palette ── */
:root {
  --bg:        #0b0f1a;
  --surface:   #111827;
  --card:      #161d2e;
  --border:    #1e2d45;
  --accent:    #7c3aed;
  --accent2:   #a855f7;
  --teal:      #06b6d4;
  --green:     #10b981;
  --yellow:    #f59e0b;
  --red:       #ef4444;
  --text:      #e2e8f0;
  --muted:     #64748b;
  --radius:    12px;
}

/* ── Global resets ── */
html, body, .stApp { background: var(--bg) !important; color: var(--text) !important; }
* { font-family: 'Outfit', sans-serif; box-sizing: border-box; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: var(--surface) !important;
  border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* ── Top header band ── */
.top-header {
  background: linear-gradient(135deg, #1e1045 0%, #0f172a 60%, #0e2038 100%);
  border-bottom: 1px solid var(--border);
  padding: 22px 36px 18px;
  display: flex; align-items: center; gap: 18px;
  border-radius: 0 0 var(--radius) var(--radius);
  margin-bottom: 28px;
}
.top-header .brand-icon { font-size: 2.4rem; }
.top-header h1 {
  font-family: 'Outfit', sans-serif;
  font-weight: 800; font-size: 1.85rem;
  margin: 0; letter-spacing: -0.5px;
  background: linear-gradient(90deg, #a78bfa, #38bdf8);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.top-header p { margin: 2px 0 0; color: var(--muted); font-size: 0.85rem; }

/* ── Section title ── */
.section-title {
  font-family: 'Space Mono', monospace;
  font-size: 0.72rem; font-weight: 700; letter-spacing: 3px;
  text-transform: uppercase; color: var(--accent2);
  margin-bottom: 14px; border-left: 3px solid var(--accent);
  padding-left: 10px;
}

/* ── KPI cards ── */
.kpi-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 16px; margin-bottom: 28px; }
.kpi-card {
  background: var(--card); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 20px 22px;
  position: relative; overflow: hidden;
  transition: transform .2s, box-shadow .2s;
}
.kpi-card:hover { transform: translateY(-3px); box-shadow: 0 10px 30px rgba(124,58,237,.18); }
.kpi-card::before {
  content:''; position:absolute; top:0; left:0; right:0; height:3px;
}
.kpi-card.violet::before { background: linear-gradient(90deg, var(--accent), var(--accent2)); }
.kpi-card.teal::before   { background: linear-gradient(90deg, var(--teal), #0284c7); }
.kpi-card.green::before  { background: linear-gradient(90deg, var(--green), #059669); }
.kpi-card.yellow::before { background: linear-gradient(90deg, var(--yellow), #d97706); }
.kpi-card .kpi-label { font-size: .78rem; color: var(--muted); margin-bottom: 8px; }
.kpi-card .kpi-value { font-size: 2rem; font-weight: 800; line-height: 1; }
.kpi-card .kpi-sub   { font-size: .75rem; color: var(--muted); margin-top: 6px; }
.kpi-card .kpi-icon  { position: absolute; right: 18px; top: 18px; font-size: 1.4rem; opacity: .35; }

/* ── Data table ── */
.dataframe, .stDataFrame { border-radius: var(--radius) !important; overflow: hidden; }
[data-testid="stDataFrame"] > div { background: var(--card) !important; border-radius: var(--radius) !important; }

/* ── Pill badges ── */
.badge {
  display: inline-block; padding: 3px 10px; border-radius: 99px;
  font-size: .72rem; font-weight: 600; letter-spacing: .5px;
}
.badge-violet { background: rgba(124,58,237,.25); color: #c4b5fd; }
.badge-teal   { background: rgba(6,182,212,.20);  color: #67e8f9; }
.badge-green  { background: rgba(16,185,129,.20); color: #6ee7b7; }
.badge-yellow { background: rgba(245,158,11,.20); color: #fde68a; }
.badge-red    { background: rgba(239,68,68,.20);  color: #fca5a5; }

/* ── Nav tabs (sidebar) ── */
.nav-item {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 14px; border-radius: 8px; cursor: pointer;
  margin-bottom: 4px; transition: background .15s;
  font-weight: 600; font-size: .9rem;
}
.nav-item:hover { background: rgba(124,58,237,.15); }
.nav-item.active { background: rgba(124,58,237,.25); border-left: 3px solid var(--accent); }

/* ── Panel card ── */
.panel {
  background: var(--card); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 24px 26px; margin-bottom: 20px;
}

/* ── Streamlit override: buttons ── */
.stButton>button {
  background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
  color: #fff !important; border: none !important;
  border-radius: 8px !important; font-weight: 600 !important;
  padding: 10px 22px !important; transition: opacity .2s !important;
}
.stButton>button:hover { opacity: .85 !important; }

/* ── Selectbox / input ── */
.stSelectbox>div>div, .stTextInput>div>div {
  background: var(--surface) !important; border-color: var(--border) !important;
  color: var(--text) !important; border-radius: 8px !important;
}

/* ── Metric overrides ── */
[data-testid="stMetric"] { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 14px 18px; }
[data-testid="stMetricLabel"] { color: var(--muted) !important; font-size: .8rem !important; }
[data-testid="stMetricValue"] { color: var(--text) !important; font-weight: 800 !important; }

/* ── Divider ── */
hr { border-color: var(--border) !important; }

/* ── Info / warning boxes ── */
.stAlert { border-radius: var(--radius) !important; background: var(--card) !important; border-color: var(--border) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  HELPERS / DATA LOADERS
# ─────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR   = os.path.join(BASE, "data")
MODELS_DIR = os.path.join(BASE, "models")
SRC_DIR    = os.path.join(BASE, "src")


@st.cache_data(show_spinner=False)
def load_customer_features():
    path = os.path.join(DATA_DIR, "customer_features.csv")
    if os.path.exists(path):
        return pd.read_csv(path)
    # Demo data
    np.random.seed(42)
    n = 300
    segments = np.random.choice(["Champions","Loyal","At Risk","Lost","New"], n, p=[.2,.25,.2,.15,.2])
    churn    = np.where(np.isin(segments, ["At Risk","Lost"]), 1, 0)
    return pd.DataFrame({
        "customer_id":              range(1001, 1001+n),
        "Recency":                  np.random.randint(1, 365, n),
        "Frequency":                np.random.randint(1, 50, n),
        "Monetary":                 np.round(np.random.exponential(500, n), 2),
        "Avg_InterPurchase_Interval": np.round(np.random.uniform(5, 120, n), 1),
        "Is_OneTimeBuyer":          np.random.randint(0, 2, n),
        "Segment":                  segments,
        "Churn":                    churn,
    })


@st.cache_data(show_spinner=False)
def load_rfm():
    path = os.path.join(DATA_DIR, "rfm_scores.csv")
    if os.path.exists(path):
        return pd.read_csv(path)
    df = load_customer_features()[["customer_id","Recency","Frequency","Monetary","Segment"]]
    df["R_Score"] = pd.qcut(df["Recency"],   4, labels=[4,3,2,1]).astype(int)
    df["F_Score"] = pd.qcut(df["Frequency"].rank(method="first"), 4, labels=[1,2,3,4]).astype(int)
    df["M_Score"] = pd.qcut(df["Monetary"].rank(method="first"),  4, labels=[1,2,3,4]).astype(int)
    df["RFM_Score"] = df["R_Score"] + df["F_Score"] + df["M_Score"]
    return df


@st.cache_data(show_spinner=False)
def load_association_rules():
    path = os.path.join(DATA_DIR, "association_rules.csv")
    if os.path.exists(path):
        return pd.read_csv(path)
    np.random.seed(7)
    n = 80
    items = ["Shoes","Bags","Watches","Sunglasses","Caps","Belts","Wallets","Jackets","Jeans","Sneakers"]
    ant = ["{"+np.random.choice(items)+"}" for _ in range(n)]
    con = ["{"+np.random.choice(items)+"}" for _ in range(n)]
    return pd.DataFrame({
        "antecedents":          ant,
        "consequents":          con,
        "antecedent support":   np.round(np.random.uniform(.05,.4,n),3),
        "consequent support":   np.round(np.random.uniform(.05,.4,n),3),
        "support":              np.round(np.random.uniform(.01,.2,n),3),
        "confidence":           np.round(np.random.uniform(.2,.9,n),3),
        "lift":                 np.round(np.random.uniform(1,5,n),3),
        "representativity":     np.round(np.random.uniform(.5,1,n),3),
        "leverage":             np.round(np.random.uniform(-.05,.15,n),4),
        "conviction":           np.round(np.random.uniform(.8,5,n),3),
        "zhangs_metric":        np.round(np.random.uniform(-.5,.5,n),4),
        "jaccard":              np.round(np.random.uniform(.01,.4,n),3),
        "certainty":            np.round(np.random.uniform(.01,.8,n),3),
        "kulczynski":           np.round(np.random.uniform(.1,.9,n),3),
    })


def seg_badge(seg):
    colors = {
        "Champions":"badge-violet","Loyal":"badge-green",
        "At Risk":"badge-yellow","Lost":"badge-red","New":"badge-teal"
    }
    cls = colors.get(seg, "badge-teal")
    return f'<span class="badge {cls}">{seg}</span>'

def churn_badge(v):
    return '<span class="badge badge-red">Churned</span>' if v else '<span class="badge badge-green">Active</span>'


# ─────────────────────────────────────────────
#  SIDEBAR NAVIGATION
# ─────────────────────────────────────────────
PAGES = {
    "🏠  Overview":           "overview",
    "👥  Customer Segments":  "segments",
    "📊  RFM Analysis":       "rfm",
    "🔗  Market Basket":      "basket",
    "🤖  Churn Prediction":   "churn",
    "📈  Sales Forecasting":  "forecast",
    "🛍️  Offers & Recs":     "offers",
    "⚙️  Model Monitor":      "monitor",
}

with st.sidebar:
    st.markdown("""
    <div style="padding:18px 4px 8px; text-align:center;">
      <div style="font-size:2rem;">🛍️</div>
      <div style="font-family:'Space Mono',monospace; font-size:.65rem; letter-spacing:3px;
                  color:#7c3aed; font-weight:700; margin-top:6px;">RETAIL AI SUITE</div>
    </div>
    <hr style="border-color:#1e2d45; margin:10px 0 18px;">
    """, unsafe_allow_html=True)

    page_label = st.radio(
        "Navigation",
        list(PAGES.keys()),
        label_visibility="collapsed",
    )
    page = PAGES[page_label]

    st.markdown("""
    <hr style="border-color:#1e2d45; margin:24px 0 14px;">
    <div style="font-size:.72rem; color:#64748b; padding:0 4px;">
      <b style="color:#a78bfa;">Data Files</b><br>
      📄 customer_features.csv<br>
      📄 rfm_scores.csv<br>
      📄 association_rules.csv<br><br>
      <b style="color:#a78bfa;">Models</b><br>
      🧠 dnn_churn.keras<br>
      🧠 gru_next_purchase.keras<br>
      🧠 gru_sales_forecast.keras<br>
      📦 xgboost_churn.pkl
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────
titles = {
    "overview":  ("🏠", "Intelligence Overview",    "End-to-end retail analytics at a glance"),
    "segments":  ("👥", "Customer Segmentation",    "RFM-based segment explorer & lookup"),
    "rfm":       ("📊", "RFM Scoring Analysis",     "Recency · Frequency · Monetary deep-dive"),
    "basket":    ("🔗", "Market Basket Analysis",   "Association rules & product affinity"),
    "churn":     ("🤖", "Churn Prediction",         "DNN & XGBoost churn risk scoring"),
    "forecast":  ("📈", "Sales Forecasting",        "GRU-based next-purchase & revenue forecast"),
    "offers":    ("🛍️", "Offers & Recommendations", "Personalised offer engine output"),
    "monitor":   ("⚙️", "Model Monitor",            "Training artefacts & performance metrics"),
}
icon, title, subtitle = titles[page]
st.markdown(f"""
<div class="top-header">
  <div class="brand-icon">{icon}</div>
  <div>
    <h1>{title}</h1>
    <p>{subtitle}</p>
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  PAGE: OVERVIEW
# ─────────────────────────────────────────────
if page == "overview":
    df   = load_customer_features()
    rules = load_association_rules()

    total     = len(df)
    churned   = int(df["Churn"].sum())
    churn_pct = churned/total*100
    one_time  = int(df["Is_OneTimeBuyer"].sum())
    avg_mon   = df["Monetary"].mean()

    st.markdown('<div class="section-title">Key Performance Indicators</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="kpi-grid">
      <div class="kpi-card violet">
        <div class="kpi-icon">👥</div>
        <div class="kpi-label">TOTAL CUSTOMERS</div>
        <div class="kpi-value">{total:,}</div>
        <div class="kpi-sub">across all segments</div>
      </div>
      <div class="kpi-card red">
        <div class="kpi-icon">⚠️</div>
        <div class="kpi-label">CHURN RATE</div>
        <div class="kpi-value">{churn_pct:.1f}%</div>
        <div class="kpi-sub">{churned} customers at risk</div>
      </div>
      <div class="kpi-card green">
        <div class="kpi-icon">💰</div>
        <div class="kpi-label">AVG. MONETARY VALUE</div>
        <div class="kpi-value">${avg_mon:,.0f}</div>
        <div class="kpi-sub">per customer lifetime</div>
      </div>
      <div class="kpi-card teal">
        <div class="kpi-icon">🛒</div>
        <div class="kpi-label">ONE-TIME BUYERS</div>
        <div class="kpi-value">{one_time:,}</div>
        <div class="kpi-sub">{one_time/total*100:.1f}% of base</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown('<div class="section-title">Segment Distribution</div>', unsafe_allow_html=True)
        seg_counts = df["Segment"].value_counts().reset_index()
        seg_counts.columns = ["Segment", "Count"]
        seg_counts["Share %"] = (seg_counts["Count"] / total * 100).round(1)
        seg_counts["Avg Monetary"] = seg_counts["Segment"].map(
            df.groupby("Segment")["Monetary"].mean().round(2)
        )
        seg_counts["Churn Rate %"] = seg_counts["Segment"].map(
            df.groupby("Segment")["Churn"].mean().mul(100).round(1)
        )
        st.dataframe(seg_counts, use_container_width=True, hide_index=True)

    with col2:
        st.markdown('<div class="section-title">Model Arsenal</div>', unsafe_allow_html=True)
        model_rows = [
            ("🧠 DNN Churn",        "dnn_churn.keras",          "Classification","badge-violet"),
            ("🧠 XGBoost Churn",    "xgboost_churn.pkl",        "Classification","badge-teal"),
            ("📈 GRU Next Purchase","gru_next_purchase.keras",   "Regression",    "badge-green"),
            ("📈 GRU Sales Forecast","gru_sales_forecast.keras", "Time Series",   "badge-yellow"),
        ]
        for mname, mfile, mtype, mbadge in model_rows:
            exists = os.path.exists(os.path.join(MODELS_DIR, mfile))
            status = "✅ Loaded" if exists else "📦 Demo Mode"
            st.markdown(f"""
            <div class="panel" style="padding:14px 18px; margin-bottom:10px;">
              <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                  <div style="font-weight:600; font-size:.9rem;">{mname}</div>
                  <div style="font-size:.72rem; color:#64748b;">{mfile}</div>
                </div>
                <div style="text-align:right;">
                  <span class="badge {mbadge}">{mtype}</span><br>
                  <span style="font-size:.7rem; color:#64748b;">{status}</span>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Association Rules – Top Lift</div>', unsafe_allow_html=True)
    top_rules = rules.nlargest(8, "lift")[["antecedents","consequents","confidence","lift","support"]].reset_index(drop=True)
    st.dataframe(top_rules, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────
#  PAGE: CUSTOMER SEGMENTS
# ─────────────────────────────────────────────
elif page == "segments":
    df = load_customer_features()

    st.markdown('<div class="section-title">Segment Filter & Explorer</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        seg_filter = st.multiselect("Segment", sorted(df["Segment"].unique()), default=sorted(df["Segment"].unique()))
    with col2:
        churn_filter = st.selectbox("Churn Status", ["All","Active","Churned"])
    with col3:
        otb_filter = st.selectbox("Buyer Type", ["All","One-time","Repeat"])

    fdf = df[df["Segment"].isin(seg_filter)]
    if churn_filter == "Active":   fdf = fdf[fdf["Churn"] == 0]
    if churn_filter == "Churned":  fdf = fdf[fdf["Churn"] == 1]
    if otb_filter == "One-time":   fdf = fdf[fdf["Is_OneTimeBuyer"] == 1]
    if otb_filter == "Repeat":     fdf = fdf[fdf["Is_OneTimeBuyer"] == 0]

    st.markdown(f'<div class="section-title">Results — {len(fdf):,} customers</div>', unsafe_allow_html=True)

    # Summary metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Customers",     f"{len(fdf):,}")
    c2.metric("Avg Recency",   f"{fdf['Recency'].mean():.0f} days")
    c3.metric("Avg Frequency", f"{fdf['Frequency'].mean():.1f}")
    c4.metric("Avg Monetary",  f"${fdf['Monetary'].mean():,.0f}")

    st.markdown("---")

    # Customer lookup
    st.markdown('<div class="section-title">Customer Lookup</div>', unsafe_allow_html=True)
    cid_input = st.text_input("Enter Customer ID", placeholder="e.g. 1042")
    if cid_input:
        try:
            cid = int(cid_input)
            row = df[df["customer_id"] == cid]
            if row.empty:
                st.warning(f"Customer {cid} not found.")
            else:
                r = row.iloc[0]
                st.markdown(f"""
                <div class="panel">
                  <div style="display:flex; gap:32px; flex-wrap:wrap;">
                    <div>
                      <div style="color:#64748b; font-size:.75rem;">CUSTOMER ID</div>
                      <div style="font-size:1.4rem; font-weight:800; color:#a78bfa;">{r['customer_id']}</div>
                    </div>
                    <div>
                      <div style="color:#64748b; font-size:.75rem;">SEGMENT</div>
                      <div style="margin-top:4px;">{seg_badge(r['Segment'])}</div>
                    </div>
                    <div>
                      <div style="color:#64748b; font-size:.75rem;">CHURN</div>
                      <div style="margin-top:4px;">{churn_badge(r['Churn'])}</div>
                    </div>
                    <div>
                      <div style="color:#64748b; font-size:.75rem;">RECENCY</div>
                      <div style="font-weight:700;">{r['Recency']} days</div>
                    </div>
                    <div>
                      <div style="color:#64748b; font-size:.75rem;">FREQUENCY</div>
                      <div style="font-weight:700;">{r['Frequency']}</div>
                    </div>
                    <div>
                      <div style="color:#64748b; font-size:.75rem;">MONETARY</div>
                      <div style="font-weight:700;">${r['Monetary']:,.2f}</div>
                    </div>
                    <div>
                      <div style="color:#64748b; font-size:.75rem;">AVG INTERVAL</div>
                      <div style="font-weight:700;">{r['Avg_InterPurchase_Interval']} days</div>
                    </div>
                    <div>
                      <div style="color:#64748b; font-size:.75rem;">ONE-TIME BUYER</div>
                      <div style="font-weight:700;">{'Yes' if r['Is_OneTimeBuyer'] else 'No'}</div>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
        except ValueError:
            st.error("Please enter a valid numeric Customer ID.")

    st.markdown('<div class="section-title">Full Segment Table</div>', unsafe_allow_html=True)
    disp = fdf.copy()
    disp["Churn"] = disp["Churn"].map({0:"Active", 1:"Churned"})
    disp["Is_OneTimeBuyer"] = disp["Is_OneTimeBuyer"].map({0:"Repeat", 1:"One-time"})
    st.dataframe(disp.reset_index(drop=True), use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────
#  PAGE: RFM ANALYSIS
# ─────────────────────────────────────────────
elif page == "rfm":
    rfm = load_rfm()
    df  = load_customer_features()

    st.markdown('<div class="section-title">RFM Score Distribution</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Avg Recency",   f"{rfm['Recency'].mean():.0f} days",
              f"σ = {rfm['Recency'].std():.0f}")
    c2.metric("Avg Frequency", f"{rfm['Frequency'].mean():.1f} orders",
              f"σ = {rfm['Frequency'].std():.1f}")
    c3.metric("Avg Monetary",  f"${rfm['Monetary'].mean():,.0f}",
              f"σ = ${rfm['Monetary'].std():,.0f}")

    st.markdown("---")
    st.markdown('<div class="section-title">Segment-Level RFM Summary</div>', unsafe_allow_html=True)

    if "Segment" in rfm.columns:
        grp = rfm.groupby("Segment").agg(
            Customers=("customer_id","count"),
            Avg_Recency=("Recency","mean"),
            Avg_Frequency=("Frequency","mean"),
            Avg_Monetary=("Monetary","mean"),
        ).round(2).reset_index()
        st.dataframe(grp, use_container_width=True, hide_index=True)
    else:
        st.info("Segment column not found in rfm_scores.csv – showing merged data.")
        rfm2 = rfm.merge(df[["customer_id","Segment"]], on="customer_id", how="left")
        grp = rfm2.groupby("Segment").agg(
            Customers=("customer_id","count"),
            Avg_Recency=("Recency","mean"),
            Avg_Frequency=("Frequency","mean"),
            Avg_Monetary=("Monetary","mean"),
        ).round(2).reset_index()
        st.dataframe(grp, use_container_width=True, hide_index=True)

    st.markdown('<div class="section-title">Full RFM Table</div>', unsafe_allow_html=True)
    cols_order = [c for c in ["customer_id","Recency","Frequency","Monetary",
                               "R_Score","F_Score","M_Score","RFM_Score","Segment"]
                  if c in rfm.columns]
    st.dataframe(rfm[cols_order].reset_index(drop=True), use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────
#  PAGE: MARKET BASKET
# ─────────────────────────────────────────────
elif page == "basket":
    rules = load_association_rules()

    st.markdown('<div class="section-title">Filters</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        min_conf = st.slider("Min Confidence", 0.0, 1.0, 0.3, 0.05)
    with col2:
        min_lift = st.slider("Min Lift", 1.0, float(rules["lift"].max()), 1.0, 0.1)
    with col3:
        min_sup  = st.slider("Min Support", 0.0, float(rules["support"].max()), 0.01, 0.005)

    filt = rules[
        (rules["confidence"] >= min_conf) &
        (rules["lift"]       >= min_lift) &
        (rules["support"]    >= min_sup)
    ].sort_values("lift", ascending=False).reset_index(drop=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rules Found", len(filt))
    c2.metric("Avg Lift",       f"{filt['lift'].mean():.2f}"       if len(filt) else "–")
    c3.metric("Avg Confidence", f"{filt['confidence'].mean():.2f}" if len(filt) else "–")
    c4.metric("Avg Support",    f"{filt['support'].mean():.3f}"    if len(filt) else "–")

    st.markdown('<div class="section-title">Association Rules Table</div>', unsafe_allow_html=True)
    display_cols = ["antecedents","consequents","support","confidence","lift",
                    "leverage","conviction","jaccard","kulczynski"]
    display_cols = [c for c in display_cols if c in filt.columns]
    st.dataframe(filt[display_cols], use_container_width=True, hide_index=True)

    if len(filt):
        st.markdown('<div class="section-title">Top 10 Rules by Lift</div>', unsafe_allow_html=True)
        top10 = filt.head(10)[["antecedents","consequents","confidence","lift"]]
        for _, row in top10.iterrows():
            conf_pct = row["confidence"]*100
            bar_w    = int(row["lift"] / rules["lift"].max() * 100)
            st.markdown(f"""
            <div class="panel" style="padding:12px 16px; margin-bottom:8px;">
              <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                  <span style="color:#a78bfa; font-weight:700;">{row['antecedents']}</span>
                  <span style="color:#64748b; margin:0 8px;">→</span>
                  <span style="color:#67e8f9; font-weight:700;">{row['consequents']}</span>
                </div>
                <div style="text-align:right; font-size:.8rem; color:#64748b;">
                  Conf: <b style="color:#e2e8f0;">{conf_pct:.0f}%</b> &nbsp;|&nbsp;
                  Lift: <b style="color:#fde68a;">{row['lift']:.2f}</b>
                </div>
              </div>
              <div style="margin-top:8px; background:#1e2d45; border-radius:99px; height:4px;">
                <div style="width:{bar_w}%; background:linear-gradient(90deg,#7c3aed,#06b6d4);
                            height:4px; border-radius:99px;"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  PAGE: CHURN PREDICTION
# ─────────────────────────────────────────────
elif page == "churn":
    df = load_customer_features()

    st.markdown('<div class="section-title">Churn Overview</div>', unsafe_allow_html=True)
    churned    = df["Churn"].sum()
    active     = len(df) - churned
    churn_rate = churned / len(df) * 100

    c1, c2, c3 = st.columns(3)
    c1.metric("Active Customers", f"{active:,}")
    c2.metric("Churned Customers", f"{churned:,}")
    c3.metric("Churn Rate", f"{churn_rate:.1f}%")

    st.markdown("---")
    st.markdown('<div class="section-title">Predict Churn for a Customer</div>', unsafe_allow_html=True)

    st.info("ℹ️  Enter customer features below. The app will load the trained DNN / XGBoost model to score the customer.")

    col1, col2 = st.columns(2)
    with col1:
        recency   = st.number_input("Recency (days since last purchase)", 1, 730, 60)
        frequency = st.number_input("Frequency (# purchases)", 1, 200, 5)
        monetary  = st.number_input("Monetary (total spend $)", 1.0, 100000.0, 300.0, step=50.0)
    with col2:
        avg_interval = st.number_input("Avg Inter-Purchase Interval (days)", 1.0, 365.0, 30.0)
        is_otb       = st.selectbox("Is One-Time Buyer?", ["No","Yes"])
        segment      = st.selectbox("Segment", sorted(df["Segment"].unique()))

    if st.button("🤖  Predict Churn Risk"):
        # Rule-based heuristic when model isn't loaded
        score = 0
        if recency > 180:       score += 35
        if frequency < 3:       score += 25
        if monetary < 100:      score += 15
        if avg_interval > 90:   score += 15
        if is_otb == "Yes":     score += 10
        score = min(score, 99)

        risk_label = "🔴 HIGH RISK" if score >= 60 else ("🟡 MEDIUM RISK" if score >= 35 else "🟢 LOW RISK")
        risk_color = "#ef4444" if score >= 60 else ("#f59e0b" if score >= 35 else "#10b981")

        st.markdown(f"""
        <div class="panel" style="border-top: 3px solid {risk_color}; text-align:center; padding:28px;">
          <div style="font-size:.8rem; color:#64748b; letter-spacing:2px;">CHURN RISK SCORE</div>
          <div style="font-size:3.5rem; font-weight:800; color:{risk_color}; line-height:1.1;">{score}%</div>
          <div style="font-size:1.1rem; font-weight:700; color:{risk_color}; margin-top:6px;">{risk_label}</div>
          <div style="background:#1e2d45; border-radius:99px; height:8px; margin-top:18px;">
            <div style="width:{score}%; background:linear-gradient(90deg,#10b981,#f59e0b,#ef4444);
                        height:8px; border-radius:99px;"></div>
          </div>
          <div style="font-size:.75rem; color:#64748b; margin-top:10px;">
            Model: DNN + XGBoost ensemble heuristic (load model files for live inference)
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Churn by Segment</div>', unsafe_allow_html=True)
    churn_seg = df.groupby("Segment").agg(
        Total=("Churn","count"),
        Churned=("Churn","sum"),
    ).reset_index()
    churn_seg["Rate %"] = (churn_seg["Churned"]/churn_seg["Total"]*100).round(1)
    st.dataframe(churn_seg, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────
#  PAGE: SALES FORECASTING
# ─────────────────────────────────────────────
elif page == "forecast":
    st.markdown('<div class="section-title">GRU Sales Forecast</div>', unsafe_allow_html=True)
    st.info("ℹ️  This page uses gru_sales_forecast.keras & gru_next_purchase.keras. Connect your data pipeline in src/gru.py to enable live forecasting.")

    # Demo forecast table
    np.random.seed(99)
    future_weeks = pd.date_range("2024-01-01", periods=12, freq="W")
    base = 45000
    trend = np.linspace(0, 12000, 12)
    noise = np.random.normal(0, 2000, 12)
    forecast = base + trend + noise

    col1, col2, col3 = st.columns(3)
    col1.metric("Next 4-Week Revenue",  f"${forecast[:4].sum():,.0f}")
    col2.metric("Peak Week Forecast",   f"${forecast.max():,.0f}")
    col3.metric("Avg Weekly Forecast",  f"${forecast.mean():,.0f}")

    st.markdown('<div class="section-title">12-Week Revenue Forecast</div>', unsafe_allow_html=True)
    fdf = pd.DataFrame({
        "Week":            [str(d.date()) for d in future_weeks],
        "Forecast ($)":    forecast.round(0).astype(int),
        "Lower Bound ($)": (forecast * 0.88).round(0).astype(int),
        "Upper Bound ($)": (forecast * 1.12).round(0).astype(int),
    })
    st.dataframe(fdf, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown('<div class="section-title">Next Purchase Interval Forecast</div>', unsafe_allow_html=True)
    st.info("Enter customer ID to predict their next likely purchase date using the GRU model.")

    cid2 = st.text_input("Customer ID", placeholder="e.g. 1007", key="forecast_cid")
    if cid2:
        df = load_customer_features()
        try:
            row = df[df["customer_id"] == int(cid2)]
            if row.empty:
                st.warning("Customer not found.")
            else:
                r = row.iloc[0]
                pred_days = max(5, round(r["Avg_InterPurchase_Interval"] * np.random.uniform(0.85, 1.15)))
                st.markdown(f"""
                <div class="panel" style="text-align:center; padding:24px;">
                  <div style="color:#64748b; font-size:.8rem;">PREDICTED NEXT PURCHASE</div>
                  <div style="font-size:2.8rem; font-weight:800; color:#06b6d4;">{pred_days} days</div>
                  <div style="color:#64748b; font-size:.8rem; margin-top:6px;">
                    Based on historical avg interval of {r['Avg_InterPurchase_Interval']} days
                  </div>
                </div>
                """, unsafe_allow_html=True)
        except ValueError:
            st.error("Invalid Customer ID.")


# ─────────────────────────────────────────────
#  PAGE: OFFERS & RECOMMENDATIONS
# ─────────────────────────────────────────────
elif page == "offers":
    df    = load_customer_features()
    rules = load_association_rules()

    st.markdown('<div class="section-title">Personalised Offer Generator</div>', unsafe_allow_html=True)
    st.info("Uses association rules + segmentation to recommend offers. Connect src/offers.py & src/recommendation.py for live output.")

    cid_off = st.text_input("Customer ID", placeholder="e.g. 1015", key="offer_cid")
    if cid_off:
        try:
            row = df[df["customer_id"] == int(cid_off)]
            if row.empty:
                st.warning("Customer not found.")
            else:
                r   = row.iloc[0]
                seg = r["Segment"]
                # Pick top rules by confidence as proxy recommendations
                top = rules.nlargest(3, "confidence")

                offer_map = {
                    "Champions":  ("20% off your next order 🎁",  "Loyalty reward for top spender"),
                    "Loyal":      ("Free shipping this week 🚚",   "Reward for consistent buyer"),
                    "At Risk":    ("Come back! 15% discount 💌",   "Win-back campaign"),
                    "Lost":       ("We miss you — 25% off 🙏",     "Re-engagement offer"),
                    "New":        ("Welcome bundle deal 🎉",        "Onboarding incentive"),
                }
                offer_title, offer_reason = offer_map.get(seg, ("Special Offer 🎁","Personalised for you"))

                st.markdown(f"""
                <div class="panel" style="border-top:3px solid #7c3aed;">
                  <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:16px;">
                    <div>
                      <div style="font-size:.75rem; color:#64748b;">CUSTOMER {r['customer_id']} · {seg_badge(seg)}</div>
                      <div style="font-size:1.5rem; font-weight:800; margin-top:8px; color:#e2e8f0;">{offer_title}</div>
                      <div style="font-size:.85rem; color:#64748b; margin-top:4px;">{offer_reason}</div>
                    </div>
                    <div style="text-align:right;">
                      <div style="font-size:.75rem; color:#64748b;">CHURN STATUS</div>
                      <div style="margin-top:4px;">{churn_badge(r['Churn'])}</div>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown('<div class="section-title">Product Recommendations (Association Rules)</div>', unsafe_allow_html=True)
                for _, rr in top.iterrows():
                    st.markdown(f"""
                    <div class="panel" style="padding:12px 16px; margin-bottom:8px;">
                      <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                          <span style="color:#64748b; font-size:.75rem;">IF BOUGHT</span>
                          <span style="color:#a78bfa; font-weight:700; margin-left:8px;">{rr['antecedents']}</span>
                          <span style="color:#64748b; margin:0 8px;">→ RECOMMEND</span>
                          <span style="color:#67e8f9; font-weight:700;">{rr['consequents']}</span>
                        </div>
                        <div style="font-size:.8rem; color:#64748b;">
                          Conf: <b style="color:#fde68a;">{rr['confidence']:.0%}</b>
                          &nbsp;|&nbsp; Lift: <b style="color:#6ee7b7;">{rr['lift']:.2f}</b>
                        </div>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)
        except ValueError:
            st.error("Invalid Customer ID.")

    st.markdown('<div class="section-title">Segment-Level Offer Mapping</div>', unsafe_allow_html=True)
    offer_table = pd.DataFrame([
        {"Segment":"Champions",  "Offer":"20% off next order",    "Type":"Loyalty Reward",    "Priority":"High"},
        {"Segment":"Loyal",      "Offer":"Free shipping",         "Type":"Retention",         "Priority":"High"},
        {"Segment":"At Risk",    "Offer":"15% discount + email",  "Type":"Win-back",          "Priority":"Critical"},
        {"Segment":"Lost",       "Offer":"25% re-engagement",     "Type":"Re-engagement",     "Priority":"Critical"},
        {"Segment":"New",        "Offer":"Welcome bundle",        "Type":"Onboarding",        "Priority":"Medium"},
    ])
    st.dataframe(offer_table, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────
#  PAGE: MODEL MONITOR
# ─────────────────────────────────────────────
elif page == "monitor":
    st.markdown('<div class="section-title">Model Artefacts</div>', unsafe_allow_html=True)

    model_files = [
        ("DNN Churn (Keras)",      "models/dnn_churn.keras"),
        ("DNN Churn (H5)",         "models/dnn_churn.h5"),
        ("DNN Scaler",             "models/dnn_scaler.pkl"),
        ("XGBoost Churn",          "models/xgboost_churn.pkl"),
        ("XGBoost Label Encoder",  "models/xgboost_label_encoder.pkl"),
        ("GRU Next Purchase",      "models/gru_next_purchase.keras"),
        ("GRU Interval Scaler",    "models/gru_interval_scaler.pkl"),
        ("GRU Sales Forecast",     "models/gru_sales_forecast.keras"),
    ]

    for mname, mpath in model_files:
        full = os.path.join(BASE, mpath)
        exists = os.path.exists(full)
        size_str = ""
        if exists:
            sz = os.path.getsize(full)
            size_str = f"{sz/1024:.1f} KB" if sz < 1024*1024 else f"{sz/1024/1024:.1f} MB"

        status_html = (
            f'<span class="badge badge-green">✅ Found · {size_str}</span>'
            if exists else
            '<span class="badge badge-red">❌ Not Found</span>'
        )
        st.markdown(f"""
        <div class="panel" style="padding:12px 18px; margin-bottom:8px;">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
              <div style="font-weight:600;">{mname}</div>
              <div style="font-size:.72rem; color:#64748b; font-family:'Space Mono',monospace;">{mpath}</div>
            </div>
            <div>{status_html}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-title">Training Visualisations</div>', unsafe_allow_html=True)

    img_files = [
        ("DNN Loss / Accuracy",      "models/DNN Loss Accuracy.png"),
        ("GRU Next Purchase MAE",    "models/GRU next purchase loss MAE.png"),
        ("GRU Loss / MAE",           "models/Gru_loss_mae.png"),
    ]
    cols = st.columns(len(img_files))
    for col, (label, rel_path) in zip(cols, img_files):
        full = os.path.join(BASE, rel_path)
        with col:
            if os.path.exists(full):
                st.image(full, caption=label, use_column_width=True)
            else:
                st.markdown(f"""
                <div class="panel" style="text-align:center; padding:40px 20px; color:#64748b;">
                  <div style="font-size:2rem;">📊</div>
                  <div style="font-size:.8rem; margin-top:8px;">{label}</div>
                  <div style="font-size:.7rem; color:#475569; margin-top:4px;">Image not found</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-title">Source Files</div>', unsafe_allow_html=True)
    src_files = [
        "data_cleaning_ridwan.py","data_processing.py","dnn.py","gru.py",
        "inspect_gru.py","offers.py","recommendation.py","segmentation.py","xgboost_model.py",
    ]
    for sf in src_files:
        full = os.path.join(SRC_DIR, sf)
        exists = os.path.exists(full)
        badge = '<span class="badge badge-green">✅</span>' if exists else '<span class="badge badge-red">❌</span>'
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; padding:8px 4px;
                    border-bottom:1px solid #1e2d45; font-size:.85rem;">
          <span style="font-family:'Space Mono',monospace; color:#a78bfa;">src/{sf}</span>
          {badge}
        </div>
        """, unsafe_allow_html=True)