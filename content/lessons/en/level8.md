## 1. Real quantum computers are not perfect

Earlier levels treated qubits and gates as ideal.

Real devices are affected by heat, vibration, electromagnetic noise, imperfect control signals, and imperfect measurement devices. These unwanted effects are called noise.

![Noise and errors](assets/images/noise_error.svg)

## 2. Noise blurs the answer

Suppose a state is supposed to produce 1 most of the time.

Without noise, the measurement results cluster around 1. If some results flip during measurement, extra 0 results appear.

This level uses a very simple bit-flip error model. Real quantum errors are more varied, but this model is enough for a first intuition.

## 3. Small error rates still matter

An error rate of 1% may sound small.

But long circuits contain many operations. Small errors can accumulate across 100 or 1000 steps.

That is why quantum computers are judged not only by qubit count, but also by error rates.

## 4. Error is different from probability

Quantum measurement being probabilistic is not the same as hardware making errors.

Probability belongs to the state itself. Error is an unwanted effect from the device or environment.

Keeping those ideas separate helps make sense of real quantum experiments.

## 5. Why error correction is hard

Classical computers can reduce errors by copying information and comparing copies.

Quantum information cannot be freely copied, and measurement changes the state. Quantum error correction therefore has to be designed very carefully.

This level only aims to show why noise is a serious problem.
