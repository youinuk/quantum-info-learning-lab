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

if not hasattr(simulator, "simulate_entanglement_limit"):
    simulator = importlib.reload(simulator)

lang = get_lang()
content = load_level_content("level12", lang)


def clear_level12_results() -> None:
    st.session_state.pop("level12_result", None)


if st.session_state.get("_active_learning_page") != "level12":
    clear_level12_results()
    st.session_state.pop("level12_controls", None)
    st.session_state["level12_run_index"] = 0
st.session_state["_active_learning_page"] = "level12"

st.title(t("level12_title"))
st.write(content.get("goal", ""))

presentation_tab, simulation_tab, resources_tab, quiz_tab = st.tabs(
    [t("tab_presentation"), t("tab_simulation"), t("tab_resources"), t("tab_quiz")]
)

with presentation_tab:
    render_lesson_cards(load_lesson_markdown("level12", lang), "level12")
    render_terms(content)
    st.success(content.get("key_takeaway", ""))

with simulation_tab:
    ui = content.get("simulation_ui", {})
    st.subheader(t("entanglement_limit_lab_title"))
    st.write(content.get("simulation_intro", ""))
    for focus in content.get("simulation_focus", []):
        st.markdown(f"- {focus}")

    diagram = content.get("simulation_diagram")
    if diagram:
        diagram_path = BASE_DIR / diagram
        if diagram_path.is_file():
            st.image(str(diagram_path), caption=ui.get("diagram_caption", ""), width="stretch")

    st.info(ui.get("message_attempt", ""))

    col1, col2, col3 = st.columns(3)
    with col1:
        alice_basis = st.radio(ui.get("alice_basis", "Alice basis"), ["Z", "X"], horizontal=True)
    with col2:
        bob_basis = st.radio(ui.get("bob_basis", "Bob basis"), ["Z", "X"], horizontal=True)
    with col3:
        shots = st.slider(t("shots"), 10, 5000, 1000, 10)

    current_controls = (alice_basis, bob_basis, int(shots))
    previous_controls = st.session_state.get("level12_controls")
    if previous_controls is not None and previous_controls != current_controls:
        clear_level12_results()
    st.session_state["level12_controls"] = current_controls

    run_col, reset_col = st.columns([1, 1])
    if run_col.button(t("run_sim"), type="primary", width="stretch"):
        run_index = st.session_state.get("level12_run_index", 0) + 1
        st.session_state["level12_run_index"] = run_index
        st.session_state["level12_result"] = simulator.simulate_entanglement_limit(
            alice_basis,
            bob_basis,
            int(shots),
            13000 + run_index,
        )
    if reset_col.button(t("reset_state"), width="stretch"):
        clear_level12_results()
        st.session_state["level12_run_index"] = 0

    result = st.session_state.get("level12_result")
    if result is not None and (result.alice_basis, result.bob_basis, result.shots) != current_controls:
        result = None

    if result is None:
        pair_rows = [
            {ui.get("pair_column", "Pair outcome"): label, ui.get("count_column", "Count"): 0}
            for label in ["00", "01", "10", "11"]
        ]
        bob_counts = [0, 0]
        bob_zero_ratio: float | str = "-"
        same_ratio: float | str = "-"
        st.info(content.get("simulation_waiting", ""))
    else:
        pair_rows = [
            {ui.get("pair_column", "Pair outcome"): label, ui.get("count_column", "Count"): count}
            for label, count in zip(result.labels(), result.pair_counts())
        ]
        bob_counts = [result.bob_count_zero, result.bob_count_one]
        bob_zero_ratio = f"{result.bob_zero_ratio:.3f}"
        same_ratio = f"{result.same_ratio:.3f}"
        note_key = "same_basis_note" if alice_basis == bob_basis else "different_basis_note"
        st.info(ui.get(note_key, ""))

    metric1, metric2 = st.columns(2)
    metric1.metric(ui.get("bob_zero_ratio", "Bob 0 ratio"), bob_zero_ratio)
    metric2.metric(ui.get("same_ratio", "Same-result ratio"), same_ratio)

    st.subheader(ui.get("message_attempt_title", "Message attempt"))
    message_value = "0" if alice_basis == "Z" else "1"
    bob_panel, compare_panel = st.columns(2)
    with bob_panel:
        st.markdown(f"**{ui.get('bob_panel_title', 'What Bob can see alone')}**")
        if result is None:
            st.info(ui.get("panel_waiting", ""))
        else:
            st.warning(
                ui.get("bob_panel_result", "").format(
                    bob_zero_ratio=bob_zero_ratio,
                    alice_basis=alice_basis,
                    message_value=message_value,
                )
            )
    with compare_panel:
        st.markdown(f"**{ui.get('compare_panel_title', 'What requires later comparison')}**")
        if result is None:
            st.info(ui.get("panel_waiting", ""))
        else:
            compare_key = "compare_panel_same" if alice_basis == bob_basis else "compare_panel_different"
            st.info(ui.get(compare_key, "").format(same_ratio=same_ratio))

    st.dataframe(pd.DataFrame(pair_rows), hide_index=True, width="stretch")

    chart_col, _ = st.columns([1, 1])
    with chart_col:
        fig = compact_count_bar(
            ["Bob 0", "Bob 1"],
            bob_counts,
            "Bob local results",
        )
        st.pyplot(fig, width="stretch")

    st.caption(content.get("simulation_caption", ""))

with resources_tab:
    st.subheader(t("tab_resources"))
    for item in load_resources("level12", lang):
        render_resource_item(item)

with quiz_tab:
    st.subheader(t("tab_quiz"))
    render_quiz_items(content.get("quiz", []), "level12")

render_level_navigation(12)
