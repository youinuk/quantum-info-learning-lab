from __future__ import annotations

import importlib

import streamlit as st

import core.simulator as simulator
from core.charts import compact_dual_interval_bar, render_fig
from core.content import load_lesson_markdown, load_level_content, load_resources
from core.i18n import get_lang, t
from core.lesson_renderer import render_lesson_cards
from core.math_display import probability_from_label, probability_select_options
from core.navigation import render_level_navigation
from core.quiz_renderer import render_quiz_items
from core.resource_renderer import render_resource_item
from core.safe_table import render_markdown_table
from core.terms_renderer import render_terms

if not hasattr(simulator, "simulate_measurement_series"):
    simulator = importlib.reload(simulator)

lang = get_lang()
content = load_level_content("level9", lang)


def clear_level9_results() -> None:
    st.session_state.pop("level9_result", None)


if st.session_state.get("_active_learning_page") != "level9":
    clear_level9_results()
    st.session_state.pop("level9_controls", None)
    st.session_state["level9_run_index"] = 0
st.session_state["_active_learning_page"] = "level9"

st.title(t("level9_title"))
st.write(content.get("goal", ""))

presentation_tab, simulation_tab, resources_tab, quiz_tab = st.tabs(
    [t("tab_presentation"), t("tab_simulation"), t("tab_resources"), t("tab_quiz")]
)

NOISE_OPTIONS = {
    "0%": 0.0,
    "5%": 0.05,
    "10%": 0.10,
    "20%": 0.20,
}
SHOT_COUNTS = (10, 100, 1000)
BATCH_COUNT = 30

with presentation_tab:
    render_lesson_cards(load_lesson_markdown("level9", lang), "level9")
    render_terms(content)
    st.success(content.get("key_takeaway", ""))

with simulation_tab:
    ui = content.get("simulation_ui", {})

    st.subheader(t("statistics_lab_title"))
    st.write(content.get("simulation_intro", ""))
    for focus in content.get("simulation_focus", []):
        st.markdown(f"- {focus}")

    control1, control2 = st.columns(2)
    with control1:
        probability_label = st.selectbox(t("prob_one"), probability_select_options(), index=2)
    with control2:
        noise_label = st.selectbox(t("noise_rate"), list(NOISE_OPTIONS.keys()), index=1)

    current_controls = (probability_label, noise_label)
    previous_controls = st.session_state.get("level9_controls")
    if previous_controls is not None and previous_controls != current_controls:
        clear_level9_results()
    st.session_state["level9_controls"] = current_controls

    run_col, reset_col = st.columns([1, 1])
    if run_col.button(t("run_sim"), type="primary", width="stretch"):
        run_index = st.session_state.get("level9_run_index", 0) + 1
        st.session_state["level9_run_index"] = run_index
        st.session_state["level9_result"] = simulator.simulate_measurement_series(
            probability_from_label(probability_label),
            NOISE_OPTIONS[noise_label],
            SHOT_COUNTS,
            BATCH_COUNT,
            11000 + run_index,
        )
    if reset_col.button(t("reset_state"), width="stretch"):
        clear_level9_results()
        st.session_state["level9_run_index"] = 0

    result = st.session_state.get("level9_result")
    if result is None:
        rows = [
            {
                ui.get("shots_column", "Shots"): shots,
                ui.get("batch_column", "Batches"): BATCH_COUNT,
                ui.get("ideal_mean_column", "Ideal mean"): "-",
                ui.get("ideal_range_column", "Ideal range"): "-",
                ui.get("noisy_mean_column", "Noisy mean"): "-",
                ui.get("noisy_range_column", "Noisy range"): "-",
            }
            for shots in SHOT_COUNTS
        ]
        ideal_means = [0.0 for _ in SHOT_COUNTS]
        ideal_lows = [0.0 for _ in SHOT_COUNTS]
        ideal_highs = [0.0 for _ in SHOT_COUNTS]
        noisy_means = [0.0 for _ in SHOT_COUNTS]
        noisy_lows = [0.0 for _ in SHOT_COUNTS]
        noisy_highs = [0.0 for _ in SHOT_COUNTS]
        target = probability_from_label(probability_label) * 100
        st.info(content.get("simulation_waiting", ""))
    else:
        rows = [
            {
                ui.get("shots_column", "Shots"): row.shots,
                ui.get("batch_column", "Batches"): row.batch_count,
                ui.get("ideal_mean_column", "Ideal mean"): f"{row.ideal_ratio_mean:.3f}",
                ui.get("ideal_range_column", "Ideal range"): f"{row.ideal_ratio_min:.3f} - {row.ideal_ratio_max:.3f}",
                ui.get("noisy_mean_column", "Noisy mean"): f"{row.noisy_ratio_mean:.3f}",
                ui.get("noisy_range_column", "Noisy range"): f"{row.noisy_ratio_min:.3f} - {row.noisy_ratio_max:.3f}",
            }
            for row in result.rows
        ]
        ideal_means = [row.ideal_ratio_mean * 100 for row in result.rows]
        ideal_lows = [row.ideal_ratio_min * 100 for row in result.rows]
        ideal_highs = [row.ideal_ratio_max * 100 for row in result.rows]
        noisy_means = [row.noisy_ratio_mean * 100 for row in result.rows]
        noisy_lows = [row.noisy_ratio_min * 100 for row in result.rows]
        noisy_highs = [row.noisy_ratio_max * 100 for row in result.rows]
        target = result.probability_one * 100
        st.info(content.get("result_note", ""))

    render_markdown_table(rows)

    chart_col, _ = st.columns([1, 1])
    with chart_col:
        fig = compact_dual_interval_bar(
            [str(shots) for shots in SHOT_COUNTS],
            ideal_means,
            ideal_lows,
            ideal_highs,
            noisy_means,
            noisy_lows,
            noisy_highs,
            "ideal",
            "noisy",
            "Mean and range across batches",
            ylabel="ratio of 1 (%)",
            target=target,
        )
        render_fig(fig, width="stretch")

    st.caption(content.get("simulation_caption", ""))

with resources_tab:
    st.subheader(t("tab_resources"))
    for item in load_resources("level9", lang):
        render_resource_item(item)

with quiz_tab:
    st.subheader(t("tab_quiz"))
    render_quiz_items(content.get("quiz", []), "level9")

render_level_navigation(9)
