from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import streamlit as st

from core.i18n import get_lang


ROOT = Path(__file__).resolve().parents[1]
GAME_SOURCE_DIR = ROOT / "games" / "photon_heist"
DEFAULT_GAME_URL = "https://quantum-info-learning-lab.youinuk.workers.dev/hub"
REQUIRED_GAME_FILES = (
    "hub.html",
    "index.html",
    "glass.html",
    "styles/hub.css",
    "styles/style.css",
    "styles/glass.css",
    "src/streamlit_bridge.js",
    "src/hub.js",
    "src/game.js",
    "src/glass_game.js",
)

LAUNCHER_TEXT = {
    "ko": {
        "title": "Photon Heist: 빛의 도둑",
        "caption": "거울과 유리 장치로 빛의 직진, 반사, 굴절을 체험하는 퍼즐 게임이다.",
        "open": "게임 열기",
        "configured": "현재 선택한 언어로 게임을 연다.",
        "source_missing": "게임 파일 일부가 없다: {files}",
    },
    "en": {
        "title": "Photon Heist",
        "caption": "A puzzle game about straight-line light, reflection, and refraction.",
        "open": "Open game",
        "configured": "The game opens in the currently selected language.",
        "source_missing": "Some game files are missing: {files}",
    },
}


def missing_game_files() -> list[str]:
    return [path for path in REQUIRED_GAME_FILES if not (GAME_SOURCE_DIR / path).is_file()]


def configured_game_url() -> str:
    try:
        secret_value = st.secrets.get("PHOTON_HEIST_URL", "")
    except Exception:
        secret_value = ""
    return str(secret_value or os.environ.get("PHOTON_HEIST_URL", "") or DEFAULT_GAME_URL).strip()


def add_language_to_url(url: str, lang: str) -> str:
    parts = urlsplit(url)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query["lang"] = "en" if lang == "en" else "ko"
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


st.session_state["_active_learning_page"] = "photon_heist"
lang = get_lang()
text = LAUNCHER_TEXT.get(lang, LAUNCHER_TEXT["ko"])

st.title(text["title"])
st.caption(text["caption"])

missing_files = missing_game_files()
if missing_files:
    st.error(text["source_missing"].format(files=", ".join(missing_files)))
else:
    game_url = configured_game_url()
    st.link_button(text["open"], add_language_to_url(game_url, lang), type="primary")
    st.caption(text["configured"])
