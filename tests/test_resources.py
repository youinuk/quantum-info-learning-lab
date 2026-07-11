import json
from pathlib import Path
from urllib.parse import parse_qs, urlparse


ROOT = Path(__file__).resolve().parents[1]
RESOURCE_PATH = ROOT / "content" / "resources.json"
LEVELS = tuple(f"level{number}" for number in range(13))
LINK_TYPES = {"link", "article_link", "simulation_link", "video_link"}


def load_resource_data() -> dict:
    return json.loads(RESOURCE_PATH.read_text(encoding="utf-8"))


def test_each_language_has_the_same_resource_structure() -> None:
    data = load_resource_data()

    for level in LEVELS:
        korean = data["ko"][level]
        english = data["en"][level]

        assert len(korean) >= 3
        assert len(korean) == len(english)
        assert [item["type"] for item in korean] == [item["type"] for item in english]


def test_external_resources_use_valid_https_links() -> None:
    data = load_resource_data()

    for lang in ("ko", "en"):
        for level in LEVELS:
            for item in data[lang][level]:
                assert item["type"] in LINK_TYPES
                parsed = urlparse(item["url"])
                assert parsed.scheme == "https"
                assert parsed.netloc
                assert item["title"] != item["url"]


def test_video_resources_link_to_content_instead_of_search_results() -> None:
    data = load_resource_data()

    for lang in ("ko", "en"):
        for level in LEVELS:
            for item in data[lang][level]:
                if item["type"] != "video_link":
                    continue

                parsed = urlparse(item["url"])
                query = parse_qs(parsed.query)
                assert parsed.path not in {"/results", "/search"}
                assert "search_query" not in query

                if parsed.netloc in {"youtube.com", "www.youtube.com"}:
                    assert parsed.path == "/watch"
                    assert query.get("v", [""])[0]
