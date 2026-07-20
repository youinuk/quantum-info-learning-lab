## 1. A circuit diagram is like a timeline

In a quantum circuit, each horizontal line represents one qubit. The left side is the beginning, and the right side is later. A box on the line is a gate applied at that point.

![H gate circuit](assets/images/level8_h_gate_circuit.svg)

For example, starting from `|0>` and applying `X` gives `|1>`. Applying `H` creates a state that can later produce 0 or 1 with equal probability. Circuit diagrams can look formal, but the first rule is simple: read from left to right.

Circuit order and equation order point in different directions. If a circuit applies X and then Z, its time order is `X → Z`. Operators next to a ket act from the right, however, so the same process is written $ZX\lvert\psi\rangle$. Read circuits left to right and apply an operator product right to left.

## 2. Measurement is the end of the question

Measurement reads a qubit as a visible 0 or 1. Before measurement, a state can carry possibilities. The measurement result itself is one value.

One measurement result is not enough to know the whole state. Repeating the same preparation many times reveals the probability pattern, as seen in Levels 0, 1, and 2.

## 3. Two-qubit circuits use two lines together

In a two-qubit circuit, read each line separately, but pay special attention to gates such as `CNOT` that connect two lines. The control dot means "this qubit sets the condition." The circled `X` means "flip this target if the condition is met."

A standard example is the Bell circuit.

![Bell circuit](assets/images/level8_bell_circuit.svg)

First, `H` on the top qubit creates possibilities for 0 and 1. Then `CNOT` connects the two qubits. At the end, measurement gives only `00` or `11`.

This app names the top line $q_0$ and the bottom line $q_1$, then displays a result in $q_0q_1$ order. This is the big-endian display order introduced in Level 5. For example, `01` means the top line is 0 and the bottom line is 1.

## 4. Equations are tools for checking meaning

You may see an expression such as this:

$$
\frac{1}{\sqrt{2}}|00\rangle + \frac{1}{\sqrt{2}}|11\rangle
$$

If the equation feels hard, skip it for now. The key meaning is that `00` and `11` remain as equal-size possibilities, while `01` and `10` do not appear.

## 5. Connecting to real tools

Tools such as Qiskit and Cirq also build circuits. You do not need to memorize code first. Read the circuit diagram first, then match each code line to the part of the circuit it creates.

SDKs can display result bitstrings differently. In particular, Qiskit draws $q_0$ on top but puts $q_0$ on the right of a result string. The app converts SDK results to its consistent $q_0q_1$ order instead of mixing the two conventions.

The goal of this level is circuit literacy, not coding speed. Once you can read circuits, real quantum SDKs feel much less foreign.
