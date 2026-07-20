## 1. 얽힘만으로는 안 되지만 얽힘은 쓸모가 있다

Level 12에서는 Bob이 자기 결과만 보고 Alice의 선택을 알아낼 수 없다는 점을 확인했다. 얽힘만으로는 원하는 메시지를 보낼 수 없다.

하지만 얽힘에 실제로 전달되는 정보를 함께 사용하면 특별한 프로토콜을 만들 수 있다. 이번 레벨에서는 두 가지를 비교한다.

- 양자전송: 고전 비트 2개를 보내 미지의 양자 상태를 복원한다.
- 초밀집 부호화: 큐비트 1개를 보내 고전 비트 2개를 복원한다.

두 프로토콜 모두 Alice와 Bob이 Bell 쌍을 미리 하나 공유했다고 가정한다.

## 2. 양자전송은 상태의 정보를 옮긴다

Alice에게 미지의 상태 $\lvert\psi\rangle$가 있고, Bob에게 그 상태를 전달하고 싶다고 하자. 입자 자체를 보내는 대신 다음 자원을 사용한다.

$$
\lvert\psi\rangle=\alpha\lvert0\rangle+\beta\lvert1\rangle,
\qquad
\lvert\alpha\rvert^2+\lvert\beta\rvert^2=1
$$

| 미리 공유한 자원 | Alice가 실제로 보내는 것 | Bob이 얻는 것 |
|---|---|---|
| Bell 쌍 1개 | 고전 비트 2개 | 원래의 양자 상태 $\lvert\psi\rangle$ |

여기서 “미지의 상태”는 Alice가 $\alpha$, $\beta$를 모르는 임의의 상태까지 포함한다. 한 큐비트를 측정하면 한 번의 결과만 얻고 원래 중첩도 바뀌므로, 그 결과만 보고 $\alpha$, $\beta$를 모두 알아내 다시 만들 수 없다.

$\alpha$와 $\beta$는 일반적으로 복소수다. 전체 위상을 정리해 $\alpha$를 실수·양수로 두면 $\beta=e^{i\phi}\lvert\beta\rvert$로 쓸 수 있다. 따라서 시뮬레이션은 $\lvert\alpha\rvert$와 상대위상 $\phi$를 조절하고, $\lvert\beta\rvert=\sqrt{1-\lvert\alpha\rvert^2}$는 자동으로 계산한다.

복제 불가능 정리(no-cloning theorem)는 미지의 임의 상태를 원본까지 남긴 채 완벽하게 복사하는 공통 양자 연산이 존재하지 않는다는 뜻이다. 이미 만드는 법을 아는 $\lvert0\rangle$이나 $\lvert+\rangle$를 여러 번 준비하는 것과, 하나뿐인 미지의 상태를 복제하는 것은 다른 문제다. 양자전송은 원본을 복제하지 않고 Alice 쪽 상태를 측정으로 없애면서 Bob 쪽에 복원한다.

:::expander 왜 CNOT으로 모든 상태를 복사할 수 없는지 수식으로 확인하기 (클릭)
CNOT은 첫 번째 큐비트가 $\lvert0\rangle$ 또는 $\lvert1\rangle$인 경우, 그 값을 처음에 $\lvert0\rangle$으로 둔 두 번째 큐비트로 옮길 수 있다. 여기서는 첫 번째 큐비트가 control, 두 번째 큐비트가 target이다.

$$
\lvert0\rangle\lvert0\rangle\longrightarrow\lvert0\rangle\lvert0\rangle,
\qquad
\lvert1\rangle\lvert0\rangle\longrightarrow\lvert1\rangle\lvert1\rangle
$$

하지만 같은 연산에 $\lvert+\rangle=(\lvert0\rangle+\lvert1\rangle)/\sqrt{2}$를 넣으면 선형성 때문에 다음 상태가 된다.

$$
\lvert+\rangle\lvert0\rangle
\longrightarrow
\frac{\lvert00\rangle+\lvert11\rangle}{\sqrt{2}}
$$

정말 두 복사본이 생겼다면 결과는 다음과 같아야 한다.

$$
\lvert+\rangle\lvert+\rangle
=\frac{\lvert00\rangle+\lvert01\rangle+\lvert10\rangle+\lvert11\rangle}{2}
$$

두 식은 다르다. 특정 기저 상태의 값을 복사하는 CNOT이 임의의 중첩까지 복제하지는 못하며, 다른 하나의 공통 연산으로 이 문제를 해결할 수도 없다.
:::

## 3. 준비 장치와 양자전송 회로를 나누어 읽는다

![양자전송 회로](assets/images/level13_teleportation_circuit.svg)

1. 왼쪽 Bell-pair preparation은 Alice가 입력 상태를 다루기 전에, 두 $\lvert0\rangle$ 상태에서 H와 CNOT으로 Bell 쌍을 준비하는 과정이다.
2. Bell A는 Alice에게, Bell B는 Bob에게 전달된다. 미지의 입력 $\lvert\psi\rangle$는 이때 Alice 구역에서 시작한다.
3. Alice가 입력 큐비트를 제어로 하는 CNOT을 적용하고, 입력 큐비트에 H를 적용한다.
4. 위 입력 큐비트의 측정값을 $a$, 아래 Bell A의 측정값을 $b$로 읽어 Bob에게 보낸다.
5. Bob은 $b=1$이면 $X$, $a=1$이면 $Z$를 적용한다. 11이면 회로에서 X를 먼저, Z를 나중에 적용하므로 전체 연산은 $ZX$이다.

Alice의 측정 결과 `00`, `01`, `10`, `11`은 각각 같은 확률로 나올 수 있다. Alice가 원하는 결과를 고르는 것은 아니지만, 어느 결과가 나와도 알맞게 보정하면 같은 입력 상태가 복원된다.

## 4. 구체적인 상태 하나를 보내 본다

Alice가 보내려는 입력이 다음과 같은 $\lvert+\rangle$ 상태라고 하자.

$$
\lvert+\rangle=\frac{\lvert0\rangle+\lvert1\rangle}{\sqrt{2}}
$$

Alice의 측정 결과가 `10`이라면 Bob의 보정 전 상태에는 `Z` 효과가 남아 $\lvert-\rangle$처럼 보인다.

$$
Z\lvert+\rangle=\lvert-\rangle
$$

Alice가 보낸 비트 `10`을 받은 Bob은 `Z`를 적용한다.

$$
Z\lvert-\rangle=\lvert+\rangle
$$

따라서 Bob은 Alice가 본래 보내려 한 $\lvert+\rangle$ 상태를 얻는다. Alice의 입자 자체가 이동한 것은 아니지만, Bob의 큐비트 상태가 처음 입력과 같아졌다.

수식이 어렵다면 “Alice의 두 비트가 Bob에게 어떤 보정을 해야 하는지 알려 준다”는 뜻만 잡으면 된다. 시뮬레이션에서는 네 측정 결과를 모두 확인할 수 있다.

:::expander 임의 상태가 네 측정 결과에서 복원되는 과정을 수식으로 따라가기 (클릭)
입력을 다음처럼 두고 큐비트 순서를 입력 $Q$, Bell A, Bell B로 쓴다.

$$
\lvert\psi\rangle_Q=\alpha\lvert0\rangle+\beta\lvert1\rangle,
\qquad
\lvert\Phi^+\rangle_{AB}=\frac{\lvert00\rangle+\lvert11\rangle}{\sqrt{2}}
$$

Alice의 CNOT과 H를 지난 상태가 왜 네 갈래로 나뉘는지 처음 상태부터 계산해 본다. 마지막에는 앞의 두 큐비트 $QA$가 같은 항끼리 묶을 것이다.

먼저 세 큐비트의 처음 상태를 $QAB$ 순서로 직접 펼친다.

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

Alice의 CNOT은 $Q=1$인 항에서만 A를 뒤집는다. 따라서 $100\rightarrow110$, $111\rightarrow101$이고, $Q=0$인 앞의 두 항은 그대로다.

$$
\lvert\Psi_1\rangle
=\frac{1}{\sqrt{2}}\big(
\alpha\lvert000\rangle+
\alpha\lvert011\rangle+
\beta\lvert110\rangle+
\beta\lvert101\rangle
\big)
$$

이제 첫 큐비트 Q에 H를 적용한다.

$$
H\lvert0\rangle=\frac{\lvert0\rangle+\lvert1\rangle}{\sqrt{2}},
\qquad
H\lvert1\rangle=\frac{\lvert0\rangle-\lvert1\rangle}{\sqrt{2}}
$$

각 항에 이를 대입하면 다음 여덟 항이 나온다.

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

이제 앞의 두 자리 $QA$가 같은 항끼리 모은다. 예를 들어 $QA=01$인 항을 $\alpha$ 항부터 쓰면 $\alpha\lvert011\rangle+\beta\lvert010\rangle$이다. Bob의 B만 떼어 쓰면 $\lvert01\rangle(\alpha\lvert1\rangle+\beta\lvert0\rangle)$이 되어 $X\lvert\psi\rangle$의 모양이 바로 보인다.

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

실제로 $X\lvert\psi\rangle=\alpha\lvert1\rangle+\beta\lvert0\rangle$이고, $XZ\lvert\psi\rangle=\alpha\lvert1\rangle-\beta\lvert0\rangle$이다. 따라서 괄호 안 네 상태는 차례로 $\lvert\psi\rangle$, $X\lvert\psi\rangle$, $Z\lvert\psi\rangle$, $XZ\lvert\psi\rangle$이며, 위 식을 짧게 쓰면 다음 결과가 된다.

$$
\frac{1}{2}\Big[
\lvert00\rangle\lvert\psi\rangle
+\lvert01\rangle X\lvert\psi\rangle
+\lvert10\rangle Z\lvert\psi\rangle
+\lvert11\rangle XZ\lvert\psi\rangle
\Big]
$$

따라서 Alice가 측정한 $ab$와 Bob의 상태 및 보정은 다음과 같다. 이 앱에서 $a$는 위쪽 입력 $Q$의 측정값, $b$는 그 아래 Bell A의 측정값이다. 즉 $ab$도 위에서 아래로 읽는 big-endian 표시다.

| $ab$ | Bob의 보정 전 상태 | Bob의 보정 |
|---|---|---|
| 00 | $\lvert\psi\rangle$ | $I$ |
| 01 | $X\lvert\psi\rangle$ | $X$ |
| 10 | $Z\lvert\psi\rangle$ | $Z$ |
| 11 | $XZ\lvert\psi\rangle$ | $ZX$ |

$ZX\lvert\psi\rangle$는 회로에서 X를 먼저 적용하고 Z를 나중에 적용한다는 뜻이다. 식에서는 오른쪽의 X가 먼저, 왼쪽의 Z가 나중에 작용하기 때문이다. 그래서 마지막 경우에는 $ZX(XZ\lvert\psi\rangle)=\lvert\psi\rangle$가 되어 원래 상태가 복원된다.
:::

## 5. 양자전송은 순간이동 장치가 아니다

양자전송이라는 이름 때문에 물질이 사라졌다가 나타난다고 생각하기 쉽지만, 실제로 옮겨지는 것은 양자 상태의 정보다.

- Bell 쌍은 프로토콜 전에 미리 분배되어 있어야 한다.
- Bob은 Alice의 고전 비트 2개가 도착하기 전에는 어떤 보정을 할지 모른다.
- 고전 정보는 빛보다 빠르게 전달되지 않는다.
- Alice의 원래 상태는 측정 뒤 그대로 남지 않으므로 복제본이 두 개 생기지 않는다.

따라서 양자전송은 무신호성과 복제 불가능 원리를 어기지 않는다.

## 6. 초밀집 부호화는 고전 비트 두 개를 보낸다

![초밀집 부호화 회로](assets/images/level13_superdense_coding_circuit.svg)

이번에는 Alice가 고전 메시지 `00`, `01`, `10`, `11` 중 하나를 Bob에게 보내려 한다.

1. 별도의 준비 과정에서 두 $\lvert0\rangle$ 상태에 H와 CNOT을 적용해 Bell 쌍을 만든 뒤 Alice와 Bob에게 하나씩 나누어 준다.
2. Alice는 메시지에 따라 자기 큐비트에 $I$, $X$, $Z$, 또는 $ZX$를 적용한다. $ZX$는 X를 먼저, Z를 나중에 적용한다는 뜻이다.
3. Alice는 조작한 큐비트 한 개를 Bob에게 실제로 보낸다.
4. Bob은 두 큐비트를 CNOT과 H로 풀어 측정하고 고전 비트 2개를 읽는다.

얽힘을 미리 공유하지 않았다면 큐비트 하나를 보내 확실한 고전 비트 두 개를 이런 방식으로 구분할 수 없다.

:::expander 네 부호화가 Bell 상태와 측정 비트로 바뀌는 과정을 따라가기 (클릭)
준비 장치가 만든 상태는 다음과 같다.

$$
\lvert\Phi^+\rangle=\frac{\lvert00\rangle+\lvert11\rangle}{\sqrt{2}}
$$

Alice가 첫 번째 큐비트에 연산하면 네 메시지가 네 Bell 상태로 바뀐다.

$$
\begin{aligned}
I\lvert\Phi^+\rangle&=\lvert\Phi^+\rangle,\\
X\lvert\Phi^+\rangle&=\frac{\lvert10\rangle+\lvert01\rangle}{\sqrt{2}}=\lvert\Psi^+\rangle,\\
Z\lvert\Phi^+\rangle&=\frac{\lvert00\rangle-\lvert11\rangle}{\sqrt{2}}=\lvert\Phi^-\rangle,\\
ZX\lvert\Phi^+\rangle&=\frac{\lvert01\rangle-\lvert10\rangle}{\sqrt{2}}=\lvert\Psi^-\rangle.
\end{aligned}
$$

Bob의 CNOT과 H는 Bell 쌍을 만든 준비 회로를 거꾸로 푸는 Bell 디코더 역할을 한다. 네 Bell 상태가 왜 00, 01, 10, 11로 바뀌는지 게이트 순서를 거꾸로 따라가 본다.

Bell 준비 회로는 첫 큐비트에 H를 적용한 뒤 CNOT을 적용한다.

$$
U_{\text{prepare}}=\operatorname{CNOT}(H\otimes I)
$$

H와 CNOT은 각각 자기 자신의 역연산이므로, 준비를 푸는 디코더는 순서를 뒤집어 CNOT을 먼저, H를 나중에 적용한다.

$$
U_{\text{decode}}=(H\otimes I)\operatorname{CNOT}
$$

위 식에서도 오른쪽 CNOT이 먼저 작용한다. CNOT을 네 Bell 상태에 적용하면 다음처럼 첫 큐비트의 $\lvert+\rangle$ 또는 $\lvert-\rangle$와 둘째 큐비트의 0 또는 1로 분리된다.

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

마지막 H는 $H\lvert+\rangle=\lvert0\rangle$, $H\lvert-\rangle=\lvert1\rangle$로 바꾼다. 따라서 디코더 전체 결과가 다음처럼 한 줄씩 대응한다.

$$
\begin{aligned}
\lvert\Phi^+\rangle&\longrightarrow\lvert00\rangle, &
\lvert\Psi^+\rangle&\longrightarrow\lvert01\rangle,\\
\lvert\Phi^-\rangle&\longrightarrow\lvert10\rangle, &
\lvert\Psi^-\rangle&\longrightarrow\lvert11\rangle.
\end{aligned}
$$

즉 Bob이 Bell 상태의 이름을 미리 알아맞히는 것이 아니다. Bell 디코더가 네 Bell 상태를 서로 다른 계산 기저 상태로 바꾸기 때문에, 평범한 측정으로 Alice의 두 비트를 읽을 수 있다.
:::

## 7. 네 메시지는 네 Bell 상태로 표시된다

Alice의 조작은 공유 Bell 쌍을 서로 구별되는 네 상태로 바꾼다.

| 보낼 비트 | Alice의 조작 | 만들어지는 Bell 상태 | Bob의 측정 |
|---|---|---|---|
| 00 | I | $\lvert\Phi^+\rangle$ | 00 |
| 01 | X | $\lvert\Psi^+\rangle$ | 01 |
| 10 | Z | $\lvert\Phi^-\rangle$ | 10 |
| 11 | $ZX$ | $\lvert\Psi^-\rangle$ | 11 |

여기서 `I`는 아무 조작도 하지 않는다는 뜻이다. Bob은 Alice가 보낸 큐비트와 자기가 가지고 있던 큐비트를 함께 측정해야 메시지를 구분할 수 있다.

결과적으로 Bob의 측정값은 Alice가 보내려 한 두 비트와 정확히 같다. 예를 들어 Alice가 `10`을 고르면 Bell 디코더 뒤에서 Bob은 `10`을 얻는다.

## 8. 두 프로토콜은 상보적이다

| 프로토콜 | 입력 | 미리 공유 | 실제 전송 | 출력 |
|---|---|---|---|---|
| 양자전송 | 미지의 큐비트 상태 1개 | Bell 쌍 1개 | 고전 비트 2개 | 큐비트 상태 1개 |
| 초밀집 부호화 | 고전 비트 2개 | Bell 쌍 1개 | 큐비트 1개 | 고전 비트 2개 |

두 회로는 Bell 쌍을 만들고 푸는 구조를 공유해 서로 거꾸로 보이는 부분이 있다. 하지만 목표와 실제 전송 자원이 다르므로 “완전히 같은 회로를 뒤집은 것”이라고만 이해하면 안 된다.

얽힘만으로는 메시지를 보낼 수 없다. 고전 비트나 실제로 전송하는 큐비트와 결합하면, 얽힘은 가능한 정보 전달 방식을 바꾸는 공유 자원으로 쓰인다.
