import re
from pathlib import Path

from core.content import load_level_content
from core.i18n import TRANSLATIONS
from core.math_display import inline_kets_to_latex, normalize_plain_notation
from core.navigation import LEVEL_PAGES


ROOT = Path(__file__).resolve().parents[1]
LEVELS = tuple(f"level{number}" for number in range(13))
HONORIFIC_PATTERN = re.compile(r"(습니다|입니다|합니다|하세요|십시오)")


def test_every_level_has_terms_and_core_learning_content() -> None:
    for lang in ("ko", "en"):
        for level in LEVELS:
            content = load_level_content(level, lang)

            assert content["goal"].strip()
            assert content["key_takeaway"].strip()
            assert len(content["terms"]) >= 4
            assert len(content["quiz"]) == 6

            for term in content["terms"]:
                assert len(term) == 2
                assert all(str(value).strip() for value in term.values())


def test_translation_keys_match_between_languages() -> None:
    assert set(TRANSLATIONS["ko"]) == set(TRANSLATIONS["en"])


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


def test_learning_navigation_covers_every_level_page() -> None:
    assert len(LEVEL_PAGES) == 13

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


def test_loaded_structured_content_contains_no_ascii_ket_endings() -> None:
    for lang in ("ko", "en"):
        for level in LEVELS:
            assert ">" not in str(load_level_content(level, lang))


def test_circuit_card_images_exist() -> None:
    for lang in ("ko", "en"):
        content = load_level_content("level9", lang)
        for option in content["circuit_options"]:
            image = option.get("image")
            assert image
            assert (ROOT / image).is_file()


def test_phase_option_images_exist() -> None:
    for lang in ("ko", "en"):
        content = load_level_content("level11", lang)
        for option in content["phase_options"]:
            image = option.get("image")
            assert image
            assert (ROOT / image).is_file()


def test_simulation_diagram_images_exist() -> None:
    for lang in ("ko", "en"):
        for level in LEVELS:
            content = load_level_content(level, lang)
            image = content.get("simulation_diagram")
            if image:
                assert (ROOT / image).is_file()
