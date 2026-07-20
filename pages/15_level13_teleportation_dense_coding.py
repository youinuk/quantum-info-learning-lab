from __future__ import annotations

import cmath
import math

import streamlit as st

import core.math_display as math_display
import core.simulator as simulator
from core.content import BASE_DIR, load_lesson_markdown, load_level_content, load_resources
from core.i18n import get_lang, t
from core.lesson_renderer import render_lesson_cards
from core.navigation import render_level_navigation
from core.quiz_renderer import render_quiz_items
from core.resource_renderer import render_resource_item
from core.runtime_modules import ensure_module_api
from core.safe_table import render_markdown_table
from core.terms_renderer import render_terms


simulator = ensure_module_api(
    simulator,
    minimum_version=0,
    required_attributes=(
        "apply_teleportation_correction",
        "explore_superdense_encoding",
        "generate_superdense_mission",
        "simulate_quantum_teleportation",
        "simulate_superdense_coding",
    ),
    required_parameters={
        "simulate_quantum_teleportation": ("amplitudes",),
        "simulate_superdense_coding": ("encoding_gate",),
    },
)
math_display = ensure_module_api(
    math_display,
    minimum_version=0,
    required_attributes=(
        "qubit_amplitudes_latex",
        "qubit_state_latex",
        "relative_phase_qubit_state_latex",
    ),
)


def clear_teleportation_result() -> None:
    st.session_state.pop("level13_teleportation_result", None)
    st.session_state.pop("level13_correction_attempt", None)


def clear_dense_exploration_result() -> None:
    st.session_state.pop("level13_dense_explore_result", None)


def clear_dense_mission_result() -> None:
    st.session_state.pop("level13_dense_mission_result", None)


def start_new_dense_mission() -> None:
    mission_index = st.session_state.get("level13_dense_mission_index", 0) + 1
    previous_bits = st.session_state.get("level13_dense_mission_bits")
    st.session_state["level13_dense_mission_index"] = mission_index
    st.session_state["level13_dense_mission_bits"] = (
        simulator.generate_superdense_mission(
            seed=13000 + mission_index,
            previous_bits=previous_bits,
        )
    )
    clear_dense_mission_result()


def render_protocol_diagram(image_path, caption: str) -> None:
    if not image_path.is_file():
        return
    image_column, _ = st.columns([4, 1])
    with image_column:
        st.image(str(image_path), caption=caption, width="stretch")


lang = get_lang()
content = load_level_content("level13", lang)
ui = content.get("simulation_ui", {})

if st.session_state.get("_active_learning_page") != "level13":
    clear_teleportation_result()
    clear_dense_exploration_result()
    clear_dense_mission_result()
    st.session_state["level13_teleportation_run_index"] = 0
    st.session_state.pop("level13_teleport_history", None)
    st.session_state.pop("level13_dense_codebook", None)
    st.session_state.pop("level13_dense_mission_bits", None)
    st.session_state.pop("level13_dense_mission_history", None)
    st.session_state["level13_dense_mission_index"] = 0
st.session_state["_active_learning_page"] = "level13"

st.title(t("level13_title"))
st.write(content.get("goal", ""))

presentation_tab, simulation_tab, resources_tab, quiz_tab = st.tabs(
    [t("tab_presentation"), t("tab_simulation"), t("tab_resources"), t("tab_quiz")]
)

with presentation_tab:
    render_lesson_cards(load_lesson_markdown("level13", lang), "level13")
    render_terms(content)
    st.success(content.get("key_takeaway", ""))

with simulation_tab:
    st.subheader(t("level13_lab_title"))
    st.write(content.get("simulation_intro", ""))
    st.info(content.get("simulation_purpose", ""))

    teleport_tab, dense_tab = st.tabs(
        [ui.get("teleport_tab", "Teleportation"), ui.get("dense_tab", "Superdense coding")]
    )

    with teleport_tab:
        st.markdown(f"### {ui.get('teleport_title', 'Teleport a quantum state')}")
        st.write(ui.get("teleport_intro", ""))
        st.caption(ui.get("convention_note", ""))

        teleportation_diagram = BASE_DIR / content.get("teleportation_diagram", "")
        render_protocol_diagram(
            teleportation_diagram,
            ui.get("teleport_diagram_caption", ""),
        )

        state_options = content.get("state_options", [])
        state_by_id = {item["id"]: item["label"] for item in state_options}
        state_control_col, _ = st.columns([3, 2])
        with state_control_col:
            selected_state = st.selectbox(
                ui.get("input_state", "Input state"),
                options=list(state_by_id),
                format_func=lambda state_id: state_by_id[state_id],
                key="level13_state_input",
            )

        custom_amplitudes: tuple[complex, complex] | None = None
        input_signature: tuple[object, ...] = (selected_state,)
        if selected_state == "custom":
            st.caption(ui.get("custom_state_intro", ""))
            compact_controls, _ = st.columns([4, 2])
            with compact_controls:
                alpha_col, phase_col = st.columns(2)
                with alpha_col:
                    alpha_magnitude = st.slider(
                        ui.get("alpha_magnitude", "|alpha|"),
                        min_value=0.0,
                        max_value=1.0,
                        value=0.8,
                        step=0.05,
                        key="level13_custom_alpha",
                    )
                beta_magnitude = math.sqrt(max(0.0, 1.0 - alpha_magnitude**2))
                with phase_col:
                    phase_degrees = st.slider(
                        ui.get("relative_phase", "Relative phase"),
                        min_value=-180,
                        max_value=180,
                        value=0,
                        step=15,
                        key="level13_custom_phase",
                        disabled=beta_magnitude < 1e-12,
                    )
            st.caption(
                ui.get("derived_beta_magnitude", "Derived |beta|").format(
                    beta_magnitude=beta_magnitude
                )
            )
            alpha = complex(alpha_magnitude)
            beta = beta_magnitude * cmath.exp(1j * math.radians(phase_degrees))
            custom_amplitudes = (alpha, beta)
            st.markdown(f"#### {ui.get('normalized_state', 'Normalized input state')}")
            st.latex(
                math_display.relative_phase_qubit_state_latex(
                    alpha_magnitude,
                    beta_magnitude,
                    phase_degrees,
                )
            )
            st.latex(math_display.qubit_amplitudes_latex(alpha, beta))
            probability_col, _ = st.columns([4, 2])
            with probability_col:
                probability_zero_col, probability_one_col = st.columns(2)
                probability_zero_col.metric(
                    ui.get("probability_zero", "P(0)"),
                    f"{abs(alpha) ** 2:.2f}",
                )
                probability_one_col.metric(
                    ui.get("probability_one", "P(1)"),
                    f"{abs(beta) ** 2:.2f}",
                )
            phase_note = ui.get("phase_probability_note", "")
            phase_note = phase_note.replace("{phase}", str(phase_degrees))
            phase_note = phase_note.replace(
                "{beta_magnitude}",
                f"{beta_magnitude:.3f}",
            )
            st.caption(phase_note)
            st.caption(ui.get("normalization_note", ""))
            input_signature = (
                selected_state,
                alpha_magnitude,
                phase_degrees,
            )

        previous_signature = st.session_state.get("level13_previous_input_signature")
        if previous_signature is not None and previous_signature != input_signature:
            clear_teleportation_result()
        st.session_state["level13_previous_input_signature"] = input_signature

        run_col, reset_col = st.columns(2)
        if run_col.button(
            t("run_sim"),
            type="primary",
            width="stretch",
            key="level13_teleport_run",
        ):
            run_index = st.session_state.get("level13_teleportation_run_index", 0) + 1
            st.session_state["level13_teleportation_run_index"] = run_index
            st.session_state["level13_teleportation_result"] = simulator.simulate_quantum_teleportation(
                selected_state,
                seed=13000 + run_index,
                amplitudes=custom_amplitudes,
            )
            st.session_state.pop("level13_correction_attempt", None)
            result = st.session_state["level13_teleportation_result"]
            history = st.session_state.setdefault(
                "level13_teleport_history",
                {"00": 0, "01": 0, "10": 0, "11": 0},
            )
            history[result.alice_bits] += 1
        if reset_col.button(t("reset_state"), width="stretch", key="level13_teleport_reset"):
            clear_teleportation_result()
            st.session_state["level13_teleportation_run_index"] = 0
            st.session_state.pop("level13_teleport_history", None)

        teleportation_result = st.session_state.get("level13_teleportation_result")
        if teleportation_result is not None and teleportation_result.input_state != selected_state:
            teleportation_result = None

        if teleportation_result is None:
            st.info(content.get("simulation_waiting", ""))
        else:
            st.info(ui.get("teleport_measurement_result", ""))
            bits_col, run_count_col, _ = st.columns([1, 1, 1])
            bits_col.metric(ui.get("alice_measurement", "Alice bits"), teleportation_result.alice_bits)
            run_count_col.metric(
                ui.get("measurement_number", "Measurement number"),
                st.session_state.get("level13_teleportation_run_index", 1),
            )

            input_col, before_col = st.columns(2)
            with input_col:
                st.markdown(f"#### {ui.get('input_state', 'Input state')}")
                st.latex(math_display.qubit_state_latex(*teleportation_result.input_amplitudes))
            with before_col:
                st.markdown(f"#### {ui.get('bob_before', 'Bob before correction')}")
                st.latex(math_display.qubit_state_latex(*teleportation_result.bob_state_before))

            selected_correction = st.segmented_control(
                ui.get("choose_correction", "Choose Bob's correction"),
                options=["I", "X", "Z", "ZX"],
                default=None,
                key="level13_selected_correction",
            )
            correction_signature = (
                teleportation_result.alice_bits,
                st.session_state.get("level13_teleportation_run_index", 0),
                selected_correction,
            )
            if st.session_state.get("level13_previous_correction_signature") != correction_signature:
                st.session_state.pop("level13_correction_attempt", None)
            st.session_state["level13_previous_correction_signature"] = correction_signature

            if st.button(
                ui.get("apply_correction", "Apply correction"),
                type="primary",
                key="level13_apply_correction",
            ):
                if selected_correction is None:
                    st.warning(ui.get("choose_correction_first", ""))
                else:
                    st.session_state["level13_correction_attempt"] = (
                        simulator.apply_teleportation_correction(
                            teleportation_result,
                            selected_correction,
                        )
                    )

            correction_attempt = st.session_state.get("level13_correction_attempt")
            if correction_attempt is not None:
                after_col, fidelity_col = st.columns(2)
                with after_col:
                    st.markdown(f"#### {ui.get('bob_after', 'Bob after correction')}")
                    st.latex(math_display.qubit_state_latex(*correction_attempt.output_amplitudes))
                fidelity_col.metric(
                    ui.get("fidelity", "Fidelity"),
                    f"{correction_attempt.fidelity:.0%}",
                )
                if correction_attempt.matches_protocol_correction:
                    st.success(ui.get("teleport_success", ""))
                else:
                    st.error(
                        ui.get("teleport_wrong_correction", "").format(
                            expected=teleportation_result.correction_label,
                        )
                    )

            history = st.session_state.get("level13_teleport_history", {})
            if history:
                st.markdown(f"#### {ui.get('measurement_history_title', 'Alice outcome history')}")
                render_markdown_table(
                    [
                        {
                            ui.get("bit_column", "Alice bits"): bits,
                            ui.get("count_column", "Count"): history.get(bits, 0),
                            ui.get("correction_column", "Correction"): correction,
                        }
                        for bits, correction in (("00", "I"), ("01", "X"), ("10", "Z"), ("11", "ZX"))
                    ]
                )
                st.caption(ui.get("measurement_history_note", ""))

        with st.expander(ui.get("correction_guide_title", "Correction guide")):
            render_markdown_table(
                [
                    {
                        ui.get("bit_column", "Alice bits"): "00",
                        ui.get("correction_column", "Correction"): "I",
                        ui.get("meaning_column", "Meaning"): ui.get("correction_none", ""),
                    },
                    {
                        ui.get("bit_column", "Alice bits"): "01",
                        ui.get("correction_column", "Correction"): "X",
                        ui.get("meaning_column", "Meaning"): ui.get("correction_x", ""),
                    },
                    {
                        ui.get("bit_column", "Alice bits"): "10",
                        ui.get("correction_column", "Correction"): "Z",
                        ui.get("meaning_column", "Meaning"): ui.get("correction_z", ""),
                    },
                    {
                        ui.get("bit_column", "Alice bits"): "11",
                        ui.get("correction_column", "Correction"): "ZX",
                        ui.get("meaning_column", "Meaning"): ui.get("correction_xz", ""),
                    },
                ]
            )

    with dense_tab:
        st.markdown(f"### {ui.get('dense_title', 'Send two classical bits')}")
        st.write(ui.get("dense_intro", ""))

        dense_diagram = BASE_DIR / content.get("dense_coding_diagram", "")
        render_protocol_diagram(
            dense_diagram,
            ui.get("dense_diagram_caption", ""),
        )

        explore_mode = ui.get("dense_explore_mode", "1. Explore gate effects")
        mission_mode = ui.get("dense_mission_mode", "2. Transmission mission")
        selected_dense_mode = st.segmented_control(
            ui.get("dense_mode_label", "Learning step"),
            options=[explore_mode, mission_mode],
            default=explore_mode,
            key="level13_dense_mode",
        )

        if selected_dense_mode == explore_mode:
            st.markdown(f"#### {ui.get('dense_explore_title', 'Explore gate effects')}")
            st.write(ui.get("dense_explore_intro", ""))

            selected_encoding = st.segmented_control(
                ui.get("choose_encoding", "Choose Alice's encoding gate"),
                options=["I", "X", "Z", "ZX"],
                default="I",
                key="level13_explore_gate",
            )
            previous_gate = st.session_state.get("level13_previous_explore_gate")
            if previous_gate is not None and previous_gate != selected_encoding:
                clear_dense_exploration_result()
            st.session_state["level13_previous_explore_gate"] = selected_encoding

            run_col, reset_col = st.columns(2)
            if run_col.button(
                ui.get("test_encoding", "Test gate"),
                type="primary",
                width="stretch",
                key="level13_explore_run",
            ):
                result = simulator.explore_superdense_encoding(selected_encoding)
                st.session_state["level13_dense_explore_result"] = result
                codebook = st.session_state.setdefault("level13_dense_codebook", {})
                codebook[result.encoding_gate] = {
                    ui.get("encoding_gate", "Encoding"): result.encoding_gate,
                    ui.get("bell_state", "Bell state"): content.get(
                        "bell_state_labels", {}
                    ).get(result.bell_state, result.bell_state),
                    ui.get("decoded_bits", "Decoded bits"): result.decoded_bits,
                }
            if reset_col.button(
                t("reset_state"),
                width="stretch",
                key="level13_explore_reset",
            ):
                clear_dense_exploration_result()
                st.session_state.pop("level13_dense_codebook", None)

            explore_result = st.session_state.get("level13_dense_explore_result")
            if explore_result is None:
                st.info(ui.get("explore_waiting", ""))
            else:
                encoding_col, bell_col, decoded_col = st.columns(3)
                encoding_col.metric(
                    ui.get("encoding_gate", "Encoding"),
                    explore_result.encoding_gate,
                )
                bell_col.metric(
                    ui.get("bell_state", "Bell state"),
                    content.get("bell_state_labels", {}).get(
                        explore_result.bell_state,
                        explore_result.bell_state,
                    ),
                )
                decoded_col.metric(
                    ui.get("decoded_bits", "Decoded bits"),
                    explore_result.decoded_bits,
                )

            codebook = st.session_state.get("level13_dense_codebook", {})
            progress_text = ui.get(
                "explore_progress", "Encoding table progress: {completed}/{total}"
            ).format(completed=len(codebook), total=4)
            st.progress(len(codebook) / 4)
            st.caption(progress_text)
            if codebook:
                st.markdown(f"#### {ui.get('codebook_title', 'Discovered encoding table')}")
                render_markdown_table(
                    [codebook[gate] for gate in ("I", "X", "Z", "ZX") if gate in codebook]
                )
            if len(codebook) == 4:
                st.success(ui.get("explore_complete", ""))

        else:
            st.markdown(f"#### {ui.get('dense_mission_title', 'Transmission mission')}")
            st.write(ui.get("dense_mission_intro", ""))

            if "level13_dense_mission_bits" not in st.session_state:
                start_new_dense_mission()
            mission_bits = st.session_state["level13_dense_mission_bits"]
            target_col, _ = st.columns([1, 3])
            target_col.metric(
                ui.get("mission_target_bits", "Bits to send this mission"),
                mission_bits,
            )

            mission_gate = st.segmented_control(
                ui.get("choose_encoding", "Choose Alice's encoding gate"),
                options=["I", "X", "Z", "ZX"],
                default="I",
                key="level13_mission_gate",
            )
            previous_gate = st.session_state.get("level13_previous_mission_gate")
            if previous_gate is not None and previous_gate != mission_gate:
                clear_dense_mission_result()
            st.session_state["level13_previous_mission_gate"] = mission_gate

            send_col, new_col = st.columns(2)
            if send_col.button(
                ui.get("send_qubit", "Send qubit"),
                type="primary",
                width="stretch",
                key="level13_mission_send",
            ):
                result = simulator.simulate_superdense_coding(
                    mission_bits,
                    encoding_gate=mission_gate,
                )
                st.session_state["level13_dense_mission_result"] = result
                history = st.session_state.setdefault(
                    "level13_dense_mission_history", []
                )
                history.append(
                    {
                        ui.get("target_bits_column", "Target bits"): result.message_bits,
                        ui.get("encoding_gate", "Encoding"): result.encoding_gate,
                        ui.get("decoded_bits", "Decoded bits"): result.decoded_bits,
                        ui.get("result_column", "Result"): (
                            ui.get("success_word", "Success")
                            if result.success
                            else ui.get("retry_word", "Mismatch")
                        ),
                    }
                )
            if new_col.button(
                ui.get("new_mission", "New mission"),
                width="stretch",
                key="level13_new_mission",
            ):
                start_new_dense_mission()
                st.rerun()

            mission_result = st.session_state.get("level13_dense_mission_result")
            if mission_result is None:
                st.info(ui.get("mission_waiting", ""))
            else:
                if mission_result.success:
                    st.success(ui.get("dense_success", ""))
                else:
                    st.error(
                        ui.get("dense_mismatch", "").format(
                            decoded=mission_result.decoded_bits,
                        )
                    )
                encoding_col, bell_col, sent_col, decoded_col = st.columns(4)
                encoding_col.metric(
                    ui.get("encoding_gate", "Encoding"),
                    mission_result.encoding_gate,
                )
                bell_col.metric(
                    ui.get("bell_state", "Bell state"),
                    content.get("bell_state_labels", {}).get(
                        mission_result.bell_state,
                        mission_result.bell_state,
                    ),
                )
                sent_col.metric(
                    ui.get("qubits_sent", "Qubits sent"),
                    ui.get("one_qubit", "1"),
                )
                decoded_col.metric(
                    ui.get("decoded_bits", "Decoded bits"),
                    mission_result.decoded_bits,
                )

            mission_history = st.session_state.get(
                "level13_dense_mission_history", []
            )
            if mission_history:
                st.markdown(
                    f"#### {ui.get('mission_history_title', 'Mission log')}"
                )
                render_markdown_table(mission_history)
                st.caption(ui.get("mission_history_note", ""))

    st.markdown(f"### {ui.get('resource_title', 'Resource comparison')}")
    render_markdown_table(
        [
            {
                ui.get("protocol_column", "Protocol"): ui.get("teleport_protocol", "Teleportation"),
                ui.get("input_column", "Input"): ui.get("unknown_state", "One unknown state"),
                ui.get("shared_column", "Shared"): ui.get("one_bell_pair", "One Bell pair"),
                ui.get("sent_column", "Sent"): ui.get("two_classical_bits", "Two classical bits"),
                ui.get("output_column", "Output"): ui.get("one_qubit_state", "One qubit state"),
            },
            {
                ui.get("protocol_column", "Protocol"): ui.get("dense_protocol", "Superdense coding"),
                ui.get("input_column", "Input"): ui.get("two_classical_bits", "Two classical bits"),
                ui.get("shared_column", "Shared"): ui.get("one_bell_pair", "One Bell pair"),
                ui.get("sent_column", "Sent"): ui.get("one_qubit_sent", "One qubit"),
                ui.get("output_column", "Output"): ui.get("two_classical_bits", "Two classical bits"),
            },
        ]
    )
    st.caption(ui.get("resource_note", ""))

with resources_tab:
    st.subheader(t("tab_resources"))
    for item in load_resources("level13", lang):
        render_resource_item(item)

with quiz_tab:
    st.subheader(t("tab_quiz"))
    render_quiz_items(content.get("quiz", []), "level13")

render_level_navigation(13)
