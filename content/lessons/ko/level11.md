## 1. 알고리즘은 문제를 푸는 절차다

알고리즘은 무엇을 어떤 순서로 할지 정한 절차다. 라면을 끓이는 순서, 목적지까지 가장 짧은 길을 찾는 과정도 알고리즘으로 볼 수 있다.

양자 알고리즘도 순서대로 작동한다. 차이는 중간에 큐비트, 양자 게이트, 간섭을 이용한다는 점이다.

양자컴퓨터가 모든 답을 한꺼번에 화면에 출력하는 것은 아니다. 측정하면 여전히 하나의 결과만 나온다. 그래서 필요한 정보만 마지막 결과에 남도록 간섭을 설계해야 한다.

![알고리즘 간섭 그림](assets/images/algorithm_interference.svg)

## 2. Deutsch 문제는 숨은 규칙의 종류를 맞히는 문제다

입력으로 `0` 또는 `1`을 받고, 출력으로 `0` 또는 `1`을 내는 숨은 함수 $f$가 있다고 하자.

가능한 규칙은 네 가지다.

| 규칙 | f(0) | f(1) | 종류 |
|---|---:|---:|---|
| A형 | 0 | 0 | constant |
| B형 | 0 | 1 | balanced |
| C형 | 1 | 1 | constant |
| D형 | 1 | 0 | balanced |

두 출력이 같으면 `constant`, 다르면 `balanced`이다. 목표는 정확한 규칙표 전체가 아니라 두 종류 중 어느 쪽인지 알아내는 것이다.

## 3. 오라클은 규칙이 든 검은 상자다

오라클은 숨은 함수 $f$를 담은 블랙박스다. 바깥에서는 내부 계산을 볼 수 없고, 회로가 오라클을 몇 번 호출했는지만 센다.

밀봉된 상자에 숫자를 넣고 표시등 하나만 확인하는 상황을 떠올리면 된다. 고전적으로 확실히 분류하려면 `0`과 `1`을 각각 넣어 두 출력을 비교해야 한다. 한 번만 물으면 다른 입력의 답을 모르기 때문이다.

Deutsch 회로는 오라클을 한 번만 호출한다. 이때 $f(0)$과 $f(1)$을 각각 꺼내는 대신, 두 값이 같은지 다른지를 첫 큐비트의 위상 차이에 담는다.

## 4. 두 큐비트는 서로 다른 역할을 맡는다

첫 번째 큐비트는 분류 결과를 담는다. `0`으로 측정되면 constant, `1`로 측정되면 balanced이다.

두 번째 큐비트는 보조 큐비트다. 오라클의 함수값이 첫 번째 큐비트의 부호 관계에 표시되도록 돕는다.

회로는 다음 상태에서 시작한다.

$$
\lvert0\rangle\lvert1\rangle
$$

첫 번째는 분류용 `0`, 두 번째는 보조용 `1`이다.

![Deutsch 알고리즘 그림](assets/images/deutsch_algorithm.svg)

## 5. 두 H 게이트가 입력과 보조 큐비트를 준비한다

두 큐비트에 H를 적용하면 첫 번째 큐비트는 입력 `0`과 `1`의 가능성을 함께 가진다. 두 번째 큐비트는 `|0>`과 `|1>`의 부호가 반대인 상태가 된다.

수식이 어렵다면 아래 식은 건너뛰어도 된다. 첫 큐비트에는 두 입력 가능성을 함께 준비하고, 보조 큐비트는 오라클의 함수값을 부호 변화로 받아낼 수 있는 상태로 만든다는 뜻이다.

$$
\lvert0\rangle\lvert1\rangle
\xrightarrow{H\otimes H}
\frac{\lvert0\rangle+\lvert1\rangle}{\sqrt{2}}
\otimes
\frac{\lvert0\rangle-\lvert1\rangle}{\sqrt{2}}
=\lvert+\rangle_1\otimes\lvert-\rangle_2
$$

## 6. 오라클은 답 대신 위상 표식을 남긴다

오라클의 표준 동작은 다음처럼 쓴다.

$$
U_f\lvert x\rangle\lvert y\rangle
=\lvert x\rangle\lvert y\oplus f(x)\rangle
$$

수식이 어렵다면 “첫 큐비트의 $x$를 보고, $f(x)=1$일 때만 보조 큐비트를 뒤집는다”는 의미만 잡으면 된다. 오라클을 지나도 $x$ 자체는 바뀌지 않는다.

보조 큐비트를 `|->`로 준비하면 오라클을 지난 뒤에도 보조 큐비트는 `|->` 상태로 정리된다. 다만 $f(x)$의 값에 따라 해당 $x$ 항 전체에 다음 부호가 곱해진다. 이 부호를 첫 큐비트의 확률 진폭에 남은 위상 표식으로 읽을 수 있다.

- $f(x)=0$인 항: `+` 표식
- $f(x)=1$인 항: `-` 표식

이 `+`와 `-`를 위상 표식이라고 부른다. 측정 확률이 양수나 음수라는 뜻이 아니라, 두 항이 마지막에 다시 섞일 때 서로 보강할지 상쇄할지를 정하는 확률 진폭의 부호다.

처음에 첫 큐비트는 `|+>` 상태다. 즉, $x=0$과 $x=1$에 해당하는 두 기저 상태 항의 확률 진폭이 모두 `+` 부호를 가진다. 이 부호 관계를 `+,+`로 표시한다. 오라클 A처럼 $f(0)=f(1)=0$이면 두 항 모두 `+` 표식을 받아 이 관계가 그대로 유지된다. 반면 오라클 B는 $f(0)=0$, $f(1)=1$이므로 $x=0$ 항에는 `+`, $x=1$ 항에는 `-`를 남긴다. 그래서 부호 관계가 `+,+`에서 `+,-`로 바뀐다.

:::expander 오라클의 함수값이 첫 큐비트의 위상 표식이 되는 과정을 수식으로 확인하기

### 1. 보조 큐비트의 `|->`를 두 항으로 푼다

보조 큐비트는 다음 상태로 준비되어 있다.

$$
\lvert-\rangle_2
=\frac{\lvert0\rangle-\lvert1\rangle}{\sqrt{2}}
$$

아래 첨자 `2`는 두 번째 큐비트라는 표시다. 오라클을 두 항에 각각 적용하면 다음과 같다.

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

여기서 $y\oplus f(x)$와 $(-1)^{f(x)}$가 같은 값이라는 뜻은 아니다. 앞의 식은 보조 큐비트의 값, 뒤의 식은 잠시 뒤 두 큐비트의 해당 상태 항 전체에 곱해지는 부호다.

### 2. $f(x)=0$과 $f(x)=1$을 직접 넣어 본다

먼저 직접 확인해 볼 수 있다.

- $f(x)=0$이면 $0\oplus0$과 $1\oplus0$은 무엇인가?
- $f(x)=1$이면 $0\oplus1$과 $1\oplus1$은 무엇인가?

힌트: XOR에 `0`을 넣으면 그대로이고, `1`을 넣으면 `0`과 `1`이 서로 바뀐다.

$f(x)=0$이면 두 항의 순서가 그대로다.

$$
\frac{
\lvert0\oplus0\rangle-\lvert1\oplus0\rangle
}{\sqrt{2}}
=
\frac{\lvert0\rangle-\lvert1\rangle}{\sqrt{2}}
=\lvert-\rangle
$$

$f(x)=1$이면 두 항의 순서가 바뀐다.

$$
\frac{
\lvert0\oplus1\rangle-\lvert1\oplus1\rangle
}{\sqrt{2}}
=
\frac{\lvert1\rangle-\lvert0\rangle}{\sqrt{2}}
=-\frac{\lvert0\rangle-\lvert1\rangle}{\sqrt{2}}
=-\lvert-\rangle
$$

이 두 경우를 짧게 묶을 때 $X^{f(x)}$라는 표기를 쓴다. `X`는 `0`과 `1`을 뒤집는 게이트다.

$$
X^{f(x)}
=
\begin{cases}
X^0=I, & f(x)=0\\
X^1=X, & f(x)=1
\end{cases}
$$

즉, $X^{f(x)}$는 새로운 연산을 갑자기 도입한 것이 아니라 “함수값이 0이면 그대로, 1이면 X 적용”을 한 기호로 줄여 쓴 것이다. 따라서 위의 두 계산을 한 줄로 쓰면 다음과 같다.

$$
X^{f(x)}\lvert-\rangle_2
=(-1)^{f(x)}\lvert-\rangle_2
$$

이를 첫 큐비트까지 포함해 쓰면 위상 킥백 식이 된다.

$$
U_f\lvert x\rangle_1\lvert-\rangle_2
=(-1)^{f(x)}
\lvert x\rangle_1\lvert-\rangle_2
$$

오라클이 첫 큐비트를 직접 뒤집은 것은 아니다. `-1`은 두 큐비트의 해당 상태 항 전체에 곱해진 수다. 보조 큐비트는 다시 `|->` 상태로 정리되므로, 이 부호를 첫 큐비트의 해당 기저 상태 항에 남은 상대위상으로 나타낼 수 있다.

### 3. 첫 큐비트의 `|+>`도 두 기저 상태 항으로 푼다

오라클 직전의 두 큐비트는 다음 상태다.

$$
\lvert+\rangle_1\lvert-\rangle_2
=
\frac{\lvert0\rangle_1+\lvert1\rangle_1}{\sqrt{2}}
\otimes
\frac{\lvert0\rangle_2-\lvert1\rangle_2}{\sqrt{2}}
$$

첫 큐비트의 `|+>`는 $x=0$에 해당하는 항과 $x=1$에 해당하는 항으로 이루어져 있다. 위상 킥백 식을 각 항에 적용하면 다음과 같다.

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

### 예: 오라클 B를 대입해 본다

오라클 B는 $f(0)=0$, $f(1)=1$이다.

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

즉, 첫 큐비트는

$$
\lvert+\rangle_1
=\frac{\lvert0\rangle_1+\lvert1\rangle_1}{\sqrt{2}}
\quad\longrightarrow\quad
\lvert-\rangle_1
=\frac{\lvert0\rangle_1-\lvert1\rangle_1}{\sqrt{2}}
$$

로 바뀌고, 보조 큐비트는 계속 $\lvert-\rangle_2$로 남는다. 오라클 전 첫 큐비트의 `|+>`는 `+,+`이고, $f(0)=f(1)=0$인 오라클이라면 이 부호가 그대로 유지된다. 오라클 B에서는 $x=1$ 항에만 `-`가 붙으므로 `+,-`로 바뀐다. 이것이 본문에서 설명한 위상 표식 변화다.

:::

## 7. 마지막 H가 숨은 표식을 측정값으로 바꾼다

오라클은 첫 큐비트의 두 기저 상태 항에 `+` 또는 `-` 위상 표식을 남긴다.

- constant 규칙은 $f(0)$과 $f(1)$이 같으므로 두 표식도 같다: `+,+` 또는 `-,-`
- balanced 규칙은 $f(0)$과 $f(1)$이 다르므로 두 표식이 반대다: `+,-` 또는 `-,+`

마지막 H를 적용하면 두 항의 부호 관계가 확률 차이로 바뀐다. 표식이 같으면 `0` 쪽 진폭은 더해지고 `1` 쪽 진폭은 상쇄되어 결과 `0`이 나온다. 표식이 반대면 반대로 `1` 쪽 진폭만 남아 결과 `1`이 나온다. 따라서 최종 측정은 다음처럼 결정된다.

$$
0\Rightarrow\text{constant},\qquad
1\Rightarrow\text{balanced}
$$

:::expander 같은 위상 표식은 0, 반대 위상 표식은 1이 되는 과정을 수식으로 확인하기

첫 큐비트의 두 기저 상태 항에 같은 `+` 표식이 있으면 `|+>` 상태이고, 반대 표식이 있으면 `|->` 상태다.

$$
\lvert+\rangle
=\frac{\lvert0\rangle+\lvert1\rangle}{\sqrt{2}},
\qquad
\lvert-\rangle
=\frac{\lvert0\rangle-\lvert1\rangle}{\sqrt{2}}
$$

H는 이 두 상태를 서로 다른 계산 기저 결과로 바꾼다.

$$
H\lvert+\rangle=\lvert0\rangle,\qquad
H\lvert-\rangle=\lvert1\rangle
$$

$f(0)=f(1)=1$인 constant 규칙은 두 항에 모두 `-` 표식을 남긴다.

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

따라서 마지막 H 뒤에는 $-\lvert0\rangle$이 된다. 상태 전체에 붙은 `-`는 전역 위상이라 측정 확률을 바꾸지 않으므로 결과는 여전히 `0`이다.

마찬가지로 `-,+`는 $-\lvert-\rangle$이며 마지막 H 뒤에 $-\lvert1\rangle$이 된다. 전역 위상을 무시하면 측정 결과는 `1`이다.

:::

시뮬레이션에서 오라클 직후와 마지막 H 직후의 확률을 비교해 보면 된다. 오라클 직후에는 두 확률이 반반이라 위상 표식이 보이지 않지만, 마지막 H에서 진폭이 더해지고 상쇄되면서 한쪽 결과의 확률이 100%가 된다.

## 8. 작은 예제이지만 중요한 이유가 있다

Deutsch 문제는 실생활의 거대한 문제를 푸는 알고리즘이 아니다. 확정적인 고전 알고리즘의 오라클 호출 2번을 양자 회로가 1번으로 줄이는 교육용 예제다.

이 작은 차이를 실제 양자컴퓨터 전체의 속도 향상으로 확대해서 이해하면 안 된다. 중요한 점은 “중첩으로 모든 답을 꺼낸다”가 아니라 “오라클이 남긴 관계를 간섭으로 읽는다”는 사고방식이다.

이 앱에서는 Deutsch-Jozsa 회로의 입력 1비트 버전을 Deutsch 알고리즘으로 다룬다. 더 큰 양자 알고리즘이 모두 이 회로와 똑같이 작동하는 것은 아니다. 하지만 문제의 특징을 위상이나 진폭에 담고, 간섭으로 필요한 정보를 측정 가능한 결과로 바꾸는 흐름은 여러 알고리즘에서 다시 등장한다.

예를 들어 Grover 탐색은 정답 후보에 위상 표식을 붙인 뒤 진폭 증폭(amplitude amplification)을 반복한다. 그러면 정답 상태의 확률 진폭이 커지고, 마지막에 정답이 측정될 확률도 높아진다. 여기서 익힌 “부호를 표시하고 간섭으로 결과 확률을 바꾼다”는 개념이 더 큰 알고리즘으로 이어지는 대표적인 예다.
