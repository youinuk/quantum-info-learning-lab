"""Render lesson markdown with local image support."""

from __future__ import annotations

import base64
import html
import re
from pathlib import Path

import streamlit as st

from core.content import BASE_DIR
from core.i18n import t
from core.math_display import inline_kets_to_latex

IMAGE_PATTERN = re.compile(r"^!\[(?P<caption>.*?)\]\((?P<path>.*?)\)\s*$")
HEADING_PATTERN = re.compile(r"^##\s+(?P<title>.+?)\s*$")
EXPANDER_PATTERN = re.compile(r"^:::expander\s+(?P<label>.+?)\s*$")
LESSON_IMAGE_WIDTHS = {
    "Doubleslit.svg": 360,
    "Doubleslit3Dspectrum.gif": 420,
    "double_slit_setup.svg": 560,
    "double_slit_wavefronts.webp": 680,
    "electron_double_slit_buildup.gif": 680,
    "double_slit_interference.svg": 680,
    "level10_deutsch_interference_bridge.svg": 680,
}
DEFAULT_LESSON_IMAGE_WIDTH = 680


def split_lesson_cards(markdown: str) -> list[dict[str, str]]:
    cards: list[dict[str, str]] = []
    current_title = ""
    current_lines: list[str] = []

    for line in markdown.splitlines():
        heading = HEADING_PATTERN.match(line)
        if heading:
            if current_title:
                cards.append({"title": current_title, "body": "\n".join(current_lines).strip()})
            current_title = heading.group("title")
            current_lines = []
            continue
        current_lines.append(line)

    if current_title:
        cards.append({"title": current_title, "body": "\n".join(current_lines).strip()})

    return cards


def render_lesson_cards(markdown: str, key: str) -> None:
    cards = split_lesson_cards(markdown)
    if not cards:
        render_lesson_markdown(markdown)
        return

    titles = [card["title"] for card in cards]
    selected_title = st.radio(t("slide_select"), titles, horizontal=False, key=f"{key}_card_select")
    card = next(item for item in cards if item["title"] == selected_title)
    st.subheader(card["title"])
    render_lesson_markdown(card["body"])


def render_lesson_markdown(markdown: str) -> None:
    buffer: list[str] = []

    def flush() -> None:
        if buffer:
            st.markdown(inline_kets_to_latex("\n".join(buffer)))
            buffer.clear()

    lines = markdown.splitlines()
    line_index = 0
    while line_index < len(lines):
        line = lines[line_index]
        expander_match = EXPANDER_PATTERN.match(line.strip())
        if expander_match:
            flush()
            expander_lines: list[str] = []
            line_index += 1
            while line_index < len(lines) and lines[line_index].strip() != ":::":
                expander_lines.append(lines[line_index])
                line_index += 1
            with st.expander(expander_match.group("label")):
                render_lesson_markdown("\n".join(expander_lines))
            line_index += 1
            continue

        match = IMAGE_PATTERN.match(line.strip())
        if not match:
            buffer.append(line)
            line_index += 1
            continue

        flush()
        image_path = BASE_DIR / Path(match.group("path"))
        caption = match.group("caption")
        if image_path.exists():
            width = LESSON_IMAGE_WIDTHS.get(image_path.name, DEFAULT_LESSON_IMAGE_WIDTH)
            if image_path.suffix.lower() == ".gif":
                encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
                alt = html.escape(caption or image_path.stem, quote=True)
                st.markdown(
                    f'<img src="data:image/gif;base64,{encoded}" alt="{alt}" '
                    f'style="width:{width}px;max-width:100%;height:auto;display:block">',
                    unsafe_allow_html=True,
                )
                if caption:
                    st.caption(caption)
            else:
                st.image(str(image_path), caption=caption or None, width=width)
        else:
            st.warning(t("lesson_image_missing").format(path=image_path))
        line_index += 1

    flush()
