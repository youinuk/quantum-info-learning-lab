## 1. Two qubits have four measurement outcomes

Measuring one qubit gives `0` or `1`.

Measuring two qubits gives four possible outcomes: `00`, `01`, `10`, and `11`. The first digit belongs to the first qubit, and the second digit belongs to the second qubit.

![Two-qubit states](assets/images/two_qubits.svg)

## 2. The state space grows quickly

Each added qubit doubles the number of basis states.

$$
1\text{ qubit}:2,\qquad
2\text{ qubits}:4,\qquad
3\text{ qubits}:8
$$

In general, `n` qubits have $2^n$ basis states.

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

Skip the calculation if needed. The main idea is that changing either qubit's probability changes several two-qubit outcomes at once.

## 4. Classical correlation and entanglement are different

Imagine placing a left glove in one box and a right glove in another. Opening one box tells you which glove is in the other. That is a classical correlation explained by values fixed in advance.

Entanglement is a more deeply quantum relationship. It cannot always be explained as two separate values that were merely hidden from us.

Level 6 compares independent states, classical correlations, and Bell entanglement using more than one measurement basis.

## 5. The goal of this level

This level does not yet try to prove or analyze entanglement. It builds familiarity with the four outcomes and how probability is distributed among them.

That foundation matters because an entangled state is not simply a fifth outcome. It is a different relationship among the same basis outcomes `00`, `01`, `10`, and `11`.
