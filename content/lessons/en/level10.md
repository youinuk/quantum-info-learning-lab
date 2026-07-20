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

## 5. Use only a short formula

If the phase difference between two paths is $\Delta\phi$, this simple model writes the bright probability as:

$$
P(\text{bright})=\frac{1+\cos(\Delta\phi)}{2}
$$

If the formula feels hard, skip it for now. Focus on the meaning. When $\Delta\phi=0$, the bright output grows. When $\Delta\phi=\pi$, the bright output disappears. Middle values split the results.
