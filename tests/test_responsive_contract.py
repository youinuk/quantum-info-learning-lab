from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def test_mobile_layout_rules_are_present() -> None:
    app_source = (ROOT / "app.py").read_text(encoding="utf-8")

    assert '@media (max-width: 700px)' in app_source
    assert 'div[data-testid="stHorizontalBlock"]' in app_source
    assert 'div[data-testid="stColumn"]' in app_source
    assert 'button[role="tab"]' in app_source
    assert ".katex-display" in app_source
    assert 'div[data-testid="stTable"]' in app_source


def test_all_matplotlib_charts_follow_the_container_width() -> None:
    page_sources = "\n".join(
        path.read_text(encoding="utf-8") for path in (ROOT / "pages").glob("*.py")
    )

    chart_calls = re.findall(r"render_fig\([^\n]+\)", page_sources)

    assert len(chart_calls) == 14
    assert "st.pyplot(" not in page_sources
    assert "use_container_width" not in page_sources
    assert all('width="stretch"' in call for call in chart_calls)


def test_learning_images_use_compact_desktop_widths() -> None:
    renderer_source = (ROOT / "core" / "lesson_renderer.py").read_text(encoding="utf-8")
    direct_image_pages = (
        "09_level8_circuit_reading.py",
        "12_level10_interference_depth.py",
        "14_level12_entanglement_limits.py",
    )

    assert "DEFAULT_LESSON_IMAGE_WIDTH = 680" in renderer_source
    assert 'LESSON_IMAGE_WIDTHS.get(image_path.name, "stretch")' not in renderer_source
    assert 'data:image/gif;base64,' in renderer_source
    assert '"double_slit_interference.svg": 680' in renderer_source
    assert '"level10_deutsch_interference_bridge.svg": 680' in renderer_source
    assert '"electron_double_slit_buildup.gif": 680' in renderer_source
    for filename in direct_image_pages:
        source = (ROOT / "pages" / filename).read_text(encoding="utf-8")
        assert 'st.image(str(image_path), caption=selected.get("label", ""), width="stretch")' not in source

    level12_source = (ROOT / "pages" / "14_level12_entanglement_limits.py").read_text(encoding="utf-8")
    assert 'caption=ui.get("diagram_caption", ""), width=760' in level12_source


def test_level10_omits_deprecated_two_path_sketch() -> None:
    for lang in ("ko", "en"):
        lesson = (ROOT / "content" / "lessons" / lang / "level10.md").read_text(encoding="utf-8")
        assert "level11_two_path_interference.svg" not in lesson
        assert "assets/images/double_slit_wavefronts.webp" in lesson
        assert "assets/images/Doubleslit3Dspectrum.gif" in lesson
        assert "assets/images/electron_double_slit_buildup.gif" not in lesson
        assert "assets/images/double_slit_interference.svg" not in lesson
