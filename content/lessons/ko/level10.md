## 1. 간섭은 가능성이 다시 만날 때 생긴다

Level 4에서는 `H`, `Z`, `H` 순서로 간섭을 처음 봤다. 이번에는 두 가능성이 따로 진행한 뒤 다시 만날 때 서로 더해지거나 지워지는 과정을 더 자세히 본다.

예를 들어 물결 두 개가 같은 타이밍으로 만나면 더 큰 물결이 된다. 반대로 한쪽이 올라갈 때 다른 쪽이 내려가면 서로 약해질 수 있다. 양자 간섭도 "가능성의 크기와 방향이 더해진다"는 점에서 이 그림과 닮았다.

![입자 관점과 파동 관점으로 본 이중슬릿](assets/images/double_slit_wavefronts.webp)

왼쪽의 입자 그림만 보면 두 슬릿 뒤에 두 줄이 생길 것 같다. 오른쪽의 파동 그림에서는 두 슬릿에서 퍼진 파면이 서로 겹치며, 위치에 따라 보강과 상쇄가 반복된다.

![위치에 따른 이중슬릿 간섭 세기](assets/images/Doubleslit3Dspectrum.gif)

이중슬릿은 이 생각을 보여 주는 대표 예시다. 빛이나 입자가 두 슬릿을 지나는 여러 가능성을 가지고, 스크린에서는 밝고 어두운 무늬가 반복된다. 두 번째 그림의 봉우리는 검출 가능성이 큰 위치, 골은 가능성이 작은 위치를 나타낸다. 단, 이 그림은 직관을 위한 예시이고 실제 양자 상태의 계산은 확률 진폭을 더해 해석한다.

## 2. 위상은 가능성의 타이밍이다

위상은 어려운 말처럼 보이지만, 처음에는 "타이밍" 또는 "화살표가 돌아간 정도"로 생각해도 된다. 두 가능성의 위상이 같으면 같은 방향으로 더해지고, 반대면 서로 지울 수 있다.

![위상 예시](assets/images/level10_phase_examples.svg)

예를 들어 이어폰의 노이즈 캔슬링은 원하지 않는 소리와 반대 모양의 소리를 섞어 줄이는 방식과 관련이 있다. 양자에서는 실제 소리 대신 확률 진폭이 더해진다.

## 3. 밝은 쪽과 어두운 쪽은 확률의 이름이다

이 레벨의 시뮬레이션에서는 결과를 `bright`와 `dark`라고 부른다. 실제 빛 실험처럼 생각하면 밝은 곳은 검출이 잘 되는 쪽이고, 어두운 곳은 검출이 잘 안 되는 쪽이다.

양자 회로로 생각하면 `bright`는 원하는 결과가 커진 경우, `dark`는 결과가 상쇄된 경우에 가깝다. 중요한 점은 한 번의 측정이 아니라 반복 측정에서 패턴이 드러난다는 것이다.

## 4. 알고리즘은 좋은 간섭을 설계한다

다음 Level 11의 Deutsch 알고리즘은 모든 답을 한 번에 출력하지 않는다. 대신 오라클이 남긴 부호와 위상 차이를 마지막 `H`가 다시 섞으면서, constant와 balanced가 서로 다른 측정 결과로 나오게 만든다.

![Deutsch 알고리즘과 간섭](assets/images/level10_deutsch_interference_bridge.svg)

같은 부호 패턴은 마지막 `H`에서 간섭한 뒤 `0`의 확률만 남고, 반대 부호 패턴은 `1`의 확률만 남는다. 이것만 기억하면 된다.

이처럼 원하지 않는 결과를 만드는 진폭은 상쇄하고, 필요한 정보가 담긴 결과를 만드는 진폭은 보강하도록 간섭을 설계할 수 있다. 그러면 마지막 측정에서 필요한 결과가 나올 확률이 높아진다.

## 5. 본문에서는 확률식의 의미만 먼저 본다

두 경로의 위상 차이를 $\Delta\phi$라고 하면, 이 단순 모델에서 밝은 쪽 확률은 다음처럼 쓸 수 있다.

$$
P(\text{bright})=\frac{1+\cos(\Delta\phi)}{2}
$$

![위상차를 간섭 결과로 바꾸는 H-P-H 회로](assets/images/level10_phase_interferometer_circuit.svg)

가운데의 $P(\Delta\phi)$는 $\lvert1\rangle$ 경로의 위상만 $\Delta\phi$만큼 바꾸는 게이트다. 첫 H가 두 경로를 만들고, 마지막 H가 두 경로를 다시 합쳐 위상차를 측정 확률로 바꾼다.

수식이 어렵다면 그냥 넘어가도 된다. 의미만 보면 된다. $\Delta\phi=0$이면 밝은 쪽이 커지고, $\Delta\phi=\pi$이면 밝은 쪽이 사라진다. 중간 값이면 두 결과가 나뉜다.

:::expander bright와 dark 확률식이 나오는 과정을 회로 상태로 확인하기

두 경로를 큐비트의 $\lvert0\rangle$과 $\lvert1\rangle$로 나타내 보자. 회로는 첫 H로 경로를 나누고, 한 경로의 위상을 바꾼 뒤, 마지막 H로 두 경로를 다시 합친다.

### 1. 첫 H가 두 경로를 같은 크기로 나눈다

시작 상태 $\lvert0\rangle$에 H를 적용하면 두 경로의 진폭이 같은 상태가 된다.

$$
\lvert0\rangle
\xrightarrow{H}
\frac{\lvert0\rangle+\lvert1\rangle}{\sqrt{2}}
$$

### 2. 한 경로에 위상차를 만든다

$\lvert1\rangle$ 경로만 $\Delta\phi$만큼 회전시키면 그 진폭에 $e^{i\Delta\phi}$가 곱해진다.

$$
\frac{\lvert0\rangle+\lvert1\rangle}{\sqrt{2}}
\longrightarrow
\frac{\lvert0\rangle+e^{i\Delta\phi}\lvert1\rangle}{\sqrt{2}}
$$

여기서 $e^{i\Delta\phi}$의 계산법이 낯설면 “두 번째 경로의 화살표 방향을 $\Delta\phi$만큼 돌린다”는 뜻만 잡으면 된다.

### 3. 마지막 H가 두 경로를 다시 합친다

H는 두 기저 상태에 다음처럼 작용한다.

$$
H\lvert0\rangle
=\frac{\lvert0\rangle+\lvert1\rangle}{\sqrt{2}},
\qquad
H\lvert1\rangle
=\frac{\lvert0\rangle-\lvert1\rangle}{\sqrt{2}}
$$

이를 위 상태의 두 항에 각각 적용하면 다음과 같다.

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

따라서 bright를 $\lvert0\rangle$, dark를 $\lvert1\rangle$ 결과라고 부르면 두 확률 진폭은 다음과 같다.

$$
A_{\text{bright}}=\frac{1+e^{i\Delta\phi}}{2},
\qquad
A_{\text{dark}}=\frac{1-e^{i\Delta\phi}}{2}
$$

### 4. 진폭의 크기를 제곱해 확률을 얻는다

복소수 진폭의 크기 제곱은 그 수와 켤레복소수를 곱해 계산한다. $e^{i\Delta\phi}$의 켤레는 $e^{-i\Delta\phi}$이고, 두 지수함수의 합은 $2\cos(\Delta\phi)$다.

$$
e^{i\Delta\phi}+e^{-i\Delta\phi}=2\cos(\Delta\phi)
$$

bright 확률을 계산하면 다음 식이 나온다.

$$
\begin{aligned}
P(\text{bright})
&=\left|\frac{1+e^{i\Delta\phi}}{2}\right|^2\\
&=\frac{(1+e^{i\Delta\phi})(1+e^{-i\Delta\phi})}{4}\\
&=\frac{1+\cos(\Delta\phi)}{2}
\end{aligned}
$$

같은 방법으로 dark 확률은 다음과 같다.

$$
P(\text{dark})
=\left|\frac{1-e^{i\Delta\phi}}{2}\right|^2
=\frac{1-\cos(\Delta\phi)}{2}
$$

두 확률을 더하면 항상 1이다. $\Delta\phi=0$이면 $e^{i\Delta\phi}=1$이라 bright 진폭만 남고, $\Delta\phi=\pi$이면 $e^{i\Delta\phi}=-1$이라 dark 진폭만 남는다. 복소수 계산이 부담스럽다면 이 두 끝점만 확인해도 수식의 의미를 이해할 수 있다.

:::
