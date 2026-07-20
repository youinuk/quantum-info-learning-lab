from pathlib import Path
from xml.etree import ElementTree

from streamlit.testing.v1 import AppTest

from core.content import load_lesson_markdown, load_level_content, load_resources


ROOT = Path(__file__).resolve().parents[1]
PAGE_PATH = ROOT / "pages" / "15_level13_teleportation_dense_coding.py"


def build_level13_app(lang: str) -> AppTest:
    wrapper = f'''\
import runpy
import streamlit as st

st.page_link = lambda *args, **kwargs: None
runpy.run_path(r"{PAGE_PATH}", run_name="__main__")
'''
    app = AppTest.from_string(wrapper, default_timeout=20)
    app.session_state["lang"] = lang
    return app


def apply_correct_teleportation_correction(app: AppTest, lang: str) -> AppTest:
    bits_label = "Alice 측정 비트" if lang == "ko" else "Alice measurement bits"
    correction_label = "Bob이 적용할 보정" if lang == "ko" else "Correction Bob applies"
    apply_label = "선택한 보정 적용" if lang == "ko" else "Apply selected correction"
    correction_by_bits = {"00": "I", "01": "X", "10": "Z", "11": "ZX"}

    bits = next(metric.value for metric in app.metric if metric.label == bits_label)
    correction = next(
        control for control in app.segmented_control if control.label == correction_label
    )
    correction.set_value(correction_by_bits[bits]).run()
    next(button for button in app.button if button.label == apply_label).click().run()
    return app


def test_level13_content_covers_both_protocols_and_resource_accounting() -> None:
    for lang in ("ko", "en"):
        content = load_level_content("level13", lang)

        assert len(content["state_options"]) == 7
        assert {item["id"] for item in content["state_options"]} >= {"plus_i", "minus_i"}
        assert content["state_options"][-1]["id"] == "custom"
        assert content["message_options"] == ["00", "01", "10", "11"]
        assert len(content["terms"]) >= 7
        assert len(content["quiz"]) == 7
        assert "resource_note" in content["simulation_ui"]
        assert "relative_phase" in content["simulation_ui"]
        assert "derived_beta_magnitude" in content["simulation_ui"]
        assert "beta_magnitude" not in content["simulation_ui"]
        assert "convention_note" in content["simulation_ui"]
        assert "dense_explore_mode" in content["simulation_ui"]
        assert "dense_mission_mode" in content["simulation_ui"]
        assert "mission_target_bits" in content["simulation_ui"]
        assert len(load_resources("level13", lang)) >= 4


def test_level13_phase_note_supports_legacy_formatting_without_treating_latex_as_a_key() -> None:
    for lang in ("ko", "en"):
        note = load_level_content("level13", lang)["simulation_ui"][
            "phase_probability_note"
        ]

        rendered = note.format(phase=90)

        assert "{phase}" not in rendered
        assert r"e^{i\phi}" in rendered


def test_level13_diagrams_exist_and_are_shared_between_languages() -> None:
    korean = load_level_content("level13", "ko")
    english = load_level_content("level13", "en")

    for key in ("teleportation_diagram", "dense_coding_diagram"):
        assert korean[key] == english[key]
        diagram_path = ROOT / korean[key]
        assert diagram_path.is_file()
        ElementTree.parse(diagram_path)
        diagram = diagram_path.read_text(encoding="utf-8")
        assert diagram.count("|0⟩</text>") == 2
        assert "|00⟩" in diagram


def test_level13_lessons_explain_no_cloning_and_operator_order() -> None:
    for lang in ("ko", "en"):
        lesson = load_lesson_markdown("level13", lang)

        assert "no-cloning theorem" in lesson
        assert lesson.count(":::expander") == 3
        assert r"ZX(XZ\lvert\psi\rangle)=\lvert\psi\rangle" in lesson
        assert r"\lvert\Psi_0\rangle" in lesson
        assert r"\lvert\Psi_1\rangle" in lesson
        assert r"\lvert\Psi_2\rangle" in lesson
        assert r"U_{\text{decode}}=(H\otimes I)\operatorname{CNOT}" in lesson
        assert r"\operatorname{CNOT}\lvert\Psi^-\rangle" in lesson
        assert r"(\alpha\lvert1\rangle+\beta\lvert0\rangle)_B" in lesson
        assert r"(\alpha\lvert1\rangle-\beta\lvert0\rangle)_B" in lesson
        assert r"(\beta\lvert0\rangle+\alpha\lvert1\rangle)_B" not in lesson
        assert "X → Z" not in lesson


def test_level13_examples_state_what_bob_finally_receives() -> None:
    expected_results = {
        "ko": (
            "Bob은 Alice가 본래 보내려 한 $\\lvert+\\rangle$ 상태를 얻는다",
            "Bob의 측정값은 Alice가 보내려 한 두 비트와 정확히 같다",
        ),
        "en": (
            "Bob therefore obtains the $\\lvert+\\rangle$ state Alice originally intended to send",
            "Bob's measured pair therefore exactly matches the two bits Alice intended to send",
        ),
    }

    for lang, phrases in expected_results.items():
        lesson = load_lesson_markdown("level13", lang)
        assert all(phrase in lesson for phrase in phrases)


def test_level13_both_primary_experiments_run() -> None:
    app = build_level13_app("en")
    app.run()
    assert not app.exception

    next(button for button in app.button if button.label == "Run experiment").click().run()
    assert not app.exception
    apply_correct_teleportation_correction(app, "en")
    assert any(
        metric.label == "Input-state fidelity" and metric.value == "100%"
        for metric in app.metric
    )

    next(button for button in app.button if button.label == "Test gate").click().run()
    assert not app.exception
    assert any(
        metric.label == "Bits decoded by Bob" and metric.value == "00"
        for metric in app.metric
    )


def test_level13_custom_amplitudes_run_and_remain_normalized() -> None:
    app = build_level13_app("en")
    app.run()

    app.selectbox[0].set_value("custom").run()
    assert not app.exception
    assert any(slider.label == "|α| magnitude" for slider in app.slider)
    assert any(slider.label == "Relative phase φ of β (degrees)" for slider in app.slider)
    assert not any(slider.label == "|β| magnitude" for slider in app.slider)

    phase_slider = next(
        slider for slider in app.slider if slider.label == "Relative phase φ of β (degrees)"
    )
    phase_slider.set_value(90).run()
    assert any(r"\beta=0.600i" in element.value for element in app.latex)
    assert any(
        metric.label == "Probability of |1⟩, |β|²" and metric.value == "0.36"
        for metric in app.metric
    )

    teleport_run = next(button for button in app.button if button.label == "Run experiment")
    teleport_run.click().run()
    assert not app.exception
    apply_correct_teleportation_correction(app, "en")
    assert any(metric.label == "Input-state fidelity" and metric.value == "100%" for metric in app.metric)


def test_level13_superdense_exploration_builds_the_codebook() -> None:
    app = build_level13_app("en")
    app.run()

    assert not any(
        control.label == "Classical bits to send"
        for control in app.segmented_control
    )
    expected_bits = {"I": "00", "X": "01", "Z": "10", "ZX": "11"}
    for gate, decoded_bits in expected_bits.items():
        encoding_control = next(
            control
            for control in app.segmented_control
            if control.label == "Alice's encoding gate"
        )
        encoding_control.set_value(gate).run()
        next(button for button in app.button if button.label == "Test gate").click().run()

        assert not app.exception
        assert any(
            metric.label == "Bits decoded by Bob" and metric.value == decoded_bits
            for metric in app.metric
        )

    assert any(
        "You found all four gate mappings" in success.value
        for success in app.success
    )


def test_level13_superdense_mission_assigns_the_target_and_checks_the_gate() -> None:
    app = build_level13_app("en")
    app.run()

    mode_control = next(
        control
        for control in app.segmented_control
        if control.label == "Learning step"
    )
    mode_control.set_value("2. Transmission mission").run()

    target = next(
        metric.value
        for metric in app.metric
        if metric.label == "Bits to send this mission"
    )
    assert not any(
        control.label == "Classical bits to send"
        for control in app.segmented_control
    )

    correct_gate = {"00": "I", "01": "X", "10": "Z", "11": "ZX"}[target]
    wrong_gate = next(gate for gate in ("I", "X", "Z", "ZX") if gate != correct_gate)
    encoding_control = next(
        control
        for control in app.segmented_control
        if control.label == "Alice's encoding gate"
    )
    encoding_control.set_value(wrong_gate).run()
    next(button for button in app.button if button.label == "Send qubit").click().run()

    assert not app.exception
    assert app.error

    encoding_control = next(
        control
        for control in app.segmented_control
        if control.label == "Alice's encoding gate"
    )
    encoding_control.set_value(correct_gate).run()
    next(button for button in app.button if button.label == "Send qubit").click().run()

    assert not app.exception
    assert any(
        metric.label == "Bits decoded by Bob" and metric.value == target
        for metric in app.metric
    )
    assert any("recovered" in success.value for success in app.success)

    next(button for button in app.button if button.label == "New mission").click().run()
    new_target = next(
        metric.value
        for metric in app.metric
        if metric.label == "Bits to send this mission"
    )
    assert new_target != target


def test_level13_page_recovers_from_a_stale_simulator_signature() -> None:
    wrapper = f'''\
import runpy
import streamlit as st
import core.simulator as simulator

def stale_teleportation(input_state, seed=None):
    raise RuntimeError("stale simulator should have been reloaded")

simulator.simulate_quantum_teleportation = stale_teleportation
st.page_link = lambda *args, **kwargs: None
runpy.run_path(r"{PAGE_PATH}", run_name="__main__")
'''
    app = AppTest.from_string(wrapper, default_timeout=20)
    app.session_state["lang"] = "en"
    app.run()
    app.selectbox[0].set_value("custom").run()

    teleport_run = next(button for button in app.button if button.label == "Run experiment")
    teleport_run.click().run()

    assert not app.exception
    apply_correct_teleportation_correction(app, "en")
    assert any(metric.label == "Input-state fidelity" and metric.value == "100%" for metric in app.metric)


def test_level13_page_recovers_when_stale_module_lacks_correction_api() -> None:
    wrapper = f'''\
import runpy
import streamlit as st
import core.math_display as math_display
import core.simulator as simulator

del math_display.qubit_amplitudes_latex
del simulator.apply_teleportation_correction
st.page_link = lambda *args, **kwargs: None
runpy.run_path(r"{PAGE_PATH}", run_name="__main__")
'''
    app = AppTest.from_string(wrapper, default_timeout=20)
    app.session_state["lang"] = "en"
    app.run()

    next(button for button in app.button if button.label == "Run experiment").click().run()
    apply_correct_teleportation_correction(app, "en")

    assert not app.exception
    assert any(metric.label == "Input-state fidelity" and metric.value == "100%" for metric in app.metric)


def test_level13_english_page_contains_no_korean_simulation_labels() -> None:
    app = build_level13_app("en")
    app.run()

    assert not app.exception
    assert any(button.label == "Run experiment" for button in app.button)
    assert any(tab.label == "Quantum teleportation" for tab in app.tabs)


def test_level13_derivation_cards_render_without_errors() -> None:
    cases = {
        "ko": (
            "4. 구체적인 상태 하나를 보내 본다",
            "6. 초밀집 부호화는 고전 비트 두 개를 보낸다",
        ),
        "en": (
            "4. Teleport one concrete state",
            "6. Superdense coding sends two classical bits",
        ),
    }

    for lang, titles in cases.items():
        app = build_level13_app(lang)
        app.run()
        for title in titles:
            app.radio[0].set_value(title).run()
            assert not app.exception
            assert app.expander
