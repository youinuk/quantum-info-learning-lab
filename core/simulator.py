"""Small simulation functions used by the education app."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict

import numpy as np

from core.quantum_conventions import (
    basis_index,
    basis_labels,
    operator_product_for_time_order,
)


@dataclass(frozen=True)
class BitExperimentResult:
    shots: int
    probability_one: float
    count_zero: int
    count_one: int

    @property
    def observed_ratio_one(self) -> float:
        if self.shots == 0:
            return 0.0
        return self.count_one / self.shots

    def as_dict(self) -> Dict[str, int]:
        return {"0": self.count_zero, "1": self.count_one}


def simulate_bit_trials(probability_one: float, shots: int, seed: int | None = None) -> BitExperimentResult:
    """Simulate repeated measurements of a classical random bit.

    Args:
        probability_one: Probability that one trial returns 1. Must be between 0 and 1.
        shots: Number of repeated trials.
        seed: Optional random seed for reproducibility.

    Returns:
        BitExperimentResult with counts and observed ratio.
    """
    if not 0.0 <= probability_one <= 1.0:
        raise ValueError("probability_one must be between 0 and 1")
    if shots < 1:
        raise ValueError("shots must be at least 1")

    rng = np.random.default_rng(seed)
    samples = rng.random(shots) < probability_one
    count_one = int(np.sum(samples))
    count_zero = int(shots - count_one)
    return BitExperimentResult(
        shots=shots,
        probability_one=probability_one,
        count_zero=count_zero,
        count_one=count_one,
    )


@dataclass(frozen=True)
class QubitState:
    alpha: complex
    beta: complex

    @property
    def probability_zero(self) -> float:
        return float(abs(self.alpha) ** 2)

    @property
    def probability_one(self) -> float:
        return float(abs(self.beta) ** 2)

    def ket_text(self) -> str:
        return f"|ψ⟩ = {_format_amplitude(self.alpha)}|0⟩ + {_format_amplitude(self.beta)}|1⟩"


def _format_amplitude(value: complex) -> str:
    if abs(value.imag) < 1e-10:
        return f"{value.real:.3f}"
    if abs(value.real) < 1e-10:
        return f"{value.imag:.3f}i"
    sign = "+" if value.imag >= 0 else "-"
    return f"{value.real:.3f}{sign}{abs(value.imag):.3f}i"


def basis_state(label: str) -> QubitState:
    if label == "1":
        return QubitState(alpha=0 + 0j, beta=1 + 0j)
    return QubitState(alpha=1 + 0j, beta=0 + 0j)


def apply_single_qubit_gate(state: QubitState, gate: str) -> QubitState:
    alpha, beta = state.alpha, state.beta
    if gate == "X":
        return QubitState(alpha=beta, beta=alpha)
    if gate == "H":
        scale = 1 / np.sqrt(2)
        return QubitState(alpha=(alpha + beta) * scale, beta=(alpha - beta) * scale)
    if gate == "Z":
        return QubitState(alpha=alpha, beta=-beta)
    if gate == "S":
        return QubitState(alpha=alpha, beta=1j * beta)
    raise ValueError(f"Unsupported gate: {gate}")


@dataclass(frozen=True)
class TwoQubitDistribution:
    p00: float
    p01: float
    p10: float
    p11: float

    def labels(self) -> list[str]:
        return list(basis_labels(2))

    def probabilities(self) -> list[float]:
        return [self.p00, self.p01, self.p10, self.p11]


def independent_two_qubit_distribution(probability_first_one: float, probability_second_one: float) -> TwoQubitDistribution:
    if not 0.0 <= probability_first_one <= 1.0:
        raise ValueError("probability_first_one must be between 0 and 1")
    if not 0.0 <= probability_second_one <= 1.0:
        raise ValueError("probability_second_one must be between 0 and 1")

    p0_a = 1.0 - probability_first_one
    p1_a = probability_first_one
    p0_b = 1.0 - probability_second_one
    p1_b = probability_second_one
    return TwoQubitDistribution(
        p00=p0_a * p0_b,
        p01=p0_a * p1_b,
        p10=p1_a * p0_b,
        p11=p1_a * p1_b,
    )


@dataclass(frozen=True)
class TwoQubitGateResult:
    input_bits: str
    gate: str
    output_bits: str
    phase: int


def apply_two_qubit_basis_gate(input_bits: str, gate: str) -> TwoQubitGateResult:
    """Apply CNOT, CZ, or SWAP to one computational-basis input."""
    if input_bits not in basis_labels(2):
        raise ValueError("input_bits must be 00, 01, 10, or 11")
    if gate not in {"CNOT", "CZ", "SWAP"}:
        raise ValueError("gate must be CNOT, CZ, or SWAP")

    first, second = (int(bit) for bit in input_bits)
    phase = 1
    if gate == "CNOT":
        second ^= first
    elif gate == "CZ":
        phase = -1 if first == second == 1 else 1
    else:
        first, second = second, first

    return TwoQubitGateResult(
        input_bits=input_bits,
        gate=gate,
        output_bits=f"{first}{second}",
        phase=phase,
    )


@dataclass(frozen=True)
class BellMeasurementResult:
    shots: int
    count_00: int
    count_01: int
    count_10: int
    count_11: int

    def labels(self) -> list[str]:
        return list(basis_labels(2))

    def counts(self) -> list[int]:
        return [self.count_00, self.count_01, self.count_10, self.count_11]

    @property
    def same_result_ratio(self) -> float:
        if self.shots == 0:
            return 0.0
        return (self.count_00 + self.count_11) / self.shots


def simulate_bell_phi_plus_measurements(shots: int, seed: int | None = None) -> BellMeasurementResult:
    if shots < 1:
        raise ValueError("shots must be at least 1")

    rng = np.random.default_rng(seed)
    samples_are_11 = rng.random(shots) < 0.5
    count_11 = int(np.sum(samples_are_11))
    count_00 = int(shots - count_11)
    return BellMeasurementResult(
        shots=shots,
        count_00=count_00,
        count_01=0,
        count_10=0,
        count_11=count_11,
    )


@dataclass(frozen=True)
class CorrelationExperimentResult:
    state_kind: str
    shots: int
    z_counts: tuple[int, int, int, int]
    x_counts: tuple[int, int, int, int]
    z_probabilities: tuple[float, float, float, float]
    x_probabilities: tuple[float, float, float, float]

    def labels(self) -> list[str]:
        return list(basis_labels(2))

    def counts_for(self, basis: str) -> tuple[int, int, int, int]:
        return self.x_counts if basis.upper() == "X" else self.z_counts

    def same_result_ratio(self, basis: str) -> float:
        counts = self.counts_for(basis)
        return (counts[0] + counts[3]) / self.shots


def _two_qubit_density_matrix(state_kind: str) -> np.ndarray:
    if state_kind == "product_plus":
        state = np.ones(4, dtype=complex) / 2
        return np.outer(state, state.conj())
    if state_kind == "classical_correlated":
        return np.diag([0.5, 0.0, 0.0, 0.5]).astype(complex)
    if state_kind == "bell_phi_plus":
        state = np.array([1 / np.sqrt(2), 0.0, 0.0, 1 / np.sqrt(2)], dtype=complex)
        return np.outer(state, state.conj())
    raise ValueError(f"Unsupported two-qubit state: {state_kind}")


def _measurement_probabilities(density_matrix: np.ndarray, basis: str) -> np.ndarray:
    if basis.upper() == "X":
        hadamard = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
        basis_change = np.kron(hadamard, hadamard)
        probabilities = []
        for outcome in range(4):
            probability = 0j
            for row in range(4):
                for column in range(4):
                    probability += (
                        basis_change[outcome, row]
                        * density_matrix[row, column]
                        * basis_change[outcome, column].conjugate()
                    )
            probabilities.append(probability.real)
        probabilities = np.array(probabilities)
    elif basis.upper() != "Z":
        raise ValueError(f"Unsupported measurement basis: {basis}")
    else:
        probabilities = np.real(np.diag(density_matrix))
    probabilities = np.clip(probabilities, 0.0, 1.0)
    return probabilities / probabilities.sum()


def simulate_two_basis_correlations(
    state_kind: str,
    shots: int,
    seed: int | None = None,
) -> CorrelationExperimentResult:
    if shots < 1:
        raise ValueError("shots must be at least 1")

    density_matrix = _two_qubit_density_matrix(state_kind)
    z_probabilities = _measurement_probabilities(density_matrix, "Z")
    x_probabilities = _measurement_probabilities(density_matrix, "X")
    rng = np.random.default_rng(seed)
    z_counts = rng.multinomial(shots, z_probabilities)
    x_counts = rng.multinomial(shots, x_probabilities)

    return CorrelationExperimentResult(
        state_kind=state_kind,
        shots=shots,
        z_counts=tuple(int(value) for value in z_counts),
        x_counts=tuple(int(value) for value in x_counts),
        z_probabilities=tuple(float(value) for value in z_probabilities),
        x_probabilities=tuple(float(value) for value in x_probabilities),
    )


@dataclass(frozen=True)
class DeutschExperimentResult:
    oracle_name: str
    f0: int
    f1: int
    classification: str
    measurement: str
    query_count: int
    prepared_probabilities: tuple[float, float]
    after_oracle_probabilities: tuple[float, float]
    final_probabilities: tuple[float, float]
    phase_markers: tuple[str, str]


def _first_qubit_probabilities(state: np.ndarray) -> tuple[float, float]:
    amplitudes_by_first_qubit = state.reshape(2, -1)
    probability_zero = float(np.sum(np.abs(amplitudes_by_first_qubit[0]) ** 2))
    probability_one = float(np.sum(np.abs(amplitudes_by_first_qubit[1]) ** 2))
    return probability_zero, probability_one


def _deutsch_oracle_matrix(f0: int, f1: int) -> np.ndarray:
    oracle = np.zeros((4, 4), dtype=complex)
    for x, fx in enumerate((f0, f1)):
        for y in (0, 1):
            input_index = basis_index(f"{x}{y}")
            output_index = basis_index(f"{x}{y ^ fx}")
            oracle[output_index, input_index] = 1.0
    return oracle


def run_deutsch_one_bit(oracle_name: str) -> DeutschExperimentResult:
    tables = {
        "constant_zero": (0, 0),
        "constant_one": (1, 1),
        "balanced_identity": (0, 1),
        "balanced_flip": (1, 0),
    }
    if oracle_name not in tables:
        raise ValueError(f"Unsupported oracle: {oracle_name}")

    f0, f1 = tables[oracle_name]

    hadamard = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    identity = np.eye(2, dtype=complex)

    # Standard two-qubit Deutsch circuit: |0>|1>, H on both, one oracle
    # query, then H and measurement on the first qubit.
    initial_state = np.zeros(4, dtype=complex)
    initial_state[basis_index("01")] = 1.0
    prepared_state = np.kron(hadamard, hadamard) @ initial_state
    after_oracle_state = _deutsch_oracle_matrix(f0, f1) @ prepared_state
    final_state = np.kron(hadamard, identity) @ after_oracle_state

    prepared_probabilities = _first_qubit_probabilities(prepared_state)
    after_oracle_probabilities = _first_qubit_probabilities(after_oracle_state)
    final_probabilities = _first_qubit_probabilities(final_state)
    measurement = "0" if final_probabilities[0] > final_probabilities[1] else "1"
    classification = "constant" if measurement == "0" else "balanced"
    return DeutschExperimentResult(
        oracle_name=oracle_name,
        f0=f0,
        f1=f1,
        classification=classification,
        measurement=measurement,
        query_count=1,
        prepared_probabilities=prepared_probabilities,
        after_oracle_probabilities=after_oracle_probabilities,
        final_probabilities=final_probabilities,
        phase_markers=("+" if f0 == 0 else "-", "+" if f1 == 0 else "-"),
    )


@dataclass(frozen=True)
class NoisyMeasurementResult:
    shots: int
    ideal_count_zero: int
    ideal_count_one: int
    noisy_count_zero: int
    noisy_count_one: int
    noise_rate: float

    @property
    def noisy_ratio_one(self) -> float:
        if self.shots == 0:
            return 0.0
        return self.noisy_count_one / self.shots


def simulate_noisy_bit_measurements(
    probability_one: float,
    noise_rate: float,
    shots: int,
    seed: int | None = None,
) -> NoisyMeasurementResult:
    if not 0.0 <= probability_one <= 1.0:
        raise ValueError("probability_one must be between 0 and 1")
    if not 0.0 <= noise_rate <= 1.0:
        raise ValueError("noise_rate must be between 0 and 1")
    if shots < 1:
        raise ValueError("shots must be at least 1")

    rng = np.random.default_rng(seed)
    ideal = rng.random(shots) < probability_one
    flips = rng.random(shots) < noise_rate
    noisy = np.logical_xor(ideal, flips)
    ideal_count_one = int(np.sum(ideal))
    noisy_count_one = int(np.sum(noisy))
    return NoisyMeasurementResult(
        shots=shots,
        ideal_count_zero=shots - ideal_count_one,
        ideal_count_one=ideal_count_one,
        noisy_count_zero=shots - noisy_count_one,
        noisy_count_one=noisy_count_one,
        noise_rate=noise_rate,
    )


@dataclass(frozen=True)
class CircuitReadoutResult:
    circuit_id: str
    shots: int
    labels: tuple[str, ...]
    probabilities: tuple[float, ...]
    counts: tuple[int, ...]
    state_latex: str


def simulate_named_circuit(
    circuit_id: str,
    shots: int,
    seed: int | None = None,
) -> CircuitReadoutResult:
    if shots < 1:
        raise ValueError("shots must be at least 1")

    circuits: dict[str, tuple[tuple[str, ...], tuple[float, ...], str]] = {
        "x_gate": (
            ("0", "1"),
            (0.0, 1.0),
            r"\lvert 1 \rangle",
        ),
        "h_gate": (
            ("0", "1"),
            (0.5, 0.5),
            rf"\frac{{1}}{{\sqrt{{2}}}}\lvert 0 \rangle + \frac{{1}}{{\sqrt{{2}}}}\lvert 1 \rangle",
        ),
        "h_then_z": (
            ("0", "1"),
            (0.5, 0.5),
            rf"\frac{{1}}{{\sqrt{{2}}}}\lvert 0 \rangle - \frac{{1}}{{\sqrt{{2}}}}\lvert 1 \rangle",
        ),
        "bell_pair": (
            basis_labels(2),
            (0.5, 0.0, 0.0, 0.5),
            rf"\frac{{1}}{{\sqrt{{2}}}}\lvert 00 \rangle + \frac{{1}}{{\sqrt{{2}}}}\lvert 11 \rangle",
        ),
    }
    if circuit_id not in circuits:
        raise ValueError(f"Unsupported circuit: {circuit_id}")

    labels, probabilities, state_latex = circuits[circuit_id]
    probability_array = np.array(probabilities, dtype=float)
    probability_array = probability_array / probability_array.sum()
    rng = np.random.default_rng(seed)
    counts = tuple(int(value) for value in rng.multinomial(shots, probability_array))
    return CircuitReadoutResult(
        circuit_id=circuit_id,
        shots=shots,
        labels=labels,
        probabilities=tuple(float(value) for value in probability_array),
        counts=counts,
        state_latex=state_latex,
    )


@dataclass(frozen=True)
class MeasurementSeriesRow:
    shots: int
    ideal_count_zero: int
    ideal_count_one: int
    noisy_count_zero: int
    noisy_count_one: int
    batch_count: int
    ideal_ratio_mean: float
    ideal_ratio_min: float
    ideal_ratio_max: float
    noisy_ratio_mean: float
    noisy_ratio_min: float
    noisy_ratio_max: float

    @property
    def ideal_ratio_one(self) -> float:
        return self.ideal_count_one / self.shots

    @property
    def noisy_ratio_one(self) -> float:
        return self.noisy_count_one / self.shots


@dataclass(frozen=True)
class MeasurementSeriesResult:
    probability_one: float
    noise_rate: float
    rows: tuple[MeasurementSeriesRow, ...]


def simulate_measurement_series(
    probability_one: float,
    noise_rate: float,
    shot_counts: tuple[int, ...],
    batch_count: int = 30,
    seed: int | None = None,
) -> MeasurementSeriesResult:
    if not 0.0 <= probability_one <= 1.0:
        raise ValueError("probability_one must be between 0 and 1")
    if not 0.0 <= noise_rate <= 1.0:
        raise ValueError("noise_rate must be between 0 and 1")
    if not shot_counts:
        raise ValueError("shot_counts must not be empty")
    if any(shots < 1 for shots in shot_counts):
        raise ValueError("each shot count must be at least 1")
    if batch_count < 1:
        raise ValueError("batch_count must be at least 1")

    rows: list[MeasurementSeriesRow] = []
    rng = np.random.default_rng(seed)
    for index, shots in enumerate(shot_counts):
        ideal = rng.random((batch_count, shots)) < probability_one
        flips = rng.random((batch_count, shots)) < noise_rate
        noisy = np.logical_xor(ideal, flips)
        ideal_counts_one = np.sum(ideal, axis=1)
        noisy_counts_one = np.sum(noisy, axis=1)
        ideal_ratios = ideal_counts_one / shots
        noisy_ratios = noisy_counts_one / shots
        ideal_count_one = int(ideal_counts_one[0])
        noisy_count_one = int(noisy_counts_one[0])
        rows.append(
            MeasurementSeriesRow(
                shots=shots,
                ideal_count_zero=shots - ideal_count_one,
                ideal_count_one=ideal_count_one,
                noisy_count_zero=shots - noisy_count_one,
                noisy_count_one=noisy_count_one,
                batch_count=batch_count,
                ideal_ratio_mean=float(np.mean(ideal_ratios)),
                ideal_ratio_min=float(np.min(ideal_ratios)),
                ideal_ratio_max=float(np.max(ideal_ratios)),
                noisy_ratio_mean=float(np.mean(noisy_ratios)),
                noisy_ratio_min=float(np.min(noisy_ratios)),
                noisy_ratio_max=float(np.max(noisy_ratios)),
            )
        )
    return MeasurementSeriesResult(
        probability_one=probability_one,
        noise_rate=noise_rate,
        rows=tuple(rows),
    )


@dataclass(frozen=True)
class PhaseInterferenceResult:
    phase_turns: float
    phase_degrees: float
    probability_bright: float
    probability_dark: float
    count_bright: int
    count_dark: int
    shots: int


def simulate_phase_interference(
    phase_turns: float,
    shots: int,
    seed: int | None = None,
) -> PhaseInterferenceResult:
    if shots < 1:
        raise ValueError("shots must be at least 1")

    phase_radians = 2 * np.pi * phase_turns
    probability_bright = float((1 + np.cos(phase_radians)) / 2)
    probability_bright = min(1.0, max(0.0, probability_bright))
    probability_dark = 1.0 - probability_bright
    rng = np.random.default_rng(seed)
    count_bright, count_dark = (int(value) for value in rng.multinomial(shots, [probability_bright, probability_dark]))

    return PhaseInterferenceResult(
        phase_turns=phase_turns,
        phase_degrees=phase_turns * 360,
        probability_bright=probability_bright,
        probability_dark=probability_dark,
        count_bright=count_bright,
        count_dark=count_dark,
        shots=shots,
    )


@dataclass(frozen=True)
class EntanglementLimitResult:
    alice_basis: str
    bob_basis: str
    shots: int
    count_00: int
    count_01: int
    count_10: int
    count_11: int

    def labels(self) -> list[str]:
        return list(basis_labels(2))

    def pair_counts(self) -> list[int]:
        return [self.count_00, self.count_01, self.count_10, self.count_11]

    @property
    def bob_count_zero(self) -> int:
        return self.count_00 + self.count_10

    @property
    def bob_count_one(self) -> int:
        return self.count_01 + self.count_11

    @property
    def bob_zero_ratio(self) -> float:
        return self.bob_count_zero / self.shots

    @property
    def same_count(self) -> int:
        return self.count_00 + self.count_11

    @property
    def different_count(self) -> int:
        return self.count_01 + self.count_10

    @property
    def same_ratio(self) -> float:
        return self.same_count / self.shots


def simulate_entanglement_limit(
    alice_basis: str,
    bob_basis: str,
    shots: int,
    seed: int | None = None,
) -> EntanglementLimitResult:
    if alice_basis not in {"Z", "X"}:
        raise ValueError("alice_basis must be Z or X")
    if bob_basis not in {"Z", "X"}:
        raise ValueError("bob_basis must be Z or X")
    if shots < 1:
        raise ValueError("shots must be at least 1")

    probabilities = np.array([0.5, 0.0, 0.0, 0.5]) if alice_basis == bob_basis else np.array([0.25, 0.25, 0.25, 0.25])
    rng = np.random.default_rng(seed)
    counts = rng.multinomial(shots, probabilities)
    return EntanglementLimitResult(
        alice_basis=alice_basis,
        bob_basis=bob_basis,
        shots=shots,
        count_00=int(counts[0]),
        count_01=int(counts[1]),
        count_10=int(counts[2]),
        count_11=int(counts[3]),
    )


TELEPORTATION_STATES: dict[str, np.ndarray] = {
    "zero": np.array([1.0, 0.0], dtype=complex),
    "one": np.array([0.0, 1.0], dtype=complex),
    "plus": np.array([1.0, 1.0], dtype=complex) / np.sqrt(2),
    "minus": np.array([1.0, -1.0], dtype=complex) / np.sqrt(2),
    "plus_i": np.array([1.0, 1.0j], dtype=complex) / np.sqrt(2),
    "minus_i": np.array([1.0, -1.0j], dtype=complex) / np.sqrt(2),
}


@dataclass(frozen=True)
class TeleportationResult:
    input_state: str
    input_amplitudes: tuple[complex, complex]
    alice_bit_zero: int
    alice_bit_one: int
    bob_state_before: tuple[complex, complex]
    correction_gates: tuple[str, ...]
    bob_state_after: tuple[complex, complex]
    fidelity: float

    @property
    def alice_bits(self) -> str:
        return f"{self.alice_bit_zero}{self.alice_bit_one}"

    @property
    def correction_label(self) -> str:
        return operator_product_for_time_order(*self.correction_gates)


@dataclass(frozen=True)
class TeleportationCorrectionAttempt:
    selected_correction: str
    output_amplitudes: tuple[complex, complex]
    fidelity: float
    matches_protocol_correction: bool


def apply_teleportation_correction(
    result: TeleportationResult,
    selected_correction: str,
) -> TeleportationCorrectionAttempt:
    """Apply a learner-selected correction to Bob's pre-correction state."""
    identity = np.eye(2, dtype=complex)
    x_gate = np.array([[0, 1], [1, 0]], dtype=complex)
    z_gate = np.array([[1, 0], [0, -1]], dtype=complex)
    operators = {
        "I": identity,
        "X": x_gate,
        "Z": z_gate,
        "ZX": z_gate @ x_gate,
    }
    if selected_correction not in operators:
        raise ValueError("selected_correction must be I, X, Z, or ZX")

    bob_before = np.asarray(result.bob_state_before, dtype=complex)
    input_state = np.asarray(result.input_amplitudes, dtype=complex)
    output = operators[selected_correction] @ bob_before
    fidelity = float(abs(np.vdot(input_state, output)) ** 2)
    return TeleportationCorrectionAttempt(
        selected_correction=selected_correction,
        output_amplitudes=tuple(complex(value) for value in output),
        fidelity=fidelity,
        matches_protocol_correction=selected_correction == result.correction_label,
    )


def simulate_quantum_teleportation(
    input_state: str,
    seed: int | None = None,
    amplitudes: tuple[complex, complex] | None = None,
) -> TeleportationResult:
    """Simulate one ideal teleportation run through Alice's random Bell outcome."""
    if input_state == "custom":
        if amplitudes is None or len(amplitudes) != 2:
            raise ValueError("custom input requires alpha and beta amplitudes")
        state = np.asarray(amplitudes, dtype=complex)
        if not np.all(np.isfinite(state)):
            raise ValueError("custom amplitudes must be finite")
        norm = float(np.linalg.norm(state))
        if norm < 1e-12:
            raise ValueError("custom amplitudes cannot both be zero")
        state = state / norm
    elif input_state not in TELEPORTATION_STATES:
        raise ValueError(f"Unsupported teleportation input state: {input_state}")
    else:
        if amplitudes is not None:
            raise ValueError("amplitudes are only accepted for the custom input state")
        state = TELEPORTATION_STATES[input_state]

    identity = np.eye(2, dtype=complex)
    x_gate = np.array([[0, 1], [1, 0]], dtype=complex)
    z_gate = np.array([[1, 0], [0, -1]], dtype=complex)

    rng = np.random.default_rng(seed)
    outcome = int(rng.integers(0, 4))
    alice_bit_zero = (outcome >> 1) & 1
    alice_bit_one = outcome & 1

    x_power = x_gate if alice_bit_one else identity
    z_power = z_gate if alice_bit_zero else identity
    bob_before = x_power @ z_power @ state

    corrections: list[str] = []
    bob_after = bob_before
    if alice_bit_one:
        bob_after = x_gate @ bob_after
        corrections.append("X")
    if alice_bit_zero:
        bob_after = z_gate @ bob_after
        corrections.append("Z")

    fidelity = float(abs(np.vdot(state, bob_after)) ** 2)
    return TeleportationResult(
        input_state=input_state,
        input_amplitudes=tuple(complex(value) for value in state),
        alice_bit_zero=alice_bit_zero,
        alice_bit_one=alice_bit_one,
        bob_state_before=tuple(complex(value) for value in bob_before),
        correction_gates=tuple(corrections),
        bob_state_after=tuple(complex(value) for value in bob_after),
        fidelity=fidelity,
    )


@dataclass(frozen=True)
class SuperdenseEncodingResult:
    encoding_gate: str
    bell_state: str
    transmitted_qubits: int
    decoded_bits: str


SUPERDENSE_ENCODINGS = {
    "00": ("I", "phi_plus"),
    "01": ("X", "psi_plus"),
    "10": ("Z", "phi_minus"),
    "11": (operator_product_for_time_order("X", "Z"), "psi_minus"),
}


def explore_superdense_encoding(encoding_gate: str) -> SuperdenseEncodingResult:
    """Return the Bell state and decoded bits produced by one encoding gate."""
    gate_to_result = {
        gate: (decoded_bits, bell_state)
        for decoded_bits, (gate, bell_state) in SUPERDENSE_ENCODINGS.items()
    }
    if encoding_gate not in gate_to_result:
        raise ValueError("encoding_gate must be I, X, Z, or ZX")

    decoded_bits, bell_state = gate_to_result[encoding_gate]
    return SuperdenseEncodingResult(
        encoding_gate=encoding_gate,
        bell_state=bell_state,
        transmitted_qubits=1,
        decoded_bits=decoded_bits,
    )


def generate_superdense_mission(seed: int, previous_bits: str | None = None) -> str:
    """Choose a reproducible two-bit mission, avoiding an immediate repeat."""
    if previous_bits is not None and previous_bits not in SUPERDENSE_ENCODINGS:
        raise ValueError("previous_bits must be one of 00, 01, 10, or 11")
    options = [bits for bits in SUPERDENSE_ENCODINGS if bits != previous_bits]
    return random.Random(seed).choice(options)


@dataclass(frozen=True)
class SuperdenseCodingResult:
    message_bits: str
    encoding_gate: str
    bell_state: str
    transmitted_qubits: int
    decoded_bits: str

    @property
    def success(self) -> bool:
        return self.message_bits == self.decoded_bits


def simulate_superdense_coding(
    message_bits: str,
    encoding_gate: str | None = None,
) -> SuperdenseCodingResult:
    """Decode a selected gate, defaulting to the correct gate for the message."""
    if message_bits not in SUPERDENSE_ENCODINGS:
        raise ValueError("message_bits must be one of 00, 01, 10, or 11")

    if encoding_gate is None:
        encoding_gate = SUPERDENSE_ENCODINGS[message_bits][0]

    encoding = explore_superdense_encoding(encoding_gate)
    return SuperdenseCodingResult(
        message_bits=message_bits,
        encoding_gate=encoding.encoding_gate,
        bell_state=encoding.bell_state,
        transmitted_qubits=encoding.transmitted_qubits,
        decoded_bits=encoding.decoded_bits,
    )
