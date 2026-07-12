from __future__ import annotations

import streamlit as st

from core.charts import compact_count_bar, render_fig
from core.content import load_lesson_markdown, load_level_content, load_resources
from core.i18n import get_lang, t
from core.lesson_renderer import render_lesson_cards
from core.navigation import render_level_navigation
from core.math_display import qubit_state_latex
from core.quiz_renderer import render_quiz_items
from core.resource_renderer import render_resource_item
from core.simulator import apply_single_qubit_gate, basis_state
from core.terms_renderer import render_terms

lang = get_lang()
content = load_level_content("level4", lang)


def clear_level4_results() -> None:
    st.session_state.pop("level4_after_middle", None)
    st.session_state.pop("level4_final_state", None)


if st.session_state.get("_active_learning_page") != "level4":
    clear_level4_results()
    st.session_state.pop("level4_controls", None)
st.session_state["_active_learning_page"] = "level4"

st.title(t("level4_title"))
st.write(content.get("goal", ""))

presentation_tab, simulation_tab, resources_tab, quiz_tab = st.tabs(
    [t("tab_presentation"), t("tab_simulation"), t("tab_resources"), t("tab_quiz")]
)

with presentation_tab:
    render_lesson_cards(load_lesson_markdown("level4", lang), "level4")
    render_terms(content)
    st.success(content.get("key_takeaway", ""))

with simulation_tab:
    ui = content.get("simulation_ui", {})
    st.subheader(t("interference_lab_title"))
    st.write(content.get("simulation_intro", ""))

    middle_gate = st.radio(
        t("middle_operation"),
        [t("middle_none"), "Z"],
        horizontal=True,
    )

    previous_control = st.session_state.get("level4_controls")
    if previous_control is not None and previous_control != middle_gate:
        clear_level4_results()
    st.session_state["level4_controls"] = middle_gate

    run_col, reset_col = st.columns([1, 1])
    if run_col.button(t("run_sim"), type="primary", width="stretch"):
        state = basis_state("0")
        after_first_h = apply_single_qubit_gate(state, "H")
        after_middle = after_first_h if middle_gate == t("middle_none") else apply_single_qubit_gate(after_first_h, "Z")
        final_state = apply_single_qubit_gate(after_middle, "H")
        st.session_state["level4_after_middle"] = after_middle
        st.session_state["level4_final_state"] = final_state
    if reset_col.button(t("reset_state"), width="stretch"):
        clear_level4_results()

    after_middle = st.session_state.get("level4_after_middle")
    final_state = st.session_state.get("level4_final_state")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption(ui.get("start_state", "Start"))
        st.latex(r"\lvert0\rangle")
    with col2:
        st.caption(ui.get("middle_state", "Middle"))
        if after_middle is None:
            st.write("-")
        else:
            st.latex(qubit_state_latex(after_middle.alpha, after_middle.beta))
    with col3:
        st.caption(ui.get("final_state", "Final"))
        if final_state is None:
            st.write("-")
        else:
            st.latex(qubit_state_latex(final_state.alpha, final_state.beta))

    p0 = 0 if final_state is None else round(final_state.probability_zero * 100)
    p1 = 0 if final_state is None else round(final_state.probability_one * 100)
    metric1, metric2 = st.columns(2)
    metric1.metric(t("expected_zero"), f"{p0}%")
    metric2.metric(t("expected_ratio"), f"{p1}%")

    chart_col, _ = st.columns([1, 1])
    with chart_col:
        fig = compact_count_bar(
            ["0", "1"],
            [p0, p1],
            "Measurement probability",
            ylabel="probability (%)",
        )
        render_fig(fig, width="stretch")

    message_key = "simulation_waiting" if final_state is None else "simulation_hint"
    st.info(content.get(message_key, ""))

with resources_tab:
    st.subheader(t("tab_resources"))
    for item in load_resources("level4", lang):
        render_resource_item(item)

with quiz_tab:
    st.subheader(t("tab_quiz"))
    render_quiz_items(content.get("quiz", []), "level4")

render_level_navigation(4)
