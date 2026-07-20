from __future__ import annotations

import streamlit as st

from core.charts import compact_count_bar, render_fig
from core.content import BASE_DIR, load_lesson_markdown, load_level_content, load_resources
from core.i18n import get_lang, t
from core.lesson_renderer import render_lesson_cards
from core.navigation import render_level_navigation
from core.quiz_renderer import render_quiz_items
from core.resource_renderer import render_resource_item
from core.safe_table import render_markdown_table
from core.simulator import run_deutsch_one_bit
from core.terms_renderer import render_terms

lang = get_lang()
content = load_level_content("level11", lang)


def clear_level11_results() -> None:
    st.session_state.pop("level11_result", None)


if st.session_state.get("_active_learning_page") != "level11":
    clear_level11_results()
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
    oracle_options = content.get("oracle_options", [])
    oracle_by_id = {item["id"]: item for item in oracle_options}

    st.subheader(t("algorithm_lab_title"))
    st.write(content.get("simulation_intro", ""))
    st.info(content.get("simulation_purpose", ""))

    st.markdown(f"### {ui.get('process_title', 'Process')}")
    for step_number, step in enumerate(content.get("simulation_steps", []), start=1):
        st.markdown(f"{step_number}. {step}")

    diagram_path = BASE_DIR / content.get("simulation_diagram", "")
    if diagram_path.is_file():
        st.image(str(diagram_path), caption=ui.get("circuit_caption", ""), width=560)

    st.markdown(f"### {ui.get('truth_table_title', 'Truth table')}")
    truth_rows = [
        {
            ui.get("rule_column", "Rule"): row.get("label", ""),
            "f(0)": row.get("f0", ""),
            "f(1)": row.get("f1", ""),
            ui.get("type_column", "Type"): content.get("classification_labels", {}).get(
                row.get("classification", ""), row.get("classification", "")
            ),
        }
        for row in content.get("truth_table", [])
    ]
    render_markdown_table(truth_rows)

    render_markdown_table(
        [
            {
                ui.get("method_column", "Method"): ui.get("classical_method", "Classical"),
                ui.get("query_column", "Oracle queries"): 2,
                ui.get("method_note_column", "How"): ui.get("classical_method_note", ""),
            },
            {
                ui.get("method_column", "Method"): ui.get("quantum_method", "Deutsch circuit"),
                ui.get("query_column", "Oracle queries"): 1,
                ui.get("method_note_column", "How"): ui.get("quantum_method_note", ""),
            },
        ]
    )

    selected_oracle = st.selectbox(
        t("hidden_rule"),
        options=list(oracle_by_id),
        format_func=lambda oracle_id: oracle_by_id[oracle_id]["label"],
    )

    run_col, reset_col = st.columns([1, 1])
    if run_col.button(t("run_sim"), type="primary", width="stretch"):
        st.session_state["level11_result"] = run_deutsch_one_bit(selected_oracle)
    if reset_col.button(t("reset_state"), width="stretch"):
        clear_level11_results()

    result = st.session_state.get("level11_result")
    if result is not None and result.oracle_name != selected_oracle:
        result = None

    if result is None:
        st.info(ui.get("waiting_note", ""))
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

        result_message_key = "result_constant" if result.classification == "constant" else "result_balanced"
        st.success(
            ui.get(result_message_key, "{measurement}: {classification}").format(
                measurement=measurement,
                classification=classification,
            )
        )

        metric1, metric2, metric3 = st.columns(3)
        metric1.metric(ui.get("query_count", "Oracle queries"), query_count)
        metric2.metric(t("quantum_measurement"), measurement)
        metric3.metric(t("classification"), classification)

        st.markdown(f"### {ui.get('phase_title', 'Oracle phase markers')}")
        render_markdown_table(
            [
                {
                    ui.get("input_column", "Input x"): input_value,
                    ui.get("phase_column", "Phase marker"): phase_marker,
                }
                for input_value, phase_marker in zip([0, 1], result.phase_markers)
            ]
        )
        phase_hint_key = "phase_same" if result.phase_markers[0] == result.phase_markers[1] else "phase_opposite"
        st.info(ui.get(phase_hint_key, ""))

        chart_col, _ = st.columns([1, 1])
        with chart_col:
            fig = compact_count_bar(
                ["first = 0", "first = 1"],
                final_probabilities,
                "Final measurement probability",
                ylabel="probability (%)",
            )
            render_fig(fig, width="stretch")

        with st.expander(ui.get("details_title", "Circuit stages")):
            render_markdown_table(stage_rows)

        with st.expander(ui.get("reveal_title", "Selected oracle truth table")):
            render_markdown_table(
                [
                    {ui.get("input_column", "Input x"): 0, "f(x)": result.f0},
                    {ui.get("input_column", "Input x"): 1, "f(x)": result.f1},
                ]
            )

        st.info(content.get("simulation_hint", ""))

with resources_tab:
    st.subheader(t("tab_resources"))
    for item in load_resources("level11", lang):
        render_resource_item(item)

with quiz_tab:
    st.subheader(t("tab_quiz"))
    render_quiz_items(content.get("quiz", []), "level11")

render_level_navigation(11)
