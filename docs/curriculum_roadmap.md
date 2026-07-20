# Quantum Lab 교육과정 및 구현 로드맵

이 문서는 학습앱의 교육 순서와 다음 구현 범위를 함께 관리하는 단일 기준 문서다. 실험 ID와 코드·원고·그림의 연결은 [실험 레지스트리](experiment_registry.md), Photon Heist의 별도 확장 계획은 [Photon Heist 확장 로드맵](photon_heist_roadmap.md)에서 관리한다.

## 대상과 학습 원칙

- 주 대상은 양자정보를 처음 접하는 고등학생과 일반 학습자다.
- 수식은 현상을 설명하는 도구로 사용하며, 수식 없이도 핵심 의미를 따라갈 수 있게 한다.
- 새 개념은 설명, 회로 또는 그림, 구체적 예시, 시뮬레이션, 퀴즈의 순환 구조로 익힌다.
- 실제 하드웨어와 SDK는 추상 회로를 이해한 뒤 연결한다.
- 특정 기업이나 하드웨어 방식의 우열을 단정하지 않는다.
- 고급 과정은 하나의 긴 직선 과정이 아니라 알고리즘, 오류정정, 응용의 여러 갈래로 제공한다.

## 현재 공개된 기초·중급 과정

| 구간 | 레벨 | 핵심 질문 |
|---|---|---|
| 고전 확률에서 큐비트로 | 0-2 | 확률, 중첩, 측정을 어떻게 구분하는가? |
| 상태를 바꾸고 연결하기 | 3-6 | 게이트, 간섭, 두 큐비트, 얽힘은 어떻게 작동하는가? |
| 실험 결과 읽기 | 7-10 | 노이즈, 회로, 통계, 위상을 어떻게 해석하는가? |
| 가능성과 한계 | 11-12 | 간섭으로 규칙을 읽고, 얽힘의 정보 한계를 어떻게 이해하는가? |
| 얽힘을 정보 자원으로 쓰기 | 13 | 양자 상태와 고전 정보를 어떤 자원으로 전달하는가? |

Level 12까지 마치면 간단한 회로와 측정 결과를 읽을 수 있다. 그러나 고급 알고리즘으로 바로 넘어가기 전에 다음 연결 경험이 더 필요하다.

1. 얽힘이 실제 정보 프로토콜에서 어떻게 쓰이는가?
2. 양자암호는 암호화, 키 분배, 양자내성암호와 어떻게 다른가?
3. 여러 장치 사이에서 얽힘을 어떻게 분배하고 유지하는가?
4. 추상 회로가 실제 장비의 연결 구조와 노이즈 제약을 어떻게 만나는가?
5. 앱의 시뮬레이터와 실제 SDK·QPU 실행은 무엇이 다른가?

Level 13은 첫 번째 연결 경험을 구현한다. 이어서 고급 과정 전에 Level 14-18의 나머지 **응용·현실 연결 트랙**을 완성한다.

## 응용·현실 연결 트랙

### Level 13 · 양자전송과 초밀집 부호화 [구현 완료]

핵심 질문: 공유한 얽힘은 양자 상태와 고전 정보를 전달할 때 어떤 자원으로 쓰이는가?

선수 레벨: 3, 6, 8, 12

학습 내용:

- 이동하는 것은 물질이 아니라 양자 상태의 정보라는 점
- 미리 공유한 Bell 쌍, Alice의 Bell 측정, 고전 비트 2개, Bob의 조건부 `X`와 `Z`
- 복제 불가능 정리와 CNOT이 임의의 중첩을 복제하지 못하는 선형성 예시
- 원래 상태가 Alice 쪽에 복사본으로 남지 않는다는 점
- 고전 통신이 필요하므로 빛보다 빠른 정보 전달이 아니라는 점
- 초밀집 부호화에서는 Alice가 $I$, $X$, $Z$, $ZX$ 중 하나로 고전 비트 2개를 표시한다는 점
- 공유한 Bell 쌍과 큐비트 1개 전송으로 Bob이 고전 비트 2개를 읽는 과정
- 두 프로토콜은 같은 얽힘 자원을 서로 상보적인 정보 전달에 사용한다는 점

최소 구현:

- 입력 상태 `|0⟩`, `|1⟩`, `|+⟩`, `|−⟩`, `|+i⟩`, `|−i⟩` 선택과 $|\alpha|$, $\beta=e^{i\phi}|\beta|$의 상대위상을 조절하는 임의 순수 상태 입력. $|\beta|$는 정규화로 자동 계산
- Bell 쌍 준비, Alice 측정, 고전 비트 전달, Bob 보정의 단계별 회로
- Alice의 무작위 측정 비트를 보고 학습자가 Bob의 $I$, $X$, $Z$, $ZX$ 보정을 직접 선택하는 실험과 결과 누적표
- 고전 비트 도착 전과 보정 후의 상태 비교
- 초밀집 부호화 게이트만 바꾸며 Bell 상태와 복원 비트의 대응표를 완성하는 탐색 실험
- 앱이 무작위로 제시한 2비트 목표에 맞춰 Alice의 부호화 게이트를 고르는 전송 미션
- 두 프로토콜의 입력 정보, 전송 자원, 출력 정보를 나란히 비교하는 표
- 물질 이동, 복제, 초광속 통신에 관한 오해 확인 퀴즈

경계:

- 임의의 복소수 상태에 대한 전체 유도는 접기 영역으로 둔다.
- 충실도는 먼저 “원래 상태와 얼마나 비슷한가”로 설명한다.
- “완전히 같은 회로의 단순 역과정”이라고 단정하지 않고 자원 교환 관계를 중심으로 비교한다.

구현 실험 ID: `EXP-COM01`, `EXP-COM02`, `EXP-COM03`

### Level 14 · 양자암호와 BB84

핵심 질문: 측정하면 상태가 달라질 수 있다는 성질을 안전한 키 분배에 어떻게 사용하는가?

선수 레벨: 2, 4, 12

학습 내용:

- 암호화와 키 분배의 역할 차이
- BB84의 비트, Z/X 기준, 기준 공개, 키 선별
- 도청자가 기준을 추측해 측정하면 QBER가 증가하는 이유
- QKD는 메시지를 직접 암호화하는 완성품이 아니라 공유 키를 만드는 한 단계라는 점
- 인증된 고전 채널이 없으면 중간자 공격을 막을 수 없다는 점
- 양자암호와 양자내성암호(PQC)는 서로 다른 접근이라는 점

최소 구현:

- Alice의 비트·기준과 Bob의 기준 기록표
- 도청자 없음, 가로채서 측정, 재전송 비교
- 기준 선별 후 남은 키 길이와 QBER 표시
- 20회 사례와 200회 통계를 분리해 표시
- QKD, 일반 암호화, PQC를 구분하는 비교 카드

경계:

- 완전한 보안 증명, 프라이버시 증폭, 실제 장비의 부채널 공격은 심화 자료로 둔다.
- “도청을 무조건 막는다”가 아니라 “도청 흔적을 통계적으로 검사한다”고 설명한다.

예정 실험 ID: `EXP-CRYPTO01`, `EXP-CRYPTO02`

### Level 15 · 양자네트워크

핵심 질문: 멀리 떨어진 장치들이 양자 상태와 얽힘을 어떻게 나누는가?

선수 레벨: 6, 12, 13, 14

학습 내용:

- 양자 채널과 고전 채널의 역할
- 광자 손실과 거리 증가가 만드는 문제
- 직접 전송, 중간 노드, 얽힘 교환의 차이
- 양자 중계기가 단순 신호 증폭기와 다른 이유
- 양자 네트워크가 고전 인터넷을 대체하기보다 함께 작동한다는 점
- 네트워크 위 양자전송과 초밀집 부호화의 위치

최소 구현:

- Alice, 중간 노드, Bob을 연결한 네트워크 지도
- 거리와 손실률에 따른 직접 전송 성공률 비교
- 두 짧은 얽힘 링크를 연결하는 얽힘 교환 단계 그림
- 고전 메시지가 도착하기 전후의 프로토콜 상태 표시
- 직접 전송과 중계 경로의 장단점 비교

경계:

- 양자 메모리와 중계기의 세부 물리 구현은 자료실에서 소개한다.
- 얽힘 교환이 초광속 통신을 허용한다는 표현을 사용하지 않는다.

예정 실험 ID: `EXP-NET01`, `EXP-NET02`

### Level 16 · 오류를 찾고 줄이는 방법

핵심 질문: 양자정보를 직접 읽거나 복사하지 않고 오류의 흔적을 어떻게 찾는가?

선수 레벨: 7, 8, 9

학습 내용:

- 읽기 오류, 비트 뒤집힘, 위상 오류의 차이
- 오류 완화, 오류 검출, 오류 정정의 차이
- 고전 3비트 반복 부호와 다수결
- 물리 큐비트와 논리 큐비트
- 신드롬은 논리 정보가 아니라 오류의 흔적을 읽는다는 생각
- 3큐비트 비트 뒤집힘 부호가 모든 양자 오류를 고치는 것은 아니라는 한계

최소 구현:

- 1비트와 3비트 반복 전송 성공률 비교
- 어느 물리 비트가 뒤집혔는지 추론하는 신드롬 표
- 여러 오류가 생겨 단순 반복 부호가 실패하는 영역 표시
- 정정 전후 성공률과 추가 큐비트 비용 동시 표시

예정 실험 ID: `EXP-EC01`, `EXP-EC02`

### Level 17 · 실제 양자 하드웨어

핵심 질문: 회로 그림의 큐비트와 게이트는 실제 장비에서 무엇으로 구현되고 어떤 제약을 받는가?

선수 레벨: 7, 8, 16

학습 내용:

- 초전도, 이온 트랩, 중성 원자, 광자 방식의 대표 구현을 정성적으로 비교
- 제어 펄스, 기본 게이트, 측정 장치가 추상 회로와 연결되는 과정
- 큐비트 연결성, 결맞음 시간, 게이트 오류, 읽기 오류, 보정 데이터
- 논리 회로를 장비의 기본 게이트와 연결 구조에 맞추는 트랜스파일

최소 구현:

- 3개 또는 5개 물리 큐비트의 연결 지도
- 연결되지 않은 CNOT에 SWAP이 추가되는 단계 그림
- 원래 회로와 변환된 회로의 게이트 수, 깊이, 예상 오류 비교
- 이상적 시뮬레이터와 단순 하드웨어 노이즈 모델 비교

경계:

- 특정 하드웨어 방식의 우열을 단정하지 않는다.
- 실제 장비 수치와 제품명은 자료실에서 최신 출처와 함께 제공한다.

예정 실험 ID: `EXP-HW01`, `EXP-HW02`

### Level 18 · SDK와 실제 실행 맛보기

핵심 질문: 같은 회로를 Qiskit과 Cirq에서 어떻게 표현하고, 시뮬레이터와 실제 장비 실행은 어떻게 다른가?

선수 레벨: 8, 9, 17

학습 내용:

- 큐비트 생성, 게이트, 측정, 반복 실행이 회로와 코드에서 대응되는 방식
- 상태를 계산하는 시뮬레이션과 측정 표본을 얻는 실행의 차이
- Qiskit의 트랜스파일과 IBM QPU 실행 흐름
- Cirq의 `Circuit`, `Simulator`, `Device` 제약과 QVM 개념
- 계정, 대기열, 사용 가능 장비가 외부 서비스 상태에 따라 달라질 수 있다는 점

최소 구현:

- Bell 회로의 앱, Qiskit, Cirq 표현 비교
- 시뮬레이터 결과와 측정 표본 비교
- Qiskit 트랜스파일 결과와 Cirq `Device` 검증 예시
- 별도 노트북 또는 SDK Lab 연결

운영 원칙:

- 기본 `requirements.txt`에는 Qiskit과 Cirq를 넣지 않는다.
- SDK 의존성은 `requirements-sdk.txt` 또는 별도 노트북 환경으로 분리한다.
- 실제 QPU 실행은 계정과 접근 권한이 있을 때만 선택적으로 제공한다.
- 코드 예시는 검증한 버전과 날짜를 함께 기록한다.

예정 실험 ID: `EXP-SDK01`, `EXP-SDK02`

## 선택형 모듈과 진입 시점

선택형 모듈은 Advanced를 모두 마친 다음 단계가 아니다. 아래 선수 개념을 배운 뒤 관심에 따라 본 과정 사이에서 열어 볼 수 있는 독립 모듈이다.

| 선택형 모듈 | 권장 진입 시점 | 핵심 경험 |
|---|---|---|
| CHSH 게임과 Bell 부등식 | Level 12 이후 | 고전적 상관과 양자 상관의 차이 |
| 양자 난수 생성 | Level 2 또는 Level 14 이후 | 측정의 확률성과 검증 가능한 난수의 차이 |
| 양자 센싱과 정밀 측정 | Level 10 또는 Advanced A0 이후 | 작은 위상 차이를 간섭으로 읽기 |
| 양자 화학과 재료 계산 | Advanced ALG3 이후 | 해밀토니안, 에너지 측정, VQE 응용 |

이 모듈들은 전체 레벨 번호를 늘리기보다 자료실, 특별 실험, 짧은 프로젝트 형태로 제공한다.

## 고급 과정 진입 기준

Level 18을 마친 학습자가 다음 질문에 답할 수 있으면 고급 과정으로 넘어간다.

- 진폭과 확률을 구분할 수 있는가?
- H, X, Z, S, CNOT, 측정을 포함한 짧은 회로를 읽고 S가 복소 상대위상을 만든다는 점을 설명할 수 있는가?
- 위상 차이가 간섭 결과를 바꾸는 이유를 설명할 수 있는가?
- 양자전송에 얽힘과 고전 통신이 모두 필요한 이유를 설명할 수 있는가?
- QKD와 PQC, 양자 채널과 고전 채널을 구분할 수 있는가?
- 반복 측정 통계와 장비 오류를 구분할 수 있는가?
- 논리 회로가 실제 장비에 맞게 변환된다는 점을 이해하는가?
- 간단한 회로를 SDK 시뮬레이터에서 실행하고 결과를 읽을 수 있는가?

## 고급 과정

고급 과정은 공통 준비 단원 뒤에 알고리즘, 오류정정, 응용 갈래로 나눈다. 학습자는 관심 있는 갈래부터 선택할 수 있다.

### Advanced A0 · 복소 진폭과 회전

- 복소수의 크기와 위상
- Bloch 구면을 회전 그림으로 읽기
- $R_x$, $R_y$, $R_z$와 위상 게이트
- Pauli 연산과 행렬의 최소 기초
- 회로 깊이, 큐비트 수, 측정 횟수를 자원으로 보는 관점

### 알고리즘 갈래

#### Advanced ALG1 · Grover search

- 오라클의 위상 표식과 진폭 증폭
- 평균을 기준으로 한 반사 직관
- 작은 검색 공간의 반복 횟수와 성공 확률
- 고전 검색과의 질의 횟수 차이

#### Advanced ALG2 · QFT와 위상 추정

- 주기와 주파수의 직관
- 위상 회전이 비트 패턴으로 바뀌는 과정
- 작은 2-3큐비트 QFT 회로
- 위상 추정과 주기 찾기의 연결

#### Advanced ALG3 · 변분 알고리즘

- 매개변수 회로와 고전 최적화의 반복
- 비용 함수와 측정값
- 작은 분자 에너지 예시를 통한 VQE 직관
- QAOA의 조합 최적화 예시
- 노이즈가 많은 장비에서의 기대와 한계

#### Advanced ALG4 · Shor 알고리즘과 보안의 큰 그림

- 주기 찾기와 공개키 암호의 연결
- 양자 알고리즘이 모든 문제를 빠르게 푸는 것은 아니라는 점
- QKD, PQC, 양자 공격의 차이 복습
- 입력 비용, 오류정정 비용, 결과 검증까지 포함한 평가

### 응용 갈래

#### Advanced APP1 · Quantum Machine Learning

선수 개념: Advanced A0, Advanced ALG3의 매개변수 회로, 기초적인 분류와 학습 데이터 개념

- 특징, 레이블, 학습·검증 데이터, 손실 함수의 고전 머신러닝 기초 복습
- 고전 데이터를 회전각이나 양자 상태로 넣는 데이터 인코딩
- 매개변수 양자 회로와 고전 최적화기가 함께 학습하는 과정
- 작은 변분 양자 분류기와 양자 커널의 직관
- 양자 데이터와 고전 데이터에서 기대할 수 있는 점의 차이
- 데이터 입력 비용, 회로 깊이, 노이즈, 학습 시간 때문에 자동으로 우월해지지 않는다는 한계

권장 시뮬레이션:

- 2차원 장난감 데이터의 학습·검증 분할
- 데이터 한 점이 회전 게이트와 상태로 바뀌는 회로 그림
- 매개변수 변화에 따른 결정 경계와 손실 곡선
- 같은 데이터에 대한 간단한 고전 분류기 기준선
- 측정 횟수와 노이즈를 바꾼 정확도 비교

구현 원칙:

- “양자 신경망”이라는 이름보다 데이터 인코딩, 회로, 측정, 고전 최적화의 실제 흐름을 먼저 보여 준다.
- 작은 예제의 정확도가 높다는 사실을 일반적인 양자 우위로 해석하지 않는다.
- 기본 앱에서는 내부 시뮬레이터를 사용하고 Qiskit Machine Learning 같은 큰 의존성은 별도 실습으로 둔다.

예정 실험 ID: `EXP-QML01`, `EXP-QML02`

### 오류정정 갈래

#### Advanced QEC1 · Stabilizer와 신드롬

- Pauli $X$, $Z$ 오류와 교환·반교환의 직관
- 상태를 직접 읽지 않고 안정자 측정값으로 오류를 찾는 방법
- 3큐비트 반복 부호를 stabilizer 관점으로 다시 읽기
- Clifford 회로를 효율적으로 추적할 수 있다는 개념
- 정식 군론과 이진 심플렉틱 표현은 참고 자료로 분리

권장 시뮬레이션:

- 데이터 큐비트와 보조 측정 큐비트가 있는 작은 안정자 회로
- 오류 위치에 따라 바뀌는 신드롬 비트
- 같은 신드롬을 만드는 오류와 논리 오류의 차이 맛보기

#### Advanced QEC2 · Surface code와 내결함성

- 2차원 격자의 데이터 큐비트와 측정 큐비트
- 반복 신드롬 측정과 오류 사슬의 끝점
- 코드 거리와 논리 오류율의 정성적 관계
- 정정 연산 자체에도 오류가 생길 수 있다는 내결함성 문제
- threshold는 “물리 오류가 충분히 낮을 때 규모 확장이 도움을 주는 경계”로 설명

권장 시뮬레이션:

- 작은 격자에 오류를 놓고 신드롬 위치 찾기
- 가장 짧은 보정 경로와 실패하는 논리 오류 경로 비교
- 코드 거리와 물리 큐비트 비용 비교

경계:

- surface code 디코더의 세부 알고리즘과 임계값 수치 경쟁은 다루지 않는다.
- 고등학생 과정에서는 격자, 패리티, 신드롬의 시각적 의미를 우선한다.

## 구현 및 의존성 원칙

1. 앱 내부 시뮬레이터로 개념을 먼저 익힌다.
2. 새 레벨은 한국어/영어 설명, 시뮬레이션, 자료실, 용어, 퀴즈를 함께 추가한다.
3. 설명과 시뮬레이션은 같은 회로 표기와 용어를 사용한다.
4. 어려운 유도식은 접기 영역으로 두고 본문에는 의미와 예시를 우선한다.
5. 그래프 라벨은 글꼴 깨짐을 피하기 위해 영어를 사용한다.
6. 실행형 SDK 실습은 Colab 또는 별도 `notebooks/` 경로로 분리한다.
7. 외부 서비스 API와 설치 버전은 구현 시점에 공식 문서에서 다시 확인한다.

## 권장 구현 순서

1. Level 13 양자전송과 초밀집 부호화: 완료
2. Level 14 양자암호와 BB84
3. Level 15 양자네트워크
4. Level 16 오류 검출·정정 입문
5. Level 17 실제 하드웨어
6. Level 18 SDK Lab
7. 기초·중급 전체 교육 검토
8. Advanced A0 뒤 알고리즘, 오류정정 또는 응용 갈래

## 새 레벨 추가 체크리스트

- `content/levels.json`
- `content/levels_en.json`
- `content/lessons/ko/levelN.md`
- `content/lessons/en/levelN.md`
- `content/resources.json`
- `core/i18n.py`
- `core/navigation.py`
- `app.py`
- `pages/NN_levelN_*.py`
- `tests/`
- `docs/curriculum_roadmap.md`
- `docs/experiment_registry.md`
- README 또는 개발 문서

## 공식 참고 자료

- [IBM Quantum Learning: Quantum teleportation](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/entanglement-in-action/quantum-teleportation)
- [IBM Quantum Learning: Superdense coding](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/entanglement-in-action/superdense-coding)
- [IBM Quantum Learning: Quantum key distribution](https://quantum.cloud.ibm.com/learning/en/modules/computer-science/quantum-key-distribution)
- [NIST: What Is Post-Quantum Cryptography?](https://www.nist.gov/cybersecurity-and-privacy/what-post-quantum-cryptography)
- [DOE Explains: Quantum Networks](https://www.energy.gov/science/doe-explainsquantum-networks)
- [IBM Quantum Learning: Foundations of quantum error correction](https://learning.quantum.ibm.com/course/foundations-of-quantum-error-correction)
- [IBM Quantum Learning: The stabilizer formalism](https://learning.quantum.ibm.com/course/foundations-of-quantum-error-correction/the-stabilizer-formalism)
- [IBM Quantum Learning: Surface codes](https://quantum.cloud.ibm.com/learning/en/courses/foundations-of-quantum-error-correction/quantum-code-constructions/other-code-families)
- [Google Quantum AI: Stabilizer measurement example](https://quantumai.google/cirq/simulate/qvm_stabilizer_example)
- [IBM Quantum Documentation: Introduction to transpilation](https://quantum.cloud.ibm.com/docs/en/guides/transpile)
- [IBM Quantum Documentation: View backend details](https://quantum.cloud.ibm.com/docs/en/guides/qpu-information)
- [IBM Quantum Documentation: Install Qiskit](https://quantum.cloud.ibm.com/docs/en/guides/install-qiskit)
- [Google Quantum AI: Cirq basics](https://quantumai.google/cirq/start/basics)
- [Google Quantum AI: Cirq install](https://quantumai.google/cirq/start/install)
- [Google Quantum AI: Google Quantum Computing Service](https://quantumai.google/cirq/google/concepts)
- [IBM Quantum Learning: Quantum Machine Learning](https://quantum.cloud.ibm.com/learning/en/courses/quantum-machine-learning)
- [TensorFlow Quantum: Quantum machine learning concepts](https://www.tensorflow.org/quantum/concepts)

외부 SDK, 하드웨어, 보안 권고는 변동 가능성이 크므로 관련 레벨을 구현할 때 링크와 API를 다시 확인한다.
