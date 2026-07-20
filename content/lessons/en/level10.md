## 1. Interference happens when possibilities meet again

Level 4 introduced interference through the sequence `H`, `Z`, `H`. This level looks at the same idea more carefully. The key point is that two possibilities can travel separately and then meet again, where they can reinforce or cancel.

For example, two water waves that meet in step can make a larger wave. If one wave is up while the other is down, they can weaken each other. Quantum interference is similar in the sense that the sizes and directions of possibilities add.

![Double slit viewed as particles and waves](assets/images/double_slit_wavefronts.webp)

The particle-only picture on the left suggests two bands behind the slits. In the wave picture on the right, wavefronts from the two slits overlap and repeatedly reinforce or cancel at different positions.

![Double-slit interference intensity across position](assets/images/Doubleslit3Dspectrum.gif)

The double-slit experiment is the classic example of this idea. Light or particles have path possibilities through the two slits, and the screen shows repeating bright and dark bands. Peaks in the second image indicate positions with a larger detection probability, while valleys indicate a smaller probability. These pictures build intuition; the quantum calculation comes from adding probability amplitudes.

## 2. Phase is the timing of a possibility

Phase sounds formal, but at first you can think of it as timing, or how far an arrow has rotated. If two possibilities have the same phase, they add in the same direction. If their phases are opposite, they can cancel.

![Phase examples](assets/images/level10_phase_examples.svg)

Noise-canceling headphones use a related idea: they add an opposite-shaped sound to reduce unwanted sound. In quantum mechanics, it is not literal sound that adds. Probability amplitudes add.

## 3. Bright and dark are names for probabilities

In this level's simulation, the two outputs are called `bright` and `dark`. In a light experiment, a bright output is where detection is likely, while a dark output is where detection is unlikely.

In a quantum-circuit picture, `bright` is like an outcome that has been amplified, while `dark` is like an outcome that has been canceled. The important pattern appears through repeated measurements, not one measurement.

## 4. Algorithms design useful interference

The Deutsch algorithm in the next Level 11 does not print every answer at once. Instead, the oracle leaves sign and phase differences, and the final `H` mixes the paths again so constant and balanced rules lead to different measurement results.

![Deutsch algorithm and interference](assets/images/level10_deutsch_interference_bridge.svg)

Same-sign patterns collect into measurement 0 after the final `H`. Opposite-sign patterns collect into measurement 1. That is the main bridge.

For example, a circuit can make unhelpful possibilities cancel while helpful information reinforces. That is the basic feeling behind many quantum algorithms.

## 5. Start with the meaning of the probability formula

If the phase difference between two paths is $\Delta\phi$, this simple model writes the bright probability as:

$$
P(\text{bright})=\frac{1+\cos(\Delta\phi)}{2}
$$

![An H-P-H circuit that converts phase difference into interference outcomes](assets/images/level10_phase_interferometer_circuit.svg)

The middle gate $P(\Delta\phi)$ changes only the phase of the $\lvert1\rangle$ path by $\Delta\phi$. The first H creates the two paths, and the final H recombines them so that the phase difference becomes a measurement probability.

If the formula feels hard, skip it for now. Focus on the meaning. When $\Delta\phi=0$, the bright output grows. When $\Delta\phi=\pi$, the bright output disappears. Middle values split the results.

:::expander Derive the bright and dark probabilities from the circuit states

Represent the two paths by $\lvert0\rangle$ and $\lvert1\rangle$. The circuit uses the first H to split the paths, changes the phase of one path, and uses the final H to recombine them.

### 1. The first H splits the paths equally

Starting from $\lvert0\rangle$, the first H gives both paths equal amplitudes:

$$
\lvert0\rangle
\xrightarrow{H}
\frac{\lvert0\rangle+\lvert1\rangle}{\sqrt{2}}
$$

### 2. One path receives a phase difference

Rotating only the $\lvert1\rangle$ path by $\Delta\phi$ multiplies its amplitude by $e^{i\Delta\phi}$:

$$
\frac{\lvert0\rangle+\lvert1\rangle}{\sqrt{2}}
\longrightarrow
\frac{\lvert0\rangle+e^{i\Delta\phi}\lvert1\rangle}{\sqrt{2}}
$$

If the exponential is unfamiliar, read it as “rotate the amplitude arrow of the second path by $\Delta\phi$.”

### 3. The final H recombines the paths

H acts on the two basis states as:

$$
H\lvert0\rangle
=\frac{\lvert0\rangle+\lvert1\rangle}{\sqrt{2}},
\qquad
H\lvert1\rangle
=\frac{\lvert0\rangle-\lvert1\rangle}{\sqrt{2}}
$$

Applying these rules to both terms gives:

$$
\begin{aligned}
H\left(
\frac{\lvert0\rangle+e^{i\Delta\phi}\lvert1\rangle}{\sqrt{2}}
\right)
&=
\frac{1}{2}
\left[
(1+e^{i\Delta\phi})\lvert0\rangle
+(1-e^{i\Delta\phi})\lvert1\rangle
\right]
\end{aligned}
$$

Calling $\lvert0\rangle$ bright and $\lvert1\rangle$ dark gives these amplitudes:

$$
A_{\text{bright}}=\frac{1+e^{i\Delta\phi}}{2},
\qquad
A_{\text{dark}}=\frac{1-e^{i\Delta\phi}}{2}
$$

### 4. Square amplitude magnitudes to obtain probabilities

The squared magnitude of a complex amplitude multiplies the number by its complex conjugate. The conjugate of $e^{i\Delta\phi}$ is $e^{-i\Delta\phi}$, and their sum is $2\cos(\Delta\phi)$:

$$
e^{i\Delta\phi}+e^{-i\Delta\phi}=2\cos(\Delta\phi)
$$

The bright probability is therefore:

$$
\begin{aligned}
P(\text{bright})
&=\left|\frac{1+e^{i\Delta\phi}}{2}\right|^2\\
&=\frac{(1+e^{i\Delta\phi})(1+e^{-i\Delta\phi})}{4}\\
&=\frac{1+\cos(\Delta\phi)}{2}
\end{aligned}
$$

The same calculation gives the dark probability:

$$
P(\text{dark})
=\left|\frac{1-e^{i\Delta\phi}}{2}\right|^2
=\frac{1-\cos(\Delta\phi)}{2}
$$

The two probabilities always add to 1. At $\Delta\phi=0$, $e^{i\Delta\phi}=1$, so only the bright amplitude remains. At $\Delta\phi=\pi$, $e^{i\Delta\phi}=-1$, so only the dark amplitude remains. These two endpoints are enough to understand the formula even if the complex-number steps are still unfamiliar.

:::
