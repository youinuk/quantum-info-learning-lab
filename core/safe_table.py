"""Safe table rendering that avoids Streamlit's pandas/Arrow path."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import streamlit as st


def _escape_markdown_cell(value: Any) -> str:
    text = "" if value is None else str(value)
    return (
        text.replace("\\", "\\\\")
        .replace("|", "\\|")
        .replace("\r\n", "<br>")
        .replace("\n", "<br>")
        .strip()
    )


def render_markdown_table(rows: list[dict[str, Any]], columns: Iterable[str] | None = None) -> None:
    """Render a small educational table without pandas or pyarrow."""
    if not rows:
        return

    headers = list(columns) if columns is not None else list(rows[0].keys())
    lines = [
        "| " + " | ".join(_escape_markdown_cell(header) for header in headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(_escape_markdown_cell(row.get(header, "")) for header in headers) + " |")

    st.markdown("\n".join(lines))
