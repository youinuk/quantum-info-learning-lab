from __future__ import annotations

import streamlit as st

from core.i18n import t
from core.navigation import LEVEL_PAGES

st.session_state["_active_learning_page"] = "home"

st.title(t("app_title"))
st.caption(t("app_subtitle"))

col1, col2 = st.columns(2)

with col1:
    st.subheader(t("home_goal_title"))
    st.write(t("home_goal_body"))

with col2:
    st.subheader(t("home_structure_title"))
    st.write(t("home_structure_body"))

st.info(t("home_start"))

st.divider()

st.subheader(t("roadmap_title"))
st.write(t("home_path_intro"))

for group_title, levels in (
    (t("home_path_foundations"), range(0, 3)),
    (t("home_path_circuits"), range(3, 6)),
    (t("home_path_quantum"), range(6, 9)),
):
    st.markdown(f"### {group_title}")
    columns = st.columns(3)
    for column, level in zip(columns, levels):
        with column:
            st.page_link(
                LEVEL_PAGES[level],
                label=t(f"nav_level{level}"),
                icon=":material/menu_book:",
                width="stretch",
            )
