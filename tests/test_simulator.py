import pytest

from core.simulator import (
    apply_single_qubit_gate,
    apply_two_qubit_basis_gate,
    apply_teleportation_correction,
    basis_state,
    explore_superdense_encoding,
    generate_superdense_mission,
    run_deutsch_one_bit,
    simulate_bell_phi_plus_measurements,
    simulate_bit_trials,
    simulate_entanglement_limit,
    simulate_measurement_series,
    simulate_named_circuit,
    simulate_noisy_bit_measurements,
    simulate_phase_interference,
    simulate_quantum_teleportation,
    simulate_superdense_coding,
    simulate_two_basis_correlations,
)


@pytest.mark.parametrize(
    ("input_bits", "gate", "output_bits", "phase"),
    (
        ("10", "CNOT", "11", 1),
        ("01", "CNOT", "01", 1),
        ("11", "CZ", "11", -1),
        ("10", "CZ", "10", 1),
        ("01", "SWAP", "10", 1),
    ),
)
def test_two_qubit_basis_gate_experiment(input_bits, gate, output_bits, phase):
    result = apply_two_qubit_basis_gate(input_bits, gate)

    assert result.output_bits == output_bits
    assert result.phase == phase


def test_two_qubit_basis_gate_rejects_unknown_inputs():
    with pytest.raises(ValueError):
        apply_two_qubit_basis_gate("12", "CNOT")
    with pytest.raises(ValueError):
        apply_two_qubit_basis_gate("00", "H")


def test_bit_trials_count_sum():
    result = simulate_bit_trials(probability_one=0.5, shots=100, seed=1)
    assert result.count_zero + result.count_one == 100


def test_bit_trials_probability_extremes():
    zero_result = simulate_bit_trials(probability_one=0.0, shots=10, seed=1)
    one_result = simulate_bit_trials(probability_one=1.0, shots=10, seed=1)
    assert zero_result.count_one == 0
    assert one_result.count_one == 10


def test_s_gate_creates_a_complex_beta_relative_phase():
    plus_state = apply_single_qubit_gate(basis_state("0"), "H")
    phased_state = apply_single_qubit_gate(plus_state, "S")

    assert phased_state.alpha == pytest.approx(1 / 2**0.5)
    assert phased_state.beta == pytest.approx(1j / 2**0.5)
    assert phased_state.probability_zero == pytest.approx(0.5)
    assert phased_state.probability_one == pytest.approx(0.5)


def test_bell_phi_plus_measurements_only_matching_states():
    result = simulate_bell_phi_plus_measurements(shots=100, seed=1)
    assert result.count_00 + result.count_11 == 100
    assert result.count_01 == 0
    assert result.count_10 == 0
    assert result.same_result_ratio == 1.0


def test_two_basis_correlation_models_have_distinct_patterns():
    product = simulate_two_basis_correlations("product_plus", shots=200, seed=1)
    classical = simulate_two_basis_correlations("classical_correlated", shots=200, seed=1)
    bell = simulate_two_basis_correlations("bell_phi_plus", shots=200, seed=1)

    assert product.z_probabilities == pytest.approx((0.25, 0.25, 0.25, 0.25))
    assert product.x_probabilities == pytest.approx((1.0, 0.0, 0.0, 0.0))
    assert classical.z_probabilities == pytest.approx((0.5, 0.0, 0.0, 0.5))
    assert classical.x_probabilities == pytest.approx((0.25, 0.25, 0.25, 0.25))
    assert bell.z_probabilities == pytest.approx((0.5, 0.0, 0.0, 0.5))
    assert bell.x_probabilities == pytest.approx((0.5, 0.0, 0.0, 0.5))

    for result in (product, classical, bell):
        assert sum(result.z_counts) == 200
        assert sum(result.x_counts) == 200


def test_deutsch_one_bit_classifies_oracles():
    expected = {
        "constant_zero": ("constant", "0", ("+", "+")),
        "constant_one": ("constant", "0", ("-", "-")),
        "balanced_identity": ("balanced", "1", ("+", "-")),
        "balanced_flip": ("balanced", "1", ("-", "+")),
    }

    for oracle_name, (classification, measurement, phases) in expected.items():
        result = run_deutsch_one_bit(oracle_name)
        assert result.classification == classification
        assert result.measurement == measurement
        assert result.phase_markers == phases
        assert result.query_count == 1
        assert result.prepared_probabilities == pytest.approx((0.5, 0.5))
        assert result.after_oracle_probabilities == pytest.approx((0.5, 0.5))

        expected_final = (1.0, 0.0) if classification == "constant" else (0.0, 1.0)
        assert result.final_probabilities == pytest.approx(expected_final)


def test_noisy_measurements_preserve_shot_count():
    result = simulate_noisy_bit_measurements(probability_one=0.75, noise_rate=0.1, shots=100, seed=1)
    assert result.ideal_count_zero + result.ideal_count_one == 100
    assert result.noisy_count_zero + result.noisy_count_one == 100


def test_named_circuit_readout_returns_expected_probabilities():
    x_result = simulate_named_circuit("x_gate", shots=40, seed=1)
    bell_result = simulate_named_circuit("bell_pair", shots=40, seed=1)

    assert x_result.labels == ("0", "1")
    assert x_result.probabilities == pytest.approx((0.0, 1.0))
    assert x_result.counts == (0, 40)
    assert bell_result.labels == ("00", "01", "10", "11")
    assert bell_result.probabilities == pytest.approx((0.5, 0.0, 0.0, 0.5))
    assert bell_result.counts[1] == 0
    assert bell_result.counts[2] == 0


def test_measurement_series_preserves_each_shot_count():
    result = simulate_measurement_series(
        probability_one=0.5,
        noise_rate=0.1,
        shot_counts=(10, 100, 1000),
        batch_count=12,
        seed=1,
    )

    assert [row.shots for row in result.rows] == [10, 100, 1000]
    for row in result.rows:
        assert row.batch_count == 12
        assert row.ideal_count_zero + row.ideal_count_one == row.shots
        assert row.noisy_count_zero + row.noisy_count_one == row.shots
        assert 0 <= row.ideal_ratio_one <= 1
        assert 0 <= row.noisy_ratio_one <= 1
        assert row.ideal_ratio_min <= row.ideal_ratio_mean <= row.ideal_ratio_max
        assert row.noisy_ratio_min <= row.noisy_ratio_mean <= row.noisy_ratio_max


def test_phase_interference_extremes_and_middle_case():
    bright = simulate_phase_interference(0.0, shots=20, seed=1)
    middle = simulate_phase_interference(0.25, shots=20, seed=1)
    dark = simulate_phase_interference(0.5, shots=20, seed=1)

    assert bright.probability_bright == 1.0
    assert bright.count_bright == 20
    assert middle.probability_bright == pytest.approx(0.5)
    assert middle.count_bright + middle.count_dark == 20
    assert dark.probability_bright == pytest.approx(0.0)
    assert dark.count_dark == 20


def test_entanglement_limit_keeps_bob_local_random_but_changes_pair_correlation():
    same_basis = simulate_entanglement_limit("Z", "Z", shots=200, seed=1)
    different_basis = simulate_entanglement_limit("Z", "X", shots=200, seed=1)

    assert same_basis.count_01 == 0
    assert same_basis.count_10 == 0
    assert same_basis.same_ratio == 1.0
    assert 0.35 < same_basis.bob_zero_ratio < 0.65
    assert 0.35 < different_basis.bob_zero_ratio < 0.65
    assert 0.35 < different_basis.same_ratio < 0.65


@pytest.mark.parametrize(
    "input_state",
    ("zero", "one", "plus", "minus", "plus_i", "minus_i"),
)
def test_quantum_teleportation_restores_each_supported_state(input_state: str):
    outcomes = {
        simulate_quantum_teleportation(input_state, seed=seed).alice_bits
        for seed in range(30)
    }

    assert outcomes == {"00", "01", "10", "11"}
    for seed in range(8):
        result = simulate_quantum_teleportation(input_state, seed=seed)
        assert result.fidelity == pytest.approx(1.0)
        assert result.alice_bits in {"00", "01", "10", "11"}


def test_quantum_teleportation_rejects_unknown_input_state():
    with pytest.raises(ValueError):
        simulate_quantum_teleportation("unknown")


def test_quantum_teleportation_restores_custom_complex_amplitudes():
    amplitudes = (0.3, 0.4 + 0.5j)

    for seed in range(12):
        result = simulate_quantum_teleportation("custom", seed=seed, amplitudes=amplitudes)
        assert result.fidelity == pytest.approx(1.0)
        assert sum(abs(value) ** 2 for value in result.input_amplitudes) == pytest.approx(1.0)


def test_complex_phase_presets_have_imaginary_beta_amplitudes():
    plus_i = simulate_quantum_teleportation("plus_i", seed=1)
    minus_i = simulate_quantum_teleportation("minus_i", seed=1)

    assert plus_i.input_amplitudes[1].imag == pytest.approx(1 / 2**0.5)
    assert minus_i.input_amplitudes[1].imag == pytest.approx(-1 / 2**0.5)


def test_quantum_teleportation_labels_the_11_correction_as_zx():
    result = next(
        result
        for seed in range(30)
        if (result := simulate_quantum_teleportation("plus", seed=seed)).alice_bits == "11"
    )

    assert result.correction_gates == ("X", "Z")
    assert result.correction_label == "ZX"


def test_quantum_teleportation_rejects_invalid_custom_amplitudes():
    with pytest.raises(ValueError):
        simulate_quantum_teleportation("custom")
    with pytest.raises(ValueError):
        simulate_quantum_teleportation("custom", amplitudes=(0.0, 0.0))
    with pytest.raises(ValueError):
        simulate_quantum_teleportation("plus", amplitudes=(1.0, 0.0))


def test_learner_selected_teleportation_correction_changes_fidelity():
    result = next(
        result
        for seed in range(30)
        if (result := simulate_quantum_teleportation(
            "custom",
            seed=seed,
            amplitudes=(0.8, 0.6j),
        )).alice_bits == "10"
    )

    correct = apply_teleportation_correction(result, "Z")
    wrong = apply_teleportation_correction(result, "I")

    assert correct.matches_protocol_correction
    assert correct.fidelity == pytest.approx(1.0)
    assert not wrong.matches_protocol_correction
    assert wrong.fidelity < 1.0
    assert abs(result.input_amplitudes[1]) ** 2 == pytest.approx(0.36)


@pytest.mark.parametrize(
    ("message_bits", "encoding_gate", "bell_state"),
    (
        ("00", "I", "phi_plus"),
        ("01", "X", "psi_plus"),
        ("10", "Z", "phi_minus"),
        ("11", "ZX", "psi_minus"),
    ),
)
def test_superdense_coding_recovers_two_classical_bits(
    message_bits: str,
    encoding_gate: str,
    bell_state: str,
):
    result = simulate_superdense_coding(message_bits)

    assert result.encoding_gate == encoding_gate
    assert result.bell_state == bell_state
    assert result.transmitted_qubits == 1
    assert result.decoded_bits == message_bits


def test_superdense_coding_rejects_non_binary_pair():
    with pytest.raises(ValueError):
        simulate_superdense_coding("101")


def test_learner_selected_superdense_gate_determines_decoded_bits():
    result = simulate_superdense_coding("10", encoding_gate="X")

    assert result.message_bits == "10"
    assert result.encoding_gate == "X"
    assert result.decoded_bits == "01"
    assert not result.success

    with pytest.raises(ValueError):
        simulate_superdense_coding("00", encoding_gate="H")


@pytest.mark.parametrize(
    ("encoding_gate", "decoded_bits", "bell_state"),
    (
        ("I", "00", "phi_plus"),
        ("X", "01", "psi_plus"),
        ("Z", "10", "phi_minus"),
        ("ZX", "11", "psi_minus"),
    ),
)
def test_superdense_exploration_has_no_target_bits(
    encoding_gate: str,
    decoded_bits: str,
    bell_state: str,
) -> None:
    result = explore_superdense_encoding(encoding_gate)

    assert result.encoding_gate == encoding_gate
    assert result.decoded_bits == decoded_bits
    assert result.bell_state == bell_state
    assert not hasattr(result, "message_bits")


def test_superdense_missions_are_reproducible_and_do_not_repeat_immediately() -> None:
    first = generate_superdense_mission(seed=13001)
    repeated = generate_superdense_mission(seed=13001)
    second = generate_superdense_mission(seed=13002, previous_bits=first)

    assert first == repeated
    assert first in {"00", "01", "10", "11"}
    assert second != first
