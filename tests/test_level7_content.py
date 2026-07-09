from core.content import load_lesson_markdown, load_level_content


ORACLE_IDS = {
    "constant_zero",
    "constant_one",
    "balanced_identity",
    "balanced_flip",
}


def test_level7_localized_content_has_matching_learning_structure():
    for lang in ("ko", "en"):
        content = load_level_content("level7", lang)
        option_ids = {item["id"] for item in content["oracle_options"]}
        lesson = load_lesson_markdown("level7", lang)

        assert option_ids == ORACLE_IDS
        assert len(content["quiz"]) == 6
        assert len(content["terms"]) == 6
        assert lesson.count("## ") == 8
        assert "assets/images/deutsch_algorithm.svg" in lesson
