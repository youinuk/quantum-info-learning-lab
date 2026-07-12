"""Term table rendering helpers."""

from __future__ import annotations

import streamlit as st

from core.i18n import t
from core.safe_table import render_markdown_table


def render_terms(content: dict) -> None:
    terms = content.get("terms", [])
    if not terms:
        return
    st.markdown(f"### {content.get('terms_title', t('terms_title_default'))}")
    render_markdown_table(terms)
