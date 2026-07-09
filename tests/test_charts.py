import matplotlib.pyplot as plt

from core.charts import compact_grouped_bar


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
