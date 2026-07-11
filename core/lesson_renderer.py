"""Render lesson markdown with local image support."""

from __future__ import annotations

import re
from pathlib import Path

import streamlit as st

from core.content import BASE_DIR
from core.i18n import t
from core.math_display import inline_kets_to_latex

IMAGE_PATTERN = re.compile(r"^!\[(?P<caption>.*?)\]\((?P<path>.*?)\)\s*$")
HEADING_PATTERN = re.compile(r"^##\s+(?P<title>.+?)\s*$")
LESSON_IMAGE_WIDTHS = {
    "Doubleslit.svg": 420,
    "Doubleslit3Dspectrum.gif": 320,
    "double_slit_interference.svg": 640,
}


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

    for line in markdown.splitlines():
        match = IMAGE_PATTERN.match(line.strip())
        if not match:
            buffer.append(line)
            continue

        flush()
        image_path = BASE_DIR / Path(match.group("path"))
        caption = match.group("caption")
        if image_path.exists():
            width = LESSON_IMAGE_WIDTHS.get(image_path.name, "stretch")
            st.image(str(image_path), caption=caption or None, width=width)
        else:
            st.warning(t("lesson_image_missing").format(path=image_path))

    flush()
