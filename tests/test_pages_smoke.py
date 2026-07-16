from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from core.navigation import LEVEL_PAGES


ROOT = Path(__file__).resolve().parents[1]
PAGE_PATHS = ("pages/00_home.py", *LEVEL_PAGES)
INTERACTION_CASES = tuple(
    (relative_path, "H" if level == 3 else "실험 실행")
    for level, relative_path in enumerate(LEVEL_PAGES)
)


def build_page_app(relative_path: str, lang: str) -> AppTest:
    page_path = ROOT / relative_path
    wrapper = f'''\
import runpy
import streamlit as st

st.page_link = lambda *args, **kwargs: None
runpy.run_path(r"{page_path}", run_name="__main__")
'''
    app = AppTest.from_string(wrapper, default_timeout=20)
    app.session_state["lang"] = lang
    return app


@pytest.mark.parametrize("lang", ("ko", "en"))
@pytest.mark.parametrize("relative_path", PAGE_PATHS)
def test_page_renders_without_streamlit_exceptions(relative_path: str, lang: str) -> None:
    app = build_page_app(relative_path, lang)
    app.run()

    assert not app.exception


@pytest.mark.parametrize(("relative_path", "button_label"), INTERACTION_CASES)
def test_level_primary_interaction_runs_without_exceptions(
    relative_path: str, button_label: str
) -> None:
    app = build_page_app(relative_path, "ko")
    app.run()

    button = next(item for item in app.button if item.label == button_label)
    button.click().run()

    assert not app.exception


@pytest.mark.parametrize("lang", ("ko", "en"))
def test_app_shell_registers_navigation_and_renders_home(lang: str) -> None:
    app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=20)
    app.session_state["lang"] = lang
    app.run()

    assert not app.exception
    assert app.selectbox[0].label == "언어 / Language"
    assert app.selectbox[0].options == ["한국어 (Korean)", "English (영어)"]
