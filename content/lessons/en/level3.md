## 1. A gate is a button that changes a qubit

Classical computers use logic operations such as AND, OR, and NOT. Quantum computers use quantum gates to change qubit states.

At this level, it is enough to think of a gate as a button that transforms the state. Matrices can wait until a more advanced course.

![Quantum gates](assets/images/quantum_gates.svg)

## 2. X swaps 0 and 1

The X gate has the most familiar effect.

$$
X\lvert0\rangle=\lvert1\rangle,\qquad
X\lvert1\rangle=\lvert0\rangle
$$

If the formula feels difficult, read it as: "X changes 0 into 1 and 1 into 0." It is similar to a classical NOT operation.

Try starting from both `|0>` and `|1>` in the simulation, then press X once and twice.

## 3. H creates an equal superposition

Applying H to `|0>` creates equal possibilities for `0` and `1`.

$$
H\lvert0\rangle=
\frac{1}{\sqrt{2}}\lvert0\rangle+
\frac{1}{\sqrt{2}}\lvert1\rangle
$$

The calculation is optional. The meaning is that H changes one definite basis state into a state with two possibilities.

Measuring this state many times produces about half `0` and half `1`.

## 4. Applying H twice returns to the start

A second H recombines the possibilities and returns the original state.

$$
H(H\lvert0\rangle)=\lvert0\rangle
$$

This is an early view of interference. Superposition is not just a mixture. When its possibilities are combined again, their signs can reinforce or cancel.

Press H twice in the gate lab and watch both the state formula and the probability graph return to the starting pattern.

## 5. Z changes a sign that probability bars may hide

Z leaves the `|0>` amplitude unchanged and reverses the sign of the `|1>` amplitude.

$$
Z\lvert0\rangle=\lvert0\rangle,\qquad
Z\lvert1\rangle=-\lvert1\rangle
$$

Changing only a sign may leave the immediate probability graph unchanged. That does not mean Z did nothing.

The sign becomes visible when another gate, such as H, brings the possibilities together. This prepares the interference experiment in Level 4.
