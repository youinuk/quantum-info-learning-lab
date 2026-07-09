"""Small simulation functions used by the education app."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import numpy as np


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
    raise ValueError(f"Unsupported gate: {gate}")


@dataclass(frozen=True)
class TwoQubitDistribution:
    p00: float
    p01: float
    p10: float
    p11: float

    def labels(self) -> list[str]:
        return ["00", "01", "10", "11"]

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
class BellMeasurementResult:
    shots: int
    count_00: int
    count_01: int
    count_10: int
    count_11: int

    def labels(self) -> list[str]:
        return ["00", "01", "10", "11"]

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
        return ["00", "01", "10", "11"]

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
    probability_zero = float(np.sum(np.abs(state[:2]) ** 2))
    probability_one = float(np.sum(np.abs(state[2:]) ** 2))
    return probability_zero, probability_one


def _deutsch_oracle_matrix(f0: int, f1: int) -> np.ndarray:
    oracle = np.zeros((4, 4), dtype=complex)
    for x, fx in enumerate((f0, f1)):
        for y in (0, 1):
            input_index = 2 * x + y
            output_index = 2 * x + (y ^ fx)
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
    initial_state[1] = 1.0
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
