# Quantum Info Learning Lab

고등학생과 일반 학습자를 위한 Streamlit 기반 양자정보 학습 앱이다. 비트와 확률에서 출발해 큐비트, 측정, 게이트, 간섭, 얽힘, 간단한 양자 알고리즘, 노이즈까지 단계적으로 다룬다.

기본 사용 환경은 PC/태블릿 최적화다. 모바일에서는 확인과 가벼운 체험이 가능하도록 호환성을 유지한다.

배포 주소:

- Quantum Info Learning Lab: https://quantum-info-learning-lab.streamlit.app
- Photon Heist: https://quantum-info-learning-lab.youinuk.workers.dev/hub

## 실행 방법

이 프로젝트는 `conda` 환경과 `conda-forge` 채널을 기준으로 관리한다. 권장 환경 이름은 `quantum_lab`이다.

```bash
cd quantum_info_learning_lab

conda create -n quantum_lab -c conda-forge python=3.11 streamlit numpy pandas matplotlib pytest
conda activate quantum_lab

streamlit run app.py
```

이미 환경이 있다면 다음처럼 맞춘다.

```bash
conda install -n quantum_lab -c conda-forge --file requirements.txt pytest
conda run -n quantum_lab pytest -q
```

## 학습 구성

- Level 0: 비트와 확률
- Level 1: 큐비트 입문
- Level 2: 측정
- Level 3: 양자 게이트
- Level 4: 간섭
- Level 5: 두 큐비트
- Level 6: 얽힘
- Level 7: 간단한 양자 알고리즘
- Level 8: 노이즈와 오류
- Level 9: 회로를 읽는 법
- Level 10: 측정과 통계
- Level 11: 간섭 심화
- Level 12: 얽힘과 정보의 한계
- Photon Heist: 빛의 직진, 반사, 굴절을 다루는 HTML5 퍼즐 게임

각 레벨은 설명, 시뮬레이션, 자료실, 퀴즈로 구성된다.

## 콘텐츠 관리

- 설명 본문: `content/lessons/{lang}/levelN.md`
- 레벨 목표, 용어, 퀴즈 등 구조화 데이터: `content/levels.json`, `content/levels_en.json`
- 자료실 링크: `content/resources.json`
- 로컬 이미지: `assets/images/`
- Photon Heist 게임 파일: `games/photon_heist/`

## 검증

```bash
conda run -n quantum_lab python -m compileall -q app.py core pages tests
conda run -n quantum_lab pytest -q
```

후속 레벨과 Photon Heist 다음 챕터 계획은 `docs/next_expansion_plan.md`에 정리한다.
개발, 배포, Cloudflare/Streamlit 연동 메모는 `docs/development.md`에 정리한다.
