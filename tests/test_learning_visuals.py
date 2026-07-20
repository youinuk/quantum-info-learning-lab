from pathlib import Path
import re
import xml.etree.ElementTree as ET

from core.content import load_lesson_markdown, load_level_content


ROOT = Path(__file__).resolve().parents[1]
IMAGE_ROOT = ROOT / "assets" / "images"
SVG_NAMESPACE = {"svg": "http://www.w3.org/2000/svg"}
UPDATED_VISUALS = (
    "interference.svg",
    "level4_interference_circuit.svg",
    "qubit_superposition.svg",
    "amplitude_probability.svg",
    "noise_measurement_example.svg",
    "noise_accumulation.svg",
)


def _number(value: str) -> float:
    match = re.match(r"-?\d+(?:\.\d+)?", value)
    assert match, f"Expected a numeric SVG value, got {value!r}"
    return float(match.group())


def test_all_svg_assets_are_parseable_and_responsive() -> None:
    for path in IMAGE_ROOT.glob("*.svg"):
        root = ET.parse(path).getroot()
        assert root.get("viewBox"), f"{path.name} has no viewBox"
        assert root.get("width") and root.get("height"), f"{path.name} has no fixed source dimensions"
        assert root.find("svg:title", SVG_NAMESPACE) is not None, f"{path.name} has no title"
        assert root.find("svg:desc", SVG_NAMESPACE) is not None, f"{path.name} has no description"
        source = path.read_text(encoding="utf-8")
        assert "&gt;" not in source, f"{path.name} still contains ASCII ket notation"


def test_updated_visual_elements_stay_inside_the_canvas() -> None:
    for filename in UPDATED_VISUALS:
        root = ET.parse(IMAGE_ROOT / filename).getroot()
        _, _, view_width, view_height = map(float, root.get("viewBox", "").split())

        for element in root.iter():
            tag = element.tag.rsplit("}", 1)[-1]
            if tag == "rect":
                x = _number(element.get("x", "0"))
                y = _number(element.get("y", "0"))
                width = _number(element.get("width", "0"))
                height = _number(element.get("height", "0"))
                assert 0 <= x <= view_width and 0 <= y <= view_height
                assert x + width <= view_width and y + height <= view_height
            elif tag == "circle":
                cx = _number(element.get("cx", "0"))
                cy = _number(element.get("cy", "0"))
                radius = _number(element.get("r", "0"))
                assert radius <= cx <= view_width - radius
                assert radius <= cy <= view_height - radius
            elif tag == "text":
                x = _number(element.get("x", "0"))
                y = _number(element.get("y", "0"))
                assert 0 <= x <= view_width and 0 <= y <= view_height


def test_level1_introduces_notation_before_amplitudes() -> None:
    expected_terms = {
        "ko": "브라-켓 표기법",
        "en": "bra-ket notation",
    }
    for lang, expected_term in expected_terms.items():
        lesson = load_lesson_markdown("level1", lang)
        content = load_level_content("level1", lang)
        term_names = {next(iter(item.values())) for item in content["terms"]}

        assert expected_term in term_names
        assert lesson.index(expected_term) < lesson.index(r"\alpha")
        assert len(re.findall(r"^## ", lesson, flags=re.MULTILINE)) == 7
        assert "assets/images/qubit_superposition.svg" in lesson
        assert "assets/images/amplitude_probability.svg" in lesson
        assert "amplitude_mixer.svg" not in lesson


def test_level7_uses_concrete_noise_examples() -> None:
    for lang in ("ko", "en"):
        lesson = load_lesson_markdown("level7", lang)

        assert r"(1-p)^n" in lesson
        assert r"0.99^{100}" in lesson
        assert "assets/images/noise_measurement_example.svg" in lesson
        assert "assets/images/noise_accumulation.svg" in lesson
        assert len(re.findall(r"^## ", lesson, flags=re.MULTILINE)) == 6
