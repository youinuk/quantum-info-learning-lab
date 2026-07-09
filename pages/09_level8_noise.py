from __future__ import annotations

import pandas as pd
import streamlit as st

from core.charts import compact_grouped_bar
from core.content import load_lesson_markdown, load_level_content, load_resources
from core.i18n import get_lang, t
from core.lesson_renderer import render_lesson_cards
from core.navigation import render_level_navigation
from core.math_display import probability_from_label, probability_select_options
from core.quiz_renderer import render_quiz_items
from core.resource_renderer import render_resource_item
from core.simulator import simulate_noisy_bit_measurements
from core.terms_renderer import render_terms

lang = get_lang()
content = load_level_content("level8", lang)


def clear_level8_results() -> None:
    st.session_state.pop("level8_result", None)


if st.session_state.get("_active_learning_page") != "level8":
    clear_level8_results()
    st.session_state.pop("level8_controls", None)
    st.session_state["level8_run_index"] = 0
st.session_state["_active_learning_page"] = "level8"

st.title(t("level8_title"))
st.write(content.get("goal", ""))

presentation_tab, simulation_tab, resources_tab, quiz_tab = st.tabs(
    [t("tab_presentation"), t("tab_simulation"), t("tab_resources"), t("tab_quiz")]
)

NOISE_OPTIONS = {
    "0%": 0.0,
    "5%": 0.05,
    "10%": 0.10,
    "20%": 0.20,
    "30%": 0.30,
}

with presentation_tab:
    render_lesson_cards(load_lesson_markdown("level8", lang), "level8")
    render_terms(content)
    st.success(content.get("key_takeaway", ""))

with simulation_tab:
    ui = content.get("simulation_ui", {})
    st.subheader(t("noise_lab_title"))
    st.write(content.get("simulation_intro", ""))

    col1, col2, col3 = st.columns(3)
    with col1:
        probability_label = st.selectbox(t("prob_one"), probability_select_options(), index=3)
    with col2:
        noise_label = st.selectbox(t("noise_rate"), list(NOISE_OPTIONS.keys()), index=2)
    with col3:
        shots = st.slider(t("shots"), 10, 5000, 1000, 10)

    current_controls = (probability_label, noise_label, int(shots))
    previous_controls = st.session_state.get("level8_controls")
    if previous_controls is not None and previous_controls != current_controls:
        clear_level8_results()
    st.session_state["level8_controls"] = current_controls

    run_col, reset_col = st.columns([1, 1])
    if run_col.button(t("run_sim"), type="primary", width="stretch"):
        run_index = st.session_state.get("level8_run_index", 0) + 1
        st.session_state["level8_run_index"] = run_index
        st.session_state["level8_result"] = simulate_noisy_bit_measurements(
            probability_from_label(probability_label),
            NOISE_OPTIONS[noise_label],
            int(shots),
            9000 + run_index,
        )
    if reset_col.button(t("reset_state"), width="stretch"):
        clear_level8_results()
        st.session_state["level8_run_index"] = 0

    result = st.session_state.get("level8_result")
    if result is None:
        rows = [
            {ui.get("case_column", "Case"): t("ideal_result"), ui.get("count_zero_column", "Count 0"): 0, ui.get("count_one_column", "Count 1"): 0},
            {ui.get("case_column", "Case"): t("noisy_result"), ui.get("count_zero_column", "Count 0"): 0, ui.get("count_one_column", "Count 1"): 0},
        ]
        ideal_counts = [0, 0]
        noisy_counts = [0, 0]
        noisy_ratio: float | str = "-"
    else:
        rows = [
            {ui.get("case_column", "Case"): t("ideal_result"), ui.get("count_zero_column", "Count 0"): result.ideal_count_zero, ui.get("count_one_column", "Count 1"): result.ideal_count_one},
            {ui.get("case_column", "Case"): t("noisy_result"), ui.get("count_zero_column", "Count 0"): result.noisy_count_zero, ui.get("count_one_column", "Count 1"): result.noisy_count_one},
        ]
        ideal_counts = [result.ideal_count_zero, result.ideal_count_one]
        noisy_counts = [result.noisy_count_zero, result.noisy_count_one]
        noisy_ratio = result.noisy_ratio_one

    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
    ratio_text = noisy_ratio if isinstance(noisy_ratio, str) else f"{noisy_ratio:.3f}"
    st.metric(t("observed_ratio"), ratio_text)

    chart_col, _ = st.columns([1, 1])
    with chart_col:
        fig = compact_grouped_bar(
            ["0", "1"],
            ideal_counts,
            noisy_counts,
            "ideal",
            "noisy",
            "Ideal vs noisy measurement",
        )
        st.pyplot(fig, width="stretch")

    if result is None:
        st.info(content.get("simulation_waiting", ""))
    st.caption(content.get("simulation_caption", ""))

with resources_tab:
    st.subheader(t("tab_resources"))
    for item in load_resources("level8", lang):
        render_resource_item(item)

with quiz_tab:
    st.subheader(t("tab_quiz"))
    render_quiz_items(content.get("quiz", []), "level8")

render_level_navigation(8)
