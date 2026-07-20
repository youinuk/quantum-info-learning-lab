# Quantum Notation and Bit-Order Conventions

이 문서는 학습 화면, 내부 시뮬레이터, 향후 Qiskit/Cirq 어댑터가 함께 지켜야 하는 기준이다.

## 회로와 연산자 순서

- 회로의 시간은 왼쪽에서 오른쪽으로 흐른다.
- 켓에 곱한 연산자는 오른쪽에서 왼쪽으로 작용한다.
- 회로에서 X 다음 Z를 적용하면 시간 순서는 `X -> Z`, 식은 $ZX\lvert\psi\rangle$이다.
- 일반적으로 회로의 시간 순서가 $U_1,U_2,\ldots,U_n$이면 최종 상태는 $U_n\cdots U_2U_1\lvert\psi\rangle$이다.

`core.quantum_conventions.operator_product_for_time_order()`가 이 변환을 담당한다. 화면의 게이트 목록은 시간 순서로 보관하고, 연산자 라벨이 필요할 때만 역순으로 조합한다.

## 앱의 큐비트와 기저 순서

앱은 학습자가 회로와 결과를 같은 방향으로 읽도록 다음 big-endian 표시 순서를 사용한다.

- 위에서 아래로 큐비트를 $q_0,q_1,\ldots$로 부른다.
- 켓과 결과 문자열은 $\lvert q_0q_1\cdots\rangle$ 순서로 쓴다.
- 왼쪽 $q_0$가 가장 큰 자리이고 마지막 큐비트가 가장 작은 자리다.
- 두 큐비트의 기저 및 상태벡터 순서는 `00`, `01`, `10`, `11`이다.
- 따라서 `basis_index("10") == 2`이고, `np.kron(q0, q1)`의 순서와 일치한다.

Deutsch 회로에서는 첫 큐비트가 $x$, 두 번째가 $y$이므로 $\lvert xy\rangle$의 인덱스는 `2*x + y`와 같다. 양자전송의 Alice 비트 $ab$도 위쪽 입력 측정 $a$, 아래쪽 Bell A 측정 $b$ 순서로 표시한다.

## Qiskit과 Cirq 경계

외부 SDK의 문자열을 앱 결과처럼 바로 표시하면 안 된다.

- Qiskit 회로 그림은 보통 $q_0$를 위에 그리지만, 비트 문자열은 $q_0$를 오른쪽의 최소 유효 비트로 둔다. Qiskit count를 앱에 넣을 때는 측정 매핑을 확인하고 앱의 $q_0q_1\cdots$ 순서로 변환한다.
- Cirq 상태벡터는 지정한 `qubit_order`에 대해 NumPy Kronecker 곱의 big-endian 순서를 사용한다. 어댑터에서 `qubit_order=[q0, q1, ...]`를 명시한다.
- SDK 예제와 실제 하드웨어 결과에는 변환 함수를 한 곳에 두고, 회로별 임시 문자열 뒤집기를 만들지 않는다.

공식 참고 자료:

- [IBM Quantum: Bit ordering in the Qiskit SDK](https://quantum.cloud.ibm.com/docs/en/guides/bit-ordering)
- [Google Quantum AI: Cirq simulation and qubit ordering](https://quantumai.google/cirq/simulate/simulation)

## 검증 기준

- `basis_labels(2)`는 `("00", "01", "10", "11")`이다.
- 시간 순서 `("X", "Z")`의 연산자 라벨은 `ZX`이다.
- 양자전송에서 `ab=11`이면 Bob의 보정 전 상태는 $XZ\lvert\psi\rangle$, 보정은 시간 순서 X 다음 Z, 즉 연산자 $ZX$이다.
- 초밀집 부호화의 메시지 `11`도 시간 순서 X 다음 Z를 사용하고 Bell $\lvert\Psi^-\rangle$로 간다. XZ와 ZX의 전역 부호 차이는 측정 결과를 바꾸지 않지만, 앱 표기는 시간 순서 규칙에 따라 `ZX`로 통일한다.
