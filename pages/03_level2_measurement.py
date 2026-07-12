from __future__ import annotations

import streamlit as st

from core.charts import compact_count_bar, render_fig
from core.content import load_lesson_markdown, load_level_content, load_resources
from core.i18n import get_lang, t
from core.lesson_renderer import render_lesson_cards
from core.navigation import render_level_navigation
from core.math_display import (
    probability_from_label,
    probability_latex,
    probability_plain,
    probability_select_options,
    single_qubit_latex,
)
from core.quiz_renderer import render_quiz_items
from core.resource_renderer import render_resource_item
from core.safe_table import render_markdown_table
from core.simulator import simulate_bit_trials
from core.terms_renderer import render_terms

lang = get_lang()
content = load_level_content("level2", lang)

LEVEL2_RESULT_KEYS = ["level2_single", "level2_rows", "level2_batch"]


def clear_level2_results() -> None:
    for key in LEVEL2_RESULT_KEYS:
        st.session_state.pop(key, None)


if st.session_state.get("_active_learning_page") != "level2":
    clear_level2_results()
    st.session_state.pop("level2_controls", None)
    st.session_state["level2_run_index"] = 0
st.session_state["_active_learning_page"] = "level2"

st.title(t("level2_title"))
st.write(content.get("goal", ""))

presentation_tab, simulation_tab, resources_tab, quiz_tab = st.tabs(
    [t("tab_presentation"), t("tab_simulation"), t("tab_resources"), t("tab_quiz")]
)

with presentation_tab:
    render_lesson_cards(load_lesson_markdown("level2", lang), "level2")
    render_terms(content)
    st.success(content.get("key_takeaway", ""))

with simulation_tab:
    st.subheader(t("measurement_lab_title"))
    st.write(content.get("simulation_intro", ""))

    col1, col2 = st.columns(2)
    with col1:
        probability_label = st.selectbox(t("prob_one"), probability_select_options(), index=2)
    with col2:
        batch = st.selectbox(t("measurement_batch"), [10, 100, 1000], index=1)

    probability_one = probability_from_label(probability_label)
    current_controls = (probability_label, int(batch))
    previous_controls = st.session_state.get("level2_controls")
    if previous_controls is not None and previous_controls != current_controls:
        clear_level2_results()
    st.session_state["level2_controls"] = current_controls

    st.latex(single_qubit_latex(probability_one))
    st.latex(rf"P(0)={probability_latex(1.0 - probability_one)},\quad P(1)={probability_latex(probability_one)}")

    run_col, reset_col = st.columns([1, 1])
    if run_col.button(t("run_sim"), type="primary", width="stretch"):
        run_index = st.session_state.get("level2_run_index", 0) + 1
        st.session_state["level2_run_index"] = run_index
        st.session_state["level2_single"] = simulate_bit_trials(probability_one, 1, 4000 + run_index)
        st.session_state["level2_rows"] = [
            simulate_bit_trials(probability_one, shots, 5000 + run_index + shots) for shots in [1, 10, 100, 1000]
        ]
        st.session_state["level2_batch"] = simulate_bit_trials(probability_one, int(batch), 6000 + run_index)
    if reset_col.button(t("reset_state"), width="stretch"):
        clear_level2_results()
        st.session_state["level2_run_index"] = 0

    single = st.session_state.get("level2_single")
    measured_value = "-" if single is None else ("1" if single.count_one else "0")
    after_state = "-" if single is None else f"|{measured_value}>"

    state1, state2, state3 = st.columns(3)
    state1.metric(t("expected_zero"), probability_plain(1.0 - probability_one))
    state2.metric(t("expected_ratio"), probability_label)
    state3.metric(t("single_result"), measured_value)

    if single is None:
        st.info(content.get("simulation_waiting", ""))
    else:
        st.info(t("measurement_state_explanation").format(result=measured_value, state=after_state))

    rows = []
    for shots, result in zip([1, 10, 100, 1000], st.session_state.get("level2_rows", [])):
        rows.append(
            {
                t("shots"): shots,
                t("count_zero"): result.count_zero,
                t("count_one"): result.count_one,
                t("observed_ratio"): round(result.observed_ratio_one, 3),
            }
        )
    if not rows:
        rows = [{t("shots"): shots, t("count_zero"): 0, t("count_one"): 0, t("observed_ratio"): 0.0} for shots in [1, 10, 100, 1000]]
    render_markdown_table(rows)

    result = st.session_state.get("level2_batch")
    count_zero = 0 if result is None else result.count_zero
    count_one = 0 if result is None else result.count_one
    chart_col, _ = st.columns([1, 1])
    with chart_col:
        fig = compact_count_bar(["0", "1"], [count_zero, count_one], "Result")
        render_fig(fig, width="stretch")
    st.caption(content.get("simulation_caption", ""))

with resources_tab:
    st.subheader(t("tab_resources"))
    for item in load_resources("level2", lang):
        render_resource_item(item)

with quiz_tab:
    st.subheader(t("tab_quiz"))
    render_quiz_items(content.get("quiz", []), "level2")

render_level_navigation(2)
