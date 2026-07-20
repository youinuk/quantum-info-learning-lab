import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")
README_KR = (ROOT / "README_KR.md").read_text(encoding="utf-8")
ROADMAP = (ROOT / "docs" / "curriculum_roadmap.md").read_text(encoding="utf-8")
REGISTRY = (ROOT / "docs" / "experiment_registry.md").read_text(encoding="utf-8")


BRIDGE_LEVELS = {
    13: "양자전송과 초밀집 부호화",
    14: "양자암호와 BB84",
    15: "양자네트워크",
    16: "오류를 찾고 줄이는 방법",
    17: "실제 양자 하드웨어",
    18: "SDK와 실제 실행 맛보기",
}


def test_readme_links_to_project_planning_documents() -> None:
    for relative_path in (
        "docs/curriculum_roadmap.md",
        "docs/photon_heist_roadmap.md",
        "docs/experiment_registry.md",
        "docs/development.md",
        "docs/content_style_guide.md",
        "docs/cloud_deploy_checklist.md",
    ):
        assert f"]({relative_path})" in README
        assert f"]({relative_path})" in README_KR
        assert (ROOT / relative_path).is_file()


def test_local_markdown_links_resolve() -> None:
    documents = [ROOT / "README.md", ROOT / "README_KR.md", *(ROOT / "docs").glob("*.md")]

    for document in documents:
        source = document.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", source):
            if "://" in target or target.startswith("#"):
                continue
            relative_target = target.split("#", maxsplit=1)[0]
            assert (document.parent / relative_target).resolve().exists(), (
                document,
                target,
            )


def test_curriculum_roadmap_is_the_single_learning_app_plan() -> None:
    assert not (ROOT / "docs" / "next_expansion_plan.md").exists()
    assert not (ROOT / "docs" / "streamlit_cloud_deploy.md").exists()
    paths = [ROOT / "README.md", ROOT / "README_KR.md", *(ROOT / "docs").glob("*.md")]
    for path in paths:
        assert "next_expansion_plan" not in path.read_text(encoding="utf-8")


def test_bridge_levels_are_registered_in_the_roadmap() -> None:
    for level, title in BRIDGE_LEVELS.items():
        assert f"Level {level} · {title}" in ROADMAP


def test_planned_experiments_use_the_bridge_level_numbers() -> None:
    expected_mappings = {
        "EXP-CRYPTO01": 14,
        "EXP-CRYPTO02": 14,
        "EXP-NET01": 15,
        "EXP-NET02": 15,
        "EXP-EC01": 16,
        "EXP-EC02": 16,
        "EXP-HW01": 17,
        "EXP-HW02": 17,
        "EXP-SDK01": 18,
        "EXP-SDK02": 18,
    }

    for experiment_id, level in expected_mappings.items():
        pattern = rf"\| {experiment_id} \|[^\n]+\| {level} \| `TBD_LEVEL{level}` \|"
        assert re.search(pattern, REGISTRY)


def test_level13_experiments_point_to_the_implemented_page() -> None:
    for experiment_id in ("EXP-COM01", "EXP-COM02", "EXP-COM03", "EXP-COM04"):
        pattern = (
            rf"\| {experiment_id} \|[^\n]+\| 13 \| "
            r"`pages/15_level13_teleportation_dense_coding\.py` \|[^\n]+\| implemented \|"
        )
        assert re.search(pattern, REGISTRY)


def test_advanced_curriculum_has_algorithm_and_error_correction_paths() -> None:
    assert "## 고급 과정 진입 기준" in ROADMAP
    for unit in (
        "Advanced A0",
        "Advanced ALG1",
        "Advanced ALG2",
        "Advanced ALG3",
        "Advanced ALG4",
        "Advanced QEC1",
        "Advanced QEC2",
        "Advanced APP1",
    ):
        assert unit in ROADMAP

    assert "Stabilizer" in ROADMAP
    assert "Surface code" in ROADMAP
    assert "Quantum Machine Learning" in ROADMAP


def test_optional_modules_are_not_presented_as_post_advanced_levels() -> None:
    optional_heading = "## 선택형 모듈과 진입 시점"
    assert optional_heading in ROADMAP
    assert ROADMAP.index(optional_heading) < ROADMAP.index("## 고급 과정 진입 기준")
    assert "Advanced를 모두 마친 다음 단계가 아니다" in ROADMAP


def test_roadmap_uses_display_ready_ket_notation() -> None:
    assert not re.search(r"\|(?:0|1|\+|-)>", ROADMAP)


def test_github_readme_is_english_and_links_to_korean_version() -> None:
    assert not re.search(r"[가-힣]", README)
    assert "](README_KR.md)" in README
    assert "](README.md)" in README_KR


def test_readme_versions_share_deployments_levels_and_document_paths() -> None:
    shared_values = (
        "https://quantum-info-learning-lab.streamlit.app",
        "https://quantum-info-learning-lab.youinuk.workers.dev/hub",
        "content/lessons/{lang}/levelN.md",
        "content/levels.json",
        "content/levels_en.json",
        "content/resources.json",
        "docs/quantum_conventions.md",
        "docs/content_style_guide.md",
        "docs/media_attributions.md",
    )
    for value in shared_values:
        assert value in README
        assert value in README_KR

    for level in range(19):
        assert f"Level {level}:" in README
        assert f"Level {level}:" in README_KR


def test_private_notes_and_local_tool_state_are_ignored() -> None:
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    for pattern in (
        ".streamlit/secrets.toml",
        ".agents/",
        ".codex/",
        ".wrangler/",
        "docs/private/",
    ):
        assert pattern in gitignore
