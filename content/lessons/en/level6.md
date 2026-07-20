## 1. Matching outcomes do not always mean entanglement

Imagine placing the same colored ball into two boxes ahead of time. Opening one box tells you what is in the other. The results are strongly correlated, but the colors were already fixed.

Quantum entanglement also creates strong relationships between outcomes. However, matching results alone do not distinguish quantum entanglement from a classical correlation.

We need to change the measurement basis and see how the relationship behaves from another direction.

## 2. We compare three two-qubit states

This level compares:

1. Independent product state `|+>|+>`: each qubit can be described separately.
2. Classically correlated mixture: prepare `|00>` half the time and `|11>` half the time.
3. Entangled Bell `|Phi+>`: `|00>` and `|11>` have a coherent phase relationship inside one quantum state.

The second and third states both produce only `00` or `11` in the Z basis. One measurement view cannot tell them apart.

## 3. H and CNOT create the Bell state

Apply the `CNOT(q₀,q₁)` introduced in Level 5 after creating a superposition. Start from `|00>`. H creates two possibilities on the first qubit, and CNOT links the second qubit to the first.

$$
\lvert00\rangle
\xrightarrow{H\otimes I}
\frac{\lvert00\rangle+\lvert10\rangle}{\sqrt{2}}
\xrightarrow{\mathrm{CNOT}}
\frac{\lvert00\rangle+\lvert11\rangle}{\sqrt{2}}
$$

The calculation can be skipped. H creates two possibilities on the first qubit. CNOT leaves the `00` branch unchanged and flips only the target in the `10` branch, turning it into `11`.

![Bell-state entanglement](assets/images/entanglement_bell.svg)

## 4. The classical mixture and Bell state match in Z

The Z basis is the usual `0` and `1` measurement used in earlier levels.

The classical mixture produces `00` and `11` half the time each. The Bell state does exactly the same.

$$
P(00)=\frac{1}{2},\quad P(11)=\frac{1}{2},\quad P(01)=P(10)=0
$$

Therefore, “the Z results always match” is not enough evidence by itself to identify entanglement.

## 5. The X basis views the state from another direction

A qubit can be measured using the X-basis states `|+>` and `|->` instead of the Z-basis states `|0>` and `|1>`.

$$
\lvert+\rangle=\frac{\lvert0\rangle+\lvert1\rangle}{\sqrt{2}},\qquad
\lvert-\rangle=\frac{\lvert0\rangle-\lvert1\rangle}{\sqrt{2}}
$$

If the formula is difficult, think of X as another direction from which to inspect the same qubit.

In a circuit, applying H and then measuring in Z is equivalent to measuring in X.

$$
\text{X-basis measurement}=H\text{ then Z-basis measurement}
$$

## 6. Changing the basis reveals the hidden difference

The classical `00/11` mixture spreads across `00`, `01`, `10`, and `11` in the X basis. Its preselected Z values contain no coherent X-basis phase link.

The Bell `|Phi+>` state still produces only `00` and `11` in X. Its whole-state quantum relationship survives as an interference pattern after the basis change.

The independent `|+>|+>` state produces only `00` in X. Its results match, but each qubit was separately prepared in `+`, so it is not entangled.

![Three states measured in two bases](assets/images/entanglement_basis_compare.svg)

## 7. Each Bell qubit is random when viewed alone

For the Bell state, either qubit by itself gives 0 and 1 with equal probability in both the Z and X bases. One isolated result does not reveal a special rule.

The strong pattern appears only when the two results are compared. The information belongs to the relationship of the whole state rather than to either qubit alone.

This does not enable faster-than-light messaging. Each result is random, so one observer cannot choose a value to send.

## 8. This lab compares three ideal known models

The app compares three ideal states whose preparation is known. It lets us see which patterns come from an independent state, a classical mixture, and Bell entanglement.

Proving entanglement for an unknown state in a real experiment may require more measurement settings, statistical analysis, a Bell inequality, or an entanglement witness.

Matching outcomes in one basis do not establish entanglement. Change the measurement basis and compare how the two-qubit relationship appears there.
