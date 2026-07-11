import pytest

from core.simulator import (
    run_deutsch_one_bit,
    simulate_bell_phi_plus_measurements,
    simulate_bit_trials,
    simulate_entanglement_limit,
    simulate_measurement_series,
    simulate_named_circuit,
    simulate_noisy_bit_measurements,
    simulate_phase_interference,
    simulate_two_basis_correlations,
)


def test_bit_trials_count_sum():
    result = simulate_bit_trials(probability_one=0.5, shots=100, seed=1)
    assert result.count_zero + result.count_one == 100


def test_bit_trials_probability_extremes():
    zero_result = simulate_bit_trials(probability_one=0.0, shots=10, seed=1)
    one_result = simulate_bit_trials(probability_one=1.0, shots=10, seed=1)
    assert zero_result.count_one == 0
    assert one_result.count_one == 10


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
