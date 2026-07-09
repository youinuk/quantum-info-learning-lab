from core.content import load_level_content
from core.i18n import TRANSLATIONS
from streamlit.testing.v1 import AppTest


LEVELS = tuple(f"level{number}" for number in range(9))
QUIZ_FIELDS = {"question", "options", "answer", "correct", "wrong"}
QUIZ_APP = """
from core.quiz_renderer import render_quiz_items

render_quiz_items(
    [
        {
            "question": "Question one?",
            "options": ["A", "B", "C"],
            "answer": "A",
            "correct": "Correct one",
            "wrong": "Wrong one",
        },
        {
            "question": "Question two?",
            "options": ["D", "E", "F"],
            "answer": "E",
            "correct": "Correct two",
            "wrong": "Wrong two",
        },
    ],
    "test",
)
"""


def test_every_level_has_six_localized_quiz_questions() -> None:
    for lang in ("ko", "en"):
        for level in LEVELS:
            quiz = load_level_content(level, lang)["quiz"]

            assert len(quiz) == 6
            assert len({item["question"] for item in quiz}) == 6


def test_quiz_questions_have_valid_answers_and_feedback() -> None:
    for lang in ("ko", "en"):
        for level in LEVELS:
            for item in load_level_content(level, lang)["quiz"]:
                assert set(item) == QUIZ_FIELDS
                assert len(item["options"]) == 3
                assert len(set(item["options"])) == 3
                assert item["answer"] in item["options"]
                assert item["question"].strip()
                assert item["correct"].strip()
                assert item["wrong"].strip()


def test_quiz_controls_are_localized() -> None:
    for lang in ("ko", "en"):
        assert TRANSLATIONS[lang]["quiz_reset"]
        assert "{answered}" in TRANSLATIONS[lang]["quiz_progress"]
        assert "{total}" in TRANSLATIONS[lang]["quiz_progress"]
        assert "{correct}" in TRANSLATIONS[lang]["quiz_progress"]


def test_quiz_feedback_progress_and_reset_flow() -> None:
    app = AppTest.from_string(QUIZ_APP)
    app.run()

    assert len(app.radio) == 2
    assert app.get("progress")[0].value == 0

    app.radio[0].set_value("A")
    app.button[1].click().run()

    assert app.success[0].value == "Correct one"
    assert app.get("progress")[0].value == 50

    app.radio[0].set_value("B").run()

    assert len(app.success) == 0
    assert len(app.error) == 0
    assert app.get("progress")[0].value == 0

    app.button[0].click().run()

    assert app.radio[0].value is None
    assert app.get("progress")[0].value == 0
