from __future__ import annotations

import faulthandler
import sys

import streamlit as st

from core.i18n import LANG_OPTIONS, get_lang, set_lang, t

faulthandler.enable(file=sys.stderr, all_threads=True)

st.set_page_config(
    page_title="Quantum Info Learning Lab",
    page_icon="Q",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1180px;
        padding-top: 1.6rem;
        padding-bottom: 3rem;
        overflow-x: clip;
    }
    img {
        max-width: 100%;
        height: auto;
    }
    div[data-testid="stMetric"] {
        border: 1px solid rgba(148, 163, 184, 0.28);
        border-radius: 8px;
        padding: 0.5rem 0.65rem;
    }
    @media (max-width: 700px) {
        .block-container {
            padding-left: 0.75rem;
            padding-right: 0.75rem;
            padding-top: 1rem;
        }
        h1 {
            font-size: 1.55rem !important;
            line-height: 1.25 !important;
        }
        h2, h3 {
            line-height: 1.3 !important;
        }
        div[data-testid="stMetric"] {
            padding: 0.45rem 0.55rem;
            min-width: 0;
        }
        div[data-testid="stMetricLabel"] {
            white-space: normal;
        }
        div[data-testid="stButton"] button {
            width: 100%;
        }
        div[data-testid="stHorizontalBlock"] {
            flex-wrap: wrap;
            gap: 0.75rem;
        }
        div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
            flex: 1 1 100% !important;
            width: 100% !important;
            min-width: 0 !important;
        }
        div[data-testid="stTabs"] [data-baseweb="tab-list"] {
            overflow-x: auto;
            overflow-y: hidden;
            white-space: nowrap;
            scrollbar-width: thin;
        }
        div[data-testid="stTabs"] button[role="tab"] {
            flex: 0 0 auto;
            min-width: max-content;
        }
        div[role="radiogroup"] {
            flex-wrap: wrap;
            gap: 0.5rem;
        }
        .katex-display {
            overflow-x: auto;
            overflow-y: hidden;
            padding-bottom: 0.25rem;
        }
        div[data-testid="stTable"],
        div[data-testid="stDataFrame"] {
            overflow-x: auto;
        }
        div[data-testid="stImage"] {
            width: 100%;
            max-width: 100%;
            overflow: hidden;
        }
        div[data-testid="stImage"] img {
            width: 100%;
            max-width: 100%;
            object-fit: contain;
        }
        p, li, [data-testid="stCaptionContainer"] {
            overflow-wrap: anywhere;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.title("Quantum Lab")
    st.caption(t("sidebar_caption"))
    current_lang = get_lang()
    current_label = next((label for label, code in LANG_OPTIONS.items() if code == current_lang), "한국어")
    selected_label = st.selectbox(
        t("language"),
        options=list(LANG_OPTIONS.keys()),
        index=list(LANG_OPTIONS.keys()).index(current_label),
    )
    set_lang(LANG_OPTIONS[selected_label])

pages = [
    st.Page("pages/00_home.py", title=t("nav_home")),
    st.Page("pages/01_level0_bit_probability.py", title=t("nav_level0")),
    st.Page("pages/02_level1_qubit_placeholder.py", title=t("nav_level1")),
    st.Page("pages/03_level2_measurement.py", title=t("nav_level2")),
    st.Page("pages/04_level3_gates.py", title=t("nav_level3")),
    st.Page("pages/05_level4_interference.py", title=t("nav_level4")),
    st.Page("pages/06_level5_two_qubits.py", title=t("nav_level5")),
    st.Page("pages/07_level6_entanglement.py", title=t("nav_level6")),
    st.Page("pages/08_level7_algorithms.py", title=t("nav_level7")),
    st.Page("pages/09_level8_noise.py", title=t("nav_level8")),
    st.Page("pages/11_level9_circuit_reading.py", title=t("nav_level9")),
    st.Page("pages/12_level10_measurement_statistics.py", title=t("nav_level10")),
    st.Page("pages/13_level11_interference_depth.py", title=t("nav_level11")),
    st.Page("pages/14_level12_entanglement_limits.py", title=t("nav_level12")),
    st.Page("pages/10_photon_heist.py", title=t("nav_photon_heist")),
]

selected_page = st.navigation(pages)
selected_page.run()
