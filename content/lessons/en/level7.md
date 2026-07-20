## 1. Real quantum computers are imperfect

Earlier levels assumed that qubits and gates worked ideally.

Real devices are affected by heat, vibration, electromagnetic disturbance, small control errors, and imperfect measurement hardware. These unwanted effects are collectively called noise.

![How noise blurs measurement statistics](assets/images/noise_error.svg)

## 2. Example: an outcome-flip error changes the record

Suppose we prepare $\lvert1\rangle$ 100 times. With no error, the record contains one hundred 1 results.

This level's simulation uses a simple outcome-flip error. At a 5% error rate, roughly five of the 1 results are expected to be recorded incorrectly as 0, leaving about five zeros and ninety-five ones.

![Numerical example of outcome-flip errors](assets/images/noise_measurement_example.svg)

An actual run of 100 trials will not always contain exactly five flips. Errors occur probabilistically, so the count varies slightly from run to run.

## 3. Small errors can accumulate in a long circuit

Let $p$ be the error probability for one operation and $n$ the number of operations. In a very simple model where errors are independent, the probability of seeing no flip is:

$$
P(\text{no flip})=(1-p)^n
$$

If the equation feels difficult, keep only this meaning: more operations create more opportunities for at least one error.

Even with a 1% error rate per operation, this simplified model gives only about a 36.6% chance of passing through one hundred operations without a flip.

$$
(1-0.01)^{100}=0.99^{100}\approx0.366
$$

![A simple model of small errors accumulating](assets/images/noise_accumulation.svg)

Errors in real quantum hardware may be correlated and come in several forms. This calculation is an illustration of why a small rate cannot simply be ignored, not a complete prediction of device accuracy.

## 4. Quantum probability and hardware error are different

Probabilistic quantum measurement is not the same as faulty hardware.

- An ideal equal superposition producing a mixture of 0 and 1 results is probability belonging to the state.
- Preparing $\lvert1\rangle$ but recording some results as 0 is the hardware error assumed by this simulation.

If the ideal distribution is already 50-50, flipping some zeros and ones can leave the overall bars looking almost unchanged. A similar histogram does not prove that every individual measurement was correct.

## 5. Noise has several forms

The simulation models only flipped measurement outcomes, but real devices face different problems.

- Readout error: like misreading a thermometer, the detector records 0 as 1 or 1 as 0.
- Control error: like turning a door slightly less or more than 90 degrees, a gate rotates the state by the wrong amount.
- Decoherence: interaction with the environment weakens the phase relationships in a superposition. A collection of aligned spinning tops gradually disturbed in different directions is a rough visual analogy.

These analogies only separate the basic ideas. Real decoherence is not a visible wobble; it is quantum-state information spreading into the environment.

## 6. Why error correction is difficult

Classical computers can reduce errors by copying information and comparing several copies.

An unknown qubit state cannot be copied freely, and directly measuring it changes the superposition we want to protect. Quantum error correction therefore distributes relationships across several physical qubits and detects traces of errors without directly reading the protected information itself.

This level focuses on distinguishing kinds of noise from ideal probability rather than constructing a full error-correction circuit.
