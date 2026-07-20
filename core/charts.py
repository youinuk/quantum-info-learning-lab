"""Small chart helpers for Streamlit pages."""

from __future__ import annotations

import math

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import streamlit as st


def render_fig(fig, **kwargs) -> None:
    """Render a Matplotlib figure in Streamlit and always release it."""
    try:
        st.pyplot(fig, **kwargs)
    finally:
        plt.close(fig)


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


def phase_interference_sweep_chart(phase_degrees: float):
    """Show relative phase vectors and the full bright/dark probability sweep."""
    phase_radians = math.radians(phase_degrees)
    degrees = list(range(361))
    bright = [(1 + math.cos(math.radians(value))) / 2 for value in degrees]
    dark = [1 - value for value in bright]
    current_bright = (1 + math.cos(phase_radians)) / 2
    current_dark = 1 - current_bright

    fig, (phase_ax, curve_ax) = plt.subplots(1, 2, figsize=(7.2, 3.0), dpi=140)

    circle = plt.Circle((0, 0), 1, fill=False, color="#cbd5e1", linewidth=1.2, linestyle="--")
    phase_ax.add_patch(circle)
    phase_ax.arrow(0, 0, 0.88, 0, width=0.025, head_width=0.12, head_length=0.12, color="#2563eb", length_includes_head=True)
    phase_ax.arrow(
        0,
        0,
        0.88 * math.cos(phase_radians),
        0.88 * math.sin(phase_radians),
        width=0.025,
        head_width=0.12,
        head_length=0.12,
        color="#f59e0b",
        length_includes_head=True,
    )
    phase_ax.text(0.55, -0.18, "path A", color="#1d4ed8", fontsize=9)
    phase_ax.text(
        0.58 * math.cos(phase_radians),
        0.58 * math.sin(phase_radians) + 0.12,
        "path B",
        color="#b45309",
        fontsize=9,
        ha="center",
    )
    phase_ax.set_title(f"Relative phase: {phase_degrees:.0f} deg", fontsize=10, pad=8)
    phase_ax.set_xlim(-1.2, 1.2)
    phase_ax.set_ylim(-1.2, 1.2)
    phase_ax.set_aspect("equal")
    phase_ax.axis("off")

    curve_ax.plot(degrees, bright, color="#2563eb", linewidth=2.2, label="bright")
    curve_ax.plot(degrees, dark, color="#f43f5e", linewidth=2.2, label="dark")
    curve_ax.axvline(phase_degrees, color="#334155", linewidth=1.2, linestyle="--")
    curve_ax.scatter([phase_degrees], [current_bright], color="#2563eb", s=42, zorder=3)
    curve_ax.scatter([phase_degrees], [current_dark], color="#f43f5e", s=42, zorder=3)
    curve_ax.set_title("Probability across phase", fontsize=10, pad=8)
    curve_ax.set_xlabel("phase difference (deg)", fontsize=9)
    curve_ax.set_ylabel("probability", fontsize=9)
    curve_ax.set_xlim(0, 360)
    curve_ax.set_ylim(0, 1.05)
    curve_ax.set_xticks([0, 90, 180, 270, 360])
    curve_ax.tick_params(labelsize=8)
    curve_ax.grid(alpha=0.2)
    curve_ax.spines["top"].set_visible(False)
    curve_ax.spines["right"].set_visible(False)
    curve_ax.legend(frameon=False, fontsize=8, ncols=2, loc="upper center")

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


def compact_interval_bar(
    labels: list[str],
    means: list[float],
    lows: list[float],
    highs: list[float],
    title: str = "",
    ylabel: str = "value",
    target: float | None = None,
):
    fig, ax = plt.subplots(figsize=(4.4, 2.65), dpi=140)
    positions = list(range(len(labels)))
    lower_errors = [max(0.0, mean - low) for mean, low in zip(means, lows)]
    upper_errors = [max(0.0, high - mean) for mean, high in zip(means, highs)]
    bars = ax.bar(
        positions,
        means,
        width=0.38,
        color="#2f80ed",
        yerr=[lower_errors, upper_errors],
        capsize=4,
        ecolor="#334155",
    )
    if target is not None:
        ax.axhline(target, color="#f43f5e", linewidth=1.4, linestyle="--", label="target")
        ax.legend(frameon=False, fontsize=8, loc="upper right")

    ax.set_title(title, fontsize=10, pad=8)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.set_xticks(positions, labels)
    ax.tick_params(axis="x", labelrotation=0, labelsize=10)
    ax.tick_params(axis="y", labelsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.2)
    ymax = max(highs + ([target] if target is not None else [0])) if highs else 1
    ax.set_ylim(0, max(1, ymax * 1.18))

    for bar, mean in zip(bars, means):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{mean:.1f}",
            ha="center",
            va="bottom",
            fontsize=8,
        )

    fig.tight_layout()
    return fig


def compact_dual_interval_bar(
    labels: list[str],
    first_means: list[float],
    first_lows: list[float],
    first_highs: list[float],
    second_means: list[float],
    second_lows: list[float],
    second_highs: list[float],
    first_label: str,
    second_label: str,
    title: str = "",
    ylabel: str = "value",
    target: float | None = None,
):
    fig, ax = plt.subplots(figsize=(4.8, 2.8), dpi=140)
    positions = list(range(len(labels)))
    width = 0.3
    first_positions = [position - width / 2 for position in positions]
    second_positions = [position + width / 2 for position in positions]

    first_errors = [
        [max(0.0, mean - low) for mean, low in zip(first_means, first_lows)],
        [max(0.0, high - mean) for mean, high in zip(first_means, first_highs)],
    ]
    second_errors = [
        [max(0.0, mean - low) for mean, low in zip(second_means, second_lows)],
        [max(0.0, high - mean) for mean, high in zip(second_means, second_highs)],
    ]

    first_bars = ax.bar(
        first_positions,
        first_means,
        width=width,
        color="#2f80ed",
        yerr=first_errors,
        capsize=3,
        ecolor="#334155",
        label=first_label,
    )
    second_bars = ax.bar(
        second_positions,
        second_means,
        width=width,
        color="#f43f5e",
        yerr=second_errors,
        capsize=3,
        ecolor="#334155",
        label=second_label,
    )
    if target is not None:
        ax.axhline(target, color="#64748b", linewidth=1.2, linestyle="--", label="target")

    ax.set_title(title, fontsize=10, pad=8)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.set_xticks(positions, labels)
    ax.tick_params(axis="x", labelrotation=0, labelsize=10)
    ax.tick_params(axis="y", labelsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.2)
    ymax_values = first_highs + second_highs + ([target] if target is not None else [0])
    ax.set_ylim(0, max(1, max(ymax_values) * 1.18))
    ax.legend(frameon=False, fontsize=8, ncols=3, loc="upper center")

    for bars, means in ((first_bars, first_means), (second_bars, second_means)):
        for bar, mean in zip(bars, means):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                f"{mean:.1f}",
                ha="center",
                va="bottom",
                fontsize=7,
            )

    fig.tight_layout()
    return fig
