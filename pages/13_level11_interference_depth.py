from __future__ import annotations

import importlib

import pandas as pd
import streamlit as st

import core.simulator as simulator
from core.charts import compact_count_bar, render_pyplot
from core.content import BASE_DIR, load_lesson_markdown, load_level_content, load_resources
from core.i18n import get_lang, t
from core.lesson_renderer import render_lesson_cards
from core.navigation import render_level_navigation
from core.quiz_renderer import render_quiz_items
from core.resource_renderer import render_resource_item
from core.terms_renderer import render_terms

if not hasattr(simulator, "simulate_phase_interference"):
    simulator = importlib.reload(simulator)

lang = get_lang()
content = load_level_content("level11", lang)


def clear_level11_results() -> None:
    st.session_state.pop("level11_result", None)


if st.session_state.get("_active_learning_page") != "level11":
    clear_level11_results()
    st.session_state.pop("level11_controls", None)
    st.session_state["level11_run_index"] = 0
st.session_state["_active_learning_page"] = "level11"

st.title(t("level11_title"))
st.write(content.get("goal", ""))

presentation_tab, simulation_tab, resources_tab, quiz_tab = st.tabs(
    [t("tab_presentation"), t("tab_simulation"), t("tab_resources"), t("tab_quiz")]
)

with presentation_tab:
    render_lesson_cards(load_lesson_markdown("level11", lang), "level11")
    render_terms(content)
    st.success(content.get("key_takeaway", ""))

with simulation_tab:
    ui = content.get("simulation_ui", {})
    phase_options = content.get("phase_options", [])
    phase_by_id = {item["id"]: item for item in phase_options}

    st.subheader(t("phase_interference_lab_title"))
    st.write(content.get("simulation_intro", ""))
    for focus in content.get("simulation_focus", []):
        st.markdown(f"- {focus}")

    control1, control2 = st.columns(2)
    with control1:
        selected_phase = st.selectbox(
            ui.get("phase_label", "Phase difference"),
            options=list(phase_by_id),
            format_func=lambda phase_id: phase_by_id[phase_id]["label"],
        )
    with control2:
        shots = st.slider(t("shots"), 10, 5000, 1000, 10)

    selected = phase_by_id[selected_phase]
    image_path = BASE_DIR / selected.get("image", "")
    if image_path.is_file():
        st.image(str(image_path), caption=selected.get("label", ""), width="stretch")
    st.caption(selected.get("reading", ""))
    st.latex(selected.get("formula", ""))

    current_controls = (selected_phase, int(shots))
    previous_controls = st.session_state.get("level11_controls")
    if previous_controls is not None and previous_controls != current_controls:
        clear_level11_results()
    st.session_state["level11_controls"] = current_controls

    run_col, reset_col = st.columns([1, 1])
    if run_col.button(t("run_sim"), type="primary", width="stretch"):
        run_index = st.session_state.get("level11_run_index", 0) + 1
        st.session_state["level11_run_index"] = run_index
        st.session_state["level11_result"] = simulator.simulate_phase_interference(
            float(selected.get("phase_turns", 0.0)),
            int(shots),
            12000 + run_index,
        )
    if reset_col.button(t("reset_state"), width="stretch"):
        clear_level11_results()
        st.session_state["level11_run_index"] = 0

    result = st.session_state.get("level11_result")
    if result is not None and (result.phase_turns != float(selected.get("phase_turns", 0.0)) or result.shots != int(shots)):
        result = None

    if result is None:
        rows = [
            {ui.get("output_column", "Output"): "bright", ui.get("probability_column", "Probability"): "-", ui.get("count_column", "Count"): 0},
            {ui.get("output_column", "Output"): "dark", ui.get("probability_column", "Probability"): "-", ui.get("count_column", "Count"): 0},
        ]
        counts = [0, 0]
        st.info(content.get("simulation_waiting", ""))
    else:
        rows = [
            {
                ui.get("output_column", "Output"): "bright",
                ui.get("probability_column", "Probability"): f"{result.probability_bright:.3f}",
                ui.get("count_column", "Count"): result.count_bright,
            },
            {
                ui.get("output_column", "Output"): "dark",
                ui.get("probability_column", "Probability"): f"{result.probability_dark:.3f}",
                ui.get("count_column", "Count"): result.count_dark,
            },
        ]
        counts = [result.count_bright, result.count_dark]
        st.info(selected.get("result_note", ""))

    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")

    chart_col, _ = st.columns([1, 1])
    with chart_col:
        fig = compact_count_bar(
            ["bright", "dark"],
            counts,
            "Interference measurement counts",
        )
        render_pyplot(fig, width="stretch")

    st.caption(content.get("simulation_caption", ""))

with resources_tab:
    st.subheader(t("tab_resources"))
    for item in load_resources("level11", lang):
        render_resource_item(item)

with quiz_tab:
    st.subheader(t("tab_quiz"))
    render_quiz_items(content.get("quiz", []), "level11")

render_level_navigation(11)
