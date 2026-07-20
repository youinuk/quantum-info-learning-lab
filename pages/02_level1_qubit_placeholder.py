from __future__ import annotations

import streamlit as st

import core.simulator as simulator
from core.charts import compact_count_bar, render_fig
from core.content import load_lesson_markdown, load_level_content, load_resources
from core.i18n import get_lang, t
from core.lesson_renderer import render_lesson_cards
from core.navigation import render_level_navigation
from core.math_display import probability_from_label, probability_latex, probability_select_options, single_qubit_latex
from core.quiz_renderer import render_quiz_items
from core.resource_renderer import render_resource_item
from core.terms_renderer import render_terms

lang = get_lang()
content = load_level_content("level1", lang)


def clear_level1_results() -> None:
    st.session_state.pop("level1_result", None)
    st.session_state.pop("level1_single", None)


if st.session_state.get("_active_learning_page") != "level1":
    clear_level1_results()
    st.session_state.pop("level1_controls", None)
    st.session_state["level1_run_index"] = 0
st.session_state["_active_learning_page"] = "level1"

st.title(t("level1_title"))
st.write(content.get("goal", t("level1_placeholder")))

presentation_tab, simulation_tab, resources_tab, quiz_tab = st.tabs(
    [t("tab_presentation"), t("tab_simulation"), t("tab_resources"), t("tab_quiz")]
)

with presentation_tab:
    st.subheader(content.get("presentation_title", t("tab_presentation")))
    render_lesson_cards(load_lesson_markdown("level1", lang), "level1")
    render_terms(content)
    st.success(content.get("key_takeaway", ""))

with simulation_tab:
    st.subheader(t("qubit_sim_title"))
    st.write(content.get("simulation_intro", ""))

    col1, col2 = st.columns(2)
    with col1:
        probability_label = st.selectbox(t("prob_one"), probability_select_options(), index=2)
    with col2:
        shots = st.slider(t("shots"), 10, 5000, 1000, 10)

    probability_one = probability_from_label(probability_label)
    current_controls = (probability_label, int(shots))
    previous_controls = st.session_state.get("level1_controls")
    if previous_controls is not None and previous_controls != current_controls:
        clear_level1_results()
    st.session_state["level1_controls"] = current_controls

    st.latex(single_qubit_latex(probability_one))
    st.latex(rf"P(0)={probability_latex(1.0 - probability_one)},\quad P(1)={probability_latex(probability_one)}")

    run_col, reset_col = st.columns([1, 1])
    if run_col.button(t("run_sim"), type="primary", width="stretch"):
        run_index = st.session_state.get("level1_run_index", 0) + 1
        st.session_state["level1_run_index"] = run_index
        st.session_state["level1_result"] = simulator.simulate_bit_trials(
            probability_one, shots, 2000 + run_index
        )
        st.session_state["level1_single"] = simulator.simulate_bit_trials(
            probability_one, 1, 3000 + run_index
        )
    if reset_col.button(t("reset_state"), width="stretch"):
        clear_level1_results()
        st.session_state["level1_run_index"] = 0

    result = st.session_state.get("level1_result")
    if result is None:
        count_zero = 0
        count_one = 0
    else:
        count_zero = result.count_zero
        count_one = result.count_one

    if result is None:
        st.info(content.get("simulation_waiting", ""))

    chart_col, _ = st.columns([1, 1])
    with chart_col:
        fig = compact_count_bar(["0", "1"], [count_zero, count_one], "Result")
        render_fig(fig, width="stretch")
    st.caption(t("qubit_sim_caption"))

    st.markdown(f"### {t('single_measurement')}")
    single = st.session_state.get("level1_single")
    measured_value = "-" if single is None else ("1" if single.count_one else "0")
    st.metric(t("single_result"), measured_value)
    st.caption(content.get("single_measurement_caption", ""))

with resources_tab:
    st.subheader(t("tab_resources"))
    for item in load_resources("level1", lang):
        render_resource_item(item)

with quiz_tab:
    st.subheader(t("tab_quiz"))
    render_quiz_items(content.get("quiz", []), "level1")

render_level_navigation(1)
