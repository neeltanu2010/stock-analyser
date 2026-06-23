import json
import math
from datetime import datetime
from urllib.parse import quote_plus

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf

# =====================================================
# FINANCIFY STOCK ANALYZER
# Free premium tool for Financify blog
# =====================================================

st.set_page_config(
    page_title="Financify Stock Analyzer",
    page_icon="🐝",
    layout="wide",
    initial_sidebar_state="auto",
)

SURECART_CHECKOUT_URL = "https://financify.blog/buy/financify-tools"
TOOLS_PAGE_URL = "https://financify.blog/tools"
BLOG_URL = "https://financify.blog"

# Mobile-friendly Plotly config
PLOTLY_MOBILE_CONFIG = {"responsive": True, "displayModeBar": False}

# -------------------------
# Premium CSS
# -------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    .stApp {
        background:
            radial-gradient(circle at 5% 8%, rgba(255, 210, 31, 0.28), transparent 32%),
            radial-gradient(circle at 95% 15%, rgba(255, 182, 0, 0.18), transparent 26%),
            radial-gradient(circle at 80% 92%, rgba(255, 210, 31, 0.18), transparent 32%),
            linear-gradient(135deg, #fffaf0 0%, #fff7d1 42%, #fffdf5 100%);
    }

    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        opacity: 0.12;
        background-image:
          linear-gradient(30deg, #111 12%, transparent 12.5%, transparent 87%, #111 87.5%, #111),
          linear-gradient(150deg, #111 12%, transparent 12.5%, transparent 87%, #111 87.5%, #111),
          linear-gradient(30deg, #111 12%, transparent 12.5%, transparent 87%, #111 87.5%, #111),
          linear-gradient(150deg, #111 12%, transparent 12.5%, transparent 87%, #111 87.5%, #111),
          linear-gradient(60deg, rgba(0,0,0,0.17) 25%, transparent 25.5%, transparent 75%, rgba(0,0,0,0.17) 75%, rgba(0,0,0,0.17));
        background-size: 58px 102px;
        background-position: 0 0, 0 0, 29px 51px, 29px 51px, 0 0;
        z-index: -1;
    }

    .block-container {
        padding-top: 1.35rem;
        padding-bottom: 3rem;
        max-width: 1240px;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #050505 0%, #171100 55%, #271e00 100%);
        border-right: 1px solid rgba(255, 210, 31, 0.28);
    }

    section[data-testid="stSidebar"] * {
        color: #fff8d8 !important;
    }

    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] textarea,
    section[data-testid="stSidebar"] select,
    section[data-testid="stSidebar"] [data-baseweb="select"] *,
    section[data-testid="stSidebar"] [data-baseweb="input"] * {
        color: #111 !important;
    }

    .hero-card {
        background: linear-gradient(135deg, #050505 0%, #171100 52%, #3b2e00 100%);
        border: 1px solid rgba(255, 210, 31, 0.58);
        border-radius: 30px;
        padding: 36px 36px 30px 36px;
        box-shadow: 0 26px 90px rgba(0,0,0,0.24);
        position: relative;
        overflow: hidden;
        margin-bottom: 22px;
    }

    .hero-card:before {
        content: "";
        position: absolute;
        inset: -2px;
        background:
            radial-gradient(circle at 86% 22%, rgba(255,210,31,0.34), transparent 22%),
            radial-gradient(circle at 72% 80%, rgba(255,180,0,0.18), transparent 26%);
        pointer-events: none;
    }

    .hero-content { position: relative; z-index: 1; }

    .eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(255, 210, 31, 0.15);
        color: #ffe680;
        border: 1px solid rgba(255, 210, 31, 0.45);
        padding: 8px 13px;
        border-radius: 999px;
        font-size: 0.86rem;
        font-weight: 850;
        letter-spacing: 0.02em;
    }

    .hero-title {
        color: #ffffff;
        font-size: clamp(2.05rem, 4vw, 4.05rem);
        line-height: 1.02;
        font-weight: 950;
        letter-spacing: -0.06em;
        margin-top: 18px;
        margin-bottom: 16px;
        max-width: 930px;
    }

    .hero-title span { color: #FFD21F; }

    .hero-subtitle {
        color: #fff4bd;
        font-size: 1.04rem;
        line-height: 1.7;
        max-width: 900px;
        margin-bottom: 20px;
    }

    .hero-pills { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 20px; }

    .pill {
        background: rgba(255, 255, 255, 0.08);
        color: #fff7cf;
        border: 1px solid rgba(255, 210, 31, 0.28);
        border-radius: 999px;
        padding: 9px 13px;
        font-size: 0.88rem;
        font-weight: 800;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.86);
        border: 1px solid rgba(17, 17, 17, 0.08);
        border-radius: 25px;
        padding: 22px;
        box-shadow: 0 14px 42px rgba(20, 14, 0, 0.08);
        backdrop-filter: blur(12px);
        margin-bottom: 18px;
    }

    .dark-card {
        background: linear-gradient(135deg, #080808 0%, #211900 70%, #493900 100%);
        border: 1px solid rgba(255, 210, 31, 0.42);
        border-radius: 26px;
        padding: 24px;
        box-shadow: 0 18px 45px rgba(0,0,0,0.20);
        color: #fff7cf;
        margin-bottom: 18px;
    }

    .metric-card {
        background: linear-gradient(180deg, #ffffff 0%, #fff8d8 100%);
        border: 1px solid rgba(17, 17, 17, 0.08);
        border-radius: 22px;
        padding: 20px;
        box-shadow: 0 12px 28px rgba(17, 17, 17, 0.08);
        min-height: 142px;
    }

    .metric-label {
        color: #5c4a00;
        font-size: 0.80rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 8px;
    }

    .metric-value {
        color: #080808;
        font-size: 1.68rem;
        font-weight: 950;
        letter-spacing: -0.04em;
        margin-bottom: 6px;
    }

    .metric-help { color: #5a5a5a; font-size: 0.89rem; line-height: 1.45; }

    .section-title {
        font-size: 1.45rem;
        font-weight: 950;
        color: #111;
        letter-spacing: -0.035em;
        margin-bottom: 8px;
    }

    .section-subtitle { color: #5b5b5b; font-size: 0.97rem; line-height: 1.58; margin-bottom: 16px; }

    .verdict-title { font-size: 1.48rem; font-weight: 950; color: #FFD21F; margin-bottom: 8px; }
    .verdict-text { color: #fff7cf; font-size: 1rem; line-height: 1.65; }

    .mini-badge {
        display: inline-block;
        background: #FFD21F;
        color: #111;
        padding: 7px 10px;
        border-radius: 999px;
        font-size: 0.77rem;
        font-weight: 950;
        margin-right: 8px;
        margin-bottom: 8px;
    }

    .soft-badge {
        display: inline-block;
        background: rgba(255, 210, 31, 0.16);
        color: #3a2c00;
        border: 1px solid rgba(255, 210, 31, 0.38);
        padding: 8px 10px;
        border-radius: 999px;
        font-size: 0.80rem;
        font-weight: 850;
        margin-right: 7px;
        margin-bottom: 7px;
    }

    .warning-box {
        background: #fff2bd;
        border-left: 6px solid #FFD21F;
        border-radius: 18px;
        padding: 16px 18px;
        color: #2f2600;
        line-height: 1.58;
        font-weight: 650;
        margin-bottom: 18px;
    }

    .danger-box {
        background: #fff0ee;
        border-left: 6px solid #ff6b4a;
        border-radius: 18px;
        padding: 16px 18px;
        color: #3b120a;
        line-height: 1.58;
        font-weight: 650;
        margin-bottom: 18px;
    }

    .cta-card {
        background: linear-gradient(135deg, #FFD21F 0%, #ffb800 100%);
        color: #111;
        border-radius: 26px;
        padding: 25px;
        border: 1px solid rgba(0,0,0,0.1);
        box-shadow: 0 18px 40px rgba(122, 91, 0, 0.18);
        margin-top: 8px;
    }

    .cta-card h3 { color: #111; font-size: 1.55rem; font-weight: 950; margin-bottom: 8px; letter-spacing: -0.035em; }
    .cta-card p { color: #241b00; line-height: 1.58; font-weight: 650; }

    .stButton > button, .stDownloadButton > button {
        border-radius: 999px !important;
        border: 1px solid rgba(17,17,17,0.13) !important;
        background: linear-gradient(135deg, #111 0%, #2a2100 100%) !important;
        color: #FFD21F !important;
        font-weight: 900 !important;
        padding: 0.72rem 1.1rem !important;
        box-shadow: 0 8px 22px rgba(0,0,0,0.18) !important;
    }

    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.80);
        border: 1px solid rgba(0,0,0,0.08);
        border-radius: 20px;
        padding: 14px 16px;
        box-shadow: 0 8px 22px rgba(0,0,0,0.06);
    }

    div[data-testid="stTabs"] button { font-weight: 850; }

    .footer-note { color: #6b5d27; text-align: center; font-size: 0.86rem; margin-top: 24px; }

    @media (max-width: 768px) {
        .hero-card { padding: 26px 20px; border-radius: 22px; }
        .glass-card, .dark-card { padding: 18px; border-radius: 20px; }
        .metric-value { font-size: 1.38rem; }
    }


    /* =====================================================
       FINANCIFY MOBILE + READABILITY PATCH
       Keeps the original theme, fixes mobile overflow and invisible text.
       ===================================================== */
    :root { color-scheme: light; }

    html, body, .stApp, [data-testid="stAppViewContainer"] {
        width: 100% !important;
        max-width: 100% !important;
        overflow-x: hidden !important;
        -webkit-text-size-adjust: 100%;
        text-rendering: optimizeLegibility;
    }

    *, *::before, *::after {
        box-sizing: border-box !important;
    }

    .main .block-container,
    [data-testid="stAppViewContainer"] .block-container {
        width: 100% !important;
        max-width: min(1260px, 100%) !important;
        padding-left: clamp(0.90rem, 3.2vw, 2.00rem) !important;
        padding-right: clamp(0.90rem, 3.2vw, 2.00rem) !important;
    }

    .block-container p,
    .block-container li,
    .block-container h1,
    .block-container h2,
    .block-container h3,
    .block-container h4,
    .block-container h5,
    .block-container h6,
    .block-container span,
    .hero-title,
    .hero-subtitle,
    .section-title,
    .section-subtitle,
    .metric-label,
    .metric-value,
    .metric-help,
    .verdict-title,
    .verdict-text,
    .light-text,
    .pill,
    .mini-badge,
    .soft-badge {
        overflow-wrap: anywhere !important;
        word-break: normal !important;
    }

    .hero-card,
    .glass-card,
    .dark-card,
    .metric-card,
    .verdict-box,
    .warning-box,
    .danger-box,
    .cta-card {
        max-width: 100% !important;
        isolation: isolate;
    }

    .hero-card > *,
    .dark-card > *,
    .verdict-box > * {
        position: relative;
        z-index: 1;
    }

    .glass-card,
    .metric-card,
    .warning-box,
    .danger-box,
    .cta-card {
        color: #111111 !important;
    }

    .glass-card p,
    .glass-card li,
    .glass-card span,
    .metric-card p,
    .metric-card li,
    .warning-box p,
    .warning-box li,
    .danger-box p,
    .danger-box li,
    .cta-card p,
    .cta-card li {
        opacity: 1 !important;
    }

    .dark-card,
    .dark-card p,
    .dark-card li,
    .dark-card span,
    .verdict-box,
    .verdict-box p,
    .verdict-box li,
    .verdict-box span,
    .hero-card,
    .hero-card p,
    .hero-card li,
    .hero-card span {
        color: #fff7cf !important;
        -webkit-text-fill-color: #fff7cf !important;
    }

    .hero-title,
    .hero-title span,
    .verdict-title,
    .section-title-light {
        -webkit-text-fill-color: currentColor !important;
    }

    .metric-label { color: #5c4a00 !important; }
    .metric-value { color: #070707 !important; }
    .metric-help { color: #4c4c4c !important; }
    .section-title { color: #111111 !important; }
    .section-subtitle { color: #4d4d4d !important; }
    .warning-box, .warning-box * { color: #2f2600 !important; -webkit-text-fill-color: #2f2600 !important; }
    .danger-box, .danger-box * { color: #3b120a !important; -webkit-text-fill-color: #3b120a !important; }
    .cta-card, .cta-card * { color: #111111 !important; -webkit-text-fill-color: #111111 !important; }

    /* Sidebar: readable labels on dark background, readable input text on light fields.
       Width is left to Streamlit default so desktop stays normal and mobile fully collapses. */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] *,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] * {
        color: #fff8d8 !important;
        -webkit-text-fill-color: #fff8d8 !important;
        opacity: 1 !important;
    }

    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] textarea,
    section[data-testid="stSidebar"] [data-baseweb="input"] input,
    section[data-testid="stSidebar"] [data-baseweb="textarea"] textarea,
    section[data-testid="stSidebar"] [data-testid="stNumberInput"] input {
        background: #fffaf0 !important;
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
        caret-color: #111111 !important;
        border: 1px solid rgba(255, 210, 31, 0.50) !important;
        border-radius: 12px !important;
        font-size: 16px !important;
        min-height: 44px !important;
    }

    section[data-testid="stSidebar"] [data-baseweb="select"] > div,
    section[data-testid="stSidebar"] [data-baseweb="select"] div[role="button"] {
        background: #fffaf0 !important;
        color: #111111 !important;
        border-color: rgba(255, 210, 31, 0.50) !important;
        border-radius: 12px !important;
        min-height: 44px !important;
    }

    section[data-testid="stSidebar"] [data-baseweb="select"] *,
    div[data-baseweb="popover"] *,
    div[data-baseweb="menu"] * {
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
    }

    div[data-baseweb="popover"] [role="option"],
    div[data-baseweb="menu"] [role="option"] {
        background: #fffaf0 !important;
    }

    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea,
    .stSelectbox [data-baseweb="select"] > div {
        font-size: 16px !important;
    }

    /* Tables and Plotly should scroll/resize instead of cutting text on phones. */
    div[data-testid="stDataFrame"],
    div[data-testid="stTable"],
    .stDataFrame,
    .stTable {
        max-width: 100% !important;
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        border-radius: 16px !important;
    }

    div[data-testid="stDataFrame"] * {
        font-size: clamp(0.74rem, 2.9vw, 0.92rem) !important;
    }

    .js-plotly-plot,
    .plotly,
    .plot-container,
    div[data-testid="stPlotlyChart"] {
        width: 100% !important;
        max-width: 100% !important;
    }

    div[data-testid="stPlotlyChart"] {
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
    }

    div[data-testid="stTabs"] [role="tablist"] {
        overflow-x: auto !important;
        overflow-y: hidden !important;
        white-space: nowrap !important;
        gap: 0.35rem !important;
        scrollbar-width: none;
    }

    div[data-testid="stTabs"] [role="tablist"]::-webkit-scrollbar {
        display: none;
    }

    div[data-testid="stTabs"] button,
    div[data-testid="stTabs"] button p {
        white-space: nowrap !important;
        font-size: clamp(0.78rem, 3.1vw, 0.94rem) !important;
        line-height: 1.2 !important;
    }

    @media (max-width: 768px) {
        .block-container {
            padding-top: 0.75rem !important;
            padding-bottom: 2rem !important;
        }

        .hero-card {
            padding: 1.25rem 1rem !important;
            border-radius: 21px !important;
            margin-bottom: 1rem !important;
        }

        .hero-title {
            font-size: clamp(1.72rem, 9vw, 2.35rem) !important;
            letter-spacing: -0.038em !important;
            line-height: 1.07 !important;
            margin-top: 0.95rem !important;
            margin-bottom: 0.75rem !important;
        }

        .hero-subtitle {
            font-size: 0.96rem !important;
            line-height: 1.55 !important;
            margin-bottom: 0.85rem !important;
        }

        .hero-pills {
            gap: 0.45rem !important;
            margin-top: 0.85rem !important;
        }

        .pill,
        .mini-badge,
        .soft-badge {
            font-size: 0.76rem !important;
            line-height: 1.2 !important;
            padding: 0.45rem 0.62rem !important;
        }

        .glass-card,
        .dark-card,
        .metric-card,
        .verdict-box,
        .warning-box,
        .danger-box,
        .cta-card {
            padding: 1rem !important;
            border-radius: 18px !important;
            margin-bottom: 0.95rem !important;
        }

        .metric-card {
            min-height: auto !important;
        }

        .metric-label {
            font-size: 0.73rem !important;
            line-height: 1.18 !important;
            letter-spacing: 0.045em !important;
        }

        .metric-value {
            font-size: clamp(1.15rem, 6.2vw, 1.55rem) !important;
            line-height: 1.13 !important;
        }

        .metric-help,
        .section-subtitle,
        .verdict-text,
        .light-text {
            font-size: 0.91rem !important;
            line-height: 1.50 !important;
        }

        .section-title,
        .section-title-light,
        .verdict-title {
            font-size: 1.18rem !important;
            line-height: 1.20 !important;
            letter-spacing: -0.025em !important;
        }

        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
            margin-bottom: 0.75rem !important;
        }

        .stButton > button,
        .stDownloadButton > button,
        section[data-testid="stSidebar"] .stButton > button {
            width: 100% !important;
            min-height: 46px !important;
            padding: 0.75rem 0.95rem !important;
            white-space: normal !important;
            line-height: 1.2 !important;
        }

        div[data-testid="stMetric"] {
            padding: 0.85rem 0.9rem !important;
        }

        div[data-testid="stMetric"] label,
        div[data-testid="stMetric"] [data-testid="stMetricLabel"] * {
            font-size: 0.76rem !important;
            white-space: normal !important;
        }

        div[data-testid="stMetricValue"] {
            font-size: 1.25rem !important;
            line-height: 1.15 !important;
            overflow-wrap: anywhere !important;
        }

        div[data-testid="stPlotlyChart"] {
            border-radius: 16px !important;
        }

        iframe,
        img,
        video,
        canvas,
        svg {
            max-width: 100% !important;
        }
    }

    @media (max-width: 420px) {
        .hero-title {
            font-size: clamp(1.58rem, 10vw, 2.05rem) !important;
        }

        .eyebrow {
            font-size: 0.74rem !important;
            padding: 0.43rem 0.58rem !important;
        }

        .metric-value {
            font-size: clamp(1.05rem, 7vw, 1.35rem) !important;
        }

        .block-container {
            padding-left: 0.72rem !important;
            padding-right: 0.72rem !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# Utility functions
# -------------------------

def clean_symbol(raw_symbol: str, market: str) -> str:
    symbol = (raw_symbol or "").strip().upper()
    if not symbol:
        return "INFY.NS"
    if market == "India NSE" and "." not in symbol:
        return f"{symbol}.NS"
    if market == "India BSE" and "." not in symbol:
        return f"{symbol}.BO"
    return symbol


def currency_symbol(currency):
    mapping = {"INR": "₹", "USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥"}
    return mapping.get(str(currency).upper(), currency or "₹")

def fmt_money(value, currency="₹"):
    currency = currency_symbol(currency)
    if value is None or not np.isfinite(value):
        return "—"
    abs_value = abs(value)
    sign = "-" if value < 0 else ""
    if abs_value >= 1e12:
        return f"{sign}{currency}{abs_value/1e12:,.2f}T"
    if abs_value >= 1e9:
        return f"{sign}{currency}{abs_value/1e9:,.2f}B"
    if abs_value >= 1e7:
        return f"{sign}{currency}{abs_value/1e7:,.2f}Cr"
    if abs_value >= 1e5:
        return f"{sign}{currency}{abs_value/1e5:,.2f}L"
    return f"{sign}{currency}{abs_value:,.2f}"


def fmt_num(value, suffix=""):
    if value is None or not np.isfinite(value):
        return "—"
    return f"{value:,.2f}{suffix}"


def fmt_pct(value):
    if value is None or not np.isfinite(value):
        return "—"
    return f"{value * 100:.2f}%"


def safe_div(a, b):
    try:
        if a is None or b is None or not np.isfinite(a) or not np.isfinite(b) or abs(b) < 1e-12:
            return np.nan
        return a / b
    except Exception:
        return np.nan


def normalize_label(label):
    return "".join(ch for ch in str(label).lower() if ch.isalnum())


def find_statement_series(df: pd.DataFrame, candidates):
    if df is None or df.empty:
        return pd.Series(dtype=float)
    normalized_map = {normalize_label(idx): idx for idx in df.index}
    for candidate in candidates:
        key = normalize_label(candidate)
        if key in normalized_map:
            s = df.loc[normalized_map[key]]
            return pd.to_numeric(s, errors="coerce")
    for candidate in candidates:
        key = normalize_label(candidate)
        for norm_idx, original_idx in normalized_map.items():
            if key and key in norm_idx:
                s = df.loc[original_idx]
                return pd.to_numeric(s, errors="coerce")
    return pd.Series(dtype=float)


def sort_series_years(s: pd.Series, max_years=6):
    if s is None or s.empty:
        return pd.Series(dtype=float)
    s = s.dropna()
    try:
        s.index = pd.to_datetime(s.index).year
    except Exception:
        s.index = [str(x)[:4] for x in s.index]
    s = s.groupby(s.index).first()
    s = s.sort_index()
    if len(s) > max_years:
        s = s.iloc[-max_years:]
    return pd.to_numeric(s, errors="coerce")


def cagr(series: pd.Series):
    s = pd.to_numeric(series, errors="coerce").dropna()
    if len(s) < 2:
        return np.nan
    start, end = s.iloc[0], s.iloc[-1]
    periods = len(s) - 1
    if start <= 0 or end <= 0 or periods <= 0:
        return np.nan
    return (end / start) ** (1 / periods) - 1


def increasing_ratio(series: pd.Series):
    s = pd.to_numeric(series, errors="coerce").dropna()
    if len(s) < 2:
        return np.nan
    return float((s.diff().dropna() > 0).mean())


def positive_ratio(series: pd.Series):
    s = pd.to_numeric(series, errors="coerce").dropna()
    if len(s) == 0:
        return np.nan
    return float((s > 0).mean())


def last_valid(series: pd.Series):
    if series is None or len(series) == 0:
        return np.nan
    s = pd.to_numeric(series, errors="coerce").dropna()
    if len(s) == 0:
        return np.nan
    return float(s.iloc[-1])


def cap_score(value, rules, missing=45):
    if value is None or not np.isfinite(value):
        return missing
    for condition, score in rules:
        try:
            if condition(value):
                return score
        except Exception:
            continue
    return 0


def clamp(x, low=0, high=100):
    if x is None or not np.isfinite(x):
        return np.nan
    return max(low, min(high, float(x)))


def grade(score):
    if score is None or not np.isfinite(score):
        return "Unknown"
    if score >= 85:
        return "A+ Royal Honey"
    if score >= 75:
        return "A Strong Hive"
    if score >= 65:
        return "B+ Quality Watch"
    if score >= 55:
        return "B Mixed but Interesting"
    if score >= 45:
        return "C Caution Zone"
    return "D Bee Careful"


def verdict_from_score(final_score, valuation_score, cash_score, balance_score, growth_score):
    if not np.isfinite(final_score):
        return "Need More Data", "The data source did not provide enough clean numbers. Use manual mode or verify financial statements before trusting any conclusion."
    if final_score >= 80 and valuation_score >= 55:
        return "Royal Honey Candidate 🐝", "The business quality signals look strong and valuation does not look completely crazy based on available data. This is not a buy signal; it means the stock deserves deeper research."
    if final_score >= 72 and valuation_score < 45:
        return "Great Hive, Expensive Honey ⚠️", "Quality looks attractive, but valuation comfort is low. A smart investor would usually demand a margin of safety instead of chasing excitement."
    if final_score >= 65:
        return "Quality Watchlist Zone 🍯", "The stock shows useful quality signals. Check moat, management, risks, and valuation before making any decision."
    if cash_score < 45:
        return "Profit Needs Cash Check 🧾", "Reported profit may not be fully backed by cash-flow strength. Check CFO, FCF and working capital movements carefully."
    if balance_score < 40:
        return "Debt Bees Buzzing 🐝⚠️", "Balance-sheet risk looks elevated. Debt is not always bad, but weak cash flow plus debt can make a business fragile."
    if growth_score < 40:
        return "Slow Hive Zone 🐌", "Growth trend does not look very strong from available data. A slow business can still be valuable, but only at the right price."
    return "Mixed Hive, Read Deeper 🔍", "Some signals look okay and some need caution. Use this as a starting filter, not a final investment decision."


@st.cache_data(ttl=60 * 60, show_spinner=False)
def fetch_yfinance_data(symbol: str):
    result = {
        "symbol": symbol,
        "info": {},
        "history": pd.DataFrame(),
        "income": pd.DataFrame(),
        "balance": pd.DataFrame(),
        "cashflow": pd.DataFrame(),
        "error": None,
    }
    try:
        ticker = yf.Ticker(symbol)
        try:
            result["info"] = ticker.info or {}
        except Exception:
            result["info"] = {}
        try:
            result["history"] = ticker.history(period="5y", auto_adjust=False)
        except Exception:
            result["history"] = pd.DataFrame()
        try:
            result["income"] = ticker.income_stmt
        except Exception:
            result["income"] = pd.DataFrame()
        try:
            result["balance"] = ticker.balance_sheet
        except Exception:
            result["balance"] = pd.DataFrame()
        try:
            result["cashflow"] = ticker.cashflow
        except Exception:
            result["cashflow"] = pd.DataFrame()
    except Exception as exc:
        result["error"] = str(exc)
    return result


def build_financial_frame(income, balance, cashflow):
    revenue = sort_series_years(find_statement_series(income, ["Total Revenue", "Revenue", "Operating Revenue"]))
    net_income = sort_series_years(find_statement_series(income, ["Net Income", "Net Income Common Stockholders", "Net Income Continuous Operations"]))
    ebit = sort_series_years(find_statement_series(income, ["EBIT", "Operating Income", "Normalized EBITDA"]))
    eps = sort_series_years(find_statement_series(income, ["Diluted EPS", "Basic EPS", "Diluted Average Shares"]))

    equity = sort_series_years(find_statement_series(balance, ["Stockholders Equity", "Total Equity Gross Minority Interest", "Common Stock Equity", "Total Stockholder Equity"]))
    total_debt = sort_series_years(find_statement_series(balance, ["Total Debt", "Net Debt", "Long Term Debt And Capital Lease Obligation"]))
    total_assets = sort_series_years(find_statement_series(balance, ["Total Assets"]))
    current_liabilities = sort_series_years(find_statement_series(balance, ["Current Liabilities", "Total Current Liabilities"]))
    cash = sort_series_years(find_statement_series(balance, ["Cash And Cash Equivalents", "Cash Cash Equivalents And Short Term Investments", "Cash Financial"]))

    cfo = sort_series_years(find_statement_series(cashflow, ["Operating Cash Flow", "Total Cash From Operating Activities", "Cash Flow From Continuing Operating Activities"]))
    capex = sort_series_years(find_statement_series(cashflow, ["Capital Expenditure", "Capital Expenditures", "Capital Expenditure Reported"]))
    fcf_reported = sort_series_years(find_statement_series(cashflow, ["Free Cash Flow"]))

    years = sorted(set(revenue.index) | set(net_income.index) | set(ebit.index) | set(equity.index) | set(total_debt.index) | set(total_assets.index) | set(current_liabilities.index) | set(cash.index) | set(cfo.index) | set(capex.index) | set(fcf_reported.index))
    df = pd.DataFrame(index=years)
    df.index.name = "Year"
    df["Revenue"] = revenue.reindex(years)
    df["Net Income"] = net_income.reindex(years)
    df["EBIT"] = ebit.reindex(years)
    df["Equity"] = equity.reindex(years)
    df["Total Debt"] = total_debt.reindex(years)
    df["Total Assets"] = total_assets.reindex(years)
    df["Current Liabilities"] = current_liabilities.reindex(years)
    df["Cash"] = cash.reindex(years)
    df["CFO"] = cfo.reindex(years)
    df["Capex"] = capex.reindex(years)

    if not fcf_reported.empty:
        df["FCF"] = fcf_reported.reindex(years)
    else:
        # Capex is usually negative in Yahoo. CFO + Capex gives FCF.
        df["FCF"] = df["CFO"] + df["Capex"].fillna(0)

    df["Profit Margin"] = df.apply(lambda r: safe_div(r["Net Income"], r["Revenue"]), axis=1)
    df["ROE"] = df.apply(lambda r: safe_div(r["Net Income"], r["Equity"]), axis=1)
    df["Capital Employed"] = df["Total Assets"] - df["Current Liabilities"]
    df["ROCE"] = df.apply(lambda r: safe_div(r["EBIT"], r["Capital Employed"]), axis=1)
    df["Debt/Equity"] = df.apply(lambda r: safe_div(r["Total Debt"], r["Equity"]), axis=1)
    df["CFO/Net Income"] = df.apply(lambda r: safe_div(r["CFO"], r["Net Income"]), axis=1)
    df["FCF Margin"] = df.apply(lambda r: safe_div(r["FCF"], r["Revenue"]), axis=1)
    return df.dropna(how="all")


def enrich_metrics(info, hist, financial_df, manual):
    currency = info.get("currency") or manual.get("currency", "₹")
    current_price = np.nan
    if hist is not None and not hist.empty and "Close" in hist:
        current_price = float(pd.to_numeric(hist["Close"], errors="coerce").dropna().iloc[-1]) if len(hist["Close"].dropna()) else np.nan
    if not np.isfinite(current_price):
        current_price = manual.get("current_price", np.nan)

    market_cap = info.get("marketCap", np.nan)
    if market_cap is None or not np.isfinite(float(market_cap)) if isinstance(market_cap, (int, float, np.number)) else True:
        market_cap = manual.get("market_cap", np.nan)
    market_cap = float(market_cap) if isinstance(market_cap, (int, float, np.number)) and np.isfinite(float(market_cap)) else np.nan

    pe = info.get("trailingPE", np.nan)
    pb = info.get("priceToBook", np.nan)
    ev_ebitda = info.get("enterpriseToEbitda", np.nan)
    dividend_yield = info.get("dividendYield", np.nan)
    if dividend_yield is not None and np.isfinite(dividend_yield) and dividend_yield > 1:
        dividend_yield = dividend_yield / 100

    info_de = info.get("debtToEquity", np.nan)
    if info_de is not None and np.isfinite(info_de):
        debt_equity = float(info_de) / 100 if float(info_de) > 5 else float(info_de)
    else:
        debt_equity = last_valid(financial_df.get("Debt/Equity", pd.Series(dtype=float)))

    profit_margin = info.get("profitMargins", np.nan)
    if profit_margin is None or not np.isfinite(profit_margin):
        profit_margin = last_valid(financial_df.get("Profit Margin", pd.Series(dtype=float)))

    roe = info.get("returnOnEquity", np.nan)
    if roe is None or not np.isfinite(roe):
        roe = last_valid(financial_df.get("ROE", pd.Series(dtype=float)))

    roce = last_valid(financial_df.get("ROCE", pd.Series(dtype=float)))
    fcf_margin = last_valid(financial_df.get("FCF Margin", pd.Series(dtype=float)))
    cfo_ni = last_valid(financial_df.get("CFO/Net Income", pd.Series(dtype=float)))

    fcf = info.get("freeCashflow", np.nan)
    if fcf is None or not np.isfinite(fcf):
        fcf = last_valid(financial_df.get("FCF", pd.Series(dtype=float)))
    cfo = info.get("operatingCashflow", np.nan)
    if cfo is None or not np.isfinite(cfo):
        cfo = last_valid(financial_df.get("CFO", pd.Series(dtype=float)))

    revenue_cagr = cagr(financial_df.get("Revenue", pd.Series(dtype=float)))
    profit_cagr = cagr(financial_df.get("Net Income", pd.Series(dtype=float)))
    cfo_cagr = cagr(financial_df.get("CFO", pd.Series(dtype=float)))
    fcf_cagr = cagr(financial_df.get("FCF", pd.Series(dtype=float)))

    fcf_yield = safe_div(fcf, market_cap)
    earnings_growth_proxy = profit_cagr if np.isfinite(profit_cagr) else info.get("earningsGrowth", np.nan)
    peg = safe_div(pe, earnings_growth_proxy * 100) if np.isfinite(pe) and np.isfinite(earnings_growth_proxy) and earnings_growth_proxy > 0 else np.nan

    return {
        "currency": currency,
        "current_price": current_price,
        "market_cap": market_cap,
        "pe": float(pe) if pe is not None and np.isfinite(pe) else np.nan,
        "pb": float(pb) if pb is not None and np.isfinite(pb) else np.nan,
        "ev_ebitda": float(ev_ebitda) if ev_ebitda is not None and np.isfinite(ev_ebitda) else np.nan,
        "dividend_yield": float(dividend_yield) if dividend_yield is not None and np.isfinite(dividend_yield) else np.nan,
        "debt_equity": debt_equity,
        "profit_margin": profit_margin,
        "roe": roe,
        "roce": roce,
        "fcf_margin": fcf_margin,
        "cfo_ni": cfo_ni,
        "fcf": fcf,
        "cfo": cfo,
        "revenue_cagr": revenue_cagr,
        "profit_cagr": profit_cagr,
        "cfo_cagr": cfo_cagr,
        "fcf_cagr": fcf_cagr,
        "fcf_yield": fcf_yield,
        "peg": peg,
    }


def apply_manual_overrides(metrics, manual_enabled, manual):
    if not manual_enabled:
        return metrics
    updated = dict(metrics)
    keys = [
        "current_price", "market_cap", "pe", "pb", "debt_equity", "profit_margin", "roe", "roce",
        "revenue_cagr", "profit_cagr", "cfo_cagr", "fcf_cagr", "cfo_ni", "fcf_margin", "fcf_yield",
    ]
    for key in keys:
        val = manual.get(key, np.nan)
        if val is not None and np.isfinite(val):
            updated[key] = val
    return updated


def calculate_scores(metrics, moat_score):
    pm = metrics["profit_margin"]
    roe = metrics["roe"]
    roce = metrics["roce"]
    fcf_margin = metrics["fcf_margin"]
    de = metrics["debt_equity"]
    cfo_ni = metrics["cfo_ni"]
    rev_cagr = metrics["revenue_cagr"]
    profit_cagr = metrics["profit_cagr"]
    cfo_cagr = metrics["cfo_cagr"]
    fcf_cagr = metrics["fcf_cagr"]
    pe = metrics["pe"]
    pb = metrics["pb"]
    ev_ebitda = metrics["ev_ebitda"]
    peg = metrics["peg"]
    fcf_yield = metrics["fcf_yield"]

    profitability = np.nanmean([
        cap_score(pm, [(lambda x: x >= 0.25, 100), (lambda x: x >= 0.18, 85), (lambda x: x >= 0.12, 68), (lambda x: x >= 0.07, 48), (lambda x: x > 0, 30)]),
        cap_score(roe, [(lambda x: x >= 0.25, 100), (lambda x: x >= 0.20, 88), (lambda x: x >= 0.15, 70), (lambda x: x >= 0.10, 52), (lambda x: x > 0, 30)]),
        cap_score(roce, [(lambda x: x >= 0.25, 100), (lambda x: x >= 0.20, 88), (lambda x: x >= 0.15, 70), (lambda x: x >= 0.10, 52), (lambda x: x > 0, 30)]),
        cap_score(fcf_margin, [(lambda x: x >= 0.15, 100), (lambda x: x >= 0.10, 82), (lambda x: x >= 0.05, 62), (lambda x: x > 0, 40)]),
    ])

    growth = np.nanmean([
        cap_score(rev_cagr, [(lambda x: x >= 0.18, 100), (lambda x: x >= 0.12, 82), (lambda x: x >= 0.07, 65), (lambda x: x >= 0.03, 48), (lambda x: x > 0, 32)]),
        cap_score(profit_cagr, [(lambda x: x >= 0.20, 100), (lambda x: x >= 0.14, 82), (lambda x: x >= 0.08, 65), (lambda x: x >= 0.03, 48), (lambda x: x > 0, 32)]),
        cap_score(cfo_cagr, [(lambda x: x >= 0.18, 100), (lambda x: x >= 0.12, 82), (lambda x: x >= 0.07, 65), (lambda x: x >= 0.03, 48), (lambda x: x > 0, 32)]),
        cap_score(fcf_cagr, [(lambda x: x >= 0.18, 100), (lambda x: x >= 0.12, 82), (lambda x: x >= 0.07, 65), (lambda x: x >= 0.03, 48), (lambda x: x > 0, 32)]),
    ])

    cash_quality = np.nanmean([
        cap_score(cfo_ni, [(lambda x: x >= 1.15, 100), (lambda x: x >= 1.0, 88), (lambda x: x >= 0.80, 68), (lambda x: x >= 0.50, 45), (lambda x: x > 0, 25)]),
        cap_score(fcf_margin, [(lambda x: x >= 0.15, 100), (lambda x: x >= 0.10, 82), (lambda x: x >= 0.05, 62), (lambda x: x > 0, 40)]),
        cap_score(fcf_yield, [(lambda x: x >= 0.06, 100), (lambda x: x >= 0.04, 82), (lambda x: x >= 0.025, 62), (lambda x: x > 0, 42)]),
    ])

    balance = cap_score(de, [
        (lambda x: x <= 0.10, 100),
        (lambda x: x <= 0.30, 88),
        (lambda x: x <= 0.60, 68),
        (lambda x: x <= 1.00, 48),
        (lambda x: x <= 2.00, 25),
    ])

    pe_score = cap_score(pe, [(lambda x: x <= 12, 95), (lambda x: x <= 20, 82), (lambda x: x <= 30, 62), (lambda x: x <= 45, 42), (lambda x: x <= 70, 22)], missing=45)
    pb_score = cap_score(pb, [(lambda x: x <= 2, 88), (lambda x: x <= 4, 70), (lambda x: x <= 7, 48), (lambda x: x <= 12, 28)], missing=45)
    ev_score = cap_score(ev_ebitda, [(lambda x: x <= 8, 90), (lambda x: x <= 12, 76), (lambda x: x <= 18, 55), (lambda x: x <= 28, 34)], missing=45)
    peg_score = cap_score(peg, [(lambda x: x <= 1.0, 95), (lambda x: x <= 1.5, 76), (lambda x: x <= 2.5, 52), (lambda x: x <= 4.0, 32)], missing=45)
    valuation = np.nanmean([pe_score, pb_score, ev_score, peg_score])

    fundamental = np.nanmean([
        profitability * 0.30,
        growth * 0.20,
        cash_quality * 0.22,
        balance * 0.16,
        valuation * 0.12,
    ]) * 5  # because nanmean of weighted components divides by count
    if not np.isfinite(fundamental):
        fundamental = np.nanmean([profitability, growth, cash_quality, balance, valuation])
    final = (fundamental * 0.78) + (moat_score * 0.22) if np.isfinite(fundamental) else np.nan

    return {
        "Profitability": clamp(profitability),
        "Growth": clamp(growth),
        "Cash Quality": clamp(cash_quality),
        "Balance Sheet": clamp(balance),
        "Valuation Comfort": clamp(valuation),
        "Moat Lens": clamp(moat_score),
        "Fundamental Score": clamp(fundamental),
        "Financify Score": clamp(final),
    }


def trend_badges(financial_df):
    badges = []
    if financial_df.empty:
        return ["Financial trend data limited"]
    checks = {
        "Revenue increasing": increasing_ratio(financial_df.get("Revenue", pd.Series(dtype=float))),
        "Profit increasing": increasing_ratio(financial_df.get("Net Income", pd.Series(dtype=float))),
        "Margin improving": increasing_ratio(financial_df.get("Profit Margin", pd.Series(dtype=float))),
        "ROE improving": increasing_ratio(financial_df.get("ROE", pd.Series(dtype=float))),
        "ROCE improving": increasing_ratio(financial_df.get("ROCE", pd.Series(dtype=float))),
        "CFO increasing": increasing_ratio(financial_df.get("CFO", pd.Series(dtype=float))),
        "FCF increasing": increasing_ratio(financial_df.get("FCF", pd.Series(dtype=float))),
    }
    for name, ratio in checks.items():
        if not np.isfinite(ratio):
            badges.append(f"{name}: data missing")
        elif ratio >= 0.75:
            badges.append(f"✅ {name}")
        elif ratio >= 0.50:
            badges.append(f"🟡 {name}: mixed")
        else:
            badges.append(f"🔴 {name}: weak")
    return badges


def strict_filter(financial_df):
    if financial_df.empty or len(financial_df.dropna(how="all")) < 3:
        return False, ["Not enough multi-year financial data for strict filter."]
    items = []
    checks = [
        ("Profit margin consistently improving", increasing_ratio(financial_df.get("Profit Margin", pd.Series(dtype=float))) >= 0.75),
        ("ROE consistently improving", increasing_ratio(financial_df.get("ROE", pd.Series(dtype=float))) >= 0.75),
        ("ROCE consistently improving", increasing_ratio(financial_df.get("ROCE", pd.Series(dtype=float))) >= 0.75),
        ("CFO consistently improving", increasing_ratio(financial_df.get("CFO", pd.Series(dtype=float))) >= 0.75),
        ("FCF consistently improving", increasing_ratio(financial_df.get("FCF", pd.Series(dtype=float))) >= 0.75),
        ("CFO positive in most years", positive_ratio(financial_df.get("CFO", pd.Series(dtype=float))) >= 0.75),
        ("FCF positive in most years", positive_ratio(financial_df.get("FCF", pd.Series(dtype=float))) >= 0.75),
    ]
    passed = all(bool(x[1]) for x in checks if x[1] is not np.nan)
    for label, ok in checks:
        items.append(f"{'✅' if ok else '❌'} {label}")
    return passed, items


def bubble_risk(metrics, scores):
    risk = 0
    notes = []
    if np.isfinite(metrics["pe"]):
        if metrics["pe"] > 70:
            risk += 28; notes.append("PE is very high compared with normal comfort zones.")
        elif metrics["pe"] > 45:
            risk += 20; notes.append("PE is elevated; future growth must justify it.")
        elif metrics["pe"] > 30:
            risk += 12; notes.append("PE is not cheap; valuation discipline matters.")
    if np.isfinite(metrics["pb"]):
        if metrics["pb"] > 12:
            risk += 20; notes.append("Price-to-book is very rich.")
        elif metrics["pb"] > 7:
            risk += 12; notes.append("Price-to-book is elevated.")
    if np.isfinite(metrics["peg"]):
        if metrics["peg"] > 3:
            risk += 20; notes.append("PEG suggests valuation may be ahead of growth.")
        elif metrics["peg"] > 2:
            risk += 12; notes.append("PEG is not very comfortable.")
    if np.isfinite(scores.get("Cash Quality", np.nan)) and scores["Cash Quality"] < 45:
        risk += 18; notes.append("Cash quality is weak, so valuation deserves extra caution.")
    if np.isfinite(metrics["debt_equity"]) and metrics["debt_equity"] > 1:
        risk += 14; notes.append("Debt is elevated, which can amplify downside risk.")
    if not notes:
        notes.append("No major valuation-bubble smell found from available data, but always check expectations and industry context.")
    return clamp(risk), notes


def make_price_chart(hist, name):
    fig = go.Figure()
    if hist is None or hist.empty or "Close" not in hist:
        fig.add_annotation(text="Price history unavailable", x=0.5, y=0.5, showarrow=False)
    else:
        h = hist.copy().dropna(subset=["Close"])
        fig.add_trace(go.Scatter(x=h.index, y=h["Close"], mode="lines", name="Close", line=dict(width=3)))
        if len(h) > 60:
            h["MA200"] = h["Close"].rolling(200).mean()
            h["MA50"] = h["Close"].rolling(50).mean()
            fig.add_trace(go.Scatter(x=h.index, y=h["MA50"], mode="lines", name="50D avg", line=dict(width=1.6)))
            fig.add_trace(go.Scatter(x=h.index, y=h["MA200"], mode="lines", name="200D avg", line=dict(width=1.6)))
    fig.update_layout(
        title=f"{name} price runway",
        template="plotly_white",
        height=390,
        margin=dict(l=18, r=18, t=58, b=38),
        font=dict(family="Inter", size=13),
        plot_bgcolor="rgba(255,255,255,0)",
        paper_bgcolor="rgba(255,255,255,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def make_score_radar(scores):
    categories = ["Profitability", "Growth", "Cash Quality", "Balance Sheet", "Valuation Comfort", "Moat Lens"]
    values = [scores.get(c, np.nan) for c in categories]
    values = [0 if not np.isfinite(v) else v for v in values]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill="toself", name="Score"))
    fig.update_layout(
        title="Financify Business DNA",
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        template="plotly_white",
        height=430,
        margin=dict(l=20, r=20, t=60, b=35),
        font=dict(family="Inter", size=13),
        paper_bgcolor="rgba(255,255,255,0)",
    )
    return fig


def make_financial_chart(financial_df):
    fig = go.Figure()
    if financial_df.empty:
        fig.add_annotation(text="Financial statement trend unavailable", x=0.5, y=0.5, showarrow=False)
    else:
        for col in ["Revenue", "Net Income", "CFO", "FCF"]:
            if col in financial_df and financial_df[col].dropna().shape[0] > 0:
                fig.add_trace(go.Bar(x=financial_df.index.astype(str), y=financial_df[col], name=col, opacity=0.84))
    fig.update_layout(
        title="Financial engine: Revenue, Profit, CFO and FCF",
        template="plotly_white",
        height=420,
        barmode="group",
        margin=dict(l=18, r=18, t=58, b=38),
        font=dict(family="Inter", size=13),
        plot_bgcolor="rgba(255,255,255,0)",
        paper_bgcolor="rgba(255,255,255,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def make_quality_chart(financial_df):
    fig = go.Figure()
    if financial_df.empty:
        fig.add_annotation(text="Quality trend unavailable", x=0.5, y=0.5, showarrow=False)
    else:
        for col in ["Profit Margin", "ROE", "ROCE", "FCF Margin"]:
            if col in financial_df and financial_df[col].dropna().shape[0] > 0:
                fig.add_trace(go.Scatter(x=financial_df.index.astype(str), y=financial_df[col] * 100, mode="lines+markers", name=col, line=dict(width=3)))
    fig.update_layout(
        title="Quality runway: margins and returns",
        template="plotly_white",
        height=420,
        yaxis_title="Percent",
        margin=dict(l=18, r=18, t=58, b=38),
        font=dict(family="Inter", size=13),
        plot_bgcolor="rgba(255,255,255,0)",
        paper_bgcolor="rgba(255,255,255,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def build_report(symbol, name, sector, industry, metrics, scores, verdict_title, verdict_text, strict_items, bubble_notes):
    generated = datetime.now().strftime("%d %b %Y, %I:%M %p")
    report = f"""
FINANCIFY STOCK ANALYZER MINI REPORT
Generated: {generated}

Stock: {name} ({symbol})
Sector: {sector or '—'}
Industry: {industry or '—'}

FINANCIFY VERDICT
{verdict_title}
{verdict_text}

CORE SNAPSHOT
Current Price: {fmt_money(metrics['current_price'], metrics['currency'])}
Market Cap: {fmt_money(metrics['market_cap'], metrics['currency'])}
PE Ratio: {fmt_num(metrics['pe'], 'x')}
PB Ratio: {fmt_num(metrics['pb'], 'x')}
Debt/Equity: {fmt_num(metrics['debt_equity'], 'x')}
Profit Margin: {fmt_pct(metrics['profit_margin'])}
ROE: {fmt_pct(metrics['roe'])}
ROCE: {fmt_pct(metrics['roce'])}
CFO/Net Income: {fmt_num(metrics['cfo_ni'], 'x')}
FCF Yield: {fmt_pct(metrics['fcf_yield'])}

FINANCIFY SCORES
Profitability: {fmt_num(scores['Profitability'])}/100
Growth: {fmt_num(scores['Growth'])}/100
Cash Quality: {fmt_num(scores['Cash Quality'])}/100
Balance Sheet: {fmt_num(scores['Balance Sheet'])}/100
Valuation Comfort: {fmt_num(scores['Valuation Comfort'])}/100
Moat Lens: {fmt_num(scores['Moat Lens'])}/100
Final Financify Score: {fmt_num(scores['Financify Score'])}/100
Grade: {grade(scores['Financify Score'])}

STRICT DURABLE FILTER
- """ + "\n- ".join(strict_items) + """

BUBBLE RISK NOTES
- """ + "\n- ".join(bubble_notes) + """

Educational disclaimer: This report is for learning and research only. It is not investment advice, a stock recommendation, or a buy/sell signal. Please do your own research or consult a SEBI-registered investment adviser before making decisions.
"""
    return report.strip()


def build_seo_draft(name, symbol, metrics, scores, verdict_title):
    stock_name = name or symbol
    title = f"{stock_name} Stock Analysis: Quality, Valuation, Cash Flow and Financify Score"
    meta = f"Analyze {stock_name} using Financify's free stock analyzer. Check ROE, ROCE, debt, profit margin, cash flow, valuation comfort and quality score."
    excerpt = f"A simple, educational stock analysis of {stock_name} covering business quality, growth, cash flow, valuation comfort and key risks using Financify's free stock analyzer."
    body = f"""
# {title}

Most beginner investors start with one question: is the stock price going up? A better question is: is the business strong enough to deserve attention?

This free Financify Stock Analyzer checks {stock_name} across profitability, growth, cash quality, balance sheet strength, valuation comfort and a qualitative moat lens.

## Quick Snapshot

- Current price: {fmt_money(metrics['current_price'], metrics['currency'])}
- Market cap: {fmt_money(metrics['market_cap'], metrics['currency'])}
- PE ratio: {fmt_num(metrics['pe'], 'x')}
- PB ratio: {fmt_num(metrics['pb'], 'x')}
- Debt-to-equity: {fmt_num(metrics['debt_equity'], 'x')}
- Profit margin: {fmt_pct(metrics['profit_margin'])}
- ROE: {fmt_pct(metrics['roe'])}
- ROCE: {fmt_pct(metrics['roce'])}
- CFO to net income: {fmt_num(metrics['cfo_ni'], 'x')}
- FCF yield: {fmt_pct(metrics['fcf_yield'])}

## Financify Score

The current Financify Score is {fmt_num(scores['Financify Score'])}/100, which falls under: {grade(scores['Financify Score'])}.

The tool verdict is: **{verdict_title}**.

## What This Means

A high-quality stock usually has a combination of strong returns on capital, healthy margins, clean cash flows, manageable debt and reasonable valuation. One metric alone is never enough. A company may have high ROE because of debt, high growth because of a temporary cycle, or a high valuation because the market has already priced in perfection.

## What To Check Next

Before making any decision, read the latest annual report, understand the business model, compare competitors, check management commentary and study whether cash flow supports reported profits.

## Disclaimer

This analysis is for educational purposes only. It is not investment advice, a stock recommendation, or a buy/sell signal. Please do your own research or consult a SEBI-registered investment adviser before investing.
""".strip()
    return title, meta, excerpt, body


# -------------------------
# Sidebar
# -------------------------
with st.sidebar:
    st.markdown("### 🐝 Stock Analyzer Inputs")
    st.caption("Enter a ticker. For Indian NSE stocks, you can type INFY, TCS, HDFCBANK, RELIANCE etc.")

    market = st.selectbox("Market", ["India NSE", "India BSE", "USA", "Custom"], index=0)
    raw_symbol = st.text_input("Ticker symbol", value="INFY")
    symbol = clean_symbol(raw_symbol, market)

    st.markdown("---")
    st.markdown("### Moat Lens")
    st.caption("This makes the tool unique: blend numbers with business-quality thinking.")
    pricing_power = st.slider("Pricing power", 0, 100, 65)
    brand_strength = st.slider("Brand / trust strength", 0, 100, 65)
    switching_cost = st.slider("Switching cost / stickiness", 0, 100, 55)
    runway = st.slider("Growth runway", 0, 100, 65)
    management_trust = st.slider("Management trust", 0, 100, 60)
    moat_score = np.nanmean([pricing_power, brand_strength, switching_cost, runway, management_trust])

    st.markdown("---")
    manual_enabled = st.toggle("Manual override / fallback mode", value=False, help="Use this if Yahoo Finance has missing data or you want to test your own numbers.")
    manual = {"currency": "₹" if market in ["India NSE", "India BSE"] else "$"}
    if manual_enabled:
        manual["current_price"] = st.number_input("Manual current price", value=0.0, step=1.0)
        manual["market_cap"] = st.number_input("Manual market cap", value=0.0, step=1000000.0)
        manual["pe"] = st.number_input("Manual PE", value=0.0, step=0.5)
        manual["pb"] = st.number_input("Manual PB", value=0.0, step=0.5)
        manual["debt_equity"] = st.number_input("Manual debt/equity", value=0.0, step=0.05)
        manual["profit_margin"] = st.number_input("Manual profit margin %", value=0.0, step=0.5) / 100
        manual["roe"] = st.number_input("Manual ROE %", value=0.0, step=0.5) / 100
        manual["roce"] = st.number_input("Manual ROCE %", value=0.0, step=0.5) / 100
        manual["revenue_cagr"] = st.number_input("Manual revenue CAGR %", value=0.0, step=0.5) / 100
        manual["profit_cagr"] = st.number_input("Manual profit CAGR %", value=0.0, step=0.5) / 100
        manual["cfo_cagr"] = st.number_input("Manual CFO CAGR %", value=0.0, step=0.5) / 100
        manual["fcf_cagr"] = st.number_input("Manual FCF CAGR %", value=0.0, step=0.5) / 100
        manual["cfo_ni"] = st.number_input("Manual CFO / Net Profit", value=0.0, step=0.05)
        manual["fcf_margin"] = st.number_input("Manual FCF margin %", value=0.0, step=0.5) / 100
        manual["fcf_yield"] = st.number_input("Manual FCF yield %", value=0.0, step=0.5) / 100

    st.markdown("---")
    st.markdown(f"[🔓 Upgrade to Financify Pro]({SURECART_CHECKOUT_URL})")
    st.markdown(f"[🧰 Explore all tools]({TOOLS_PAGE_URL})")

# -------------------------
# Hero
# -------------------------
st.markdown(
    """
    <div class="hero-card"><div class="hero-content">
        <div class="eyebrow">🐝 Free Financify Tool • Stock Analyzer</div>
        <div class="hero-title">Analyze a stock like a <span>business</span>, not like a lottery ticket.</div>
        <div class="hero-subtitle">
            A premium free stock-quality lab that checks profitability, ROE, ROCE, cash flow, debt, growth, valuation comfort,
            bubble smell, and a Warren-style moat lens.
        </div>
        <div class="hero-pills">
            <div class="pill">Financify Score</div>
            <div class="pill">Warren Lens</div>
            <div class="pill">Cash Flow Truth Check</div>
            <div class="pill">Bubble Smell Meter</div>
            <div class="pill">Strict Durable Filter</div>
            <div class="pill">SEO Draft Generator</div>
        </div>
    </div></div>
    """,
    unsafe_allow_html=True,
)

with st.spinner(f"Fetching and analyzing {symbol}..."):
    data = fetch_yfinance_data(symbol)

info = data.get("info", {}) or {}
hist = data.get("history", pd.DataFrame())
financial_df = build_financial_frame(data.get("income", pd.DataFrame()), data.get("balance", pd.DataFrame()), data.get("cashflow", pd.DataFrame()))
metrics = enrich_metrics(info, hist, financial_df, manual)
metrics = apply_manual_overrides(metrics, manual_enabled, manual)

name = info.get("longName") or info.get("shortName") or raw_symbol.upper()
sector = info.get("sector", "")
industry = info.get("industry", "")
last_updated = datetime.now().strftime("%d %b %Y, %I:%M %p")

scores = calculate_scores(metrics, moat_score)
verdict_title, verdict_text = verdict_from_score(scores["Financify Score"], scores["Valuation Comfort"], scores["Cash Quality"], scores["Balance Sheet"], scores["Growth"])
strict_passed, strict_items = strict_filter(financial_df)
bubble_score, bubble_notes = bubble_risk(metrics, scores)

if data.get("error"):
    st.markdown(f"<div class='danger-box'><b>Data warning:</b> {data['error']}. You can use manual mode from the sidebar.</div>", unsafe_allow_html=True)

if financial_df.empty and not manual_enabled:
    st.markdown(
        """
        <div class="warning-box">
        <b>Data note:</b> Financial statement data is limited for this ticker. If numbers look incomplete, use manual override or verify from annual reports, Screener, Tijori, exchange filings, or company reports.
        </div>
        """,
        unsafe_allow_html=True,
    )

# -------------------------
# Metric cards
# -------------------------
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Financify Score</div>
        <div class="metric-value">{fmt_num(scores['Financify Score'])}/100</div>
        <div class="metric-help">{grade(scores['Financify Score'])}</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Price</div>
        <div class="metric-value">{fmt_money(metrics['current_price'], metrics['currency'])}</div>
        <div class="metric-help">Ticker: {symbol}</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">ROE / ROCE</div>
        <div class="metric-value">{fmt_pct(metrics['roe'])} / {fmt_pct(metrics['roce'])}</div>
        <div class="metric-help">Return strength check.</div>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Debt / Equity</div>
        <div class="metric-value">{fmt_num(metrics['debt_equity'], 'x')}</div>
        <div class="metric-help">Lower is usually safer.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

left, right = st.columns([0.95, 1.35], gap="large")
with left:
    st.markdown(f"""
    <div class="dark-card">
        <div class="verdict-title">{verdict_title}</div>
        <div class="verdict-text">{verdict_text}</div>
        <br>
        <span class="mini-badge">Grade: {grade(scores['Financify Score'])}</span>
        <span class="mini-badge">Bubble Risk: {fmt_num(bubble_score)}/100</span>
        <span class="mini-badge">Updated: {last_updated}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="glass-card">
            <div class="section-title">🐝 Strict Durable Business Filter</div>
            <div class="section-subtitle">This is intentionally strict. Very few companies pass it every year, but it reveals durability.</div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(f"**Result:** {'✅ Passed' if strict_passed else '⚠️ Not fully passed / data limited'}")
    for item in strict_items:
        st.markdown(f"- {item}")
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("<div class='glass-card'><div class='section-title'>📈 Price Runway</div><div class='section-subtitle'>Price is not the whole story, but it helps users visually understand market behaviour.</div>", unsafe_allow_html=True)
    st.plotly_chart(make_price_chart(hist, name), use_container_width=True, config=PLOTLY_MOBILE_CONFIG)
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Tabs
# -------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🧬 Business DNA",
    "💸 Cash Truth",
    "🧠 Warren Lens",
    "🫧 Bubble Risk",
    "📤 Report & Share",
    "📝 SEO Draft",
])

with tab1:
    a, b = st.columns([1, 1.2], gap="large")
    with a:
        st.markdown("<div class='glass-card'><div class='section-title'>Financify Score Radar</div><div class='section-subtitle'>A visual business-quality fingerprint.</div>", unsafe_allow_html=True)
        st.plotly_chart(make_score_radar(scores), use_container_width=True, config=PLOTLY_MOBILE_CONFIG)
        st.markdown("</div>", unsafe_allow_html=True)
    with b:
        st.markdown("<div class='glass-card'><div class='section-title'>Core Metrics</div><div class='section-subtitle'>A clean snapshot for beginner investors.</div>", unsafe_allow_html=True)
        metrics_table = pd.DataFrame([
            ["Market Cap", fmt_money(metrics['market_cap'], metrics['currency'])],
            ["PE Ratio", fmt_num(metrics['pe'], 'x')],
            ["PB Ratio", fmt_num(metrics['pb'], 'x')],
            ["EV/EBITDA", fmt_num(metrics['ev_ebitda'], 'x')],
            ["PEG Proxy", fmt_num(metrics['peg'], 'x')],
            ["Profit Margin", fmt_pct(metrics['profit_margin'])],
            ["ROE", fmt_pct(metrics['roe'])],
            ["ROCE", fmt_pct(metrics['roce'])],
            ["Revenue CAGR", fmt_pct(metrics['revenue_cagr'])],
            ["Profit CAGR", fmt_pct(metrics['profit_cagr'])],
            ["CFO CAGR", fmt_pct(metrics['cfo_cagr'])],
            ["FCF CAGR", fmt_pct(metrics['fcf_cagr'])],
            ["CFO / Net Income", fmt_num(metrics['cfo_ni'], 'x')],
            ["FCF Yield", fmt_pct(metrics['fcf_yield'])],
        ], columns=["Metric", "Value"])
        st.dataframe(metrics_table, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='glass-card'><div class='section-title'>Trend Badges</div><div class='section-subtitle'>Quickly see whether the company is improving or just looking good for one year.</div>", unsafe_allow_html=True)
    badges = trend_badges(financial_df)
    badge_html = "".join([f"<span class='soft-badge'>{b}</span>" for b in badges])
    st.markdown(badge_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("<div class='glass-card'><div class='section-title'>Financial Engine</div><div class='section-subtitle'>Profit without cash is like honey without sweetness. CFO and FCF matter.</div>", unsafe_allow_html=True)
        st.plotly_chart(make_financial_chart(financial_df), use_container_width=True, config=PLOTLY_MOBILE_CONFIG)
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='glass-card'><div class='section-title'>Quality Runway</div><div class='section-subtitle'>Margins, ROE, ROCE and FCF margin show business durability.</div>", unsafe_allow_html=True)
        st.plotly_chart(make_quality_chart(financial_df), use_container_width=True, config=PLOTLY_MOBILE_CONFIG)
        st.markdown("</div>", unsafe_allow_html=True)

    if not financial_df.empty:
        display_fin = financial_df.copy()
        money_cols = ["Revenue", "Net Income", "EBIT", "Equity", "Total Debt", "Cash", "CFO", "FCF"]
        pct_cols = ["Profit Margin", "ROE", "ROCE", "Debt/Equity", "CFO/Net Income", "FCF Margin"]
        for col in money_cols:
            if col in display_fin:
                display_fin[col] = display_fin[col].map(lambda x: fmt_money(x, metrics['currency']))
        for col in pct_cols:
            if col in display_fin and col not in ["Debt/Equity", "CFO/Net Income"]:
                display_fin[col] = display_fin[col].map(fmt_pct)
            elif col in display_fin:
                display_fin[col] = display_fin[col].map(lambda x: fmt_num(x, 'x'))
        st.markdown("<div class='glass-card'><div class='section-title'>Historical Statement Snapshot</div><div class='section-subtitle'>Use this to verify trends. Data comes from Yahoo Finance when available.</div>", unsafe_allow_html=True)
        st.dataframe(display_fin, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    st.markdown("<div class='glass-card'><div class='section-title'>What Warren Would Check Next</div><div class='section-subtitle'>A good free tool should teach users how to think, not just throw a score.</div>", unsafe_allow_html=True)
    warren_checks = [
        ("Understandable business", "Can you explain how the company makes money in two simple lines?"),
        ("Durable moat", "Does it have brand, cost advantage, distribution, network effect, switching cost, or regulation advantage?"),
        ("Consistent returns", "Are ROE and ROCE strong without relying on dangerous debt?"),
        ("Cash conversion", "Does CFO broadly support reported profits?"),
        ("Reinvestment runway", "Can the company deploy capital for many years without destroying returns?"),
        ("Valuation discipline", "Even a wonderful company can be a poor investment at a foolish price."),
        ("Management quality", "Are capital allocation, disclosures and governance trustworthy?"),
    ]
    for label, desc in warren_checks:
        st.checkbox(f"{label} — {desc}", value=False)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='dark-card'><div class='verdict-title'>Moat Lens Interpretation</div>", unsafe_allow_html=True)
    if moat_score >= 75:
        moat_text = "Your qualitative moat score is strong. Now confirm it with industry data, annual reports and long-term return on capital."
    elif moat_score >= 55:
        moat_text = "Your qualitative moat score is decent but not unquestionable. Look for proof of pricing power and customer stickiness."
    else:
        moat_text = "Your qualitative moat score is weak. The company may still be tradable, but long-term compounding needs stronger business evidence."
    st.markdown(f"<div class='verdict-text'>{moat_text}</div></div>", unsafe_allow_html=True)

with tab4:
    st.markdown("<div class='glass-card'><div class='section-title'>Bubble Smell Meter</div><div class='section-subtitle'>This does not predict crashes. It simply checks whether price expectations may be getting too excited.</div>", unsafe_allow_html=True)
    st.progress(int(bubble_score) if np.isfinite(bubble_score) else 0)
    st.markdown(f"### Bubble Risk Score: {fmt_num(bubble_score)}/100")
    for note in bubble_notes:
        st.markdown(f"- {note}")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="warning-box">
        <b>Bubble smell rule:</b> High valuation is not automatically bad. It becomes dangerous when high expectations meet weak cash flow, falling growth, poor returns or excessive debt.
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab5:
    report = build_report(symbol, name, sector, industry, metrics, scores, verdict_title, verdict_text, strict_items, bubble_notes)
    st.markdown("<div class='glass-card'><div class='section-title'>Shareable Mini Report</div><div class='section-subtitle'></div>", unsafe_allow_html=True)
    st.text_area("Copy report", value=report, height=390)
    st.download_button(
        "⬇️ Download stock analysis report",
        data=report,
        file_name=f"financify_stock_analyzer_{symbol.replace('.', '_').lower()}.txt",
        mime="text/plain",
    )
    share_text = f"I analyzed {name} ({symbol}) using Financify Stock Analyzer. Score: {fmt_num(scores['Financify Score'])}/100, Grade: {grade(scores['Financify Score'])}. Try it: {TOOLS_PAGE_URL}"
    st.markdown(f"[📲 Share on WhatsApp](https://wa.me/?text={quote_plus(share_text)})  &nbsp;&nbsp; [𝕏 Share on X](https://twitter.com/intent/tweet?text={quote_plus(share_text)})", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tab6:
    title, meta, excerpt, body = build_seo_draft(name, symbol, metrics, scores, verdict_title)
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f"How does Financify analyze {name}?",
                "acceptedAnswer": {"@type": "Answer", "text": "Financify checks profitability, growth, cash quality, balance sheet strength, valuation comfort and a qualitative moat lens for educational analysis."},
            },
            {
                "@type": "Question",
                "name": "Is this a stock recommendation?",
                "acceptedAnswer": {"@type": "Answer", "text": "No. The tool is for education and research only. It is not investment advice or a buy/sell signal."},
            },
        ],
    }
    st.markdown("<div class='glass-card'><div class='section-title'>SEO Article Draft Generator</div><div class='section-subtitle'>Create human-editable WordPress drafts around the stock analysis. Do not mass publish blindly.</div>", unsafe_allow_html=True)
    st.text_input("SEO title", value=title)
    st.text_area("Meta description", value=meta, height=85)
    st.text_area("Excerpt", value=excerpt, height=85)
    st.text_area("Article draft", value=body, height=520)
    st.text_area("Optional FAQ schema", value=json.dumps(faq_schema, indent=2), height=250)
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# CTA + Disclaimer
# -------------------------
st.markdown(
    f"""
    <div class="cta-card">
        <h3>Want the full Financify deep scan?</h3>
        <p>
        This free analyzer is built to educate users. For deeper analysis, connect it with your advanced Financify tools:
        Honey Scanner, Bubble Sniffer, DCF Calculator, Intrinsic Value Calculator and Hive Cycle Predictor.
        </p>
        <p><b>Free tool:</b> quick analysis and learning. <b>Pro tools:</b> deeper scans, usage limits, advanced scoring, and full report layers.</p>
        <p>👉 <a href="{SURECART_CHECKOUT_URL}" target="_blank" style="color:#111;font-weight:950;">Upgrade to Financify Pro</a> &nbsp; | &nbsp;
        <a href="{TOOLS_PAGE_URL}" target="_blank" style="color:#111;font-weight:950;">Explore all Financify tools</a></p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    """
    <div class="warning-box">
    <b>Educational disclaimer:</b> This tool is for learning and research only. It is not investment advice, a stock recommendation, or a buy/sell signal. Market data and financial data may be delayed, incomplete or inaccurate. Always verify numbers from official filings and consult a SEBI-registered investment adviser for personalised advice.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='footer-note'>🐝 Financify • Madness of Money Bees • Analyze businesses, not buzz.</div>", unsafe_allow_html=True)
