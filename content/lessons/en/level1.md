## 1. Bits and qubits answer different questions

A bit asks, "Is the current value 0 or 1?" Its value is already definite, and reading it reveals that value.

A qubit is different. Before measurement, its state can include a possibility of measuring `0` and a possibility of measuring `1`. Measurement still returns only one result.

## 2. Superposition combines two possibilities

A qubit state is commonly written as:

$$
\lvert\psi\rangle=\alpha\lvert0\rangle+\beta\lvert1\rangle
$$

If the formula feels difficult, keep only this meaning: a qubit state carries a `0` part and a `1` part before measurement.

The numbers `alpha` and `beta` are amplitudes. An amplitude is not itself a probability. The squared magnitude of an amplitude gives the measurement probability.

![Qubit state](assets/images/qubit_superposition.svg)

## 3. Example: think of a possibility mixer

Imagine an audio mixer that can make one sound louder and another sound softer.

A qubit state similarly gives different weights to the `|0>` and `|1>` possibilities. Quantum amplitudes also have signs and phases, which matter when possibilities interfere. Level 4 returns to that idea.

![Possibility mixer](assets/images/amplitude_mixer.svg)

## 4. Fractions and square roots show the structure

A common qubit state gives equal probability to both outcomes.

$$
\lvert\psi\rangle=
\frac{1}{\sqrt{2}}\lvert0\rangle+
\frac{1}{\sqrt{2}}\lvert1\rangle
$$

You do not need to memorize the calculation. The important point is that squaring either amplitude gives one half.

$$
P(0)=\left(\frac{1}{\sqrt{2}}\right)^2=\frac{1}{2},\qquad
P(1)=\left(\frac{1}{\sqrt{2}}\right)^2=\frac{1}{2}
$$

The decimal `0.707` may look more familiar, but $\frac{1}{\sqrt{2}}$ shows the exact structure: it is the amplitude whose square is $\frac{1}{2}$.

## 5. Example: a blurry picture and a sharp result

As a rough analogy, the state before measurement is like a picture carrying several possible details. Pressing the measurement button leaves one sharp result on the screen.

The analogy is not perfect. A qubit is not simply hiding a classical value that we have not discovered. Its state before measurement is genuinely described as a combination of possibilities.

## 6. One measurement cannot reveal the whole state

Measuring once shows only `0` or `1`. From that single result, we cannot tell whether the original probabilities were `1/2 : 1/2` or `1/4 : 3/4`.

To estimate the state, prepare the same state many times and measure each preparation once. "Prepare again" matters because measurement changes the state rather than merely looking at it.
