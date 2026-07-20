import re
from pathlib import Path

from core.i18n import DEFAULT_LANG, LANG_OPTIONS, normalize_lang


ROOT = Path(__file__).resolve().parents[1]
HANGUL = re.compile(r"[가-힣]")
EXPECTED_CARD_COUNTS = [4, 7, 5, 6, 6, 7, 8, 6, 5, 5, 5, 8, 5, 8]
IMAGE_PATTERN = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def test_app_defaults_to_english_without_removing_korean() -> None:
    assert DEFAULT_LANG == "en"
    assert list(LANG_OPTIONS.values()) == ["en", "ko"]
    assert normalize_lang(None) == "en"
    assert normalize_lang("unknown") == "en"
    assert normalize_lang("ko") == "ko"


def test_korean_and_english_lessons_have_matching_card_counts():
    for level, expected_count in enumerate(EXPECTED_CARD_COUNTS):
        korean = (ROOT / "content" / "lessons" / "ko" / f"level{level}.md").read_text(encoding="utf-8")
        english = (ROOT / "content" / "lessons" / "en" / f"level{level}.md").read_text(encoding="utf-8")

        assert len(re.findall(r"^## ", korean, flags=re.MULTILINE)) == expected_count
        assert len(re.findall(r"^## ", english, flags=re.MULTILINE)) == expected_count
        assert not HANGUL.search(english)


def test_every_lesson_image_reference_exists():
    for lesson_path in (ROOT / "content" / "lessons").rglob("*.md"):
        lesson = lesson_path.read_text(encoding="utf-8")
        for image_path in IMAGE_PATTERN.findall(lesson):
            assert (ROOT / image_path).is_file(), f"Missing image referenced by {lesson_path}: {image_path}"


def test_korean_and_english_lessons_use_the_same_images():
    for level in range(14):
        korean = (ROOT / "content" / "lessons" / "ko" / f"level{level}.md").read_text(encoding="utf-8")
        english = (ROOT / "content" / "lessons" / "en" / f"level{level}.md").read_text(encoding="utf-8")

        assert IMAGE_PATTERN.findall(korean) == IMAGE_PATTERN.findall(english)


def test_english_structured_content_contains_no_hangul():
    english_content = (ROOT / "content" / "levels_en.json").read_text(encoding="utf-8")
    assert not HANGUL.search(english_content)
