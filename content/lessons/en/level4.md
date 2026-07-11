## 1. Superposition alone is not the whole story

Quantum computing is not special only because a qubit can hold multiple possibilities before measurement.

The important part is that possibilities can meet again and add or cancel. This is called interference.

![Interference](assets/images/interference.svg)

## 2. Everyday examples help

Two water waves can meet and become larger. They can also meet out of step and reduce each other.

Noise-canceling headphones use a related idea: they create an opposite wave to reduce unwanted sound.

Quantum interference is not literally sound, but the wave image helps explain why some results become more likely and others disappear.

## 3. The double-slit experiment is a classic example

Light or electrons sent through two narrow slits can create bright and dark bands.

Bright bands show reinforced possibilities. Dark bands show canceled possibilities.

In this app, we use H and Z gates as a tiny qubit version of the same idea.

![Double-slit setup](assets/images/Doubleslit.svg)

![Double-slit interference spectrum](assets/images/Doubleslit3Dspectrum.gif)

One detection gives only one dot on the screen. Repeating the same experiment many times creates dense and sparse regions, and that density pattern becomes the interference pattern.

![Detection dots building into an interference pattern](assets/images/double_slit_interference.svg)

## 4. H-H experiment

Start from `|0>`. Applying H creates a 50:50 superposition.

If the equation looks difficult, skip it and keep the meaning: one H creates two possibilities, and the second H brings them together again.

$$
H\lvert0\rangle=
\frac{1}{\sqrt{2}}\lvert0\rangle+
\frac{1}{\sqrt{2}}\lvert1\rangle
$$

Applying H again returns the state to `|0>` because the `|0>` possibility is reinforced while the `|1>` possibility is canceled.

$$
H(H\lvert0\rangle)=\lvert0\rangle
$$

## 5. H-Z-H experiment

Putting Z in the middle changes the sign.

The equation only records one important change: the plus sign before the `|1>` term becomes a minus sign.

$$
Z\left(
\frac{1}{\sqrt{2}}\lvert0\rangle+
\frac{1}{\sqrt{2}}\lvert1\rangle
\right)
=
\frac{1}{\sqrt{2}}\lvert0\rangle-
\frac{1}{\sqrt{2}}\lvert1\rangle
$$

After the second H, that relative sign makes the final state `|1>`.

$$
HZH\lvert0\rangle=\lvert1\rangle
$$

## 6. The key idea

Possibilities are not just mixed together. When they meet again, some outcomes grow and some outcomes shrink.

Quantum algorithms use this property to increase the chance of useful answers and reduce the chance of wrong ones.

![Interference in an algorithm](assets/images/algorithm_interference.svg)
