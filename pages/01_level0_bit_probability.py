from __future__ import annotations

import streamlit as st

import core.simulator as simulator
from core.charts import compact_count_bar, render_fig
from core.content import load_lesson_markdown, load_level_content, load_resources
from core.i18n import get_lang, t
from core.lesson_renderer import render_lesson_cards
from core.navigation import render_level_navigation
from core.math_display import probability_from_label, probability_latex, probability_select_options
from core.quiz_renderer import render_quiz_items
from core.resource_renderer import render_resource_item
from core.terms_renderer import render_terms

lang = get_lang()
content = load_level_content("level0", lang)


def clear_level0_results() -> None:
    st.session_state.pop("level0_result", None)


if st.session_state.get("_active_learning_page") != "level0":
    clear_level0_results()
    st.session_state.pop("level0_controls", None)
    st.session_state["level0_run_index"] = 0
st.session_state["_active_learning_page"] = "level0"

st.title(t("level0_title"))
st.write(content.get("goal", t("level0_goal")))

presentation_tab, simulation_tab, resources_tab, quiz_tab = st.tabs(
    [t("tab_presentation"), t("tab_simulation"), t("tab_resources"), t("tab_quiz")]
)

with presentation_tab:
    render_lesson_cards(load_lesson_markdown("level0", lang), "level0")
    render_terms(content)
    st.success(content.get("key_takeaway", ""))

with simulation_tab:
    st.subheader(t("sim_title"))

    col1, col2 = st.columns(2)
    with col1:
        probability_label = st.selectbox(t("prob_one"), probability_select_options(), index=2)
    with col2:
        shots = st.slider(t("shots"), 10, 5000, 1000, 10)

    probability_one = probability_from_label(probability_label)
    current_controls = (probability_label, int(shots))
    previous_controls = st.session_state.get("level0_controls")
    if previous_controls is not None and previous_controls != current_controls:
        clear_level0_results()
    st.session_state["level0_controls"] = current_controls

    st.latex(rf"P(1) = {probability_latex(probability_one)},\quad P(0) = {probability_latex(1.0 - probability_one)}")

    run_col, reset_col = st.columns([1, 1])
    if run_col.button(t("run_sim"), type="primary", width="stretch"):
        run_index = st.session_state.get("level0_run_index", 0) + 1
        st.session_state["level0_run_index"] = run_index
        st.session_state["level0_result"] = simulator.simulate_bit_trials(
            probability_one, shots, 1000 + run_index
        )
    if reset_col.button(t("reset_state"), width="stretch"):
        clear_level0_results()
        st.session_state["level0_run_index"] = 0

    result = st.session_state.get("level0_result")
    if result is None:
        count_zero = 0
        count_one = 0
        observed_ratio = 0.0
    else:
        count_zero = result.count_zero
        count_one = result.count_one
        observed_ratio = result.observed_ratio_one

    if result is None:
        st.info(content.get("simulation_waiting", ""))

    st.markdown(f"### {t('result')}")
    metric1, metric2, metric3, metric4 = st.columns(4)
    metric1.metric(t("count_zero"), count_zero)
    metric2.metric(t("count_one"), count_one)
    metric3.metric(t("observed_ratio"), f"{observed_ratio:.3f}")
    metric4.metric(t("expected_ratio"), probability_label)

    chart_col, _ = st.columns([1, 1])
    with chart_col:
        fig = compact_count_bar(["0", "1"], [count_zero, count_one], "Result")
        render_fig(fig, width="stretch")

    st.caption(content.get("simulation_caption", ""))

with resources_tab:
    st.subheader(t("tab_resources"))
    resources = load_resources("level0", lang)
    for item in resources:
        render_resource_item(item)

with quiz_tab:
    st.subheader(t("tab_quiz"))
    render_quiz_items(content.get("quiz", []), "level0")

render_level_navigation(0)
