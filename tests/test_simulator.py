import pytest

from core.simulator import (
    run_deutsch_one_bit,
    simulate_bell_phi_plus_measurements,
    simulate_bit_trials,
    simulate_noisy_bit_measurements,
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
