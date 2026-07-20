from __future__ import annotations

import streamlit as st

import core.math_display as math_display
import core.simulator as simulator
from core.charts import compact_count_bar, render_fig
from core.content import load_lesson_markdown, load_level_content, load_resources
from core.i18n import get_lang, t
from core.lesson_renderer import render_lesson_cards
from core.navigation import render_level_navigation
from core.quiz_renderer import render_quiz_items
from core.resource_renderer import render_resource_item
from core.runtime_modules import ensure_module_api
from core.terms_renderer import render_terms


simulator = ensure_module_api(
    simulator,
    minimum_version=0,
    required_attributes=("apply_single_qubit_gate", "basis_state"),
)
math_display = ensure_module_api(
    math_display,
    minimum_version=0,
    required_attributes=(
        "probability_plain",
        "qubit_amplitudes_latex",
        "qubit_state_latex",
    ),
)

lang = get_lang()
content = load_level_content("level3", lang)


def reset_level3_state() -> None:
    initial_state = st.session_state.get("level3_initial", "0")
    st.session_state["level3_state"] = simulator.basis_state(initial_state)
    st.session_state["level3_history"] = [f"|{initial_state}>"]


if st.session_state.get("_active_learning_page") != "level3":
    for key in ["level3_initial", "level3_state", "level3_history"]:
        st.session_state.pop(key, None)
st.session_state["_active_learning_page"] = "level3"

st.title(t("level3_title"))
st.write(content.get("goal", ""))

presentation_tab, simulation_tab, resources_tab, quiz_tab = st.tabs(
    [t("tab_presentation"), t("tab_simulation"), t("tab_resources"), t("tab_quiz")]
)

with presentation_tab:
    render_lesson_cards(load_lesson_markdown("level3", lang), "level3")
    render_terms(content)
    st.success(content.get("key_takeaway", ""))

with simulation_tab:
    st.subheader(t("gate_lab_title"))
    st.write(content.get("simulation_intro", ""))

    st.radio(
        t("initial_state"),
        ["0", "1"],
        horizontal=True,
        key="level3_initial",
        on_change=reset_level3_state,
    )
    if "level3_state" not in st.session_state:
        reset_level3_state()
    if st.button(t("reset_state")):
        reset_level3_state()

    state = st.session_state["level3_state"]

    gate1, gate2, gate3, gate4 = st.columns(4)
    if gate1.button("X", width="stretch"):
        state = simulator.apply_single_qubit_gate(state, "X")
        st.session_state["level3_state"] = state
        st.session_state["level3_history"].append("X")
    if gate2.button("H", width="stretch"):
        state = simulator.apply_single_qubit_gate(state, "H")
        st.session_state["level3_state"] = state
        st.session_state["level3_history"].append("H")
    if gate3.button("Z", width="stretch"):
        state = simulator.apply_single_qubit_gate(state, "Z")
        st.session_state["level3_state"] = state
        st.session_state["level3_history"].append("Z")
    if gate4.button("S", width="stretch"):
        state = simulator.apply_single_qubit_gate(state, "S")
        st.session_state["level3_state"] = state
        st.session_state["level3_history"].append("S")

    metric1, metric2 = st.columns(2)
    metric1.metric(t("expected_zero"), math_display.probability_plain(state.probability_zero))
    metric2.metric(t("expected_ratio"), math_display.probability_plain(state.probability_one))

    st.latex(math_display.qubit_state_latex(state.alpha, state.beta))
    st.latex(math_display.qubit_amplitudes_latex(state.alpha, state.beta))
    st.caption(f"{t('gate_sequence')}: {' -> '.join(st.session_state['level3_history'])}")

    chart_col, _ = st.columns([1, 1])
    with chart_col:
        fig = compact_count_bar(
            ["0", "1"],
            [round(state.probability_zero * 100), round(state.probability_one * 100)],
            "Measurement probability",
            ylabel="probability (%)",
        )
        render_fig(fig, width="stretch")

    if st.session_state["level3_history"][-1] == "S" and abs(state.beta) < 1e-10:
        hint = content.get("s_zero_beta_note", content.get("simulation_hint", ""))
    elif st.session_state["level3_history"][-1] == "S":
        hint = content.get("s_complex_beta_note", content.get("simulation_hint", ""))
    else:
        hint = content.get("simulation_hint", "")
    st.info(hint)

with resources_tab:
    st.subheader(t("tab_resources"))
    for item in load_resources("level3", lang):
        render_resource_item(item)

with quiz_tab:
    st.subheader(t("tab_quiz"))
    render_quiz_items(content.get("quiz", []), "level3")

render_level_navigation(3)
