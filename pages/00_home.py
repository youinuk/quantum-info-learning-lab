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

level_count = len(LEVEL_PAGES)
roadmap_groups = (
    (t("home_path_foundations"), range(0, min(3, level_count))),
    (t("home_path_circuits"), range(3, min(6, level_count))),
    (t("home_path_quantum"), range(6, level_count)),
)

for group_title, levels in roadmap_groups:
    if not levels:
        continue
    st.markdown(f"### {group_title}")
    group_levels = list(levels)
    for row_start in range(0, len(group_levels), 3):
        columns = st.columns(3)
        for column, level in zip(columns, group_levels[row_start : row_start + 3]):
            with column:
                st.page_link(
                    LEVEL_PAGES[level],
                    label=t(f"nav_level{level}"),
                    icon=":material/menu_book:",
                    width="stretch",
                )
