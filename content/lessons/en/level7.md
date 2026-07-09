## 1. An algorithm is a procedure

An algorithm is an ordered procedure for solving a problem. A recipe and a route-finding process are everyday examples.

A quantum algorithm is also a sequence of steps, but it uses qubits, quantum gates, and interference. It does not print every possible answer at once. Measurement still returns one result, so the circuit must make useful information survive in that result.

![Algorithm interference](assets/images/algorithm_interference.svg)

## 2. The Deutsch problem asks for the type of a hidden rule

Imagine a hidden function `f` that accepts `0` or `1` and returns `0` or `1`.

| Rule | f(0) | f(1) | Type |
|---|---:|---:|---|
| A | 0 | 0 | constant |
| B | 0 | 1 | balanced |
| C | 1 | 1 | constant |
| D | 1 | 0 | balanced |

The function is `constant` when its two outputs match and `balanced` when they differ. The task is to learn the type, not to print the entire truth table.

## 3. An oracle is a black box containing the rule

The oracle contains the hidden function `f`. We cannot inspect its internal work; we count how many times an algorithm queries it.

A deterministic classical method must ask for both `f(0)` and `f(1)` before it can compare them with certainty. One classical query leaves the other output unknown.

The Deutsch circuit queries the oracle once and marks the relationship between the two outputs in phase information.

## 4. The two qubits have different jobs

The first qubit carries the classification. Measuring `0` means constant, while measuring `1` means balanced.

The second qubit is a helper. It lets the oracle turn a function value into a relative sign on the first qubit.

The circuit starts in:

$$
\lvert0\rangle\lvert1\rangle
$$

![Deutsch algorithm](assets/images/deutsch_algorithm.svg)

## 5. The first H gates prepare both input possibilities

Applying H to both qubits gives the first qubit the possibilities `0` and `1`. It prepares the helper qubit with opposite signs.

Skip the equation if it feels heavy. It only says: “prepare both inputs on the first qubit and prepare the helper to receive a sign.”

$$
\lvert0\rangle\lvert1\rangle
\xrightarrow{H\otimes H}
\frac{\lvert0\rangle+\lvert1\rangle}{\sqrt{2}}
\otimes
\frac{\lvert0\rangle-\lvert1\rangle}{\sqrt{2}}
$$

## 6. The oracle leaves phase markers instead of printing answers

The standard oracle action is:

$$
U_f\lvert x\rangle\lvert y\rangle
=\lvert x\rangle\lvert y\oplus f(x)\rangle
$$

If the formula is difficult, read it as: “the oracle applies the function value to the helper qubit.”

With the helper prepared as above, the function value comes back as a `+` or `-` marker on the first-qubit possibility. This is called **phase kickback**.

$$
U_f\lvert x\rangle\lvert-\rangle
=(-1)^{f(x)}\lvert x\rangle\lvert-\rangle
$$

The first-qubit probabilities are still 50:50 immediately after the oracle. Nothing seems different if we only inspect probability bars, but the relative signs now carry the rule information.

## 7. The final H turns the hidden markers into a result

The final H recombines the two first-qubit possibilities.

- Matching phase markers reinforce `0` and cancel `1`.
- Opposite phase markers reinforce `1` and cancel `0`.

The final measurement therefore means:

$$
0\Rightarrow\text{constant},\qquad
1\Rightarrow\text{balanced}
$$

Compare the probabilities after the oracle and after the final H in the simulation. This is where an invisible phase relationship becomes visible through interference.

## 8. This tiny example shows an important pattern

The Deutsch problem is a teaching example, not a large practical speedup. It reduces two oracle queries for a deterministic classical method to one quantum query.

Do not stretch that small result into a claim that every quantum program is faster. The important pattern is not “print all answers from superposition.” It is “mark a relationship in phase, then use interference to read it.”

This app treats the one-input-bit Deutsch-Jozsa circuit as the Deutsch algorithm. Larger quantum algorithms reuse the same broad idea: encode useful structure into phase and shape the final measurement with interference.
