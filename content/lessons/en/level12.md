## 1. Entanglement creates a strong relationship

Level 6 showed that a Bell state creates a strong relationship between two qubits. If both qubits are measured in the same basis, the outcomes match strongly.

But a strong relationship is not the same as a message. The relationship appears when two people compare their records later. One person's screen alone still does not show a readable sentence.

![Entanglement is not a direct message](assets/images/level12_no_signal.svg)

## 2. Bob alone still sees randomness

Suppose Alice and Bob share a Bell pair. Bob measures only his own qubit. His results come out roughly half 0 and half 1.

For example, Bob's record might look like `0, 1, 1, 0, 0, 1, ...`. From that record alone, he cannot tell which basis Alice chose. It just looks like a random string.

## 3. The relationship appears after comparison

Later, Alice and Bob can compare their records using ordinary communication. Then the pattern becomes visible. If they used the same basis, the outcomes match strongly.

![Comparing entangled records](assets/images/level12_compare_records.svg)

For example, if both measure in the Z basis, `00` and `11` appear often. But Bob alone still sees roughly half 0 and half 1, so he cannot directly read what Alice did.

## 4. Different bases change the relationship

In a simple Bell-state model, measuring both qubits in the Z basis can be summarized like this.

$$
P(00)=\frac{1}{2},\quad P(11)=\frac{1}{2},\quad P(01)=P(10)=0
$$

If the formula feels hard, focus on the meaning: with the same basis, the two records often match as `00` or `11`.

If Alice measures in Z while Bob measures in X, the four paired outcomes become much more mixed.

$$
P(00)\approx P(01)\approx P(10)\approx P(11)\approx \frac{1}{4}
$$

So the same-result ratio weakens when the bases are different. Even then, Bob's local 0 and 1 counts still stay close to half and half.

## 5. This is not faster-than-light communication

Imagine Alice tries to send a secret message by agreeing that "choosing Z means 0, choosing X means 1." Bob still sees only his own local record, which looks like a half-0 half-1 random string.

The local result can be summarized like this.

$$
P(\text{Bob}=0)=P(\text{Bob}=1)=\frac{1}{2}
$$

If the formula feels hard, remember only this: changing Alice's basis does not turn Bob's local results into a readable message. Entanglement appears in the **shared relationship**, not in either **local record alone**.
