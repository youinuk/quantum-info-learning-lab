from __future__ import annotations

import streamlit as st

import core.simulator as simulator
from core.charts import compact_count_bar, render_fig
from core.content import BASE_DIR, load_lesson_markdown, load_level_content, load_resources
from core.i18n import get_lang, t
from core.lesson_renderer import render_lesson_cards
from core.navigation import render_level_navigation
from core.quantum_conventions import basis_labels
from core.math_display import (
    probability_from_label,
    probability_select_options,
    two_qubit_probability_text,
)
from core.quiz_renderer import render_quiz_items
from core.resource_renderer import render_resource_item
from core.runtime_modules import ensure_module_api
from core.safe_table import render_markdown_table
from core.terms_renderer import render_terms


simulator = ensure_module_api(
    simulator,
    minimum_version=0,
    required_attributes=("apply_two_qubit_basis_gate", "independent_two_qubit_distribution"),
)

lang = get_lang()
content = load_level_content("level5", lang)


def clear_level5_results() -> None:
    st.session_state.pop("level5_distribution", None)
    st.session_state.pop("level5_gate_result", None)


if st.session_state.get("_active_learning_page") != "level5":
    clear_level5_results()
    st.session_state.pop("level5_controls", None)
st.session_state["_active_learning_page"] = "level5"

st.title(t("level5_title"))
st.write(content.get("goal", ""))

presentation_tab, simulation_tab, resources_tab, quiz_tab = st.tabs(
    [t("tab_presentation"), t("tab_simulation"), t("tab_resources"), t("tab_quiz")]
)

with presentation_tab:
    render_lesson_cards(load_lesson_markdown("level5", lang), "level5")
    render_terms(content)
    st.success(content.get("key_takeaway", ""))

with simulation_tab:
    st.subheader(t("two_qubit_lab_title"))
    st.write(content.get("simulation_intro", ""))

    col1, col2 = st.columns(2)
    with col1:
        first_label = st.selectbox(t("first_qubit_prob"), probability_select_options(), index=0)
    with col2:
        second_label = st.selectbox(t("second_qubit_prob"), probability_select_options(), index=0)

    current_controls = (first_label, second_label)
    previous_controls = st.session_state.get("level5_controls")
    if previous_controls is not None and previous_controls != current_controls:
        clear_level5_results()
    st.session_state["level5_controls"] = current_controls

    run_col, reset_col = st.columns([1, 1])
    if run_col.button(t("run_sim"), type="primary", width="stretch", key="level5_probability_run"):
        p_first = probability_from_label(first_label)
        p_second = probability_from_label(second_label)
        st.session_state["level5_distribution"] = simulator.independent_two_qubit_distribution(
            p_first,
            p_second,
        )
    if reset_col.button(t("reset_state"), width="stretch", key="level5_probability_reset"):
        clear_level5_results()

    dist = st.session_state.get("level5_distribution")
    if dist is None:
        labels = list(basis_labels(2))
        probabilities = [0.0, 0.0, 0.0, 0.0]
    else:
        labels = dist.labels()
        probabilities = dist.probabilities()

    render_markdown_table(
        [
            {"state": label, "probability": two_qubit_probability_text(value)}
            for label, value in zip(labels, probabilities)
        ]
    )

    chart_col, _ = st.columns([1, 1])
    with chart_col:
        fig = compact_count_bar(
            labels,
            [round(value * 100) for value in probabilities],
            "Measurement probability",
            ylabel="probability (%)",
        )
        render_fig(fig, width="stretch")

    message_key = "simulation_waiting" if dist is None else "simulation_hint"
    st.info(content.get(message_key, ""))

    st.divider()
    st.subheader(content.get("gate_lab_title", "Two-qubit gate lab"))
    st.write(content.get("gate_lab_intro", ""))

    gate_diagram = BASE_DIR / content.get("two_qubit_gate_diagram", "")
    if gate_diagram.is_file():
        gate_image_col, _ = st.columns([4, 2])
        with gate_image_col:
            st.image(str(gate_diagram), width="stretch")

    gate_controls, _ = st.columns([4, 2])
    with gate_controls:
        input_col, gate_col = st.columns(2)
        with input_col:
            gate_input = st.selectbox(
                content.get("gate_input_label", "Input basis state"),
                options=list(basis_labels(2)),
                format_func=lambda bits: f"|{bits}⟩",
                key="level5_gate_input",
            )
        with gate_col:
            selected_gate = st.selectbox(
                content.get("gate_label", "Gate"),
                options=["CNOT", "CZ", "SWAP"],
                key="level5_gate_choice",
            )

    gate_signature = (gate_input, selected_gate)
    if st.session_state.get("level5_gate_signature") not in (None, gate_signature):
        st.session_state.pop("level5_gate_result", None)
    st.session_state["level5_gate_signature"] = gate_signature

    gate_run_col, gate_reset_col = st.columns(2)
    if gate_run_col.button(
        t("run_sim"),
        type="primary",
        width="stretch",
        key="level5_gate_run",
    ):
        st.session_state["level5_gate_result"] = simulator.apply_two_qubit_basis_gate(
            gate_input,
            selected_gate,
        )
    if gate_reset_col.button(
        t("reset_state"),
        width="stretch",
        key="level5_gate_reset",
    ):
        st.session_state.pop("level5_gate_result", None)

    gate_result = st.session_state.get("level5_gate_result")
    if gate_result is None:
        st.info(content.get("gate_waiting", ""))
    else:
        output_sign = "-" if gate_result.phase < 0 else ""
        render_markdown_table(
            [
                {
                    content.get("gate_input_column", "Input"): f"|{gate_result.input_bits}⟩",
                    content.get("gate_column", "Gate"): gate_result.gate,
                    content.get("gate_output_column", "Output"): (
                        f"{output_sign}|{gate_result.output_bits}⟩"
                    ),
                }
            ]
        )
        st.info(content.get("gate_result_explanations", {}).get(gate_result.gate, ""))

with resources_tab:
    st.subheader(t("tab_resources"))
    for item in load_resources("level5", lang):
        render_resource_item(item)

with quiz_tab:
    st.subheader(t("tab_quiz"))
    render_quiz_items(content.get("quiz", []), "level5")

render_level_navigation(5)
