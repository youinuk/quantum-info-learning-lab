from __future__ import annotations

import importlib
import math

import streamlit as st

import core.simulator as simulator
from core.charts import compact_count_bar, phase_interference_sweep_chart, render_fig
from core.content import load_lesson_markdown, load_level_content, load_resources
from core.i18n import get_lang, t
from core.lesson_renderer import render_lesson_cards
from core.navigation import render_level_navigation
from core.quiz_renderer import render_quiz_items
from core.resource_renderer import render_resource_item
from core.safe_table import render_markdown_table
from core.terms_renderer import render_terms

if not hasattr(simulator, "simulate_phase_interference"):
    simulator = importlib.reload(simulator)

lang = get_lang()
content = load_level_content("level10", lang)


def clear_level10_results() -> None:
    st.session_state.pop("level10_result", None)


if st.session_state.get("_active_learning_page") != "level10":
    clear_level10_results()
    st.session_state.pop("level10_controls", None)
    st.session_state["level10_run_index"] = 0
st.session_state["_active_learning_page"] = "level10"

st.title(t("level10_title"))
st.write(content.get("goal", ""))

presentation_tab, simulation_tab, resources_tab, quiz_tab = st.tabs(
    [t("tab_presentation"), t("tab_simulation"), t("tab_resources"), t("tab_quiz")]
)

with presentation_tab:
    render_lesson_cards(load_lesson_markdown("level10", lang), "level10")
    render_terms(content)
    st.success(content.get("key_takeaway", ""))

with simulation_tab:
    ui = content.get("simulation_ui", {})

    st.subheader(t("phase_interference_lab_title"))
    st.write(content.get("simulation_intro", ""))
    st.info(ui.get("advanced_purpose", ""))

    for focus in content.get("simulation_focus", []):
        st.markdown(f"- {focus}")

    control1, control2 = st.columns(2)
    with control1:
        phase_degrees = st.slider(
            ui.get("phase_label", "Phase difference"),
            min_value=0,
            max_value=360,
            value=0,
            step=5,
            format="%d°",
        )
    with control2:
        shots = st.slider(t("shots"), 10, 5000, 1000, 10)

    phase_turns = phase_degrees / 360
    phase_radians = math.radians(phase_degrees)
    theoretical_bright = (1 + math.cos(phase_radians)) / 2
    theoretical_dark = 1 - theoretical_bright

    sweep_col, _ = st.columns([3, 1])
    with sweep_col:
        sweep_fig = phase_interference_sweep_chart(float(phase_degrees))
        render_fig(sweep_fig, width="stretch")
    st.caption(ui.get("curve_caption", ""))
    st.latex(
        rf"\Delta\phi={phase_degrees}^\circ,\qquad "
        rf"P(\mathrm{{bright}})=\frac{{1+\cos(\Delta\phi)}}{{2}}={theoretical_bright:.3f}"
    )

    current_controls = (int(phase_degrees), int(shots))
    previous_controls = st.session_state.get("level10_controls")
    if previous_controls is not None and previous_controls != current_controls:
        clear_level10_results()
    st.session_state["level10_controls"] = current_controls

    run_col, reset_col = st.columns([1, 1])
    if run_col.button(t("run_sim"), type="primary", width="stretch"):
        run_index = st.session_state.get("level10_run_index", 0) + 1
        st.session_state["level10_run_index"] = run_index
        st.session_state["level10_result"] = simulator.simulate_phase_interference(
            phase_turns,
            int(shots),
            12000 + run_index,
        )
    if reset_col.button(t("reset_state"), width="stretch"):
        clear_level10_results()
        st.session_state["level10_run_index"] = 0

    result = st.session_state.get("level10_result")
    if result is not None and (abs(result.phase_turns - phase_turns) > 1e-12 or result.shots != int(shots)):
        result = None

    if result is None:
        rows = [
            {
                ui.get("output_column", "Output"): "bright",
                ui.get("theory_column", "Theory"): f"{theoretical_bright * 100:.1f}%",
                ui.get("observed_column", "Observed"): "-",
                ui.get("count_column", "Count"): "-",
                ui.get("gap_column", "Gap"): "-",
            },
            {
                ui.get("output_column", "Output"): "dark",
                ui.get("theory_column", "Theory"): f"{theoretical_dark * 100:.1f}%",
                ui.get("observed_column", "Observed"): "-",
                ui.get("count_column", "Count"): "-",
                ui.get("gap_column", "Gap"): "-",
            },
        ]
        st.info(content.get("simulation_waiting", ""))
    else:
        observed_bright = result.count_bright / result.shots
        observed_dark = result.count_dark / result.shots
        rows = [
            {
                ui.get("output_column", "Output"): "bright",
                ui.get("theory_column", "Theory"): f"{result.probability_bright * 100:.1f}%",
                ui.get("observed_column", "Observed"): f"{observed_bright * 100:.1f}%",
                ui.get("count_column", "Count"): result.count_bright,
                ui.get("gap_column", "Gap"): f"{abs(observed_bright - result.probability_bright) * 100:.1f} pp",
            },
            {
                ui.get("output_column", "Output"): "dark",
                ui.get("theory_column", "Theory"): f"{result.probability_dark * 100:.1f}%",
                ui.get("observed_column", "Observed"): f"{observed_dark * 100:.1f}%",
                ui.get("count_column", "Count"): result.count_dark,
                ui.get("gap_column", "Gap"): f"{abs(observed_dark - result.probability_dark) * 100:.1f} pp",
            },
        ]

    st.markdown(f"### {ui.get('comparison_title', 'Theory and measurement')}")
    render_markdown_table(rows)

    if result is not None:
        metric1, metric2, metric3 = st.columns(3)
        metric1.metric(ui.get("phase_metric", "Phase"), f"{phase_degrees}°")
        metric2.metric(ui.get("predicted_bright", "Predicted bright"), f"{theoretical_bright * 100:.1f}%")
        metric3.metric(ui.get("observed_bright", "Observed bright"), f"{observed_bright * 100:.1f}%")

        if phase_degrees in {0, 360}:
            result_key = "result_constructive"
        elif phase_degrees == 180:
            result_key = "result_destructive"
        else:
            result_key = "result_partial"
        st.success(ui.get(result_key, "").format(phase=phase_degrees))

        chart_col, _ = st.columns([1, 1])
        with chart_col:
            fig = compact_count_bar(
                ["bright", "dark"],
                [result.count_bright, result.count_dark],
                "Interference measurement counts",
            )
            render_fig(fig, width="stretch")

        st.info(
            ui.get("sampling_note", "").format(
                gap=abs(observed_bright - theoretical_bright) * 100,
                shots=result.shots,
            )
        )

    st.caption(content.get("simulation_caption", ""))

with resources_tab:
    st.subheader(t("tab_resources"))
    for item in load_resources("level10", lang):
        render_resource_item(item)

with quiz_tab:
    st.subheader(t("tab_quiz"))
    render_quiz_items(content.get("quiz", []), "level10")

render_level_navigation(10)
