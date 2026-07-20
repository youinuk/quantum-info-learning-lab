from pathlib import Path

import numpy as np
import pytest

from core.content import load_lesson_markdown
from core.quantum_conventions import (
    BASIS_BIT_ORDER,
    OPERATOR_APPLICATION_ORDER,
    basis_index,
    basis_labels,
    operator_product_for_time_order,
)


ROOT = Path(__file__).resolve().parents[1]


def test_app_uses_big_endian_basis_labels_and_indices() -> None:
    assert BASIS_BIT_ORDER == "big-endian"
    assert basis_labels(1) == ("0", "1")
    assert basis_labels(2) == ("00", "01", "10", "11")
    assert [basis_index(label) for label in basis_labels(2)] == [0, 1, 2, 3]


def test_operator_products_reverse_chronological_circuit_order() -> None:
    assert OPERATOR_APPLICATION_ORDER == "right-to-left"
    assert operator_product_for_time_order() == "I"
    assert operator_product_for_time_order("X") == "X"
    assert operator_product_for_time_order("X", "Z") == "ZX"
    assert operator_product_for_time_order("H", "Z", "H") == "HZH"


def test_invalid_basis_and_gate_inputs_are_rejected() -> None:
    with pytest.raises(ValueError):
        basis_labels(0)
    with pytest.raises(ValueError):
        basis_index("")
    with pytest.raises(ValueError):
        basis_index("02")
    with pytest.raises(ValueError):
        operator_product_for_time_order("X", "")


def test_lessons_explain_the_shared_ordering_conventions() -> None:
    for lang in ("ko", "en"):
        level5 = load_lesson_markdown("level5", lang)
        level8 = load_lesson_markdown("level8", lang)
        level13 = load_lesson_markdown("level13", lang)

        assert "big-endian" in level5
        assert r"ZX\lvert\psi\rangle" in level8
        assert "big-endian" in level8
        assert "big-endian" in level13


def test_sdk_boundary_conventions_are_documented() -> None:
    conventions = (ROOT / "docs" / "quantum_conventions.md").read_text(encoding="utf-8")

    assert "Qiskit" in conventions
    assert "Cirq" in conventions
    assert "basis_index(\"10\") == 2" in conventions
    assert "operator_product_for_time_order" in conventions


def test_teleportation_expansion_matches_four_bob_state_blocks() -> None:
    state = np.array([0.3 + 0.2j, -0.4 + 0.5j], dtype=complex)
    state = state / np.linalg.norm(state)
    bell_phi_plus = np.array([1.0, 0.0, 0.0, 1.0], dtype=complex) / np.sqrt(2)

    cnot_q_to_a = np.zeros((8, 8), dtype=complex)
    for q in (0, 1):
        for a in (0, 1):
            for b in (0, 1):
                input_index = basis_index(f"{q}{a}{b}")
                output_index = basis_index(f"{q}{a ^ q}{b}")
                cnot_q_to_a[output_index, input_index] = 1.0

    hadamard = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    identity = np.eye(2, dtype=complex)
    x_gate = np.array([[0, 1], [1, 0]], dtype=complex)
    z_gate = np.array([[1, 0], [0, -1]], dtype=complex)
    h_on_q = np.kron(np.kron(hadamard, identity), identity)

    expanded = h_on_q @ cnot_q_to_a @ np.kron(state, bell_phi_plus)
    grouped = np.concatenate(
        [state, x_gate @ state, z_gate @ state, x_gate @ z_gate @ state]
    ) / 2

    assert expanded == pytest.approx(grouped)


def test_bell_decoder_maps_bell_states_to_app_ordered_bits() -> None:
    hadamard = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    identity = np.eye(2, dtype=complex)
    cnot = np.array(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0],
        ],
        dtype=complex,
    )
    decoder = np.kron(hadamard, identity) @ cnot
    bell_states = (
        np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2),
        np.array([0, 1, 1, 0], dtype=complex) / np.sqrt(2),
        np.array([1, 0, 0, -1], dtype=complex) / np.sqrt(2),
        np.array([0, 1, -1, 0], dtype=complex) / np.sqrt(2),
    )

    for expected_index, bell_state in enumerate(bell_states):
        decoded = decoder @ bell_state
        expected = np.zeros(4, dtype=complex)
        expected[expected_index] = 1.0
        assert decoded == pytest.approx(expected)
