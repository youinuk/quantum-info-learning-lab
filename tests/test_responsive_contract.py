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

    chart_calls = re.findall(r"st\.pyplot\([^\n]+\)", page_sources)

    assert len(chart_calls) == 13
    assert "use_container_width" not in page_sources
    assert all('width="stretch"' in call for call in chart_calls)
