from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGES_DIR = ROOT / "pages"


def _page_sources() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8") for path in PAGES_DIR.glob("*.py")
    )


def test_pages_do_not_implement_their_own_module_reload_logic() -> None:
    sources = _page_sources()

    assert "import importlib" not in sources
    assert "importlib.reload" not in sources


def test_pages_access_simulator_through_one_module_boundary() -> None:
    sources = _page_sources()

    assert "from core.simulator import" not in sources


def test_change_prone_pages_validate_cached_module_apis() -> None:
    for relative_path in (
        "04_level3_gates.py",
        "06_level5_two_qubits.py",
        "09_level8_circuit_reading.py",
        "11_level9_measurement_statistics.py",
        "12_level10_interference_depth.py",
        "14_level12_entanglement_limits.py",
        "15_level13_teleportation_dense_coding.py",
    ):
        source = (PAGES_DIR / relative_path).read_text(encoding="utf-8")
        assert "ensure_module_api(" in source


def test_streamlit_uses_polling_instead_of_disabling_source_updates() -> None:
    config = (ROOT / ".streamlit" / "config.toml").read_text(encoding="utf-8")

    assert 'fileWatcherType = "poll"' in config
