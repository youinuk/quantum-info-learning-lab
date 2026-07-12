from __future__ import annotations

import pandas as pd
import streamlit as st

from core.charts import compact_count_bar, render_pyplot
from core.content import load_lesson_markdown, load_level_content, load_resources
from core.i18n import get_lang, t
from core.lesson_renderer import render_lesson_cards
from core.navigation import render_level_navigation
from core.quiz_renderer import render_quiz_items
from core.resource_renderer import render_resource_item
from core.simulator import run_deutsch_one_bit
from core.terms_renderer import render_terms

lang = get_lang()
content = load_level_content("level7", lang)
st.session_state["_active_learning_page"] = "level7"

st.title(t("level7_title"))
st.write(content.get("goal", ""))

presentation_tab, simulation_tab, resources_tab, quiz_tab = st.tabs(
    [t("tab_presentation"), t("tab_simulation"), t("tab_resources"), t("tab_quiz")]
)

with presentation_tab:
    render_lesson_cards(load_lesson_markdown("level7", lang), "level7")
    render_terms(content)
    st.success(content.get("key_takeaway", ""))

with simulation_tab:
    ui = content.get("simulation_ui", {})
    oracle_options = content.get("oracle_options", [])
    oracle_by_id = {item["id"]: item for item in oracle_options}

    st.subheader(t("algorithm_lab_title"))
    st.write(content.get("simulation_intro", ""))
    st.latex(
        r"\lvert0\rangle\lvert1\rangle"
        r"\;\xrightarrow{H\otimes H}\;"
        r"U_f"
        r"\;\xrightarrow{H\otimes I}\;"
        r"\text{measure the first qubit}"
    )
    st.caption(ui.get("circuit_caption", ""))

    selected_oracle = st.selectbox(
        t("hidden_rule"),
        options=list(oracle_by_id),
        format_func=lambda oracle_id: oracle_by_id[oracle_id]["label"],
    )

    run_col, reset_col = st.columns([1, 1])
    if run_col.button(t("run_sim"), type="primary", width="stretch"):
        st.session_state["level7_result"] = run_deutsch_one_bit(selected_oracle)
    if reset_col.button(t("reset_state"), width="stretch"):
        st.session_state.pop("level7_result", None)

    result = st.session_state.get("level7_result")
    if result is not None and result.oracle_name != selected_oracle:
        result = None

    if result is None:
        stage_rows = [
            {
                ui.get("stage_column", "Stage"): ui.get("waiting_stage", "-"),
                ui.get("p0_column", "P(first=0)"): "-",
                ui.get("p1_column", "P(first=1)"): "-",
                ui.get("observation_column", "Observation"): ui.get("waiting_note", ""),
            }
        ]
        final_probabilities = [0.0, 0.0]
        measurement = "-"
        classification = "-"
        query_count: int | str = "-"
    else:
        probability_steps = [
            (ui.get("stage_start", "Start"), (1.0, 0.0), ui.get("note_start", "")),
            (ui.get("stage_prepared", "After H x H"), result.prepared_probabilities, ui.get("note_prepared", "")),
            (ui.get("stage_oracle", "After oracle"), result.after_oracle_probabilities, ui.get("note_oracle", "")),
            (ui.get("stage_final", "After final H"), result.final_probabilities, ui.get("note_final", "")),
        ]
        stage_rows = [
            {
                ui.get("stage_column", "Stage"): stage,
                ui.get("p0_column", "P(first=0)"): f"{probabilities[0] * 100:.0f}%",
                ui.get("p1_column", "P(first=1)"): f"{probabilities[1] * 100:.0f}%",
                ui.get("observation_column", "Observation"): note,
            }
            for stage, probabilities, note in probability_steps
        ]
        final_probabilities = [round(value * 100, 6) for value in result.final_probabilities]
        measurement = result.measurement
        classification = content.get("classification_labels", {}).get(result.classification, result.classification)
        query_count = result.query_count

    st.markdown(f"### {ui.get('stage_title', 'Circuit stages')}")
    st.dataframe(pd.DataFrame(stage_rows), hide_index=True, width="stretch")

    metric1, metric2, metric3 = st.columns(3)
    metric1.metric(ui.get("query_count", "Oracle queries"), query_count)
    metric2.metric(t("quantum_measurement"), measurement)
    metric3.metric(t("classification"), classification)

    chart_col, _ = st.columns([1, 1])
    with chart_col:
        fig = compact_count_bar(
            ["first = 0", "first = 1"],
            final_probabilities,
            "Final measurement probability",
            ylabel="probability (%)",
        )
        render_pyplot(fig, width="stretch")

    if result is not None:
        st.markdown(f"### {ui.get('phase_title', 'Oracle phase markers')}")
        st.dataframe(
            pd.DataFrame(
                {
                    ui.get("input_column", "Input x"): [0, 1],
                    ui.get("phase_column", "Phase marker"): list(result.phase_markers),
                }
            ),
            hide_index=True,
            width="stretch",
        )
        phase_hint_key = "phase_same" if result.phase_markers[0] == result.phase_markers[1] else "phase_opposite"
        st.info(ui.get(phase_hint_key, ""))

        with st.expander(ui.get("reveal_title", "Reveal the hidden rule")):
            st.dataframe(
                pd.DataFrame(
                    {
                        ui.get("input_column", "Input x"): [0, 1],
                        "f(x)": [result.f0, result.f1],
                    }
                ),
                hide_index=True,
                width="stretch",
            )

    st.info(content.get("simulation_hint", ""))

with resources_tab:
    st.subheader(t("tab_resources"))
    for item in load_resources("level7", lang):
        render_resource_item(item)

with quiz_tab:
    st.subheader(t("tab_quiz"))
    render_quiz_items(content.get("quiz", []), "level7")

render_level_navigation(7)
