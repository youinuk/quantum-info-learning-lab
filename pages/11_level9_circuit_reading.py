from __future__ import annotations

import importlib

import pandas as pd
import streamlit as st

import core.simulator as simulator
from core.charts import compact_count_bar
from core.content import BASE_DIR, load_lesson_markdown, load_level_content, load_resources
from core.i18n import get_lang, t
from core.lesson_renderer import render_lesson_cards
from core.navigation import render_level_navigation
from core.quiz_renderer import render_quiz_items
from core.resource_renderer import render_resource_item
from core.terms_renderer import render_terms

if not hasattr(simulator, "simulate_named_circuit"):
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

with presentation_tab:
    render_lesson_cards(load_lesson_markdown("level9", lang), "level9")
    render_terms(content)
    st.success(content.get("key_takeaway", ""))

with simulation_tab:
    ui = content.get("simulation_ui", {})
    circuit_options = content.get("circuit_options", [])
    circuit_by_id = {item["id"]: item for item in circuit_options}

    st.subheader(t("circuit_reading_lab_title"))
    st.write(content.get("simulation_intro", ""))

    control1, control2 = st.columns(2)
    with control1:
        selected_circuit = st.selectbox(
            ui.get("circuit_label", "Circuit"),
            options=list(circuit_by_id),
            format_func=lambda circuit_id: circuit_by_id[circuit_id]["label"],
        )
    with control2:
        shots = st.slider(t("shots"), 10, 5000, 1000, 10)

    selected = circuit_by_id[selected_circuit]
    image_path = BASE_DIR / selected.get("image", "")
    if image_path.is_file():
        st.image(str(image_path), caption=selected.get("label", ""), width="stretch")
    else:
        st.code(selected.get("diagram", ""), language="text")
    st.caption(selected.get("reading", ""))

    current_controls = (selected_circuit, int(shots))
    previous_controls = st.session_state.get("level9_controls")
    if previous_controls is not None and previous_controls != current_controls:
        clear_level9_results()
    st.session_state["level9_controls"] = current_controls

    run_col, reset_col = st.columns([1, 1])
    if run_col.button(t("run_sim"), type="primary", width="stretch"):
        run_index = st.session_state.get("level9_run_index", 0) + 1
        st.session_state["level9_run_index"] = run_index
        st.session_state["level9_result"] = simulator.simulate_named_circuit(
            selected_circuit,
            int(shots),
            10000 + run_index,
        )
    if reset_col.button(t("reset_state"), width="stretch"):
        clear_level9_results()
        st.session_state["level9_run_index"] = 0

    result = st.session_state.get("level9_result")
    if result is not None and (result.circuit_id != selected_circuit or result.shots != int(shots)):
        result = None

    labels = tuple(selected.get("labels", ["0", "1"]))
    if result is None:
        probabilities = [0.0 for _ in labels]
        counts = [0 for _ in labels]
        st.info(content.get("simulation_waiting", ""))
    else:
        probabilities = list(result.probabilities)
        counts = list(result.counts)
        st.latex(result.state_latex)
        st.info(selected.get("result_note", ""))

    rows = [
        {
            ui.get("outcome_column", "Outcome"): label,
            ui.get("probability_column", "Probability"): f"{probability:.2f}",
            ui.get("count_column", "Count"): count,
        }
        for label, probability, count in zip(labels, probabilities, counts)
    ]
    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")

    chart_col, _ = st.columns([1, 1])
    with chart_col:
        fig = compact_count_bar(
            list(labels),
            counts,
            "Measurement counts",
        )
        st.pyplot(fig, width="stretch")

    with st.expander(ui.get("sdk_title", "SDK preview")):
        st.write(selected.get("sdk_note", ""))
        st.code(selected.get("qiskit", ""), language="python")
        st.code(selected.get("cirq", ""), language="python")

with resources_tab:
    st.subheader(t("tab_resources"))
    for item in load_resources("level9", lang):
        render_resource_item(item)

with quiz_tab:
    st.subheader(t("tab_quiz"))
    render_quiz_items(content.get("quiz", []), "level9")

render_level_navigation(9)
