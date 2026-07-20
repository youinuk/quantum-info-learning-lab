## 1. Bits and qubits answer different questions

A bit asks, “Is the current value 0 or 1?” Its value is already definite, and reading it reveals that value.

A qubit is different. Before measurement, its state can include a possibility of measuring 0 and a possibility of measuring 1. Measurement still returns only one result.

## 2. Bra-ket notation is a way to write quantum states

Quantum states are commonly written with **bra-ket notation**. This level uses only the right-angle form called a **ket**.

$$
\lvert0\rangle,\qquad \lvert1\rangle,\qquad \lvert\psi\rangle
$$

$\lvert0\rangle$ is read as “ket zero,” and $\lvert1\rangle$ as “ket one.” In $\lvert\psi\rangle$, $\psi$ (psi) is a name assigned to a quantum state. The vertical bar and angle bracket form one state symbol; they are not an absolute value or ordinary brackets.

Recognizing the notation is enough for now. Later levels use it repeatedly for the starting, intermediate, and final states of circuits.

## 3. Superposition combines two possibilities

A qubit state is commonly written as:

$$
\lvert\psi\rangle=\alpha\lvert0\rangle+\beta\lvert1\rangle
$$

If the formula feels difficult, keep only this meaning: a qubit state carries a 0 part and a 1 part before measurement.

Here $\psi$ (psi) names the state, while $\alpha$ (alpha) and $\beta$ (beta) are the **amplitudes** of its state terms. An amplitude is not itself a probability. Its squared magnitude gives a measurement probability.

$$
P(0)=\lvert\alpha\rvert^2,\qquad
P(1)=\lvert\beta\rvert^2
$$

![Amplitudes and measurement probabilities](assets/images/qubit_superposition.svg)

## 4. Example: squaring amplitudes gives probabilities

Consider this state:

$$
\lvert\psi\rangle=
\frac{\sqrt{3}}{2}\lvert0\rangle+
\frac{1}{2}\lvert1\rangle
$$

Squaring the amplitude of the $\lvert0\rangle$ term gives $\frac{3}{4}$, while the $\lvert1\rangle$ term gives $\frac{1}{4}$. Repeated preparations therefore produce roughly 75% zero results and 25% one results.

![Example of squaring amplitudes to obtain probabilities](assets/images/amplitude_probability.svg)

## 5. Fractions and square roots show the structure

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

The decimal 0.707 may look more familiar, but $\frac{1}{\sqrt{2}}$ shows the exact structure: it is the amplitude whose square is $\frac{1}{2}$.

## 6. The state before measurement is not merely a hidden answer

As a rough analogy, the state before measurement is like a picture carrying several possible details. Pressing the measurement button leaves one sharp result on the screen.

The analogy is not perfect. A qubit is not simply hiding a predetermined 0 or 1 that we have not discovered. Its state before measurement is genuinely represented as a combination of state terms and amplitudes.

## 7. One measurement cannot reveal the whole state

Measuring once shows only 0 or 1. From that single result, we cannot tell whether the original probabilities were $1/2:1/2$ or $1/4:3/4$.

To estimate the state, prepare the same state many times and measure each preparation once. “Prepare again” matters because measurement changes the state rather than merely looking at it.
