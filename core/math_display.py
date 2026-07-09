"""Small helpers for learner-facing probability and ket text."""

from __future__ import annotations

import re
from typing import Any


PLAIN_KET_REPLACEMENTS = {
    "|Phi+>": "|Φ+⟩",
    "|Phi->": "|Φ-⟩",
    "|psi>": "|ψ⟩",
    "|00>": "|00⟩",
    "|01>": "|01⟩",
    "|10>": "|10⟩",
    "|11>": "|11⟩",
    "|+>": "|+⟩",
    "|->": "|-⟩",
    "|0>": "|0⟩",
    "|1>": "|1⟩",
}
INLINE_KET_PATTERN = re.compile(r"`\|(?P<label>[^`>]+)>`")


def normalize_plain_notation(value: Any) -> Any:
    """Use readable ket glyphs in widgets, tables, and other plain text."""
    if isinstance(value, dict):
        return {key: normalize_plain_notation(item) for key, item in value.items()}
    if isinstance(value, list):
        return [normalize_plain_notation(item) for item in value]
    if not isinstance(value, str):
        return value

    for source, target in PLAIN_KET_REPLACEMENTS.items():
        value = value.replace(source, target)
    return value


def inline_kets_to_latex(markdown: str) -> str:
    """Render backticked ket notation as inline LaTeX in lesson prose."""
    def replace(match: re.Match[str]) -> str:
        label = match.group("label").replace("Phi", r"\Phi").replace("psi", r"\psi")
        return rf"$\lvert {label} \rangle$"

    return INLINE_KET_PATTERN.sub(replace, markdown)

PROBABILITY_OPTIONS = {
    "0": 0.0,
    "1/4": 0.25,
    "1/2": 0.5,
    "3/4": 0.75,
    "1": 1.0,
}

AMPLITUDE_BY_PROBABILITY = {
    0.0: ("1", "0"),
    0.25: (r"\frac{\sqrt{3}}{2}", r"\frac{1}{2}"),
    0.5: (r"\frac{1}{\sqrt{2}}", r"\frac{1}{\sqrt{2}}"),
    0.75: (r"\frac{1}{2}", r"\frac{\sqrt{3}}{2}"),
    1.0: ("0", "1"),
}

PROBABILITY_TEXT = {
    0.0: "0",
    0.25: r"\frac{1}{4}",
    0.5: r"\frac{1}{2}",
    0.75: r"\frac{3}{4}",
    1.0: "1",
}

PROBABILITY_PLAIN_TEXT = {
    0.0: "0",
    0.25: "1/4",
    0.5: "1/2",
    0.75: "3/4",
    1.0: "1",
}


def probability_select_options() -> list[str]:
    return list(PROBABILITY_OPTIONS.keys())


def probability_from_label(label: str) -> float:
    return PROBABILITY_OPTIONS[label]


def probability_latex(value: float) -> str:
    return PROBABILITY_TEXT.get(value, f"{value:.2f}")


def probability_plain(value: float) -> str:
    return PROBABILITY_PLAIN_TEXT.get(value, f"{value:.2f}")


def single_qubit_latex(probability_one: float) -> str:
    alpha, beta = AMPLITUDE_BY_PROBABILITY.get(probability_one, ("?", "?"))
    if probability_one == 0.0:
        return r"\lvert\psi\rangle = \lvert0\rangle"
    if probability_one == 1.0:
        return r"\lvert\psi\rangle = \lvert1\rangle"
    return rf"\lvert\psi\rangle = {alpha}\lvert0\rangle + {beta}\lvert1\rangle"


def two_qubit_probability_text(value: float) -> str:
    if value in PROBABILITY_PLAIN_TEXT:
        return PROBABILITY_PLAIN_TEXT[value]
    return f"{value:.3f}"


def _amplitude_latex(value: complex) -> str:
    real = value.real
    if abs(real) < 1e-10:
        return ""
    sign = "-" if real < 0 else "+"
    magnitude = abs(real)
    if abs(magnitude - 1.0) < 1e-10:
        body = ""
    elif abs(magnitude - 1 / 2**0.5) < 1e-10:
        body = r"\frac{1}{\sqrt{2}}"
    elif abs(magnitude - 0.5) < 1e-10:
        body = r"\frac{1}{2}"
    else:
        body = f"{magnitude:.3f}"
    return f"{sign}{body}"


def qubit_state_latex(alpha: complex, beta: complex) -> str:
    terms: list[str] = []
    for amplitude, ket in [(alpha, r"\lvert0\rangle"), (beta, r"\lvert1\rangle")]:
        text = _amplitude_latex(amplitude)
        if not text:
            continue
        sign = "-" if text.startswith("-") else "+"
        body = text[1:]
        terms.append((sign, body, ket))

    if not terms:
        return r"\lvert\psi\rangle = 0"

    expression = ""
    for index, (sign, body, ket) in enumerate(terms):
        prefix = "-" if index == 0 and sign == "-" else ("" if index == 0 else f" {sign} ")
        expression += f"{prefix}{body}{ket}"
    return rf"\lvert\psi\rangle = {expression}"
