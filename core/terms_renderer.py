"""Term table rendering helpers."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from core.i18n import t


def render_terms(content: dict) -> None:
    terms = content.get("terms", [])
    if not terms:
        return
    st.markdown(f"### {content.get('terms_title', t('terms_title_default'))}")
    st.table(pd.DataFrame(terms))
