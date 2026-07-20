## 1. Two qubits have four measurement outcomes

Measuring one qubit gives `0` or `1`.

Measuring two qubits gives four possible outcomes: `00`, `01`, `10`, and `11`.

This app writes two qubits as $\lvert q_0q_1\rangle$. The left digit is the first, top circuit qubit $q_0$; the right digit is the second, bottom qubit $q_1$. Thus $\lvert01\rangle$ means $q_0=0$ and $q_1=1$.

Treating the left $q_0$ as the more significant position and listing states as `00`, `01`, `10`, `11` is this app's big-endian display order. Every state table, chart, and simulation in the app follows this order.

![Two-qubit states](assets/images/two_qubits.svg)

A basis state is one of the basic states used as coordinates for describing a quantum state. In the computational basis used here, the two-qubit basis states are $\lvert00\rangle$, $\lvert01\rangle$, $\lvert10\rangle$, and $\lvert11\rangle$.

When a two-qubit state contains several possible outcomes, it can be written as a sum of these basis states. Each basis state appearing in that expression is a basis-state term, or simply a term. Measurement produces the outcome corresponding to one of them.

## 2. The state space grows quickly

Each added qubit doubles the number of basis states.

$$
1\text{ qubit}:2,\qquad
2\text{ qubits}:4,\qquad
3\text{ qubits}:8
$$

In general, $n$ qubits have $2^n$ basis states.

$$
n\text{ qubits}\longrightarrow 2^n\text{ basis states}
$$

If exponents are unfamiliar, focus on the pattern: every new qubit doubles the list.

## 3. Begin with independently prepared qubits

This level first treats the two qubits as separately prepared states.

Suppose the first qubit has a $\frac{1}{2}$ probability of being measured as `1`, and the second has a $\frac{1}{4}$ probability. For independent preparations, multiply the probabilities to find the chance of `11`.

$$
P(11)=P(\text{first}=1)P(\text{second}=1)
=\frac{1}{2}\times\frac{1}{4}=\frac{1}{8}
$$

The calculation can be skipped. Changing either qubit's probability changes several two-qubit outcomes at once.

## 4. Two-qubit gates use two circuit wires

A single-qubit gate changes one qubit. A two-qubit gate acts on a condition or relationship involving two qubits. This app reads the upper wire as $q_0$ and the lower wire as $q_1$.

![Two-qubit gate circuits](assets/images/two_qubit_gates.svg)

- CNOT flips its target only when the control is `1`.
- CZ changes the sign of the $\lvert11\rangle$ term. It does not immediately flip a measured bit, but the sign can affect later interference.
- SWAP exchanges the positions of the two qubits, so $\lvert01\rangle$ becomes $\lvert10\rangle$.

This app writes controlled gates as `CNOT(control, target)` and `CZ(control, target)`. In `CNOT(q₀,q₁)` and `CZ(q₀,q₁)`, the first qubit $q_0$ is the control and the second qubit $q_1$ is the target. Books and software may order arguments differently. In a circuit diagram, read the solid dot `●` as the control and the connected `⊕` or gate box as the target.

## 5. CNOT flips the second qubit conditionally

For `CNOT(q₀,q₁)`, $q_1$ stays unchanged when $q_0=0$ and flips `0↔1` when $q_0=1$.

$$
\lvert00\rangle\rightarrow\lvert00\rangle,\quad
\lvert01\rangle\rightarrow\lvert01\rangle,\quad
\lvert10\rangle\rightarrow\lvert11\rangle,\quad
\lvert11\rangle\rightarrow\lvert10\rangle
$$

For input $\lvert10\rangle$, the first control qubit is `1`, so the second target flips from `0` to `1` and the output is $\lvert11\rangle$. For $\lvert01\rangle$, the control is `0`, so the output remains $\lvert01\rangle$.

Level 6 applies CNOT after the first qubit has both `0` and `1` possibilities, allowing the gate to create a Bell state.

## 6. Classical correlation and entanglement are different

Imagine placing a left glove in one box and a right glove in another. Opening one box tells you which glove is in the other. That is a classical correlation explained by values fixed in advance.

Entanglement is a more deeply quantum relationship. It cannot always be explained as two separate values that were merely hidden from us.

Level 6 compares independent states, classical correlations, and Bell entanglement using more than one measurement basis.

## 7. The goal of this level

This level does not yet try to prove or analyze entanglement. It builds familiarity with the four outcomes and how probability is distributed among them.

That foundation matters because an entangled state is not simply a fifth outcome. It is a different relationship among the same basis outcomes `00`, `01`, `10`, and `11`.
