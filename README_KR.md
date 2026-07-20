# Quantum Info Learning Lab

[English README](README.md)

고등학생과 일반 학습자를 위한 Streamlit 기반 양자정보 학습 앱이다. 비트와 확률에서 출발해 큐비트, 측정, 게이트, 간섭, 얽힘, 노이즈, 회로 읽기, 측정 통계, 간섭 심화, 간단한 양자 알고리즘, 양자전송까지 단계적으로 다룬다.

기본 사용 환경은 PC/태블릿 최적화다. 모바일에서는 확인과 가벼운 체험이 가능하도록 호환성을 유지한다.

앱의 기본 언어는 영어이며 사이드바에서 한국어로 바꿀 수 있다. 한국어 콘텐츠와 문서는 그대로 함께 관리한다.

배포 주소:

- Quantum Info Learning Lab: https://quantum-info-learning-lab.streamlit.app
- Photon Heist: https://quantum-info-learning-lab.youinuk.workers.dev/hub

## 실행 방법

이 프로젝트는 `conda` 환경과 `conda-forge` 채널을 기준으로 관리한다. 권장 환경 이름은 `quantum_lab`이다.

```bash
cd quantum_info_learning_lab

conda create -n quantum_lab -c conda-forge python=3.12
conda activate quantum_lab
conda install -c conda-forge --file requirements.txt pytest

python -m streamlit run app.py
```

이 프로젝트의 로컬 Streamlit 프로세스는 하나만 실행한다. 앱을 사용하는 동안 실행
터미널을 열어 둔다. 8501 포트에서 다시 실행하기 전에는 기존 터미널에서 `Ctrl+C`로
종료한다. 소스 감시는 polling 방식을 사용해 native watchdog 없이 변경된 프로젝트
모듈을 다시 읽는다.

이미 환경이 있다면 다음처럼 맞춘다.

```bash
conda install -n quantum_lab -c conda-forge --file requirements.txt pytest
conda run -n quantum_lab pytest -q
```

## 학습 구성

- Level 0: 비트와 확률
- Level 1: 큐비트 입문
- Level 2: 측정
- Level 3: S 게이트의 복소 위상을 포함한 양자 게이트
- Level 4: 간섭
- Level 5: 두 큐비트와 두 큐비트 게이트
- Level 6: 얽힘
- Level 7: 노이즈와 오류
- Level 8: 회로를 읽는 법
- Level 9: 측정과 통계
- Level 10: 간섭 심화
- Level 11: 간단한 양자 알고리즘
- Level 12: 얽힘과 정보의 한계
- Level 13: 보정을 직접 선택하는 양자전송과 부호표 탐색·전송 미션으로 구성된 초밀집 부호화
- Photon Heist: 빛의 직진, 반사, 굴절을 다루는 HTML5 퍼즐 게임

각 레벨은 설명, 시뮬레이션, 자료실, 퀴즈로 구성된다.

### 다음 응용·현실 연결 트랙

Level 13 이후 고급 과정으로 넘어가기 전에 다음 다섯 레벨을 추가한다.

- Level 14: 양자암호와 BB84
- Level 15: 양자네트워크
- Level 16: 오류를 찾고 줄이는 방법
- Level 17: 실제 양자 하드웨어
- Level 18: Qiskit/Cirq SDK와 실제 실행 맛보기

이후 과정은 복소 진폭을 공통 기반으로 삼고, Grover search·QFT·변분 알고리즘을 다루는 알고리즘 갈래, stabilizer·surface code를 다루는 오류정정 갈래, QML을 다루는 응용 갈래로 분리한다. 상세 순서와 진입 기준은 [교육과정 및 구현 로드맵](docs/curriculum_roadmap.md)에 정리한다.

## 콘텐츠 관리

- 설명 본문: `content/lessons/{lang}/levelN.md`
- 레벨 목표, 용어, 퀴즈 등 구조화 데이터: `content/levels.json`, `content/levels_en.json`
- 자료실 링크: `content/resources.json`
- 로컬 이미지: `assets/images/`
- 외부 미디어 출처와 라이선스: [미디어 출처](docs/media_attributions.md)
- Photon Heist 게임 파일: `games/photon_heist/`

## 검증

```bash
conda run -n quantum_lab python -m compileall -q app.py core pages tests
conda run -n quantum_lab pytest -q
```

## 프로젝트 문서

- 교육과정, 다음 구현 순서와 고급 과정: [교육과정 및 구현 로드맵](docs/curriculum_roadmap.md)
- Photon Heist Chapter 3 이후 계획: [Photon Heist 확장 로드맵](docs/photon_heist_roadmap.md)
- 개발, 배포, Cloudflare/Streamlit 운영: [개발 노트](docs/development.md)
- 회로 연산자, 큐비트와 SDK 비트 순서: [양자 표기 및 비트 순서 규약](docs/quantum_conventions.md)
- 설명 문체, 수식 전개와 한영 원고 작성 기준: [학습 콘텐츠 문체 지침](docs/content_style_guide.md)
- 배포 직전 점검: [Cloud 배포 체크리스트](docs/cloud_deploy_checklist.md)
- 실험 ID, 앱·원고·그림 연결과 재현성 정보: [실험 레지스트리](docs/experiment_registry.md)
- 외부 그림과 미디어 출처: [미디어 출처](docs/media_attributions.md)

이 문서들은 비밀 정보가 아닌 기여자용 설계·운영 기록이므로 저장소에서 함께 관리한다. 토큰, 실제 secret, 개인 경로와 비공개 메모는 커밋하지 않으며 로컬 전용 문서는 `docs/private/`에 둔다.
