# Quantum Info Learning Lab

[Korean README](README_KR.md)

Quantum Info Learning Lab is a bilingual Streamlit learning app for high-school students and general learners. It builds quantum-information concepts step by step, beginning with bits and probability and continuing through qubits, measurement, gates, interference, entanglement, noise, circuit reading, quantum algorithms, and quantum teleportation.

The primary experience is optimized for desktop and tablet screens, while mobile browsers remain supported for reading and lightweight interaction.

English is the default interface language. Korean can be selected from the sidebar, and the complete Korean learning content is maintained alongside the English version.

Live deployments:

- Quantum Info Learning Lab: https://quantum-info-learning-lab.streamlit.app
- Photon Heist: https://quantum-info-learning-lab.youinuk.workers.dev/hub

## Run Locally

The project uses a Conda environment with packages from `conda-forge`. The recommended environment name is `quantum_lab`.

```bash
cd quantum_info_learning_lab

conda create -n quantum_lab -c conda-forge python=3.12
conda activate quantum_lab
conda install -c conda-forge --file requirements.txt pytest

python -m streamlit run app.py
```

Run one local Streamlit instance for this project. Stop it with `Ctrl+C` before
starting another instance on port 8501. Keep that terminal open while using the
app. The polling source watcher reloads
changed project modules without enabling the native watchdog backend.

To update an existing environment:

```bash
conda install -n quantum_lab -c conda-forge --file requirements.txt pytest
conda run -n quantum_lab pytest -q
```

## Curriculum

- Level 0: Bits and Probability
- Level 1: Qubit Basics
- Level 2: Measurement
- Level 3: Quantum Gates, Including Complex Phase with S
- Level 4: Interference
- Level 5: Two Qubits and Two-Qubit Gates
- Level 6: Entanglement
- Level 7: Noise and Errors
- Level 8: Reading Quantum Circuits
- Level 9: Measurement Statistics
- Level 10: Interference in Depth
- Level 11: Simple Quantum Algorithms
- Level 12: Entanglement and Information Limits
- Level 13: Interactive Quantum Teleportation plus superdense-coding exploration and transmission missions
- Photon Heist: An HTML5 puzzle game about straight-line propagation, reflection, and refraction

Each level contains lesson cards, an interactive simulation, curated resources, and a quiz.

### Next Applied Track

Five bridge levels are planned before the advanced tracks:

- Level 14: Quantum Cryptography and BB84
- Level 15: Quantum Networks
- Level 16: Detecting and Reducing Errors
- Level 17: Real Quantum Hardware
- Level 18: Qiskit/Cirq SDK and Execution Basics

The later curriculum branches into quantum algorithms such as Grover search, QFT, and variational methods; error correction including stabilizer and surface codes; and applications such as quantum machine learning. See the [curriculum and implementation roadmap](docs/curriculum_roadmap.md) for the detailed sequence and entry requirements.

## Content Layout

- Lesson prose: `content/lessons/{lang}/levelN.md`
- Goals, terms, simulation labels, and quizzes: `content/levels.json`, `content/levels_en.json`
- Curated resource links: `content/resources.json`
- Local images: `assets/images/`
- Media sources and licenses: [media attributions](docs/media_attributions.md)
- Photon Heist source: `games/photon_heist/`

## Verification

```bash
conda run -n quantum_lab python -m compileall -q app.py core pages tests
conda run -n quantum_lab pytest -q
```

## Project Documents

- Curriculum, implementation order, and advanced tracks: [curriculum roadmap](docs/curriculum_roadmap.md)
- Photon Heist work after Chapter 3: [Photon Heist roadmap](docs/photon_heist_roadmap.md)
- Development, deployment, and service operations: [development notes](docs/development.md)
- Operator composition, qubit order, and SDK bit order: [quantum conventions](docs/quantum_conventions.md)
- Learning-copy tone, equation flow, and bilingual authoring rules: [content style guide](docs/content_style_guide.md)
- Pre-deployment checks: [cloud deployment checklist](docs/cloud_deploy_checklist.md)
- Experiment IDs, source links, figures, and reproducibility: [experiment registry](docs/experiment_registry.md)
- External image and media sources: [media attributions](docs/media_attributions.md)

These files contain contributor-facing design and operating notes, not secrets, and are intentionally versioned. Never commit tokens, real secret values, personal filesystem paths, or private notes. Store local-only documents under `docs/private/`.
