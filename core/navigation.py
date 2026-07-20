"""Shared navigation for the linear learning path."""

from __future__ import annotations

import streamlit as st

from core.i18n import t


LEVEL_PAGES = [
    "pages/01_level0_bit_probability.py",
    "pages/02_level1_qubit_placeholder.py",
    "pages/03_level2_measurement.py",
    "pages/04_level3_gates.py",
    "pages/05_level4_interference.py",
    "pages/06_level5_two_qubits.py",
    "pages/07_level6_entanglement.py",
    "pages/08_level7_noise.py",
    "pages/09_level8_circuit_reading.py",
    "pages/11_level9_measurement_statistics.py",
    "pages/12_level10_interference_depth.py",
    "pages/13_level11_algorithms.py",
    "pages/14_level12_entanglement_limits.py",
    "pages/15_level13_teleportation_dense_coding.py",
]


def _safe_page_link(page: str, *, label: str, icon: str, icon_position: str = "left") -> None:
    try:
        st.page_link(
            page,
            label=label,
            icon=icon,
            icon_position=icon_position,
            width="stretch",
        )
    except (KeyError, RuntimeError):
        st.caption(label)


def render_level_navigation(current_level: int) -> None:
    """Render previous, home, and next links below a level."""
    if not 0 <= current_level < len(LEVEL_PAGES):
        raise ValueError(f"current_level must be between 0 and {len(LEVEL_PAGES) - 1}")

    st.divider()
    previous_col, home_col, next_col = st.columns(3)

    with previous_col:
        if current_level > 0:
            previous = current_level - 1
            _safe_page_link(
                LEVEL_PAGES[previous],
                label=t("previous_level").format(title=t(f"nav_level{previous}")),
                icon=":material/arrow_back:",
            )

    with home_col:
        _safe_page_link(
            "pages/00_home.py",
            label=t("nav_home"),
            icon=":material/home:",
        )

    with next_col:
        if current_level < len(LEVEL_PAGES) - 1:
            following = current_level + 1
            _safe_page_link(
                LEVEL_PAGES[following],
                label=t("next_level").format(title=t(f"nav_level{following}")),
                icon=":material/arrow_forward:",
                icon_position="right",
            )
