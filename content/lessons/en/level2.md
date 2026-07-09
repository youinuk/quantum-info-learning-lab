## 1. Measurement asks a question

Measurement asks a qubit, "Are you 0 or 1 in this measurement basis?" The observed answer is always one of those two classical values.

Superposition does not mean that the screen displays `0` and `1` at the same time. Before measurement, the state is a combination of possibilities. The measurement result is one definite value.

![Measurement process](assets/images/measurement_collapse.svg)

## 2. The state just after measurement matches the result

Suppose the state before measurement is:

$$
\lvert\psi\rangle=
\frac{1}{\sqrt{2}}\lvert0\rangle+
\frac{1}{\sqrt{2}}\lvert1\rangle
$$

Skip the formula if needed. It simply represents equal possibilities for `0` and `1` before measurement.

If the result is `0`, the state immediately after this ideal measurement is represented as `|0>`. If the result is `1`, it is represented as `|1>`.

The simulation shows the state before measurement, the result from this run, and the state immediately after measurement.

## 3. One result does not describe the full state

Even if a state has a $\frac{3}{4}$ probability of producing `1`, a single measurement can still give `0`. That is not automatically an error. Low-probability events can happen.

Think of a basketball player with a high free-throw percentage. The player can still miss one shot. A larger set of attempts describes the player's usual pattern better than one success or failure.

![Repeated measurement statistics](assets/images/measurement_statistics.svg)

## 4. Repeat by preparing the same state again

Measurement leaves one result, so repeatedly inspecting the same measured qubit does not recover its original probabilities.

Instead, prepare many qubits in the same state and measure each one once. Collecting those results reveals the probability pattern of the preparation.

## 5. What to observe in the simulation

Compare experiments with 1, 10, 100, and 1000 trials. Small samples move around strongly because of chance.

As the sample grows, the observed ratio usually moves closer to the probability configured for the state. The result does not become perfectly exact, but the statistical pattern becomes clearer.
