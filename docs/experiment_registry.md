# Experiment Registry

This registry connects the learning app, internal experiment IDs, manuscript chapters,
figures, and simulator functions. It is intended for developers, instructors, and
reproducibility tracking. Learner-facing chapters should use readable names rather
than these internal IDs.

## Current app baseline

- Repository: `https://github.com/youinuk/quantum-info-learning-lab`
- Public curriculum baseline: `v0.4.0`
- Release commit: `3024e3e`
- Public release scope at `v0.4.0`: Level 0-12
- Current development scope: Level 0-13
- Remaining bridge before the Advanced track: Level 14-18

For publication release, connect the stable release tag to an archived DOI.

## Registry table

| Internal ID | Display name | App level | Page file | Primary simulator/function | Manuscript chapter | Figure/output targets | Status |
|---|---|---:|---|---|---|---|---|
| EXP-C01 | Classical bit sampling | 0 | `pages/01_level0_bit_probability.py` | `simulate_bit_trials` | Ch. 1, Ch. 2 | `fig_exp_c01_sampling` | public |
| EXP-Q01 | Qubit probability and one-shot measurement | 1 | `pages/02_level1_qubit_placeholder.py` | `QubitState`, `basis_state` | Ch. 3 | `fig_exp_q01_state_probability` | public |
| EXP-Q02 | Repeated state preparation | 2 | `pages/03_level2_measurement.py` | page-level measurement logic | Ch. 4 | `fig_exp_q02_repeated_preparation` | public |
| EXP-M01 | Immediate remeasurement in the same basis | 2 | `pages/03_level2_measurement.py` | page-level measurement logic | Ch. 4 | `fig_exp_m01_remeasurement` | public |
| EXP-G01 | X, H, Z, and complex-phase S transformations | 3 | `pages/04_level3_gates.py` | `apply_single_qubit_gate` | Ch. 5 | `fig_exp_g01_gate_transformations` | implemented |
| EXP-G02 | Two-gate return experiments | 3 | `pages/04_level3_gates.py` | `apply_single_qubit_gate` | Ch. 5 | `fig_exp_g02_two_gate_returns` | public |
| EXP-I01 | H-H versus H-Z-H interference | 4 | `pages/05_level4_interference.py` | `apply_single_qubit_gate` | Ch. 6, Ch. 7 | `fig_ch06_hidden_phase_concept`, `fig_ch06_recombination_flow` | public |
| EXP-I02 | Constructive/destructive amplitude comparison | 4, 10 | `pages/05_level4_interference.py`, `pages/12_level10_interference_depth.py` | symbolic derivation / checked values | Ch. 6, Ch. 7 | `tab_ch06_amplitude_probability` | public |
| EXP-I03 | Variable phase-difference interference | 10 | `pages/12_level10_interference_depth.py` | `simulate_phase_interference` | Ch. 6, Ch. 7 | `fig_ch06_phase_sweep` | public |
| EXP-TQ01 | Independent two-qubit joint distribution | 5 | `pages/06_level5_two_qubits.py` | `independent_two_qubit_distribution` | Ch. 8 | `fig_exp_tq01_joint_distribution` | public |
| EXP-TQ02 | CNOT, CZ, and SWAP basis-state transformations | 5 | `pages/06_level5_two_qubits.py` | `apply_two_qubit_basis_gate` | Ch. 8 | `two_qubit_gates.svg` | implemented |
| EXP-ENT01 | Product, classical mixture, and Bell state in Z/X bases | 6 | `pages/07_level6_entanglement.py` | `simulate_two_basis_correlations` | Ch. 9 | `fig_exp_ent01_basis_compare` | public |
| EXP-ALG01 | Deutsch oracle classification | 11 | `pages/13_level11_algorithms.py` | `run_deutsch_one_bit` | Ch. 7, Ch. 11 | `fig_exp_alg01_deutsch_stages` | public |
| EXP-N01 | Symmetric outcome-flip noise | 7 | `pages/08_level7_noise.py` | `simulate_noisy_bit_measurements` | Ch. 12 | `fig_exp_n01_outcome_flip` | public |
| EXP-CIR01 | Circuit-card reading | 8 | `pages/09_level8_circuit_reading.py` | `simulate_named_circuit` | Ch. 5, Ch. 8, Ch. 11 | `fig_exp_cir01_cards` | public |
| EXP-CIR02 | Measurement-placement comparison | 8 | `pages/09_level8_circuit_reading.py` | `simulate_named_circuit` | Ch. 5 | `fig_exp_cir02_measurement_placement` | public |
| EXP-STAT01 | 10/100/1000-shot comparison | 9 | `pages/11_level9_measurement_statistics.py` | `simulate_measurement_series` | Ch. 2, Ch. 4 | `fig_exp_stat01_shot_comparison` | public |
| EXP-STAT02 | Sampling and noise comparison | 9 | `pages/11_level9_measurement_statistics.py` | `simulate_measurement_series` | Ch. 2, Ch. 12 | `fig_exp_stat02_noise_sampling` | public |
| EXP-ENT02 | Local data versus paired joint data | 12 | `pages/14_level12_entanglement_limits.py` | `simulate_entanglement_limit` | Ch. 9, Ch. 10 | `fig_exp_ent02_local_joint` | public |
| EXP-ENT03 | Same-basis and different-basis comparison | 12 | `pages/14_level12_entanglement_limits.py` | `simulate_entanglement_limit` | Ch. 10 | `fig_exp_ent03_basis_pairs` | public |
| EXP-COM01 | Quantum teleportation stages | 13 | `pages/15_level13_teleportation_dense_coding.py` | `simulate_quantum_teleportation` | TBD | `level13_teleportation_circuit.svg` | implemented |
| EXP-COM02 | Learner-selected Bob correction | 13 | `pages/15_level13_teleportation_dense_coding.py` | `apply_teleportation_correction` | TBD | correction attempt, fidelity, and outcome history | implemented |
| EXP-COM03 | Superdense gate-effect codebook | 13 | `pages/15_level13_teleportation_dense_coding.py` | `explore_superdense_encoding` | TBD | `level13_superdense_coding_circuit.svg` and discovered codebook | implemented |
| EXP-COM04 | Randomized superdense transmission mission | 13 | `pages/15_level13_teleportation_dense_coding.py` | `generate_superdense_mission`, `simulate_superdense_coding` | TBD | target bits, selected gate, decoded bits, and mission log | implemented |
| EXP-CRYPTO01 | BB84 basis sifting | 14 | `TBD_LEVEL14` | `TBD` | TBD | `fig_exp_crypto01_basis_sifting` | planned |
| EXP-CRYPTO02 | Eavesdropper and QBER comparison | 14 | `TBD_LEVEL14` | `TBD` | TBD | `fig_exp_crypto02_qber` | planned |
| EXP-NET01 | Direct entanglement distribution with loss | 15 | `TBD_LEVEL15` | `TBD` | TBD | `fig_exp_net01_direct_link` | planned |
| EXP-NET02 | Entanglement swapping across nodes | 15 | `TBD_LEVEL15` | `TBD` | TBD | `fig_exp_net02_swapping` | planned |
| EXP-EC01 | One-bit versus three-bit repetition | 16 | `TBD_LEVEL16` | `TBD` | Ch. 12 | `fig_exp_ec01_repetition` | planned |
| EXP-EC02 | Repetition-code failure at high noise | 16 | `TBD_LEVEL16` | `TBD` | Ch. 12 | `fig_exp_ec02_noise_sweep` | planned |
| EXP-HW01 | Logical-to-physical qubit mapping | 17 | `TBD_LEVEL17` | `TBD` | TBD | `fig_exp_hw01_connectivity` | planned |
| EXP-HW02 | Ideal versus hardware-aware circuit | 17 | `TBD_LEVEL17` | `TBD` | TBD | `fig_exp_hw02_transpilation` | planned |
| EXP-SDK01 | Bell circuit in Qiskit | 18 | `TBD_LEVEL18` | external SDK notebook | SDK Lab | `fig_exp_sdk01_qiskit_bell` | planned |
| EXP-SDK02 | Bell circuit in Cirq | 18 | `TBD_LEVEL18` | external SDK notebook | SDK Lab | `fig_exp_sdk02_cirq_bell` | planned |
| EXP-QEC01 | Stabilizer syndrome measurement | Advanced QEC1 | `TBD_ADV_QEC1` | `TBD` | TBD | `fig_exp_qec01_syndrome` | planned |
| EXP-QEC02 | Surface-code error chains | Advanced QEC2 | `TBD_ADV_QEC2` | `TBD` | TBD | `fig_exp_qec02_surface_code` | planned |
| EXP-QML01 | Variational quantum classifier workflow | Advanced APP1 | `TBD_ADV_APP1` | `TBD` | TBD | `fig_exp_qml01_classifier` | planned |
| EXP-QML02 | Classical baseline and noise comparison | Advanced APP1 | `TBD_ADV_APP1` | `TBD` | TBD | `fig_exp_qml02_baseline` | planned |

## Policy

- Do not expose internal IDs in learner-facing chapter prose unless there is a clear reason.
- Use internal IDs in reproducibility appendices, figure manifests, tests, and instructor notes.
- When a level changes, update this registry in the same pull request.
- Before publication, each public experiment should have a stable display name, a tested simulator function, and a documented figure-generation path.
