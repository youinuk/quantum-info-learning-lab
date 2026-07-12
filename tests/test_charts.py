from pathlib import Path

import matplotlib.pyplot as plt

from core.charts import compact_dual_interval_bar, compact_grouped_bar, compact_interval_bar


ROOT = Path(__file__).resolve().parents[1]


def test_grouped_bar_renders_both_series():
    figure = compact_grouped_bar(
        ["0", "1"],
        [40, 60],
        [45, 55],
        "ideal",
        "noisy",
        "Comparison",
    )

    axis = figure.axes[0]
    assert len(axis.patches) == 4
    assert [text.get_text() for text in axis.get_legend().get_texts()] == ["ideal", "noisy"]
    plt.close(figure)


def test_interval_bar_renders_target_line_and_bars():
    figure = compact_interval_bar(
        ["10", "100", "1000"],
        [60, 52, 50],
        [30, 45, 48],
        [90, 60, 52],
        "Sampling range",
        target=50,
    )

    axis = figure.axes[0]
    assert len(axis.patches) == 3
    assert len(axis.lines) >= 1
    plt.close(figure)


def test_dual_interval_bar_renders_two_series():
    figure = compact_dual_interval_bar(
        ["10", "100", "1000"],
        [50, 51, 50],
        [20, 42, 48],
        [80, 60, 52],
        [54, 55, 55],
        [25, 46, 53],
        [85, 64, 57],
        "ideal",
        "noisy",
        "Mean and range",
        target=50,
    )

    axis = figure.axes[0]
    assert len(axis.patches) == 6
    assert set(text.get_text() for text in axis.get_legend().get_texts()) == {"ideal", "noisy", "target"}
    plt.close(figure)


def test_pages_use_chart_render_helper_instead_of_direct_st_pyplot():
    for page_path in (ROOT / "pages").glob("*.py"):
        source = page_path.read_text(encoding="utf-8")
        assert "st.pyplot(" not in source
