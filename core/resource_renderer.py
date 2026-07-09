"""Streamlit rendering helpers for learning resources."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from core.content import BASE_DIR
from core.i18n import t


def render_resource_item(item: dict) -> None:
    title = item.get("title", "Resource")
    item_type = item.get("type")
    url = item.get("url", "")

    if item_type in {"link", "video_link", "simulation_link", "article_link"}:
        st.markdown(f"[{title}]({url})")
        return

    if item_type == "local_image":
        path = BASE_DIR / Path(item.get("path", ""))
        if path.exists() and path.is_file():
            st.image(str(path), caption=item.get("caption", title), width=item.get("width"))
        else:
            st.warning(t("resource_missing").format(title=title, path=path))
