## 1. An algorithm is a procedure

An algorithm is an ordered procedure for solving a problem. A recipe and a route-finding process are everyday examples.

A quantum algorithm is also a sequence of steps, but it uses qubits, quantum gates, and interference. It does not print every possible answer at once. Measurement still returns one result, so the circuit must make useful information survive in that result.

![Algorithm interference](assets/images/algorithm_interference.svg)

## 2. The Deutsch problem asks for the type of a hidden rule

Imagine a hidden function $f$ that accepts `0` or `1` and returns `0` or `1`.

| Rule | f(0) | f(1) | Type |
|---|---:|---:|---|
| A | 0 | 0 | constant |
| B | 0 | 1 | balanced |
| C | 1 | 1 | constant |
| D | 1 | 0 | balanced |

The function is `constant` when its two outputs match and `balanced` when they differ. The task is to learn the type, not to print the entire truth table.

## 3. An oracle is a black box containing the rule

The oracle contains the hidden function $f$. We cannot inspect its internal work; we count how many times an algorithm queries it.

A deterministic classical method must ask for both $f(0)$ and $f(1)$ before it can compare them with certainty. One classical query leaves the other output unknown.

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
=\lvert+\rangle_1\otimes\lvert-\rangle_2
$$

## 6. The oracle leaves phase markers instead of printing answers

The standard oracle action is:

$$
U_f\lvert x\rangle\lvert y\rangle
=\lvert x\rangle\lvert y\oplus f(x)\rangle
$$

If the formula is difficult, read it as: “the oracle looks at $x$ and flips the helper only when $f(x)=1$.” The value of $x$ itself does not change.

When the helper is prepared in `|->`, it returns to the same `|->` shape after the oracle. The probability amplitude of each corresponding $x$ basis-state term instead keeps one of these signs:

- Term with $f(x)=0$: `+` marker
- Term with $f(x)=1$: `-` marker

These signs are called phase markers. They do not mean that a measurement probability is positive or negative. They are signs of probability amplitudes and tell us whether the terms will reinforce or cancel when mixed later.

Initially, the first qubit is in `|+>`. The probability amplitudes of its $x=0$ and $x=1$ basis-state terms therefore both have a `+` sign, giving the pattern `+,+`. Oracle A has $f(0)=f(1)=0$, so both terms receive `+` markers and that pattern stays unchanged. Oracle B has $f(0)=0$ and $f(1)=1$, so it leaves `+` on the $x=0$ term and `-` on the $x=1$ term. The pattern therefore changes from `+,+` to `+,-`.

:::expander Check with equations how this sign becomes a phase marker on the first qubit

### 1. Expand the helper state into two terms

The helper is prepared as:

$$
\lvert-\rangle_2
=\frac{\lvert0\rangle-\lvert1\rangle}{\sqrt{2}}
$$

The subscript `2` marks the second qubit. Apply the oracle to both terms:

$$
\begin{aligned}
U_f\lvert x\rangle_1\lvert-\rangle_2
&=\frac{1}{\sqrt{2}}
\left(
U_f\lvert x\rangle_1\lvert0\rangle_2
-
U_f\lvert x\rangle_1\lvert1\rangle_2
\right)\\
&=\frac{\lvert x\rangle_1}{\sqrt{2}}
\left(
\lvert0\oplus f(x)\rangle_2
-
\lvert1\oplus f(x)\rangle_2
\right)
\end{aligned}
$$

This does not mean that $y\oplus f(x)$ and $(-1)^{f(x)}$ are the same quantity. The first is the helper's bit value. The second will be a sign multiplying the corresponding two-qubit state term.

### 2. Substitute $f(x)=0$ and $f(x)=1$

Try these before reading on:

- What are $0\oplus0$ and $1\oplus0$?
- What are $0\oplus1$ and $1\oplus1$?

Hint: XOR with `0` leaves a bit unchanged. XOR with `1` swaps `0` and `1`.

When $f(x)=0$, the two terms keep their order:

$$
\frac{
\lvert0\oplus0\rangle-\lvert1\oplus0\rangle
}{\sqrt{2}}
=
\frac{\lvert0\rangle-\lvert1\rangle}{\sqrt{2}}
=\lvert-\rangle
$$

When $f(x)=1$, their order is swapped:

$$
\frac{
\lvert0\oplus1\rangle-\lvert1\oplus1\rangle
}{\sqrt{2}}
=
\frac{\lvert1\rangle-\lvert0\rangle}{\sqrt{2}}
=-\frac{\lvert0\rangle-\lvert1\rangle}{\sqrt{2}}
=-\lvert-\rangle
$$

The notation $X^{f(x)}$ packages these two cases. `X` is the gate that swaps `0` and `1`:

$$
X^{f(x)}
=
\begin{cases}
X^0=I, & f(x)=0\\
X^1=X, & f(x)=1
\end{cases}
$$

This is not a new unexplained operation. It is shorthand for “leave the helper unchanged when the function value is 0, and apply X when it is 1.” The two calculations above can therefore be summarized as:

$$
X^{f(x)}\lvert-\rangle_2
=(-1)^{f(x)}\lvert-\rangle_2
$$

Including the first qubit gives the phase-kickback equation:

$$
U_f\lvert x\rangle_1\lvert-\rangle_2
=(-1)^{f(x)}
\lvert x\rangle_1\lvert-\rangle_2
$$

The oracle did not flip the first qubit. The coefficient multiplies the corresponding two-qubit state term. Because the helper returns to the same `|->` shape, the coefficient can be expressed as a relative phase on the corresponding first-qubit basis-state term.

### 3. Expand the first qubit's `|+>` state

Immediately before the oracle, the two qubits are:

$$
\lvert+\rangle_1\lvert-\rangle_2
=
\frac{\lvert0\rangle_1+\lvert1\rangle_1}{\sqrt{2}}
\otimes
\frac{\lvert0\rangle_2-\lvert1\rangle_2}{\sqrt{2}}
$$

The first qubit consists of an $x=0$ term and an $x=1$ term. Apply phase kickback to each term:

$$
U_f\lvert+\rangle_1\lvert-\rangle_2
=
\frac{
(-1)^{f(0)}\lvert0\rangle_1
+
(-1)^{f(1)}\lvert1\rangle_1
}{\sqrt{2}}
\lvert-\rangle_2
$$

### Example: substitute Oracle B

Oracle B has $f(0)=0$ and $f(1)=1$:

$$
\begin{aligned}
U_f\lvert+\rangle_1\lvert-\rangle_2
&=
\frac{
(-1)^0\lvert0\rangle_1
+
(-1)^1\lvert1\rangle_1
}{\sqrt{2}}
\lvert-\rangle_2\\
&=
\frac{\lvert0\rangle_1-\lvert1\rangle_1}{\sqrt{2}}
\lvert-\rangle_2\\
&=\lvert-\rangle_1\lvert-\rangle_2
\end{aligned}
$$

The first qubit changes as:

$$
\lvert+\rangle_1
=\frac{\lvert0\rangle_1+\lvert1\rangle_1}{\sqrt{2}}
\quad\longrightarrow\quad
\lvert-\rangle_1
=\frac{\lvert0\rangle_1-\lvert1\rangle_1}{\sqrt{2}}
$$

The helper remains $\lvert-\rangle_2$. Before the oracle, the first qubit's `|+>` state has the `+,+` pattern. An oracle with $f(0)=f(1)=0$ would leave those signs unchanged. Oracle B adds a `-` marker only to the $x=1$ term, producing `+,-`. This is the phase-marker change described above.

:::

## 7. The final H turns the hidden markers into a result

Only one idea from the previous section is needed here: the oracle leaves a `+` or `-` phase marker on each first-qubit basis-state term.

- A constant rule has matching $f(0)$ and $f(1)$, so its markers match: `+,+` or `-,-`
- A balanced rule has different $f(0)$ and $f(1)$, so its markers are opposite: `+,-` or `-,+`

The final H separates those two relationships. Matching markers collect into result `0`, while opposite markers collect into result `1`. The final measurement therefore means:

$$
0\Rightarrow\text{constant},\qquad
1\Rightarrow\text{balanced}
$$

:::expander Check with equations why matching markers give 0 and opposite markers give 1

Matching `+` markers form `|+>`, while opposite markers form `|->`:

$$
\lvert+\rangle
=\frac{\lvert0\rangle+\lvert1\rangle}{\sqrt{2}},
\qquad
\lvert-\rangle
=\frac{\lvert0\rangle-\lvert1\rangle}{\sqrt{2}}
$$

H maps those two states to different computational-basis results:

$$
H\lvert+\rangle=\lvert0\rangle,\qquad
H\lvert-\rangle=\lvert1\rangle
$$

A constant rule with $f(0)=f(1)=1$ leaves a `-` marker on both terms:

$$
\begin{aligned}
\frac{
(-1)^1\lvert0\rangle+(-1)^1\lvert1\rangle
}{\sqrt{2}}
&=
\frac{-\lvert0\rangle-\lvert1\rangle}{\sqrt{2}}\\
&=
-\left(
\frac{\lvert0\rangle+\lvert1\rangle}{\sqrt{2}}
\right)
=-\lvert+\rangle
\end{aligned}
$$

The final H therefore gives $-\lvert0\rangle$. The overall minus sign is a global phase, which does not change measurement probabilities, so the observed result is still `0`.

Similarly, the `-,+` pattern is $-\lvert-\rangle$, and the final H gives $-\lvert1\rangle$. Ignoring the global phase, the measured result is `1`.

:::

Compare the probabilities after the oracle and after the final H in the simulation. This is where an invisible phase relationship becomes visible through interference.

## 8. This tiny example shows an important pattern

The Deutsch problem is a teaching example, not a large practical speedup. It reduces two oracle queries for a deterministic classical method to one quantum query.

Do not stretch that small result into a claim that every quantum program is faster. The important pattern is not “print all answers from superposition.” It is “mark a relationship in phase, then use interference to read it.”

This app treats the one-input-bit Deutsch-Jozsa circuit as the Deutsch algorithm. Larger quantum algorithms reuse the same broad idea: encode useful structure into phase and shape the final measurement with interference.
