from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import streamlit as st

from core.i18n import get_lang


ROOT = Path(__file__).resolve().parents[1]
GAME_SOURCE_DIR = ROOT / "games" / "photon_heist"
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
        "title": "Photon Heist · 빛의 도둑",
        "caption": "거울과 유리 장치를 조작해 빛의 직진, 반사, 굴절 경로를 설계하는 HTML5 물리 퍼즐이다.",
        "intro": (
            "게임은 Streamlit 화면 안에 끼워 넣지 않고 별도 정적 웹사이트로 연다. "
            "이 방식이 PC와 모바일 브라우저에서 클릭, 키보드, 화면 크기 문제를 가장 적게 만든다."
        ),
        "open": "게임 열기",
        "configured": "현재 설정된 게임 주소로 이동한다. 언어 선택은 URL의 `lang` 값으로 전달된다.",
        "missing_url": "아직 배포된 게임 주소가 설정되지 않았다.",
        "setup": "Streamlit Cloud secrets 또는 환경 변수에 다음 값을 추가하면 이 버튼이 실제 게임으로 연결된다.",
        "source_ok": "정적 게임 원본 파일은 프로젝트 안에 준비되어 있다.",
        "source_missing": "정적 게임 원본 파일 일부가 없다: {files}",
        "deploy_title": "권장 배포 방식",
        "deploy_body": (
            "Cloudflare Pages나 Netlify에서 `games/photon_heist` 폴더를 정적 사이트로 배포한다. "
            "빌드 명령은 비워 두고, 시작 파일은 `hub.html` 또는 `index.html`로 둔다."
        ),
        "move_note": (
            "배포가 안정되면 `games/photon_heist`를 별도 repo나 프로젝트 밖 폴더로 옮겨도 된다. "
            "그때 Streamlit 쪽은 `PHOTON_HEIST_URL`만 새 주소로 바꾸면 된다."
        ),
    },
    "en": {
        "title": "Photon Heist",
        "caption": "An HTML5 physics puzzle about straight-line light, reflection, and refraction.",
        "intro": (
            "The game opens as a separate static website instead of being embedded inside Streamlit. "
            "This keeps clicks, keyboard input, and responsive layout much more reliable on desktop and mobile browsers."
        ),
        "open": "Open game",
        "configured": "This opens the configured game URL. The selected language is passed through the `lang` query value.",
        "missing_url": "No deployed game URL is configured yet.",
        "setup": "Add this value to Streamlit Cloud secrets or to the environment to connect the button to the game.",
        "source_ok": "The static game source files are present in this project.",
        "source_missing": "Some static game source files are missing: {files}",
        "deploy_title": "Recommended deployment",
        "deploy_body": (
            "Deploy `games/photon_heist` as a static site on Cloudflare Pages or Netlify. "
            "Leave the build command empty, and use `hub.html` or `index.html` as the entry file."
        ),
        "move_note": (
            "After the deployment is stable, `games/photon_heist` can move to a separate repo or a folder outside this project. "
            "The Streamlit app only needs the `PHOTON_HEIST_URL` value updated."
        ),
    },
}


def missing_game_files() -> list[str]:
    return [path for path in REQUIRED_GAME_FILES if not (GAME_SOURCE_DIR / path).is_file()]


def configured_game_url() -> str:
    try:
        secret_value = st.secrets.get("PHOTON_HEIST_URL", "")
    except Exception:
        secret_value = ""
    return str(secret_value or os.environ.get("PHOTON_HEIST_URL", "")).strip()


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

game_url = configured_game_url()
missing_files = missing_game_files()

if missing_files:
    st.error(text["source_missing"].format(files=", ".join(missing_files)))
else:
    st.success(text["source_ok"])

if game_url:
    st.link_button(text["open"], add_language_to_url(game_url, lang), type="primary")
    st.caption(text["configured"])
else:
    st.warning(text["missing_url"])
    st.write(text["setup"])
    st.code('PHOTON_HEIST_URL = "https://your-photon-heist-site.example/hub.html"', language="toml")

st.subheader(text["deploy_title"])
st.write(text["deploy_body"])
st.info(text["move_note"])
