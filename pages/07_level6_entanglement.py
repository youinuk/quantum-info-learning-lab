from __future__ import annotations

import streamlit as st

from core.charts import compact_count_bar, render_fig
from core.content import load_lesson_markdown, load_level_content, load_resources
from core.i18n import get_lang, t
from core.lesson_renderer import render_lesson_cards
from core.navigation import render_level_navigation
from core.quiz_renderer import render_quiz_items
from core.resource_renderer import render_resource_item
from core.safe_table import render_markdown_table
from core.simulator import simulate_two_basis_correlations
from core.terms_renderer import render_terms

lang = get_lang()
content = load_level_content("level6", lang)
st.session_state["_active_learning_page"] = "level6"

st.title(t("level6_title"))
st.write(content.get("goal", ""))

presentation_tab, simulation_tab, resources_tab, quiz_tab = st.tabs(
    [t("tab_presentation"), t("tab_simulation"), t("tab_resources"), t("tab_quiz")]
)

with presentation_tab:
    render_lesson_cards(load_lesson_markdown("level6", lang), "level6")
    render_terms(content)
    st.success(content.get("key_takeaway", ""))

with simulation_tab:
    ui = content.get("simulation_ui", {})
    state_options = content.get("state_options", [])
    state_by_id = {item["id"]: item for item in state_options}

    st.subheader(t("entanglement_lab_title"))
    st.write(content.get("simulation_intro", ""))

    control1, control2 = st.columns(2)
    with control1:
        selected_state = st.selectbox(
            ui.get("state_label", "State"),
            options=list(state_by_id),
            format_func=lambda state_id: state_by_id[state_id]["label"],
        )
    with control2:
        shots = st.slider(t("shots"), 10, 5000, 1000, 10)

    st.latex(state_by_id[selected_state]["latex"])
    st.caption(content.get("simulation_caption", ""))

    run_col, reset_col = st.columns([1, 1])
    if run_col.button(t("run_sim"), type="primary", width="stretch"):
        run_index = st.session_state.get("level6_run_index", 0) + 1
        st.session_state["level6_run_index"] = run_index
        st.session_state["level6_result"] = simulate_two_basis_correlations(
            selected_state,
            int(shots),
            7000 + run_index,
        )
    if reset_col.button(t("reset_state"), width="stretch"):
        st.session_state.pop("level6_result", None)
        st.session_state["level6_run_index"] = 0

    result = st.session_state.get("level6_result")
    if result is not None and (result.state_kind != selected_state or result.shots != int(shots)):
        result = None

    basis = st.radio(ui.get("basis_view", "Basis"), ["Z", "X"], horizontal=True)

    if result is None:
        z_ratio: float | str = "-"
        x_ratio: float | str = "-"
        counts = [0, 0, 0, 0]
        rows = [
            {
                ui.get("state_column", "Outcome"): label,
                ui.get("z_count_column", "Z count"): 0,
                ui.get("x_count_column", "X count"): 0,
            }
            for label in ["00", "01", "10", "11"]
        ]
        st.info(ui.get("waiting_note", ""))
    else:
        z_ratio = f"{result.same_result_ratio('Z'):.3f}"
        x_ratio = f"{result.same_result_ratio('X'):.3f}"
        counts = list(result.counts_for(basis))
        rows = [
            {
                ui.get("state_column", "Outcome"): label,
                ui.get("z_count_column", "Z count"): z_count,
                ui.get("x_count_column", "X count"): x_count,
            }
            for label, z_count, x_count in zip(result.labels(), result.z_counts, result.x_counts)
        ]

    metric1, metric2 = st.columns(2)
    metric1.metric(ui.get("z_same_ratio", "Same in Z"), z_ratio)
    metric2.metric(ui.get("x_same_ratio", "Same in X"), x_ratio)

    render_markdown_table(rows)

    chart_col, _ = st.columns([1, 1])
    with chart_col:
        fig = compact_count_bar(
            ["00", "01", "10", "11"],
            counts,
            f"{basis}-basis measurement",
        )
        render_fig(fig, width="stretch")

    if result is not None:
        st.info(ui.get("result_explanations", {}).get(result.state_kind, ""))

    with st.expander(ui.get("comparison_title", "Compare the three states")):
        comparison_columns = ui.get("comparison_columns", [])
        comparison_rows = [
            dict(zip(comparison_columns, row))
            for row in ui.get("comparison_rows", [])
        ]
        render_markdown_table(comparison_rows, comparison_columns)

with resources_tab:
    st.subheader(t("tab_resources"))
    for item in load_resources("level6", lang):
        render_resource_item(item)

with quiz_tab:
    st.subheader(t("tab_quiz"))
    render_quiz_items(content.get("quiz", []), "level6")

render_level_navigation(6)
