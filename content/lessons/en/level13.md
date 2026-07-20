## 1. Entanglement alone cannot signal, but it is still useful

Level 12 showed that Bob cannot infer Alice's choice from his local results alone. Entanglement by itself cannot carry a chosen message.

When entanglement is combined with information that is actually transmitted, however, it enables special protocols. This level compares two of them.

- Quantum teleportation: send two classical bits so Bob can recover an unknown quantum state.
- Superdense coding: send one qubit so Bob can recover two classical bits.

Both protocols assume that Alice and Bob already share one Bell pair.

## 2. Teleportation transfers quantum-state information

Suppose Alice has an unknown state $\lvert\psi\rangle$ and wants Bob to receive that state. Instead of sending the original particle, they use these resources.

$$
\lvert\psi\rangle=\alpha\lvert0\rangle+\beta\lvert1\rangle,
\qquad
\lvert\alpha\rvert^2+\lvert\beta\rvert^2=1
$$

| Shared beforehand | What Alice actually sends | What Bob obtains |
|---|---|---|
| One Bell pair | Two classical bits | The original quantum state $\lvert\psi\rangle$ |

“Unknown” can include an arbitrary state whose amplitudes $\alpha$ and $\beta$ Alice does not know. Measuring one qubit gives only one outcome and changes the original superposition, so Alice cannot read both amplitudes from it and simply prepare a copy.

In general, $\alpha$ and $\beta$ are complex. After removing the global phase and choosing $\alpha$ to be real and nonnegative, write $\beta=e^{i\phi}\lvert\beta\rvert$. The simulation therefore controls $\lvert\alpha\rvert$ and the relative phase $\phi$, while calculating $\lvert\beta\rvert=\sqrt{1-\lvert\alpha\rvert^2}$ automatically.

The no-cloning theorem says that no single quantum operation can perfectly copy every arbitrary unknown state while preserving the original. Repeating a known preparation recipe for $\lvert0\rangle$ or $\lvert+\rangle$ is different from cloning one unknown specimen. Teleportation does not duplicate the state: Alice's original is removed by measurement while the state is reconstructed on Bob's side.

:::expander Check with equations why CNOT cannot copy every state (click)
When the first qubit is known to be $\lvert0\rangle$ or $\lvert1\rangle$, CNOT can transfer that value to a second qubit initialized as $\lvert0\rangle$. Here the first qubit is the control and the second is the target.

$$
\lvert0\rangle\lvert0\rangle\longrightarrow\lvert0\rangle\lvert0\rangle,
\qquad
\lvert1\rangle\lvert0\rangle\longrightarrow\lvert1\rangle\lvert1\rangle
$$

Applying the same operation to $\lvert+\rangle=(\lvert0\rangle+\lvert1\rangle)/\sqrt{2}$ gives the following result by linearity.

$$
\lvert+\rangle\lvert0\rangle
\longrightarrow
\frac{\lvert00\rangle+\lvert11\rangle}{\sqrt{2}}
$$

Two genuine copies would instead be

$$
\lvert+\rangle\lvert+\rangle
=\frac{\lvert00\rangle+\lvert01\rangle+\lvert10\rangle+\lvert11\rangle}{2}.
$$

The states differ. A CNOT that copies basis values does not clone arbitrary superpositions, and no other single universal operation can do so.
:::

## 3. Separate preparation from the teleportation circuit

![Quantum teleportation circuit](assets/images/level13_teleportation_circuit.svg)

1. Bell-pair preparation is the process that starts from two $\lvert0\rangle$ states and uses H and CNOT to create the Bell pair before Alice handles the input state.
2. Bell A goes to Alice and Bell B goes to Bob. The unknown input $\lvert\psi\rangle$ begins inside Alice's section.
3. Alice applies CNOT with the input as control, then applies H to the input.
4. The upper input measurement is bit $a$ and the lower Bell A measurement is bit $b$. Alice sends both to Bob.
5. Bob applies $X$ when $b=1$ and $Z$ when $a=1$. For 11, X occurs first and Z second, so the total operator is $ZX$.

Alice may obtain `00`, `01`, `10`, or `11`, each with equal probability. She cannot choose the outcome, but every outcome leads to the same restored input when Bob applies the matching corrections.

## 4. Teleport one concrete state

Let the state Alice wants to send be the following $\lvert+\rangle$ state.

$$
\lvert+\rangle=\frac{\lvert0\rangle+\lvert1\rangle}{\sqrt{2}}
$$

If Alice measures `10`, Bob's state before correction carries a `Z` effect and looks like $\lvert-\rangle$.

$$
Z\lvert+\rangle=\lvert-\rangle
$$

After receiving Alice's bits `10`, Bob applies `Z`.

$$
Z\lvert-\rangle=\lvert+\rangle
$$

Bob therefore obtains the $\lvert+\rangle$ state Alice originally intended to send. Alice's particle did not move, but Bob's qubit now has the same state as the input.

If the equations feel difficult, keep only this meaning: Alice's two bits tell Bob which correction to apply. The simulation lets you observe all four measurement outcomes.

:::expander Follow an arbitrary state through all four measurement outcomes (click)
Write the input as follows and order the qubits as input $Q$, Bell A, and Bell B.

$$
\lvert\psi\rangle_Q=\alpha\lvert0\rangle+\beta\lvert1\rangle,
\qquad
\lvert\Phi^+\rangle_{AB}=\frac{\lvert00\rangle+\lvert11\rangle}{\sqrt{2}}
$$

Start from the initial state to see why Alice's CNOT and H produce four branches. At the end, collect terms that share the same first two qubits $QA$.

First expand the initial three-qubit state in $QAB$ order.

$$
\begin{aligned}
\lvert\Psi_0\rangle
&=\lvert\psi\rangle_Q\lvert\Phi^+\rangle_{AB}\\
&=\frac{1}{\sqrt{2}}\big(
\alpha\lvert000\rangle+
\alpha\lvert011\rangle+
\beta\lvert100\rangle+
\beta\lvert111\rangle
\big).
\end{aligned}
$$

Alice's CNOT flips A only in terms where $Q=1$. Thus $100\rightarrow110$ and $111\rightarrow101$, while the first two terms remain unchanged.

$$
\lvert\Psi_1\rangle
=\frac{1}{\sqrt{2}}\big(
\alpha\lvert000\rangle+
\alpha\lvert011\rangle+
\beta\lvert110\rangle+
\beta\lvert101\rangle
\big)
$$

Now apply H to the first qubit Q.

$$
H\lvert0\rangle=\frac{\lvert0\rangle+\lvert1\rangle}{\sqrt{2}},
\qquad
H\lvert1\rangle=\frac{\lvert0\rangle-\lvert1\rangle}{\sqrt{2}}
$$

Substituting these expressions into the four terms gives eight terms.

$$
\begin{aligned}
\lvert\Psi_2\rangle=\frac{1}{2}\big(&
\alpha\lvert000\rangle+\alpha\lvert100\rangle+
\alpha\lvert011\rangle+\alpha\lvert111\rangle\\
&+\beta\lvert010\rangle-\beta\lvert110\rangle+
\beta\lvert001\rangle-\beta\lvert101\rangle
\big).
\end{aligned}
$$

Collect terms with the same first two bits $QA$. Writing the alpha term first, the $QA=01$ terms are $\alpha\lvert011\rangle+\beta\lvert010\rangle$. Factoring out $\lvert01\rangle$ leaves Bob's state $\alpha\lvert1\rangle+\beta\lvert0\rangle$, so the form of $X\lvert\psi\rangle$ is immediately visible.

$$
\begin{aligned}
\lvert\Psi_2\rangle=\frac{1}{2}\Big[&
\lvert00\rangle_{QA}(\alpha\lvert0\rangle+\beta\lvert1\rangle)_B\\
&+\lvert01\rangle_{QA}(\alpha\lvert1\rangle+\beta\lvert0\rangle)_B\\
&+\lvert10\rangle_{QA}(\alpha\lvert0\rangle-\beta\lvert1\rangle)_B\\
&+\lvert11\rangle_{QA}(\alpha\lvert1\rangle-\beta\lvert0\rangle)_B
\Big].
\end{aligned}
$$

Indeed, $X\lvert\psi\rangle=\alpha\lvert1\rangle+\beta\lvert0\rangle$ and $XZ\lvert\psi\rangle=\alpha\lvert1\rangle-\beta\lvert0\rangle$. The four states in parentheses are therefore $\lvert\psi\rangle$, $X\lvert\psi\rangle$, $Z\lvert\psi\rangle$, and $XZ\lvert\psi\rangle$. The compact form is

$$
\frac{1}{2}\Big[
\lvert00\rangle\lvert\psi\rangle
+\lvert01\rangle X\lvert\psi\rangle
+\lvert10\rangle Z\lvert\psi\rangle
+\lvert11\rangle XZ\lvert\psi\rangle
\Big]
$$

This gives the following state and correction for each measured pair $ab$. In this app, $a$ is the measurement of the top input qubit $Q$, and $b$ is the measurement of Bell A below it. Thus $ab$ also follows the top-to-bottom big-endian display order.

| $ab$ | Bob before correction | Bob's correction |
|---|---|---|
| 00 | $\lvert\psi\rangle$ | $I$ |
| 01 | $X\lvert\psi\rangle$ | $X$ |
| 10 | $Z\lvert\psi\rangle$ | $Z$ |
| 11 | $XZ\lvert\psi\rangle$ | $ZX$ |

In $ZX\lvert\phi\rangle$, the circuit applies X first and Z second because the rightmost X acts first in the equation. Thus the last row gives $ZX(XZ\lvert\psi\rangle)=\lvert\psi\rangle$.
:::

## 5. Teleportation is not a science-fiction transporter

The name can suggest that matter disappears and reappears, but what is transferred is quantum-state information.

- The Bell pair must be distributed before the protocol begins.
- Bob does not know which correction to apply until Alice's two classical bits arrive.
- Classical information does not travel faster than light.
- Alice's original state does not remain intact after measurement, so two copies are not created.

Teleportation therefore respects both no-signaling and the no-cloning principle.

## 6. Superdense coding sends two classical bits

![Superdense coding circuit](assets/images/level13_superdense_coding_circuit.svg)

This time Alice wants to send one message from `00`, `01`, `10`, and `11`.

1. A separate preparation process applies H and CNOT to two $\lvert0\rangle$ states, then distributes one Bell qubit to Alice and the other to Bob.
2. Alice applies $I$, $X$, $Z$, or $ZX$ to her qubit. Here $ZX$ means X first and Z second.
3. Alice physically sends that one qubit to Bob.
4. Bob uses CNOT and H to decode the pair, measures both qubits, and reads two classical bits.

Without the shared entanglement, one transmitted qubit could not distinguish two reliable classical bits in this way.

:::expander Follow the four encodings into Bell states and measured bits (click)
The preparation device creates

$$
\lvert\Phi^+\rangle=\frac{\lvert00\rangle+\lvert11\rangle}{\sqrt{2}}.
$$

Alice's operation on the first qubit maps the four messages to four Bell states.

$$
\begin{aligned}
I\lvert\Phi^+\rangle&=\lvert\Phi^+\rangle,\\
X\lvert\Phi^+\rangle&=\frac{\lvert10\rangle+\lvert01\rangle}{\sqrt{2}}=\lvert\Psi^+\rangle,\\
Z\lvert\Phi^+\rangle&=\frac{\lvert00\rangle-\lvert11\rangle}{\sqrt{2}}=\lvert\Phi^-\rangle,\\
ZX\lvert\Phi^+\rangle&=\frac{\lvert01\rangle-\lvert10\rangle}{\sqrt{2}}=\lvert\Psi^-\rangle.
\end{aligned}
$$

Bob's CNOT and H act as a Bell decoder that reverses the preparation structure. Follow the reversed gate sequence to see why the four Bell states become 00, 01, 10, and 11.

Bell preparation applies H to the first qubit and then CNOT.

$$
U_{\text{prepare}}=\operatorname{CNOT}(H\otimes I)
$$

Both H and CNOT are their own inverses, so the decoder reverses their order: CNOT first, then H.

$$
U_{\text{decode}}=(H\otimes I)\operatorname{CNOT}
$$

The rightmost CNOT acts first in this equation. Applying it to each Bell state separates the pair into $\lvert+\rangle$ or $\lvert-\rangle$ on the first qubit and 0 or 1 on the second.

$$
\begin{aligned}
\operatorname{CNOT}\lvert\Phi^+\rangle
&=\frac{\lvert00\rangle+\lvert10\rangle}{\sqrt{2}}
=\lvert+\rangle\lvert0\rangle,\\
\operatorname{CNOT}\lvert\Psi^+\rangle
&=\frac{\lvert01\rangle+\lvert11\rangle}{\sqrt{2}}
=\lvert+\rangle\lvert1\rangle,\\
\operatorname{CNOT}\lvert\Phi^-\rangle
&=\frac{\lvert00\rangle-\lvert10\rangle}{\sqrt{2}}
=\lvert-\rangle\lvert0\rangle,\\
\operatorname{CNOT}\lvert\Psi^-\rangle
&=\frac{\lvert01\rangle-\lvert11\rangle}{\sqrt{2}}
=\lvert-\rangle\lvert1\rangle.
\end{aligned}
$$

The final H uses $H\lvert+\rangle=\lvert0\rangle$ and $H\lvert-\rangle=\lvert1\rangle$. The complete decoder therefore gives

$$
\begin{aligned}
\lvert\Phi^+\rangle&\longrightarrow\lvert00\rangle, &
\lvert\Psi^+\rangle&\longrightarrow\lvert01\rangle,\\
\lvert\Phi^-\rangle&\longrightarrow\lvert10\rangle, &
\lvert\Psi^-\rangle&\longrightarrow\lvert11\rangle.
\end{aligned}
$$

Bob does not somehow guess the Bell-state name. The Bell decoder converts the four Bell states into four computational-basis states, so an ordinary measurement can reveal Alice's two bits.
:::

## 7. Four messages become four Bell states

Alice's operation changes the shared Bell pair into one of four distinguishable states.

| Bits to send | Alice's operation | Bell state | Bob's result |
|---|---|---|---|
| 00 | I | $\lvert\Phi^+\rangle$ | 00 |
| 01 | X | $\lvert\Psi^+\rangle$ | 01 |
| 10 | Z | $\lvert\Phi^-\rangle$ | 10 |
| 11 | $ZX$ | $\lvert\Psi^-\rangle$ | 11 |

Here `I` means no change. Bob must measure Alice's transmitted qubit together with the qubit he already held to distinguish the message.

Bob's measured pair therefore exactly matches the two bits Alice intended to send. For example, if Alice chooses `10`, Bob obtains `10` after the Bell decoder.

## 8. The two protocols are complementary

| Protocol | Input | Shared beforehand | Actual transmission | Output |
|---|---|---|---|---|
| Teleportation | One unknown qubit state | One Bell pair | Two classical bits | One qubit state |
| Superdense coding | Two classical bits | One Bell pair | One qubit | Two classical bits |

The circuits share Bell-pair preparation and decoding structures, so parts of them look reversed. Their goals and transmitted resources are different, however, so they are not merely one identical circuit played backward.

Entanglement alone does not carry a message. Combined with classical bits or a physically transmitted qubit, it becomes a shared resource that changes which communication tasks are possible.
