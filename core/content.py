"""Content and resource loading helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from core.math_display import normalize_plain_notation

BASE_DIR = Path(__file__).resolve().parents[1]
RESOURCE_PATH = BASE_DIR / "content" / "resources.json"
LEVEL_CONTENT_PATH = BASE_DIR / "content" / "levels.json"
LESSON_DIR = BASE_DIR / "content" / "lessons"


def _load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_level_content(level: str, lang: str) -> Dict[str, Any]:
    localized_path = BASE_DIR / "content" / f"levels_{lang}.json"
    localized_data = _load_json(localized_path)
    content = localized_data.get(level)
    if content is not None:
        return normalize_plain_notation(content)

    data = _load_json(LEVEL_CONTENT_PATH)
    content = data.get(lang, {}).get(level)
    if content is None:
        content = data.get("ko", {}).get(level)
    if content is None:
        content = data.get("en", {}).get(level)
    return normalize_plain_notation(content or {})


def load_resources(level: str, lang: str) -> List[Dict[str, Any]]:
    data = _load_json(RESOURCE_PATH)
    resources = data.get(lang, {}).get(level)
    if resources is None and lang != "en":
        resources = data.get("en", {}).get(level)
    return resources or []


def level0_slides(lang: str) -> List[Dict[str, str]]:
    return load_level_content("level0", lang).get("slides", [])


def load_lesson_markdown(level: str, lang: str) -> str:
    path = LESSON_DIR / lang / f"{level}.md"
    if not path.exists() and lang != "en":
        path = LESSON_DIR / "en" / f"{level}.md"
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")
