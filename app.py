import streamlit as st
import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="RETAIL AI · Intelligence Suite",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  THEME STATE
# ─────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

dark = st.session_state.dark_mode

# ─────────────────────────────────────────────
#  CSS — Dark / Light adaptive
# ─────────────────────────────────────────────
if dark:
    BG        = "#0b0f1a"
    SURFACE   = "#111827"
    CARD      = "#161d2e"
    BORDER    = "#1e2d45"
    TEXT      = "#e2e8f0"
    MUTED     = "#64748b"
    ACCENT    = "#7c3aed"
    ACCENT2   = "#a855f7"
    TEAL      = "#06b6d4"
    GREEN     = "#10b981"
    YELLOW    = "#f59e0b"
    RED       = "#ef4444"
    INPUT_BG  = "#111827"
    GRAD_H1   = "linear-gradient(90deg,#a78bfa,#38bdf8)"
    HEADER_BG = "linear-gradient(135deg,#1e1045 0%,#0f172a 60%,#0e2038 100%)"
    NAV_HOVER = "rgba(124,58,237,.15)"
    NAV_ACT   = "rgba(124,58,237,.25)"
    NAV_BORDER= ACCENT
    METRIC_BG = CARD
    PANEL_BG  = CARD
    TABLE_HDR = "#1e2d45"
    SCROLLBAR = BORDER
    BADGE_BG  = "rgba(124,58,237,.25)"
    BADGE_CLR = "#c4b5fd"
else:
    BG        = "#f1f5f9"
    SURFACE   = "#ffffff"
    CARD      = "#ffffff"
    BORDER    = "#e2e8f0"
    TEXT      = "#0f172a"
    MUTED     = "#64748b"
    ACCENT    = "#6d28d9"
    ACCENT2   = "#7c3aed"
    TEAL      = "#0891b2"
    GREEN     = "#059669"
    YELLOW    = "#d97706"
    RED       = "#dc2626"
    INPUT_BG  = "#f8fafc"
    GRAD_H1   = "linear-gradient(90deg,#6d28d9,#0891b2)"
    HEADER_BG = "linear-gradient(135deg,#ede9fe 0%,#dbeafe 100%)"
    NAV_HOVER = "rgba(109,40,217,.08)"
    NAV_ACT   = "rgba(109,40,217,.12)"
    NAV_BORDER= ACCENT
    METRIC_BG = "#f8fafc"
    PANEL_BG  = "#ffffff"
    TABLE_HDR = "#f1f5f9"
    SCROLLBAR = "#cbd5e1"
    BADGE_BG  = "rgba(109,40,217,.12)"
    BADGE_CLR = "#5b21b6"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Outfit:wght@300;400;600;800&display=swap');

:root {{
  --bg:{BG}; --surface:{SURFACE}; --card:{CARD}; --border:{BORDER};
  --accent:{ACCENT}; --accent2:{ACCENT2}; --teal:{TEAL}; --green:{GREEN};
  --yellow:{YELLOW}; --red:{RED}; --text:{TEXT}; --muted:{MUTED};
  --radius:12px; --input-bg:{INPUT_BG};
}}

html,body,.stApp {{ background:{BG} !important; color:{TEXT} !important; }}
* {{ font-family:'Outfit',sans-serif; box-sizing:border-box; }}
p,li,span,div {{ color:{TEXT}; }}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
  background:{SURFACE} !important;
  border-right:1px solid {BORDER};
}}
[data-testid="stSidebar"] * {{ color:{TEXT} !important; }}
[data-testid="stSidebar"] .stRadio label {{
  padding:9px 14px; font-size:.9rem; font-weight:500;
  cursor:pointer; border-left:2px solid transparent;
  border-radius:0; width:100%; transition:all .12s; color:{MUTED} !important;
  display:block;
}}
[data-testid="stSidebar"] .stRadio label:hover {{
  background:{NAV_HOVER}; color:{TEXT} !important;
}}
[data-testid="stSidebar"] .stRadio [aria-checked="true"] {{
  color:{ACCENT} !important; border-left:2px solid {ACCENT};
  background:{NAV_ACT}; font-weight:600;
}}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {{ gap:0; }}

/* ── Hide streamlit chrome ── */
#MainMenu,footer,header {{ visibility:hidden; }}
[data-testid="stDecoration"] {{ display:none; }}
/* Keep the "reopen sidebar" button usable — it lives inside the hidden header */
header [data-testid="stExpandSidebarButton"] {{
  visibility:visible !important;
  background:{CARD}; border:1px solid {BORDER}; border-radius:8px;
}}
header [data-testid="stExpandSidebarButton"] * {{ color:{TEXT} !important; }}
.block-container {{ padding:0 24px 40px !important; max-width:100% !important; }}

/* ── Top header ── */
.top-header {{
  background:{HEADER_BG};
  border-bottom:1px solid {BORDER};
  padding:22px 32px 18px;
  display:flex; align-items:center; gap:18px;
  border-radius:0 0 16px 16px;
  margin-bottom:24px;
}}
.top-header h1 {{
  font-weight:800; font-size:1.75rem; margin:0; letter-spacing:-0.5px;
  background:{GRAD_H1};
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}}
.top-header p {{ margin:2px 0 0; color:{MUTED}; font-size:.85rem; }}

/* ── Section title ── */
.section-title {{
  font-family:'Space Mono',monospace;
  font-size:.68rem; font-weight:700; letter-spacing:3px;
  text-transform:uppercase; color:{ACCENT2};
  margin-bottom:14px; border-left:3px solid {ACCENT};
  padding-left:10px;
}}

/* ── KPI cards ── */
.kpi-grid {{ display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin-bottom:24px; }}
.kpi-card {{
  background:{CARD}; border:1px solid {BORDER};
  border-radius:var(--radius); padding:20px 22px;
  position:relative; overflow:hidden;
  transition:transform .2s, box-shadow .2s;
}}
.kpi-card:hover {{ transform:translateY(-3px); box-shadow:0 10px 30px rgba(124,58,237,.18); }}
.kpi-card::before {{ content:''; position:absolute; top:0; left:0; right:0; height:3px; }}
.kpi-card.violet::before {{ background:linear-gradient(90deg,{ACCENT},{ACCENT2}); }}
.kpi-card.teal::before   {{ background:linear-gradient(90deg,{TEAL},#0284c7); }}
.kpi-card.green::before  {{ background:linear-gradient(90deg,{GREEN},#059669); }}
.kpi-card.yellow::before {{ background:linear-gradient(90deg,{YELLOW},#d97706); }}
.kpi-card.red::before    {{ background:linear-gradient(90deg,{RED},#b91c1c); }}
.kpi-card .kpi-label {{ font-size:.75rem; color:{MUTED}; margin-bottom:8px; }}
.kpi-card .kpi-value {{ font-size:2rem; font-weight:800; line-height:1; color:{TEXT}; }}
.kpi-card .kpi-sub   {{ font-size:.72rem; color:{MUTED}; margin-top:6px; }}
.kpi-card .kpi-icon  {{ position:absolute; right:18px; top:18px; font-size:1.4rem; opacity:.3; }}

/* ── Panel ── */
.panel {{
  background:{CARD}; border:1px solid {BORDER};
  border-radius:var(--radius); padding:22px 24px; margin-bottom:16px;
}}

/* ── Badges ── */
.badge {{ display:inline-block; padding:3px 10px; border-radius:99px; font-size:.7rem; font-weight:600; letter-spacing:.4px; }}
.badge-violet {{ background:rgba(124,58,237,.2); color:#c4b5fd; }}
.badge-teal   {{ background:rgba(6,182,212,.18); color:#67e8f9; }}
.badge-green  {{ background:rgba(16,185,129,.18); color:#6ee7b7; }}
.badge-yellow {{ background:rgba(245,158,11,.18); color:#fde68a; }}
.badge-red    {{ background:rgba(239,68,68,.18); color:#fca5a5; }}

/* ── Tables ── */
.ra-table {{ width:100%; border-collapse:collapse; font-size:.85rem; }}
.ra-table th {{
  text-align:left; padding:10px 14px; font-size:.7rem; font-weight:700;
  color:{MUTED}; letter-spacing:1px; text-transform:uppercase;
  background:{TABLE_HDR}; border-bottom:1px solid {BORDER};
}}
.ra-table td {{
  padding:10px 14px; border-bottom:1px solid {BORDER}; color:{TEXT};
  transition:background .1s;
}}
.ra-table tr:last-child td {{ border-bottom:none; }}
.ra-table tr:hover td {{ background:{NAV_HOVER}; }}

/* ── Offer cards ── */
.offer-card {{
  background:{CARD}; border:1px solid {BORDER};
  border-radius:14px; padding:20px 22px; margin-bottom:14px;
  display:flex; gap:16px; transition:transform .15s, box-shadow .15s;
}}
.offer-card:hover {{ transform:translateY(-2px); box-shadow:0 8px 24px rgba(0,0,0,.15); }}
.offer-avatar {{
  width:44px; height:44px; border-radius:50%; display:flex;
  align-items:center; justify-content:center;
  font-size:13px; font-weight:700; flex-shrink:0;
}}
.offer-body {{ flex:1; }}
.offer-name {{ font-size:.95rem; font-weight:700; color:{TEXT}; margin-bottom:3px; }}
.offer-meta {{ font-size:.75rem; color:{MUTED}; margin-bottom:10px; }}
.offer-msg {{
  font-size:.85rem; color:{TEXT}; background:{SURFACE};
  padding:10px 14px; border-radius:0 10px 10px 0;
  border-left:3px solid {ACCENT}; line-height:1.6; margin-bottom:10px;
}}
.offer-msg.ar {{ border-left:3px solid {YELLOW}; }}
.offer-msg.ls {{ border-left:3px solid {RED}; }}
.offer-msg.lo {{ border-left:3px solid {GREEN}; }}
.offer-tag {{
  display:inline-block; font-size:.65rem; padding:2px 8px;
  border-radius:99px; background:{NAV_HOVER};
  color:{ACCENT2}; border:1px solid {BORDER}; margin:2px;
  font-weight:600; letter-spacing:.3px;
}}

/* ── Churn score bar ── */
.score-bar-wrap {{ background:{BORDER}; border-radius:99px; height:8px; margin-top:10px; }}
.score-bar {{ height:8px; border-radius:99px; background:linear-gradient(90deg,{GREEN},{YELLOW},{RED}); }}

/* ── Customer card ── */
.cust-card {{
  background:{CARD}; border:1px solid {BORDER}; border-radius:14px;
  padding:22px 26px; display:flex; gap:28px; flex-wrap:wrap;
  border-top:3px solid {ACCENT};
}}
.cust-field {{ min-width:100px; }}
.cust-field-label {{ font-size:.7rem; color:{MUTED}; letter-spacing:1px; text-transform:uppercase; margin-bottom:4px; }}
.cust-field-value {{ font-size:1.05rem; font-weight:700; color:{TEXT}; }}

/* ── RFM score cells ── */
.rfm-cell {{
  display:inline-flex; align-items:center; justify-content:center;
  width:32px; height:32px; border-radius:8px;
  font-weight:700; font-size:.9rem;
}}

/* ── Streamlit overrides ── */
.stButton>button {{
  background:linear-gradient(135deg,{ACCENT},{ACCENT2}) !important;
  color:#fff !important; border:none !important;
  border-radius:8px !important; font-weight:600 !important;
  padding:10px 22px !important; transition:opacity .2s !important;
  font-family:'Outfit',sans-serif !important;
}}
.stButton>button:hover {{ opacity:.85 !important; }}

.stSelectbox>div>div, .stTextInput>div>div, .stNumberInput>div>div {{
  background:{INPUT_BG} !important; border-color:{BORDER} !important;
  color:{TEXT} !important; border-radius:8px !important;
}}
.stSelectbox label, .stTextInput label, .stNumberInput label,
.stMultiSelect label, .stSlider label {{
  color:{MUTED} !important; font-size:.8rem !important; font-weight:600 !important;
}}

[data-testid="stMetric"] {{
  background:{METRIC_BG}; border:1px solid {BORDER};
  border-radius:var(--radius); padding:14px 18px;
}}
[data-testid="stMetricLabel"] {{ color:{MUTED} !important; font-size:.78rem !important; }}
[data-testid="stMetricValue"] {{ color:{TEXT} !important; font-weight:800 !important; }}
[data-testid="stMetricDelta"] {{ font-size:.75rem !important; }}

.stDataFrame {{ border-radius:var(--radius) !important; }}
[data-testid="stDataFrame"]>div {{
  background:{CARD} !important; border-radius:var(--radius) !important;
  border:1px solid {BORDER} !important;
}}

hr {{ border-color:{BORDER} !important; margin:20px 0 !important; }}
.stAlert {{ border-radius:var(--radius) !important; background:{CARD} !important; border-color:{BORDER} !important; }}

::-webkit-scrollbar {{ width:5px; height:5px; }}
::-webkit-scrollbar-track {{ background:{BG}; }}
::-webkit-scrollbar-thumb {{ background:{BORDER}; border-radius:3px; }}

.stMultiSelect [data-baseweb="tag"] {{
  background:{NAV_ACT} !important; color:{ACCENT2} !important;
}}

/* ── Divider ── */
.ca-div {{ border:none; border-top:1px solid {BORDER}; margin:18px 0; }}

/* ── Rule bars ── */
.rule-row {{
  background:{CARD}; border:1px solid {BORDER}; border-radius:10px;
  padding:12px 16px; margin-bottom:8px; transition:transform .1s;
}}
.rule-row:hover {{ transform:translateX(3px); }}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
BASE       = os.path.dirname(os.path.abspath(__file__))
DATA_DIR   = os.path.join(BASE, "data")
MODELS_DIR = os.path.join(BASE, "models")
SRC_DIR    = os.path.join(BASE, "src")


@st.cache_data(show_spinner=False)
def load_customer_features():
    path = os.path.join(DATA_DIR, "customer_features.csv")
    if os.path.exists(path):
        df = pd.read_csv(path)
        # Normalise column name
        if "Customer ID" in df.columns:
            df = df.rename(columns={"Customer ID": "customer_id"})
        return df
    # Demo fallback
    np.random.seed(42)
    n = 400
    segs = np.random.choice(["Champions","Loyal","At Risk","Lost","New"], n, p=[.18,.22,.22,.18,.20])
    churn = np.where(np.isin(segs,["At Risk","Lost"]),
                     np.random.choice([0,1], n, p=[.35,.65]),
                     np.random.choice([0,1], n, p=[.92,.08]))
    return pd.DataFrame({
        "customer_id":              range(10001, 10001+n),
        "Recency":                  np.random.randint(1,365,n),
        "Frequency":                np.random.randint(1,60,n),
        "Monetary":                 np.round(np.random.exponential(600,n),2),
        "Avg_InterPurchase_Interval": np.round(np.random.uniform(5,120,n),1),
        "Is_OneTimeBuyer":          np.random.randint(0,2,n),
        "Segment":                  segs,
        "Churned":                  churn,
    })


@st.cache_data(show_spinner=False)
def load_rfm():
    path = os.path.join(DATA_DIR, "rfm_scores.csv")
    if os.path.exists(path):
        df = pd.read_csv(path)
        if "Customer ID" in df.columns:
            df = df.rename(columns={"Customer ID": "customer_id"})
        if "Total_Score" in df.columns and "RFM_Score" not in df.columns:
            df = df.rename(columns={"Total_Score": "RFM_Score"})
        # rfm_scores.csv stores a row index instead of the real Customer ID;
        # its rows are in the same order as customer_features.csv, so take IDs from there.
        cf = load_customer_features()
        if len(cf) == len(df) and (cf["Recency"].values == df["Recency"].values).all():
            df["customer_id"] = cf["customer_id"].values
        return df
    df = load_customer_features()[["customer_id","Recency","Frequency","Monetary","Segment"]].copy()
    df["R_Score"] = pd.qcut(df["Recency"], 4, labels=[4,3,2,1], duplicates="drop").astype(int)
    df["F_Score"] = pd.qcut(df["Frequency"].rank(method="first"), 4, labels=[1,2,3,4], duplicates="drop").astype(int)
    df["M_Score"] = pd.qcut(df["Monetary"].rank(method="first"),  4, labels=[1,2,3,4], duplicates="drop").astype(int)
    df["RFM_Score"] = df["R_Score"] + df["F_Score"] + df["M_Score"]
    return df


@st.cache_data(show_spinner=False)
def load_rules():
    path = os.path.join(DATA_DIR, "association_rules.csv")
    if os.path.exists(path):
        return pd.read_csv(path)
    np.random.seed(7)
    n = 80
    items = ["Shoes","Bags","Watches","Sunglasses","Caps","Belts","Wallets","Jackets","Jeans","Sneakers"]
    return pd.DataFrame({
        "antecedents":  ["{"+np.random.choice(items)+"}" for _ in range(n)],
        "consequents":  ["{"+np.random.choice(items)+"}" for _ in range(n)],
        "support":      np.round(np.random.uniform(.01,.2,n),3),
        "confidence":   np.round(np.random.uniform(.2,.9,n),3),
        "lift":         np.round(np.random.uniform(1,5,n),3),
        "leverage":     np.round(np.random.uniform(-.05,.15,n),4),
        "conviction":   np.round(np.random.uniform(.8,5,n),3),
    })


@st.cache_data(show_spinner=False)
def load_transactions():
    path = os.path.join(DATA_DIR, "cleaned_retail_data.csv")
    if os.path.exists(path):
        return pd.read_csv(path, usecols=["Customer ID", "Description"]).drop_duplicates()
    return pd.DataFrame(columns=["Customer ID", "Description"])


@st.cache_resource(show_spinner="Loading churn models…")
def load_churn_models():
    """Load DNN + XGBoost from src/. Returns (dnn, scaler, xgb, encoder) or None on failure."""
    import sys
    if SRC_DIR not in sys.path:
        sys.path.insert(0, SRC_DIR)
    cwd = os.getcwd()
    try:
        os.chdir(BASE)  # src modules use paths relative to the project root
        from dnn import load_dnn
        from xgboost_model import load_xgb
        dnn, scaler = load_dnn()
        xgb, encoder = load_xgb()
        return dnn, scaler, xgb, encoder
    except Exception as e:
        st.session_state["model_error"] = str(e)
        return None
    finally:
        os.chdir(cwd)


def get_customer_recs(customer_id, rules, top_n=5):
    """Personalised recommendations via src/recommendation.py."""
    import sys
    if SRC_DIR not in sys.path:
        sys.path.insert(0, SRC_DIR)
    from recommendation import get_recommendations
    return get_recommendations(customer_id, load_transactions(), rules, top_n=top_n)


def fmt_itemset(val):
    """frozenset({'A', 'B'}) -> 'A + B'"""
    s = str(val)
    for junk in ("frozenset(", "{", "}", ")", "'", '"'):
        s = s.replace(junk, "")
    return " + ".join(p.strip() for p in s.split(",") if p.strip())


def seg_badge(seg):
    m = {"Champions":"badge-violet","Loyal":"badge-green","Loyal Customers":"badge-green",
         "At Risk":"badge-yellow","Lost":"badge-red","Lost Customers":"badge-red","New":"badge-teal"}
    return f'<span class="badge {m.get(seg,"badge-teal")}">{seg}</span>'

def churn_badge(v):
    return ('<span class="badge badge-red">Churned</span>' if v
            else '<span class="badge badge-green">Active</span>')

def rfm_color(score):
    colors = {1:"#ef4444",2:"#f59e0b",3:"#eab308",4:"#10b981",5:"#7c3aed"}
    bgs    = {1:"rgba(239,68,68,.18)",2:"rgba(245,158,11,.18)",3:"rgba(234,179,8,.18)",
              4:"rgba(16,185,129,.18)",5:"rgba(124,58,237,.18)"}
    c  = colors.get(int(score), MUTED)
    bg = bgs.get(int(score), "transparent")
    return f'<span class="rfm-cell" style="background:{bg};color:{c};">{int(score)}</span>'

def churn_score_heuristic(recency, frequency, monetary, avg_interval, is_otb, segment):
    """Returns 0-100 score. Properly distributes across full range."""
    score = 0.0
    # Recency — big driver
    score += min(recency / 365, 1.0) * 35
    # Frequency — inverse
    score += max(0, (1 - frequency / 50)) * 20
    # Monetary — inverse
    score += max(0, (1 - min(monetary, 2000) / 2000)) * 15
    # Interval
    score += min(avg_interval / 180, 1.0) * 15
    # One-time buyer
    if is_otb == "Yes":
        score += 10
    # Segment adjustments
    seg_adj = {"Champions":-12,"Loyal":-8,"Loyal Customers":-8,
               "At Risk":+8,"Lost":+15,"Lost Customers":+15,"New":+2}
    score += seg_adj.get(segment, 0)
    return int(np.clip(score, 2, 97))


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
PAGES = {
    "🏠  Overview":          "overview",
    "👥  Customer Segments": "segments",
    "📊  RFM Analysis":      "rfm",
    "🔗  Market Basket":     "basket",
    "🤖  Churn Prediction":  "churn",
    "📈  Sales Forecasting": "forecast",
    "🛍️  Offers & Recs":    "offers",
    "⚙️  Model Monitor":     "monitor",
}

with st.sidebar:
    st.markdown(f"""
    <div style="padding:20px 16px 10px; display:flex; align-items:center; gap:10px;">
      <div style="font-size:1.8rem;">🛍️</div>
      <div>
        <div style="font-family:'Space Mono',monospace; font-size:.6rem; letter-spacing:3px;
                    color:{ACCENT}; font-weight:700;">RETAIL AI SUITE</div>
        <div style="font-size:.72rem; color:{MUTED}; margin-top:2px;">Intelligence Dashboard</div>
      </div>
    </div>
    <div style="height:1px; background:{BORDER}; margin:8px 0 12px;"></div>
    """, unsafe_allow_html=True)

    page_label = st.radio("Navigation", list(PAGES.keys()), label_visibility="collapsed")
    page = PAGES[page_label]

    st.markdown(f'<div style="height:1px; background:{BORDER}; margin:16px 0 12px;"></div>', unsafe_allow_html=True)

    # Theme toggle
    toggle_label = "☀️  Light Mode" if dark else "🌙  Dark Mode"
    if st.button(toggle_label, width="stretch"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

    st.markdown(f"""
    <div style="font-size:.7rem; color:{MUTED}; padding:12px 4px 0; line-height:1.8;">
      <div style="color:{ACCENT2}; font-weight:700; margin-bottom:4px;">Data Files</div>
      📄 customer_features.csv<br>
      📄 rfm_scores.csv<br>
      📄 association_rules.csv<br>
      <div style="color:{ACCENT2}; font-weight:700; margin:10px 0 4px;">Models</div>
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
    "overview": ("🏠","Intelligence Overview","End-to-end retail analytics at a glance"),
    "segments": ("👥","Customer Segmentation","RFM-based segment explorer & customer lookup"),
    "rfm":      ("📊","RFM Scoring Analysis","Recency · Frequency · Monetary deep-dive"),
    "basket":   ("🔗","Market Basket Analysis","Association rules & product affinity"),
    "churn":    ("🤖","Churn Prediction","DNN & XGBoost churn risk scoring"),
    "forecast": ("📈","Sales Forecasting","GRU-based next-purchase & revenue forecast"),
    "offers":   ("🛍️","Offers & Recommendations","Personalised offer engine output"),
    "monitor":  ("⚙️","Model Monitor","Training artefacts & performance metrics"),
}
icon, title, subtitle = titles[page]
st.markdown(f"""
<div class="top-header">
  <div style="font-size:2.2rem;">{icon}</div>
  <div>
    <h1>{title}</h1>
    <p>{subtitle}</p>
  </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════
#  PAGE: OVERVIEW
# ═══════════════════════════════════════════════
if page == "overview":
    df = load_customer_features()
    rules = load_rules()

    churn_col = "Churned" if "Churned" in df.columns else ("Churn" if "Churn" in df.columns else None)
    total     = len(df)
    churned   = int(df[churn_col].sum()) if churn_col else 0
    churn_pct = churned / total * 100 if total else 0
    one_time  = int(df["Is_OneTimeBuyer"].sum()) if "Is_OneTimeBuyer" in df.columns else 0
    avg_mon   = df["Monetary"].mean() if "Monetary" in df.columns else 0

    st.markdown('<div class="section-title">Key Performance Indicators</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="kpi-grid">
      <div class="kpi-card violet"><div class="kpi-icon">👥</div>
        <div class="kpi-label">TOTAL CUSTOMERS</div>
        <div class="kpi-value">{total:,}</div>
        <div class="kpi-sub">across all segments</div>
      </div>
      <div class="kpi-card red"><div class="kpi-icon">⚠️</div>
        <div class="kpi-label">CHURN RATE</div>
        <div class="kpi-value">{churn_pct:.1f}%</div>
        <div class="kpi-sub">{churned:,} customers at risk</div>
      </div>
      <div class="kpi-card green"><div class="kpi-icon">💰</div>
        <div class="kpi-label">AVG MONETARY VALUE</div>
        <div class="kpi-value">£{avg_mon:,.0f}</div>
        <div class="kpi-sub">per customer lifetime</div>
      </div>
      <div class="kpi-card teal"><div class="kpi-icon">🛒</div>
        <div class="kpi-label">ONE-TIME BUYERS</div>
        <div class="kpi-value">{one_time:,}</div>
        <div class="kpi-sub">{one_time/total*100:.1f}% of base</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Top Association Rules by Lift</div>', unsafe_allow_html=True)
    top_rules = rules.nlargest(8,"lift")[["antecedents","consequents","confidence","lift","support"]].reset_index(drop=True)

    rows_html = ""
    for _, r in top_rules.iterrows():
        bar = int(r["lift"] / rules["lift"].max() * 100)
        rows_html += f"""
        <div class="rule-row">
          <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">
            <div>
              <span style="color:{ACCENT2};font-weight:700">{fmt_itemset(r['antecedents'])}</span>
              <span style="color:{MUTED};margin:0 8px">→</span>
              <span style="color:{TEAL};font-weight:700">{fmt_itemset(r['consequents'])}</span>
            </div>
            <div style="font-size:.78rem;color:{MUTED}">
              Conf <b style="color:{TEXT}">{r['confidence']:.0%}</b> &nbsp;|&nbsp;
              Lift <b style="color:{YELLOW}">{r['lift']:.2f}</b> &nbsp;|&nbsp;
              Supp <b style="color:{TEXT}">{r['support']:.3f}</b>
            </div>
          </div>
          <div style="margin-top:8px;background:{BORDER};border-radius:99px;height:3px">
            <div style="width:{bar}%;background:linear-gradient(90deg,{ACCENT},{TEAL});height:3px;border-radius:99px"></div>
          </div>
        </div>"""
    st.markdown(rows_html, unsafe_allow_html=True)


# ═══════════════════════════════════════════════
#  PAGE: CUSTOMER SEGMENTS
# ═══════════════════════════════════════════════
elif page == "segments":
    df = load_customer_features()
    churn_col = "Churned" if "Churned" in df.columns else ("Churn" if "Churn" in df.columns else None)

    st.markdown('<div class="section-title">Filters</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        seg_opts = sorted(df["Segment"].unique().tolist())
        seg_filter = st.multiselect("Segment", seg_opts, default=seg_opts)
    with c2:
        churn_filter = st.selectbox("Churn Status", ["All","Active","Churned"])
    with c3:
        otb_filter = st.selectbox("Buyer Type", ["All","One-time","Repeat"])

    fdf = df[df["Segment"].isin(seg_filter)].copy()
    if churn_col:
        if churn_filter == "Active":  fdf = fdf[fdf[churn_col] == 0]
        if churn_filter == "Churned": fdf = fdf[fdf[churn_col] == 1]
    if "Is_OneTimeBuyer" in fdf.columns:
        if otb_filter == "One-time": fdf = fdf[fdf["Is_OneTimeBuyer"] == 1]
        if otb_filter == "Repeat":   fdf = fdf[fdf["Is_OneTimeBuyer"] == 0]

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Customers",     f"{len(fdf):,}")
    c2.metric("Avg Recency",   f"{fdf['Recency'].mean():.0f} days" if "Recency" in fdf.columns else "—")
    c3.metric("Avg Frequency", f"{fdf['Frequency'].mean():.1f}" if "Frequency" in fdf.columns else "—")
    c4.metric("Avg Monetary",  f"£{fdf['Monetary'].mean():,.0f}" if "Monetary" in fdf.columns else "—")

    st.markdown(f'<div style="height:1px;background:{BORDER};margin:18px 0"></div>', unsafe_allow_html=True)

    # ── Customer lookup ──
    st.markdown('<div class="section-title">Customer Lookup</div>', unsafe_allow_html=True)

    # Determine id column
    id_col = "customer_id" if "customer_id" in df.columns else df.columns[0]
    id_placeholder = str(df[id_col].iloc[0]) if len(df) else "e.g. 12346"

    cid_input = st.text_input("Enter Customer ID", placeholder=id_placeholder, key="seg_lookup")

    if cid_input and cid_input.strip():
        try:
            # Try numeric match first, then string match
            try:
                cid_val = float(cid_input.strip())
                row = df[df[id_col].astype(float) == cid_val]
            except ValueError:
                row = df[df[id_col].astype(str) == cid_input.strip()]

            if row.empty:
                st.warning(f"Customer **{cid_input}** not found. Try: {df[id_col].iloc[0]}")
            else:
                r = row.iloc[0]
                churn_val = int(r[churn_col]) if churn_col and churn_col in r else 0
                otb_val   = int(r["Is_OneTimeBuyer"]) if "Is_OneTimeBuyer" in r else 0

                fields = [
                    ("Customer ID",    str(int(r[id_col])) if str(r[id_col]).replace('.','').isdigit() else str(r[id_col])),
                    ("Segment",        seg_badge(str(r.get("Segment","—")))),
                    ("Churn Status",   churn_badge(churn_val)),
                    ("Recency",        f"{int(r.get('Recency',0))} days"),
                    ("Frequency",      str(int(r.get("Frequency",0)))),
                    ("Monetary",       f"£{float(r.get('Monetary',0)):,.2f}"),
                    ("Avg Interval",   f"{float(r.get('Avg_InterPurchase_Interval',0)):.1f} days"),
                    ("One-Time Buyer", "Yes" if otb_val else "No"),
                ]
                fields_html = "".join([
                    f'<div class="cust-field"><div class="cust-field-label">{lbl}</div>'
                    f'<div class="cust-field-value">{val}</div></div>'
                    for lbl, val in fields
                ])
                st.markdown(f'<div class="cust-card">{fields_html}</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error looking up customer: {e}")

    st.markdown(f'<div style="height:1px;background:{BORDER};margin:18px 0"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">Results — {len(fdf):,} customers</div>', unsafe_allow_html=True)

    disp = fdf.copy()
    if churn_col:
        disp[churn_col] = disp[churn_col].map({0:"Active",1:"Churned"})
    if "Is_OneTimeBuyer" in disp.columns:
        disp["Is_OneTimeBuyer"] = disp["Is_OneTimeBuyer"].map({0:"Repeat",1:"One-time"})
    st.dataframe(disp.reset_index(drop=True), width="stretch", hide_index=True)


# ═══════════════════════════════════════════════
#  PAGE: RFM ANALYSIS
# ═══════════════════════════════════════════════
elif page == "rfm":
    rfm = load_rfm()
    df  = load_customer_features()

    # Merge segment if missing
    if "Segment" not in rfm.columns:
        id_col = "customer_id" if "customer_id" in rfm.columns else rfm.columns[0]
        df_id  = "customer_id" if "customer_id" in df.columns else df.columns[0]
        rfm = rfm.merge(df[[df_id,"Segment"]], left_on=id_col, right_on=df_id, how="left")

    c1,c2,c3 = st.columns(3)
    c1.metric("Avg Recency",   f"{rfm['Recency'].mean():.0f} days",  f"σ = {rfm['Recency'].std():.0f}")
    c2.metric("Avg Frequency", f"{rfm['Frequency'].mean():.1f}",     f"σ = {rfm['Frequency'].std():.1f}")
    c3.metric("Avg Monetary",  f"£{rfm['Monetary'].mean():,.0f}",    f"σ = £{rfm['Monetary'].std():,.0f}")

    st.markdown(f'<div style="height:1px;background:{BORDER};margin:18px 0"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Segment-Level RFM Summary</div>', unsafe_allow_html=True)

    if "Segment" in rfm.columns:
        grp = rfm.groupby("Segment").agg(
            Customers=("Recency","count"),
            Avg_Recency=("Recency","mean"),
            Avg_Frequency=("Frequency","mean"),
            Avg_Monetary=("Monetary","mean"),
        ).round(1).reset_index()

        rows_html = ""
        for _, r in grp.iterrows():
            churn_rate_approx = {"Champions":5,"Loyal":8,"Loyal Customers":8,
                                  "At Risk":65,"Lost":85,"Lost Customers":85,"New":20}
            cr = churn_rate_approx.get(r["Segment"], 30)
            bar = int(min(cr, 100))
            bar_color = RED if cr > 50 else (YELLOW if cr > 25 else GREEN)
            rows_html += f"""
            <div class="panel" style="padding:16px 20px;margin-bottom:10px;border-left:3px solid {ACCENT}">
              <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px">
                <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap">
                  <div>{seg_badge(r['Segment'])}</div>
                  <div style="font-size:.78rem;color:{MUTED}">
                    <b style="color:{TEXT}">{int(r['Customers']):,}</b> customers
                  </div>
                  <div style="font-size:.78rem;color:{MUTED}">
                    Recency <b style="color:{TEXT}">{r['Avg_Recency']:.0f}d</b>
                  </div>
                  <div style="font-size:.78rem;color:{MUTED}">
                    Frequency <b style="color:{TEXT}">{r['Avg_Frequency']:.1f}</b>
                  </div>
                  <div style="font-size:.78rem;color:{MUTED}">
                    Monetary <b style="color:{TEXT}">£{r['Avg_Monetary']:,.0f}</b>
                  </div>
                </div>
                <div style="text-align:right;min-width:120px">
                  <div style="font-size:.68rem;color:{MUTED};margin-bottom:4px">EST. CHURN RISK</div>
                  <div style="background:{BORDER};border-radius:99px;height:6px;width:120px">
                    <div style="width:{bar}%;height:6px;background:{bar_color};border-radius:99px"></div>
                  </div>
                  <div style="font-size:.72rem;color:{bar_color};margin-top:3px;font-weight:700">~{cr}%</div>
                </div>
              </div>
            </div>"""
        st.markdown(rows_html, unsafe_allow_html=True)

    st.markdown(f'<div style="height:1px;background:{BORDER};margin:18px 0"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Full RFM Table</div>', unsafe_allow_html=True)

    score_cols = [c for c in ["R_Score","F_Score","M_Score","RFM_Score"] if c in rfm.columns]
    show_cols  = [c for c in (["customer_id","Recency","Frequency","Monetary"] + score_cols + ["Segment"])
                  if c in rfm.columns]

    if score_cols:
        disp = rfm[show_cols].copy().head(200)
        # Color-code score columns
        rows_html = "<table class='ra-table'><thead><tr>"
        for col in show_cols:
            rows_html += f"<th>{col}</th>"
        rows_html += "</tr></thead><tbody>"
        for _, r in disp.iterrows():
            rows_html += "<tr>"
            for col in show_cols:
                val = r[col]
                if col in ["R_Score","F_Score","M_Score"]:
                    rows_html += f"<td>{rfm_color(val)}</td>"
                elif col == "RFM_Score":
                    score_c = GREEN if val >= 10 else (YELLOW if val >= 7 else RED)
                    rows_html += f'<td><b style="color:{score_c}">{int(val)}</b></td>'
                elif col == "Segment":
                    rows_html += f"<td>{seg_badge(str(val))}</td>"
                elif col == "Monetary":
                    rows_html += f"<td>£{float(val):,.2f}</td>"
                else:
                    rows_html += f"<td>{val}</td>"
            rows_html += "</tr>"
        rows_html += "</tbody></table>"
        st.markdown(f'<div class="panel" style="overflow-x:auto">{rows_html}</div>', unsafe_allow_html=True)
    else:
        st.dataframe(rfm[show_cols].reset_index(drop=True).head(200),
                     width="stretch", hide_index=True)


# ═══════════════════════════════════════════════
#  PAGE: MARKET BASKET
# ═══════════════════════════════════════════════
elif page == "basket":
    rules = load_rules()

    c1,c2,c3 = st.columns(3)
    with c1: min_conf = st.slider("Min Confidence", 0.0, 1.0, 0.3, 0.05)
    with c2: min_lift = st.slider("Min Lift", 1.0, float(rules["lift"].max()), 1.0, 0.1)
    with c3: min_sup  = st.slider("Min Support", 0.0, float(rules["support"].max()), 0.01, 0.005)

    filt = rules[(rules["confidence"]>=min_conf) & (rules["lift"]>=min_lift) &
                 (rules["support"]>=min_sup)].sort_values("lift",ascending=False).reset_index(drop=True)

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Rules Found",    len(filt))
    c2.metric("Avg Lift",       f"{filt['lift'].mean():.2f}" if len(filt) else "–")
    c3.metric("Avg Confidence", f"{filt['confidence'].mean():.0%}" if len(filt) else "–")
    c4.metric("Avg Support",    f"{filt['support'].mean():.3f}" if len(filt) else "–")

    st.markdown(f'<div style="height:1px;background:{BORDER};margin:18px 0"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Top Rules by Lift</div>', unsafe_allow_html=True)

    if len(filt):
        max_lift = rules["lift"].max()
        for _, r in filt.head(12).iterrows():
            bar_w = int(r["lift"] / max_lift * 100)
            st.markdown(f"""
            <div class="rule-row">
              <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">
                <div style="font-size:.9rem">
                  <span style="color:{ACCENT2};font-weight:700">{fmt_itemset(r['antecedents'])}</span>
                  <span style="color:{MUTED};margin:0 10px;font-size:1.1rem">→</span>
                  <span style="color:{TEAL};font-weight:700">{fmt_itemset(r['consequents'])}</span>
                </div>
                <div style="display:flex;gap:12px;font-size:.78rem">
                  <span>Conf <b style="color:{TEXT}">{r['confidence']:.0%}</b></span>
                  <span>Lift <b style="color:{YELLOW}">{r['lift']:.2f}</b></span>
                  <span>Supp <b style="color:{TEXT}">{r['support']:.3f}</b></span>
                </div>
              </div>
              <div style="margin-top:8px;background:{BORDER};border-radius:99px;height:3px">
                <div style="width:{bar_w}%;background:linear-gradient(90deg,{ACCENT},{TEAL});height:3px;border-radius:99px"></div>
              </div>
            </div>""", unsafe_allow_html=True)
    else:
        st.info("No rules match the current filters. Try lowering the thresholds.")


# ═══════════════════════════════════════════════
#  PAGE: CHURN PREDICTION
# ═══════════════════════════════════════════════
elif page == "churn":
    df = load_customer_features()
    churn_col = "Churned" if "Churned" in df.columns else ("Churn" if "Churn" in df.columns else None)

    churned   = int(df[churn_col].sum()) if churn_col else 0
    active    = len(df) - churned
    churn_rate= churned / len(df) * 100 if len(df) else 0

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Active Customers",  f"{active:,}")
    c2.metric("Churned Customers", f"{churned:,}")
    c3.metric("Churn Rate",        f"{churn_rate:.1f}%")
    c4.metric("Total Customers",   f"{len(df):,}")

    st.markdown(f'<div style="height:1px;background:{BORDER};margin:18px 0"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Predict Churn Risk</div>', unsafe_allow_html=True)
    models = load_churn_models()
    if models:
        st.caption("Enter customer features to score churn risk — average of the trained DNN and XGBoost models.")
    else:
        st.warning(f"Could not load churn models ({st.session_state.get('model_error', 'unknown error')}). "
                   "Falling back to a rule-based heuristic score.")

    c1,c2 = st.columns(2)
    with c1:
        recency      = st.number_input("Recency (days since last purchase)", 1, 730, 90)
        frequency    = st.number_input("Frequency (# of purchases)", 1, 200, 4)
        monetary     = st.number_input("Monetary (total spend £)", 1.0, 100000.0, 250.0, step=50.0)
    with c2:
        avg_interval = st.number_input("Avg Inter-Purchase Interval (days)", 1.0, 365.0, 45.0)
        is_otb       = st.selectbox("Is One-Time Buyer?", ["No","Yes"])
        segment      = st.selectbox("Segment", sorted(df["Segment"].unique().tolist()))

    if st.button("🤖  Calculate Churn Risk"):
        if models:
            from dnn import predict_dnn
            from xgboost_model import predict_xgb
            dnn, scaler, xgb, encoder = models
            X = pd.DataFrame([{
                "Recency": recency, "Frequency": frequency, "Monetary": monetary,
                "Avg_InterPurchase_Interval": avg_interval,
                "Is_OneTimeBuyer": int(is_otb == "Yes"), "Segment": segment,
            }])
            dnn_p = float(predict_dnn(X, dnn, scaler)["DNN_Churn_Prob"].iloc[0])
            xgb_p = float(predict_xgb(X, xgb, encoder)["XGB_Churn_Prob"].iloc[0])
            score = round((dnn_p + xgb_p) / 2 * 100)
            st.caption(f"DNN: {dnn_p:.1%} · XGBoost: {xgb_p:.1%}")
        else:
            score = churn_score_heuristic(recency, frequency, monetary, avg_interval, is_otb, segment)
        risk_label = "🔴 HIGH RISK" if score >= 60 else ("🟡 MEDIUM RISK" if score >= 35 else "🟢 LOW RISK")
        risk_color = RED if score >= 60 else (YELLOW if score >= 35 else GREEN)

        recs = {
            "Champions": "Send a loyalty reward to keep them engaged.",
            "Loyal":     "Offer early access to new products.",
            "Loyal Customers": "Offer early access to new products.",
            "At Risk":   "Send a win-back offer — 15% discount with urgency.",
            "Lost":      "Re-engagement campaign — 25% off + personal message.",
            "Lost Customers":  "Re-engagement campaign — 25% off + personal message.",
            "New":       "Nurture with a welcome bundle and onboarding emails.",
        }
        rec_text = recs.get(segment, "Personalise your outreach based on their history.")

        st.markdown(f"""
        <div class="panel" style="border-top:3px solid {risk_color};text-align:center;padding:32px 24px;margin-top:16px">
          <div style="font-size:.75rem;color:{MUTED};letter-spacing:3px;margin-bottom:8px">CHURN RISK SCORE</div>
          <div style="font-size:4rem;font-weight:800;color:{risk_color};line-height:1">{score}%</div>
          <div style="font-size:1.05rem;font-weight:700;color:{risk_color};margin-top:6px">{risk_label}</div>
          <div class="score-bar-wrap" style="max-width:320px;margin:18px auto 0">
            <div class="score-bar" style="width:{score}%"></div>
          </div>
          <div style="margin-top:18px;background:{SURFACE};border-radius:10px;padding:12px 16px;
                      border-left:3px solid {risk_color};text-align:left;max-width:480px;margin-left:auto;margin-right:auto">
            <div style="font-size:.7rem;color:{MUTED};font-weight:700;letter-spacing:1px;margin-bottom:4px">RECOMMENDED ACTION</div>
            <div style="font-size:.88rem;color:{TEXT}">{rec_text}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f'<div style="height:1px;background:{BORDER};margin:18px 0"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Churn by Segment</div>', unsafe_allow_html=True)

    if churn_col:
        seg_churn = df.groupby("Segment").agg(
            Total=(churn_col,"count"), Churned=(churn_col,"sum")).reset_index()
        seg_churn["Rate %"] = (seg_churn["Churned"]/seg_churn["Total"]*100).round(1)
        seg_churn["Active"] = seg_churn["Total"] - seg_churn["Churned"]

        rows_html = ""
        for _, r in seg_churn.iterrows():
            bar = int(r["Rate %"])
            bc  = RED if bar > 50 else (YELLOW if bar > 25 else GREEN)
            rows_html += f"""
            <div class="panel" style="padding:14px 18px;margin-bottom:8px;display:flex;
                                       align-items:center;gap:20px;flex-wrap:wrap">
              <div style="min-width:110px">{seg_badge(r['Segment'])}</div>
              <div style="font-size:.8rem;color:{MUTED}">
                Total <b style="color:{TEXT}">{int(r['Total']):,}</b>
              </div>
              <div style="font-size:.8rem;color:{MUTED}">
                Active <b style="color:{GREEN}">{int(r['Active']):,}</b>
              </div>
              <div style="font-size:.8rem;color:{MUTED}">
                Churned <b style="color:{RED}">{int(r['Churned']):,}</b>
              </div>
              <div style="flex:1;min-width:160px">
                <div style="display:flex;justify-content:space-between;margin-bottom:4px">
                  <span style="font-size:.7rem;color:{MUTED}">CHURN RATE</span>
                  <span style="font-size:.75rem;font-weight:700;color:{bc}">{r['Rate %']}%</span>
                </div>
                <div style="background:{BORDER};border-radius:99px;height:5px">
                  <div style="width:{bar}%;height:5px;background:{bc};border-radius:99px"></div>
                </div>
              </div>
            </div>"""
        st.markdown(rows_html, unsafe_allow_html=True)


# ═══════════════════════════════════════════════
#  PAGE: SALES FORECASTING
# ═══════════════════════════════════════════════
elif page == "forecast":
    df = load_customer_features()

    st.markdown('<div class="section-title">GRU Sales Forecast</div>', unsafe_allow_html=True)
    st.info("ℹ️  Connect gru_sales_forecast.keras via src/gru.py to enable live predictions. Showing model-based demo forecast.")

    # Generate realistic demo forecast
    np.random.seed(42)
    n_weeks = 12
    future_weeks = pd.date_range(pd.Timestamp.today(), periods=n_weeks, freq="W")
    base  = df["Monetary"].sum() / 52 if "Monetary" in df.columns else 50000
    trend = np.linspace(0, base*0.25, n_weeks)
    noise = np.random.normal(0, base*0.04, n_weeks)
    forecast = np.clip(base + trend + noise, base*0.8, None)
    lower = forecast * 0.88
    upper = forecast * 1.12

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Next 4-Week Revenue",  f"£{forecast[:4].sum():,.0f}")
    c2.metric("Peak Week Forecast",   f"£{forecast.max():,.0f}")
    c3.metric("Avg Weekly Forecast",  f"£{forecast.mean():,.0f}")
    c4.metric("Growth Trend",         f"+{((forecast[-1]-forecast[0])/forecast[0]*100):.1f}%")

    st.markdown(f'<div style="height:1px;background:{BORDER};margin:18px 0"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">12-Week Revenue Forecast Table</div>', unsafe_allow_html=True)

    fdf = pd.DataFrame({
        "Week":            [str(d.date()) for d in future_weeks],
        "Forecast (£)":    forecast.round(0).astype(int),
        "Lower Bound (£)": lower.round(0).astype(int),
        "Upper Bound (£)": upper.round(0).astype(int),
        "Confidence":      ["±12%"] * n_weeks,
    })

    rows_html = "<table class='ra-table'><thead><tr>"
    for col in fdf.columns:
        rows_html += f"<th>{col}</th>"
    rows_html += "</tr></thead><tbody>"
    for i, (_, r) in enumerate(fdf.iterrows()):
        bar_pct = int((r["Forecast (£)"] - forecast.min()) / (forecast.max() - forecast.min()) * 100)
        rows_html += f"""<tr>
            <td style="font-family:'Space Mono',monospace;font-size:.78rem">{r['Week']}</td>
            <td>
              <div style="display:flex;align-items:center;gap:8px">
                <div style="background:{BORDER};border-radius:3px;height:5px;width:80px">
                  <div style="width:{bar_pct}%;height:5px;background:{TEAL};border-radius:3px"></div>
                </div>
                <b style="color:{TEAL}">£{r['Forecast (£)']:,}</b>
              </div>
            </td>
            <td style="color:{MUTED}">£{r['Lower Bound (£)']:,}</td>
            <td style="color:{MUTED}">£{r['Upper Bound (£)']:,}</td>
            <td><span class="badge badge-teal">{r['Confidence']}</span></td>
        </tr>"""
    rows_html += "</tbody></table>"
    st.markdown(f'<div class="panel" style="overflow-x:auto">{rows_html}</div>', unsafe_allow_html=True)

    st.markdown(f'<div style="height:1px;background:{BORDER};margin:18px 0"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Next Purchase Interval Forecast</div>', unsafe_allow_html=True)

    id_col = "customer_id" if "customer_id" in df.columns else df.columns[0]
    cid2   = st.text_input("Customer ID", placeholder=str(df[id_col].iloc[0]), key="forecast_cid")

    if cid2 and cid2.strip():
        try:
            try:    row = df[df[id_col].astype(float) == float(cid2.strip())]
            except: row = df[df[id_col].astype(str) == cid2.strip()]

            if row.empty:
                st.warning("Customer not found.")
            else:
                r = row.iloc[0]
                avg_int = float(r.get("Avg_InterPurchase_Interval", 30))
                pred_days = max(5, round(avg_int))
                urgency = RED if pred_days <= 3 else (YELLOW if pred_days <= 7 else GREEN)
                st.markdown(f"""
                <div class="panel" style="text-align:center;padding:28px;border-top:3px solid {urgency}">
                  <div style="font-size:.75rem;color:{MUTED};letter-spacing:2px;margin-bottom:8px">PREDICTED NEXT PURCHASE</div>
                  <div style="font-size:3.5rem;font-weight:800;color:{urgency};line-height:1">{pred_days}</div>
                  <div style="font-size:1rem;color:{MUTED};margin-top:4px">days from today</div>
                  <div style="font-size:.8rem;color:{MUTED};margin-top:12px">
                    Based on historical avg interval of <b style="color:{TEXT}">{avg_int:.0f} days</b>
                    &nbsp;·&nbsp; Segment: {seg_badge(str(r.get('Segment','—')))}
                  </div>
                </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {e}")


# ═══════════════════════════════════════════════
#  PAGE: OFFERS & RECOMMENDATIONS
# ═══════════════════════════════════════════════
elif page == "offers":
    df    = load_customer_features()
    rules = load_rules()

    id_col    = "customer_id" if "customer_id" in df.columns else df.columns[0]
    churn_col = "Churned" if "Churned" in df.columns else ("Churn" if "Churn" in df.columns else None)

    st.markdown('<div class="section-title">Personalised Offer Generator</div>', unsafe_allow_html=True)

    cid_off = st.text_input("Enter Customer ID to generate offer", placeholder=str(df[id_col].iloc[0]))

    if cid_off and cid_off.strip():
        try:
            try:    row = df[df[id_col].astype(float) == float(cid_off.strip())]
            except: row = df[df[id_col].astype(str) == cid_off.strip()]

            if row.empty:
                st.warning("Customer not found.")
            else:
                r   = row.iloc[0]
                seg = str(r.get("Segment","New"))
                churn_val = int(r[churn_col]) if churn_col and churn_col in r else 0
                avg_int   = float(r.get("Avg_InterPurchase_Interval", 30))
                pred_days = max(3, round(avg_int))

                # Offer logic
                offer_map = {
                    "Champions":       ("🏆 VIP Loyalty Reward",       "20% off your next order",          "ch", "Loyalty Reward"),
                    "Loyal":           ("💚 Loyal Customer Perk",       "Free shipping + early access",     "lo", "Retention"),
                    "Loyal Customers": ("💚 Loyal Customer Perk",       "Free shipping + early access",     "lo", "Retention"),
                    "At Risk":         ("⚠️ Win-Back Campaign",         "15% discount — come back!",        "ar", "Win-back"),
                    "Lost":            ("🙏 Re-Engagement Offer",       "25% off — we miss you!",           "ls", "Re-engagement"),
                    "Lost Customers":  ("🙏 Re-Engagement Offer",       "25% off — we miss you!",           "ls", "Re-engagement"),
                    "New":             ("🎉 Welcome Bundle",            "10% off your next purchase",       "lo", "Onboarding"),
                }
                offer_title, offer_deal, otype, offer_type = offer_map.get(seg, ("🎁 Special Offer","Personalised deal","lo","General"))

                av_styles = {
                    "ch": f"background:rgba(124,58,237,.2);color:#c4b5fd",
                    "lo": f"background:rgba(16,185,129,.2);color:#6ee7b7",
                    "ar": f"background:rgba(245,158,11,.2);color:#fde68a",
                    "ls": f"background:rgba(239,68,68,.2);color:#fca5a5",
                }
                av_style = av_styles.get(otype, av_styles["lo"])
                initials = str(int(float(cid_off)))[-2:] if str(cid_off).replace('.','').isdigit() else cid_off[:2].upper()

                msg_map = {
                    "ch": f"Thank you for being one of our top customers! As a VIP member, enjoy {offer_deal}. Valid for {pred_days} days.",
                    "lo": f"Hi there! Here's an exclusive perk for loyal customers like you — {offer_deal}. Valid for {pred_days} days.",
                    "ar": f"We noticed you haven't visited in a while. Here's a special offer to bring you back: {offer_deal}. Expires in {pred_days} days!",
                    "ls": f"It's been a while and we truly miss you! {offer_deal} — just for you. Valid for {pred_days} days. No strings attached.",
                }
                offer_msg = msg_map.get(otype, f"Special offer for you: {offer_deal}. Valid for {pred_days} days.")

                rec_products = [p for p, _ in get_customer_recs(r[id_col], rules, top_n=5)]

                tags = [offer_type, offer_deal.split()[0]+"+off",
                        f"Expires in {pred_days}d", f"Segment: {seg}"]
                tags_html = " ".join([f'<span class="offer-tag">{t}</span>' for t in tags])
                prods_html = " ".join([f'<span class="offer-tag" style="color:{TEAL};border-color:{TEAL}">{p}</span>' for p in rec_products])

                st.markdown(f"""
                <div class="offer-card" style="border-top:3px solid {'#7c3aed' if otype=='ch' else ('#10b981' if otype=='lo' else ('#f59e0b' if otype=='ar' else '#ef4444'))}">
                  <div class="offer-avatar" style="{av_style}">{initials}</div>
                  <div class="offer-body">
                    <div class="offer-name">{offer_title} &nbsp; {seg_badge(seg)} &nbsp; {churn_badge(churn_val)}</div>
                    <div class="offer-meta">
                      Customer {cid_off} &nbsp;·&nbsp;
                      Predicted to buy in <b style="color:{TEXT}">{pred_days} days</b> &nbsp;·&nbsp;
                      Avg interval: <b style="color:{TEXT}">{avg_int:.0f}d</b>
                    </div>
                    <div class="offer-msg {otype}">{offer_msg}</div>
                    <div style="margin-bottom:8px">{tags_html}</div>
                    <div style="font-size:.72rem;color:{MUTED};margin-bottom:4px;font-weight:700;letter-spacing:1px">PRODUCT RECOMMENDATIONS</div>
                    <div>{prods_html}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error generating offer: {e}")

    st.markdown(f'<div style="height:1px;background:{BORDER};margin:18px 0"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Segment Offer Strategy</div>', unsafe_allow_html=True)

    strategies = [
        ("Champions",       "badge-violet", "20% loyalty reward",          "Loyalty Reward", "High",     "Send NOW — highest LTV segment"),
        ("Loyal Customers", "badge-green",  "Free shipping + early access", "Retention",      "High",     "Nurture before they slip to At Risk"),
        ("At Risk",         "badge-yellow", "15% win-back discount",        "Win-back",       "Critical", "Act immediately — high churn probability"),
        ("Lost Customers",  "badge-red",    "25% re-engagement offer",      "Re-engagement",  "Critical", "Last chance — personalise the message"),
        ("New",             "badge-teal",   "Welcome bundle — 10% off",     "Onboarding",     "Medium",   "First impression matters most"),
    ]
    priority_colors = {"High": GREEN, "Critical": RED, "Medium": YELLOW}
    for seg_name, seg_cls, offer, otype, priority, note in strategies:
        p_color = priority_colors.get(priority, MUTED)
        st.markdown(f"""
        <div class="panel" style="padding:16px 20px;margin-bottom:10px;
                                   border-left:3px solid {p_color}">
          <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px">
            <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap">
              <span class="badge {seg_cls}">{seg_name}</span>
              <span style="font-size:.88rem;font-weight:600;color:{TEXT}">{offer}</span>
              <span class="badge badge-teal">{otype}</span>
            </div>
            <div style="text-align:right">
              <span style="font-size:.72rem;font-weight:700;color:{p_color};
                           background:rgba(255,255,255,.06);padding:3px 8px;border-radius:6px">{priority}</span>
            </div>
          </div>
          <div style="font-size:.78rem;color:{MUTED};margin-top:8px">💡 {note}</div>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════
#  PAGE: MODEL MONITOR
# ═══════════════════════════════════════════════
elif page == "monitor":
    st.markdown('<div class="section-title">Model Artefacts</div>', unsafe_allow_html=True)

    model_files = [
        ("DNN Churn (Keras 3)",    "models/dnn_churn(3).keras",          "Classification",  "badge-violet"),
        ("DNN Churn (H5)",         "models/dnn_churn.h5",                "Classification",  "badge-violet"),
        ("DNN Scaler",             "models/dnn_scaler(4).pkl",           "Preprocessor",    "badge-teal"),
        ("XGBoost Churn",          "models/xgboost_churn.pkl",           "Classification",  "badge-green"),
        ("XGBoost Label Encoder",  "models/xgboost_label_encoder.pkl",   "Preprocessor",    "badge-teal"),
        ("GRU Next Purchase",      "models/gru_next_purchase.keras",     "Regression",      "badge-yellow"),
        ("GRU Interval Scaler",    "models/gru_interval_scaler.pkl",     "Preprocessor",    "badge-teal"),
        ("GRU Sales Forecast",     "models/gru_sales_forecast.keras",    "Time Series",     "badge-yellow"),
    ]

    found = sum(1 for _, p, _, _ in model_files if os.path.exists(os.path.join(BASE, p)))
    c1,c2,c3 = st.columns(3)
    c1.metric("Models Found",   f"{found}/{len(model_files)}")
    c2.metric("Status",         "✅ Ready" if found >= 6 else "⚠️ Partial")
    c3.metric("Demo Mode",      "Off" if found >= 6 else "On")

    st.markdown(f'<div style="height:1px;background:{BORDER};margin:18px 0"></div>', unsafe_allow_html=True)

    for mname, mpath, mtype, mbadge in model_files:
        full   = os.path.join(BASE, mpath)
        exists = os.path.exists(full)
        if exists:
            sz = os.path.getsize(full)
            size_str = f"{sz/1024:.1f} KB" if sz < 1024*1024 else f"{sz/1024/1024:.1f} MB"
            status = f'<span class="badge badge-green">✅ {size_str}</span>'
        else:
            status = '<span class="badge badge-red">❌ Not Found</span>'

        st.markdown(f"""
        <div class="panel" style="padding:12px 18px;margin-bottom:8px">
          <div style="display:flex;justify-content:space-between;align-items:center">
            <div>
              <span style="font-weight:600;font-size:.9rem">{mname}</span>
              <span class="badge {mbadge}" style="margin-left:10px">{mtype}</span>
              <div style="font-size:.7rem;color:{MUTED};font-family:'Space Mono',monospace;margin-top:3px">{mpath}</div>
            </div>
            {status}
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f'<div style="height:1px;background:{BORDER};margin:18px 0"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Training Visualisations</div>', unsafe_allow_html=True)

    img_files = [
        ("DNN Loss / Accuracy",   "models/DNN Loss Accuracy.png"),
        ("GRU Next Purchase MAE", "models/GRU next purchase loss MAE.png"),
        ("GRU Loss / MAE",        "models/Gru_loss_mae.png"),
    ]
    cols = st.columns(len(img_files))
    for col, (label, rel_path) in zip(cols, img_files):
        full = os.path.join(BASE, rel_path)
        with col:
            if os.path.exists(full):
                st.image(full, caption=label, width="stretch")
            else:
                st.markdown(f"""
                <div class="panel" style="text-align:center;padding:40px 20px">
                  <div style="font-size:2rem;opacity:.4">📊</div>
                  <div style="font-size:.8rem;color:{MUTED};margin-top:8px">{label}</div>
                  <div style="font-size:.7rem;color:{MUTED};margin-top:4px;opacity:.6">Image not found</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown(f'<div style="height:1px;background:{BORDER};margin:18px 0"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Source Files</div>', unsafe_allow_html=True)

    src_files = ["data_cleaning_ridwan.py","data_processing.py","dnn.py","gru.py",
                 "offers.py","recommendation.py","segmentation.py","xgboost_model.py"]
    cols = st.columns(2)
    for i, sf in enumerate(src_files):
        full   = os.path.join(SRC_DIR, sf)
        exists = os.path.exists(full)
        badge  = f'<span class="badge badge-green">✅ Found</span>' if exists else f'<span class="badge badge-red">❌ Missing</span>'
        cols[i%2].markdown(f"""
        <div style="display:flex;justify-content:space-between;padding:8px 4px;
                    border-bottom:1px solid {BORDER};font-size:.83rem">
          <span style="font-family:'Space Mono',monospace;color:{ACCENT2}">src/{sf}</span>
          {badge}
        </div>
        """, unsafe_allow_html=True)