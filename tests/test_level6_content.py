from core.content import load_lesson_markdown, load_level_content


STATE_IDS = {
    "product_plus",
    "classical_correlated",
    "bell_phi_plus",
}


def test_level6_localized_content_has_matching_comparison_structure():
    for lang in ("ko", "en"):
        content = load_level_content("level6", lang)
        state_ids = {item["id"] for item in content["state_options"]}
        lesson = load_lesson_markdown("level6", lang)

        assert state_ids == STATE_IDS
        assert len(content["quiz"]) == 6
        assert len(content["terms"]) == 6
        assert lesson.count("## ") == 8
        assert "assets/images/entanglement_basis_compare.svg" in lesson
        assert "Level 5" in lesson
        assert r"\xrightarrow{\mathrm{CNOT}}" in lesson
