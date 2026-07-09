# Photon Heist: 빛의 도둑

빛의 직진, 반사, 굴절을 다루는 HTML5 물리 퍼즐이다.

현재 배포 주소:

- Hub: https://quantum-info-learning-lab.youinuk.workers.dev/hub
- Mirror Mission: https://quantum-info-learning-lab.youinuk.workers.dev/index.html
- Glass Route: https://quantum-info-learning-lab.youinuk.workers.dev/glass.html

## 로컬 확인

브라우저에서 다음 파일을 직접 열 수 있다.

- `hub.html`: 챕터 선택과 진행 상황
- `index.html`: 거울 작전
- `glass.html`: 유리 작전

정적 파일만 사용하므로 별도 빌드 과정은 없다.

## 구성

- `styles/`: 화면 스타일
- `src/`: 게임 로직, 렌더링, 레벨 데이터, 언어 처리
- `tests/`: 브라우저에서 직접 열어 확인하는 런타임 프로브

## 진행 기록

진행 기록은 서버가 아니라 각 브라우저의 `localStorage`에 저장된다. 다른 사용자는 자신의 브라우저에서 처음부터 시작한다.

## 확장

현재 중심은 Mirror Mission과 Glass Route다. 이후 렌즈, 프리즘, 파동, 간섭, 양자정보 챕터를 단계적으로 추가할 수 있다.
