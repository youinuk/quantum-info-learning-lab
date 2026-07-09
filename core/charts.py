"""Small chart helpers for Streamlit pages."""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


def compact_count_bar(
    labels: list[str],
    counts: list[int | float],
    title: str = "",
    ylabel: str = "count",
):
    fig_width = 3.4 if len(labels) <= 2 else 4.4
    fig, ax = plt.subplots(figsize=(fig_width, 2.45), dpi=140)
    palette = ["#2f80ed", "#6366f1", "#8b5cf6", "#f43f5e"]
    colors = palette[: len(labels)]
    bars = ax.bar(labels, counts, color=colors, width=0.36)
    ax.set_title(title, fontsize=10, pad=8)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.tick_params(axis="x", labelrotation=0, labelsize=10)
    ax.tick_params(axis="y", labelsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.2)
    ymax = max(counts) if counts else 1
    ax.set_ylim(0, max(1, ymax * 1.18))
    for bar, count in zip(bars, counts):
        label = f"{count:g}" if isinstance(count, float) else str(count)
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            label,
            ha="center",
            va="bottom",
            fontsize=9,
        )
    fig.tight_layout()
    return fig


def compact_grouped_bar(
    labels: list[str],
    first_values: list[int | float],
    second_values: list[int | float],
    first_label: str,
    second_label: str,
    title: str = "",
    ylabel: str = "count",
):
    fig, ax = plt.subplots(figsize=(4.4, 2.65), dpi=140)
    positions = list(range(len(labels)))
    width = 0.32
    first_positions = [position - width / 2 for position in positions]
    second_positions = [position + width / 2 for position in positions]
    first_bars = ax.bar(first_positions, first_values, width=width, color="#2f80ed", label=first_label)
    second_bars = ax.bar(second_positions, second_values, width=width, color="#f43f5e", label=second_label)

    ax.set_title(title, fontsize=10, pad=8)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.set_xticks(positions, labels)
    ax.tick_params(axis="x", labelrotation=0, labelsize=10)
    ax.tick_params(axis="y", labelsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.2)
    ymax = max(first_values + second_values) if first_values or second_values else 1
    ax.set_ylim(0, max(1, ymax * 1.2))
    ax.legend(frameon=False, fontsize=8, ncols=2, loc="upper center")

    for bars, values in ((first_bars, first_values), (second_bars, second_values)):
        for bar, value in zip(bars, values):
            label = f"{value:g}" if isinstance(value, float) else str(value)
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                label,
                ha="center",
                va="bottom",
                fontsize=8,
            )

    fig.tight_layout()
    return fig
