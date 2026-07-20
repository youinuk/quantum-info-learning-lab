"""Shared qubit, basis, and operator-order conventions for the app."""

from __future__ import annotations


BASIS_BIT_ORDER = "big-endian"
OPERATOR_APPLICATION_ORDER = "right-to-left"


def basis_labels(qubit_count: int) -> tuple[str, ...]:
    """Return computational-basis labels in app display order.

    The app writes ``|q0 q1 ...>`` with q0 on the left as the most
    significant bit, so two-qubit labels are 00, 01, 10, 11.
    """
    if qubit_count < 1:
        raise ValueError("qubit_count must be at least 1")
    return tuple(format(index, f"0{qubit_count}b") for index in range(2**qubit_count))


def basis_index(bits: str) -> int:
    """Map an app-order basis label to its state-vector index."""
    if not bits or any(bit not in "01" for bit in bits):
        raise ValueError("bits must be a non-empty binary string")
    return int(bits, 2)


def operator_product_for_time_order(*gates: str) -> str:
    """Write chronological gates as an operator product acting on a ket.

    Circuit time runs left to right. Matrix products act on kets from right
    to left, so chronological X then Z is written ZX|psi>.
    """
    if any(not gate for gate in gates):
        raise ValueError("gate labels must be non-empty")
    return "I" if not gates else "".join(reversed(gates))
