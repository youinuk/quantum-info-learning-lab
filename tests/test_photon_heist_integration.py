import re
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest


ROOT = Path(__file__).resolve().parents[1]
GAME_DIR = ROOT / "games" / "photon_heist"
HTML_FILES = ("index.html", "hub.html", "glass.html")
JS_FILES = tuple((GAME_DIR / "src").glob("*.js"))
SCRIPT_PATTERN = re.compile(r'<script\s+src="([^"]+)"')
STYLE_PATTERN = re.compile(r'<link\s+rel="stylesheet"\s+href="([^"]+)"')
STAGE_PATTERN = re.compile(r'^\s*id:\s*"[^"]+"', re.MULTILINE)


def asset_path(src: str) -> str:
    return src.split("?", 1)[0]


def test_game_keeps_separate_local_assets_and_language_bridge() -> None:
    for relative_html in HTML_FILES:
        html = (GAME_DIR / relative_html).read_text(encoding="utf-8")
        scripts = SCRIPT_PATTERN.findall(html)
        styles = STYLE_PATTERN.findall(html)

        assert asset_path(scripts[0]) == "src/streamlit_bridge.js"
        assert styles
        assert all((GAME_DIR / asset_path(path)).is_file() for path in scripts + styles)
        assert "?v=20260710c" in html
        assert "??/option" not in html
        assert "??/button" not in html


def test_language_controls_are_identifiable_in_both_languages() -> None:
    for relative_html in HTML_FILES:
        html = (GAME_DIR / relative_html).read_text(encoding="utf-8")
        assert ">언어 / Language<" in html
        assert '<option value="ko">한국어 (Korean)</option>' in html
        assert '<option value="en">English (영어)</option>' in html

    for relative_js in ("i18n.js", "hub.js", "glass_game.js", "text_fixes.js"):
        source = (GAME_DIR / "src" / relative_js).read_text(encoding="utf-8")
        assert 'language: "언어 / Language"' in source


def test_existing_mirror_and_glass_stage_sets_are_preserved() -> None:
    mirror_levels = (GAME_DIR / "src" / "levels.js").read_text(encoding="utf-8")
    glass_levels = (GAME_DIR / "src" / "glass_levels.js").read_text(encoding="utf-8")

    assert len(STAGE_PATTERN.findall(mirror_levels)) == 10
    assert len(STAGE_PATTERN.findall(glass_levels)) == 10


def test_language_bridge_supports_standalone_static_site_mode() -> None:
    bridge = (GAME_DIR / "src" / "streamlit_bridge.js").read_text(encoding="utf-8")
    mirror = (GAME_DIR / "src" / "game.js").read_text(encoding="utf-8")
    glass = (GAME_DIR / "src" / "glass_game.js").read_text(encoding="utf-8")
    hub = (GAME_DIR / "src" / "hub.js").read_text(encoding="utf-8")

    assert 'new URLSearchParams(window.location.search).get("lang")' in bridge
    assert "window.parent !== window" in bridge
    assert "streamlit:componentReady" in bridge
    assert "streamlit:render" in bridge
    assert "streamlit:setFrameHeight" in bridge
    assert "saveLanguage(readLanguage())" in bridge
    assert "withLanguage" in bridge
    assert all("PhotonHeistBridge" in source for source in (mirror, glass, hub))
    assert all("photonheist:language" in source for source in (mirror, glass, hub))
    assert all("withLanguage" in source for source in (mirror, glass, hub))
    assert "el.languageSelect.value = state.lang" in mirror
    assert "glassEl.languageSelect.value = glassState.lang" in glass


def test_refraction_board_angle_labels_are_localized() -> None:
    glass = (GAME_DIR / "src" / "glass_game.js").read_text(encoding="utf-8")

    assert 'glassState.lang === "ko" ? "입사" : "Incident"' in glass
    assert 'glassState.lang === "ko" ? "굴절" : "Refracted"' in glass
    assert "iLbl.textContent = `입사" not in glass
    assert "rLbl.textContent = `굴절" not in glass


def test_mirror_board_and_hub_navigation_have_explicit_handlers() -> None:
    renderer = (GAME_DIR / "src" / "renderer.js").read_text(encoding="utf-8")
    game = (GAME_DIR / "src" / "game.js").read_text(encoding="utf-8")
    hub = (GAME_DIR / "src" / "hub.js").read_text(encoding="utf-8")

    assert "const actions = state.actions || {}" in renderer
    assert "actions.selectMirror" in renderer
    assert "actions.selectLaser" in renderer
    assert "selectMirror," in game
    assert "selectLaser" in game
    assert "link.href = hubUrl(chapter.file)" in hub
    assert "window.location.assign(chapter.file)" not in hub


def test_game_sources_do_not_contain_known_mojibake_breakage() -> None:
    for path in [
        GAME_DIR / "index.html",
        GAME_DIR / "hub.html",
        GAME_DIR / "glass.html",
        GAME_DIR / "src" / "levels.js",
        GAME_DIR / "src" / "glass_levels.js",
        GAME_DIR / "src" / "i18n.js",
        GAME_DIR / "src" / "glass_game.js",
        GAME_DIR / "src" / "hub.js",
        GAME_DIR / "src" / "renderer.js",
        GAME_DIR / "src" / "text_fixes.js",
    ]:
        source = path.read_text(encoding="utf-8")
        assert "\ufffd" not in source
        for pattern in ("쨌", "罐", "諛", "怨", "嫄", "援", "鍮", "吏", "痢", "?꾨", "?덉", "?묒", "?뚰", "?좊", "?"):
            assert pattern not in source, f"{path} contains mojibake pattern {pattern!r}"
        assert "??/option" not in source
        assert "??/button" not in source
        assert 'textContent = "??;' not in source
        assert 'return "??.repeat' not in source


def test_game_korean_ui_strings_are_not_left_as_english_defaults() -> None:
    i18n = (GAME_DIR / "src" / "i18n.js").read_text(encoding="utf-8")
    hub = (GAME_DIR / "src" / "hub.js").read_text(encoding="utf-8")
    game = (GAME_DIR / "src" / "game.js").read_text(encoding="utf-8")
    glass_game = (GAME_DIR / "src" / "glass_game.js").read_text(encoding="utf-8")

    for relative_html in HTML_FILES:
        html = (GAME_DIR / relative_html).read_text(encoding="utf-8")
        assert "src/text_fixes.js?v=20260710c" in html

    assert 'chapter: "거울 작전"' in i18n
    assert 'language: "언어 / Language"' in i18n
    assert 'fire: "레이저 발사"' in i18n
    assert 'planningTitle: "경로 계획"' in i18n
    assert 'hub: "작전 허브"' in i18n
    assert 'route: "캠페인 경로"' in hub
    assert 'state.lang === "ko" ? `스테이지 ${state.level.id}`' in game
    assert 'chapter: "유리 작전 · 굴절 경로"' in glass_game
    assert 'glassState.lang === "ko" ? `유리 ${level.id}`' in glass_game
    assert 'glassState.lang === "ko" ? "잠김" : "LOCK"' in glass_game
    assert "applyPhotonHeistTextFixes?.()" in hub


def test_game_javascript_string_quotes_stay_balanced() -> None:
    for path in JS_FILES:
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            assert line.count('"') % 2 == 0, f"{path.name}:{line_no} has an unbalanced string literal"
            assert line.count("`") % 2 == 0, f"{path.name}:{line_no} has an unbalanced template literal"


def test_runtime_probe_is_available_for_browser_validation() -> None:
    probe = GAME_DIR / "tests" / "runtime_probe.html"
    source = probe.read_text(encoding="utf-8")

    assert probe.is_file()
    assert "window.__probeErrors" in source
    assert "text_fixes.js" in source
    assert "selectedAfterClick" in source
    assert "successAfterRotate" in source
    assert "badText" in source
    assert "querySelectorAll(\".cell\").length" in source


def test_hub_runtime_probe_checks_localized_continue_link() -> None:
    probe = GAME_DIR / "tests" / "hub_runtime_probe.html"
    source = probe.read_text(encoding="utf-8")

    assert probe.is_file()
    assert "photonHeistProgressV1" in source
    assert "빛의 규칙을 훔쳐라" not in source
    assert "linkHref" in source
    assert "lang" in source
    assert "chapter-enter" in source


def test_glass_runtime_probe_checks_first_refraction_interaction() -> None:
    probe = GAME_DIR / "tests" / "glass_runtime_probe.html"
    source = probe.read_text(encoding="utf-8")

    assert probe.is_file()
    assert "glass_game.js" in source
    assert "loadGlassLevel(1)" in source
    assert "successAfterAim" in source
    assert "badText" in source


def test_game_page_is_registered_as_external_launcher() -> None:
    app_source = (ROOT / "app.py").read_text(encoding="utf-8")
    page_source = (ROOT / "pages" / "10_photon_heist.py").read_text(encoding="utf-8")
    requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")

    assert 'st.Page("pages/10_photon_heist.py"' in app_source
    assert "PHOTON_HEIST_URL" in page_source
    assert "DEFAULT_GAME_URL" in page_source
    assert "https://quantum-info-learning-lab.youinuk.workers.dev/hub" in page_source
    assert "st.link_button" in page_source
    assert "add_language_to_url" in page_source
    assert "render_photon_heist" not in page_source
    assert "declare_component" not in page_source
    assert not (ROOT / "core" / "photon_heist_component.py").exists()
    assert "streamlit==1.59.1" in requirements


@pytest.mark.parametrize("lang", ("ko", "en"))
def test_game_launcher_page_renders_without_streamlit_exceptions(lang: str) -> None:
    app = AppTest.from_file(str(ROOT / "pages" / "10_photon_heist.py"), default_timeout=20)
    app.session_state["lang"] = lang
    app.run()

    assert not app.exception
    assert not app.warning
    assert app.title
