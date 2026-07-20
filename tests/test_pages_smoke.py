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
    assert app.selectbox[0].label == "Language / 언어"
    assert app.selectbox[0].options == ["English (영어)", "한국어 (Korean)"]


def test_app_shell_defaults_to_english() -> None:
    app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=20)
    app.run()

    assert not app.exception
    assert app.selectbox[0].value == "English (영어)"


def test_level5_two_qubit_gate_experiment_runs() -> None:
    app = build_page_app("pages/06_level5_two_qubits.py", "ko")
    app.run()

    gate_run = [button for button in app.button if button.label == "실험 실행"][1]
    gate_run.click().run()

    assert not app.exception
    assert any("CNOT" in markdown.value for markdown in app.markdown)


def test_level5_page_recovers_when_stale_module_lacks_gate_api() -> None:
    page_path = ROOT / "pages" / "06_level5_two_qubits.py"
    wrapper = f'''\
import runpy
import streamlit as st
import core.simulator as simulator

del simulator.apply_two_qubit_basis_gate
st.page_link = lambda *args, **kwargs: None
runpy.run_path(r"{page_path}", run_name="__main__")
'''
    app = AppTest.from_string(wrapper, default_timeout=20)
    app.session_state["lang"] = "en"
    app.run()

    gate_run = [button for button in app.button if button.label == "Run experiment"][1]
    gate_run.click().run()

    assert not app.exception


def test_level3_reloads_simulator_before_using_the_s_gate() -> None:
    page_path = ROOT / "pages" / "04_level3_gates.py"
    wrapper = f'''\
import runpy
import streamlit as st
import core.math_display as math_display
import core.simulator as simulator

del math_display.qubit_amplitudes_latex
del simulator.apply_single_qubit_gate
st.page_link = lambda *args, **kwargs: None
runpy.run_path(r"{page_path}", run_name="__main__")
'''
    app = AppTest.from_string(wrapper, default_timeout=20)
    app.session_state["lang"] = "en"
    app.run()

    next(button for button in app.button if button.label == "S").click().run()
    assert any(r"\beta=0" in element.value for element in app.latex)
    assert any("Beta is currently zero" in element.value for element in app.info)

    next(button for button in app.button if button.label == "H").click().run()
    next(button for button in app.button if button.label == "S").click().run()

    assert not app.exception
    assert any(
        r"\beta=\frac{1}{\sqrt{2}}i" in element.value for element in app.latex
    )
