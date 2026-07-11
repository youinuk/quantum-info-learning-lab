from core.content import load_level_content


def test_localized_simulations_have_waiting_messages():
    for lang in ("ko", "en"):
        for level in ("level0", "level1", "level2", "level4", "level5", "level8", "level10"):
            assert load_level_content(level, lang)["simulation_waiting"]


def test_localized_level4_and_level8_table_labels_exist():
    for lang in ("ko", "en"):
        level4_ui = load_level_content("level4", lang)["simulation_ui"]
        level8_ui = load_level_content("level8", lang)["simulation_ui"]

        assert set(level4_ui) == {"start_state", "middle_state", "final_state"}
        assert set(level8_ui) == {"case_column", "count_zero_column", "count_one_column"}
