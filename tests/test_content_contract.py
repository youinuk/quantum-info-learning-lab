import re
from pathlib import Path

from core.content import load_level_content
from core.i18n import TRANSLATIONS
from core.math_display import (
    inline_kets_to_latex,
    normalize_plain_notation,
    qubit_amplitudes_latex,
    qubit_state_latex,
    relative_phase_qubit_state_latex,
)
from core.navigation import LEVEL_PAGES


ROOT = Path(__file__).resolve().parents[1]
LEVELS = tuple(f"level{number}" for number in range(14))
HONORIFIC_PATTERN = re.compile(r"(습니다|입니다|합니다|하세요|십시오)")


def test_every_level_has_terms_and_core_learning_content() -> None:
    for lang in ("ko", "en"):
        for level in LEVELS:
            content = load_level_content(level, lang)

            assert content["goal"].strip()
            assert content["key_takeaway"].strip()
            assert len(content["terms"]) >= 4
            assert len(content["quiz"]) >= 6

            for term in content["terms"]:
                assert len(term) == 2
                assert all(str(value).strip() for value in term.values())


def test_level5_introduces_basis_state_and_basis_state_term() -> None:
    expected_terms = {
        "ko": {"기저 상태", "기저 상태 항"},
        "en": {"basis state", "basis-state term"},
    }

    for lang in ("ko", "en"):
        content = load_level_content("level5", lang)
        lesson = (
            ROOT / "content" / "lessons" / lang / "level5.md"
        ).read_text(encoding="utf-8")
        term_names = {next(iter(term.values())) for term in content["terms"]}

        assert expected_terms[lang] <= term_names
        assert all(term in lesson for term in expected_terms[lang])

    korean_sources = (
        (ROOT / "content" / "levels.json").read_text(encoding="utf-8")
        + (ROOT / "content" / "lessons" / "ko" / "level5.md").read_text(encoding="utf-8")
    )
    assert "기준 상태" not in korean_sources


def test_level5_introduces_two_qubit_gates_before_entanglement() -> None:
    expected_terms = {"CNOT", "CZ", "SWAP"}

    for lang in ("ko", "en"):
        content = load_level_content("level5", lang)
        lesson = (ROOT / "content" / "lessons" / lang / "level5.md").read_text(
            encoding="utf-8"
        )
        term_names = {next(iter(term.values())) for term in content["terms"]}

        assert expected_terms <= term_names
        expected_diagram = "assets/images/two_qubit_gates.svg"
        assert expected_diagram in lesson
        assert content["two_qubit_gate_diagram"] == expected_diagram
        assert "CNOT(control, target)" in lesson
        assert r"\lvert10\rangle\rightarrow\lvert11\rangle" in lesson
        assert len(content["quiz"]) == 8

    assert (ROOT / "assets" / "images" / "two_qubit_gates.svg").is_file()


def test_translation_keys_match_between_languages() -> None:
    assert set(TRANSLATIONS["ko"]) == set(TRANSLATIONS["en"])


def test_qubit_state_latex_keeps_complex_amplitudes_visible() -> None:
    rendered = qubit_state_latex(0.5, 0.5 + 0.5j)

    assert r"\lvert0\rangle" in rendered
    assert r"\lvert1\rangle" in rendered
    assert "i" in rendered


def test_named_qubit_amplitudes_keep_zero_and_complex_values_visible() -> None:
    initial = qubit_amplitudes_latex(1, 0)
    phased = qubit_amplitudes_latex(2**-0.5, 1j * 2**-0.5)

    assert initial == r"\alpha=1,\qquad\beta=0"
    assert r"\beta=\frac{1}{\sqrt{2}}i" in phased


def test_lesson_inline_kets_keep_the_lvert_command() -> None:
    lessons = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (ROOT / "content" / "lessons").rglob("*.md")
    )

    assert "$lvert" not in lessons


def test_relative_phase_state_uses_polar_complex_notation() -> None:
    rendered = relative_phase_qubit_state_latex(0.8, 0.6, 90)

    assert r"e^{i\phi}" in rendered
    assert r"e^{i(90^\circ)}" in rendered
    assert r"0.600\lvert1\rangle" in rendered


def test_korean_learner_copy_uses_plain_declarative_style() -> None:
    sources = [
        (ROOT / "content" / "levels.json").read_text(encoding="utf-8"),
        (ROOT / "core" / "i18n.py").read_text(encoding="utf-8"),
    ]
    sources.extend(
        path.read_text(encoding="utf-8")
        for path in (ROOT / "content" / "lessons" / "ko").glob("*.md")
    )

    assert not HONORIFIC_PATTERN.search("\n".join(sources))


def test_lesson_cards_avoid_decorative_bold_and_canned_summaries() -> None:
    lessons = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (ROOT / "content" / "lessons").rglob("*.md")
    )

    assert "**" not in lessons
    for phrase in ("핵심은 간단", "In short:", "The main idea is"):
        assert phrase not in lessons


def test_learning_navigation_covers_every_level_page() -> None:
    assert len(LEVEL_PAGES) == 14

    for level, relative_path in enumerate(LEVEL_PAGES):
        page_path = ROOT / relative_path
        source = page_path.read_text(encoding="utf-8")

        assert page_path.is_file()
        assert "from core.navigation import render_level_navigation" in source
        assert f"render_level_navigation({level})" in source


def test_home_roadmap_uses_registered_level_pages() -> None:
    source = (ROOT / "pages" / "00_home.py").read_text(encoding="utf-8")

    assert "len(LEVEL_PAGES)" in source
    assert "range(6, 13)" not in source


def test_ket_notation_is_normalized_for_each_rendering_context() -> None:
    structured = normalize_plain_notation(
        {"state": "|psi> = |0>", "basis": ["|00>", "Bell |Phi+>"]}
    )

    assert structured == {
        "state": "|ψ⟩ = |0⟩",
        "basis": ["|00⟩", "Bell |Φ+⟩"],
    }
    assert inline_kets_to_latex("Start from `|0>` and measure `|1>`.") == (
        r"Start from $\lvert 0 \rangle$ and measure $\lvert 1 \rangle$."
    )
    assert normalize_plain_notation("Bell |Psi+> or |Psi->") == "Bell |Ψ+⟩ or |Ψ-⟩"


def test_loaded_structured_content_contains_no_ascii_ket_endings() -> None:
    for lang in ("ko", "en"):
        for level in LEVELS:
            assert ">" not in str(load_level_content(level, lang))


def test_lesson_math_is_not_written_as_inline_code() -> None:
    math_code_pattern = re.compile(
        r"`(?:"
        r"2\^n|N_1|Delta phi(?: = (?:0|pi))?|"
        r"X\^\{f\(x\)\}|f(?:\([01x]\))?(?:=[^`]*)?|x(?:=[01])?"
        r")`"
    )

    for language in ("ko", "en"):
        for lesson in (ROOT / "content" / "lessons" / language).glob("*.md"):
            source = lesson.read_text(encoding="utf-8")
            assert not math_code_pattern.search(source), lesson
            assert not re.search(r"(?<![\w\\])(?:1/2|1/4|3/4|1/8)", source), lesson


def test_circuit_card_images_exist() -> None:
    for lang in ("ko", "en"):
        content = load_level_content("level8", lang)
        for option in content["circuit_options"]:
            image = option.get("image")
            assert image
            assert (ROOT / image).is_file()


def test_phase_option_images_exist() -> None:
    for lang in ("ko", "en"):
        content = load_level_content("level10", lang)
        for option in content["phase_options"]:
            image = option.get("image")
            assert image
            assert (ROOT / image).is_file()


def test_level10_simulation_exposes_continuous_phase_comparison() -> None:
    for lang in ("ko", "en"):
        content = load_level_content("level10", lang)
        ui = content["simulation_ui"]

        assert "theory_column" in ui
        assert "observed_column" in ui
        assert "gap_column" in ui
        assert "advanced_purpose" in ui


def test_simulation_diagram_images_exist() -> None:
    for lang in ("ko", "en"):
        for level in LEVELS:
            content = load_level_content(level, lang)
            image = content.get("simulation_diagram")
            if image:
                assert (ROOT / image).is_file()
