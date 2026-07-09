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
        "caption": "거울과 유리 장치를 조작해 빛의 직진, 반사, 굴절 경로를 설계하는 HTML5 물리 퍼즐이다.",
        "intro": (
            "게임은 별도 정적 사이트에서 열린다. "
            "이 방식이 PC와 모바일 브라우저에서 클릭, 키보드 입력, 화면 크기 문제를 가장 안정적으로 만든다."
        ),
        "open": "게임 열기",
        "configured": "현재 선택한 언어로 게임을 연다.",
        "source_missing": "정적 게임 원본 파일 일부가 없다: {files}",
        "admin_title": "배포 설정",
        "admin_body": (
            "`PHOTON_HEIST_URL` secret 또는 환경 변수를 설정하면 기본 게임 주소를 덮어쓸 수 있다. "
            "값이 없으면 현재 Cloudflare 배포 주소를 사용한다."
        ),
        "admin_code": f'PHOTON_HEIST_URL = "{DEFAULT_GAME_URL}"',
    },
    "en": {
        "title": "Photon Heist",
        "caption": "An HTML5 physics puzzle about straight-line light, reflection, and refraction.",
        "intro": (
            "The game opens as a separate static website. "
            "This keeps clicks, keyboard input, and responsive layout much more reliable on desktop and mobile browsers."
        ),
        "open": "Open game",
        "configured": "The game opens in the currently selected language.",
        "source_missing": "Some static game source files are missing: {files}",
        "admin_title": "Deployment Settings",
        "admin_body": (
            "Set the `PHOTON_HEIST_URL` secret or environment variable to override the default game URL. "
            "If it is not set, the app uses the current Cloudflare deployment."
        ),
        "admin_code": f'PHOTON_HEIST_URL = "{DEFAULT_GAME_URL}"',
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
st.write(text["intro"])

missing_files = missing_game_files()
if missing_files:
    st.error(text["source_missing"].format(files=", ".join(missing_files)))
else:
    game_url = configured_game_url()
    st.link_button(text["open"], add_language_to_url(game_url, lang), type="primary")
    st.caption(text["configured"])

with st.expander(text["admin_title"]):
    st.write(text["admin_body"])
    st.code(text["admin_code"], language="toml")
