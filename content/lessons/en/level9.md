## 1. One measurement is one piece

When you measure one qubit, the screen shows one value: 0 or 1. That one value does not reveal the whole original state.

Suppose a 50:50 state is measured once and gives 1. That does not mean the state always gives 1. You need to repeat the same preparation many times.

## 2. Repeated measurement reveals a pattern

With 10 measurements, the result can wobble a lot. With 100 or 1000 measurements, the observed ratio tends to move closer to the original probability.

![Measurement count and statistics](assets/images/level10_sampling_statistics.svg)

The important phrase is not "becomes exactly equal." It is "tends to move closer." Probability experiments always keep some fluctuation.

## 3. Separate probability from noise

A quantum state having probability is different from a device making errors.

![Probability and noise comparison](assets/images/level10_noise_vs_probability.svg)

Probability belongs to the prepared state. Noise is unwanted disturbance from measurement devices, the environment, or imperfect operations. Mixing these ideas can lead to a wrong interpretation of real data.

## 4. More samples do not remove every problem

Increasing the number of measurements reduces random wobble. But if the device keeps flipping some results, a large experiment can still show a biased pattern.

For example, suppose the original probability of 1 is 1/2 and we measure 1000 times. Without noise, the ratio of 1 usually stays near 0.5. If the device keeps flipping 10% of the results, individual results still contain errors. Even if the final ratio happens to look close to 0.5, that does not prove there were no errors.

As another example, if a state should almost always give 1 but the error rate is 20%, then 1000 measurements may still show a ratio near 0.8 rather than 1.0. More samples reduce random wobble, but they do not automatically remove device bias.

That is why real quantum computers need more than repetition. They also need ways to reduce noise and identify which errors are happening.

## 5. Interpretation comes before formulas

The most basic formula is the observed ratio.

$$
\hat{p}=\frac{N_1}{N}
$$

Here, `N_1` is the number of 1 results, and `N` is the total number of measurements.

For example, if 1 appears 57 times in 100 measurements, the observed ratio is:

$$
\hat{p}=\frac{57}{100}=0.57
$$

If we repeat the same experiment in several batches, each batch can have a slightly different observed ratio. The mean summarizes the batches, and the range shows how much they wobbled. If the formula feels hard, focus only on the fraction for now. The key idea is to look at repeated patterns, not just one value.

One measurement is one photo. Repeated measurements are an album. Noise is like dust on the camera lens: it can blur the whole picture.
