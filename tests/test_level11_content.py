import re

from core.content import load_lesson_markdown, load_level_content


ORACLE_IDS = {
    "constant_zero",
    "constant_one",
    "balanced_identity",
    "balanced_flip",
}


def test_level11_localized_content_has_matching_learning_structure():
    for lang in ("ko", "en"):
        content = load_level_content("level11", lang)
        option_ids = {item["id"] for item in content["oracle_options"]}
        lesson = load_lesson_markdown("level11", lang)

        assert option_ids == ORACLE_IDS
        assert len(content["quiz"]) == 6
        assert len(content["terms"]) == 6
        assert len(content["truth_table"]) == 4
        assert len(content["simulation_steps"]) == 4
        assert content["simulation_diagram"] == "assets/images/level11_deutsch_circuit.svg"
        assert len(re.findall(r"^## ", lesson, flags=re.MULTILINE)) == 8
        assert "assets/images/deutsch_algorithm.svg" in lesson
        assert r"(-1)^{f(x)}" in lesson
        assert r"\lvert0\oplus f(x)\rangle" in lesson
        assert r"\lvert0\oplus0\rangle" in lesson
        assert r"\lvert0\oplus1\rangle" in lesson
        assert r"X^0=I" in lesson
        assert r"X^1=X" in lesson
        assert r"X^{f(x)}\lvert-\rangle_2" in lesson
        assert r"(-1)^{f(0)}\lvert0\rangle_1" in lesson
        assert r"=\lvert+\rangle_1\otimes\lvert-\rangle_2" in lesson
        assert r"(-1)^1\lvert0\rangle+(-1)^1\lvert1\rangle" in lesson
        assert lesson.count(":::expander") == 2
        assert "(선택)" not in lesson
        assert "(optional)" not in lesson
        if lang == "ko":
            assert "오라클의 함수값이 첫 큐비트의 위상 표식이 되는 과정을 수식으로 확인하기" in lesson
            assert "같은 위상 표식은 0, 반대 위상 표식은 1이 되는 과정을 수식으로 확인하기" in lesson
            assert "기저 상태 항" in lesson
            assert "`x` 가지" not in lesson
        else:
            assert "how this sign becomes a phase marker on the first qubit" in lesson
            assert "why matching markers give 0 and opposite markers give 1" in lesson
            assert "basis-state term" in lesson
            assert " branch" not in lesson.lower()
        assert "상태 항 전체에 곱해진 수" in lesson or "corresponding two-qubit state term" in lesson
        assert not any(character in lesson for character in ("\x0b", "\x0c", "\x0e", "\x0f"))
