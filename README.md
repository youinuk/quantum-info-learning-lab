# Quantum Info Learning Lab

고등학생과 일반 학습자를 위한 Streamlit 기반 양자정보 학습 앱이다. 비트와 확률에서 출발해 큐비트, 측정, 게이트, 간섭, 얽힘, 간단한 양자 알고리즘, 노이즈까지 단계적으로 다룬다.

기본 사용 환경은 PC/태블릿 최적화다. 모바일에서는 확인과 가벼운 체험이 가능하도록 호환성을 유지한다.

## 실행 방법

이 프로젝트는 `conda` 환경과 `conda-forge` 채널을 기준으로 관리한다. 현재 권장 환경 이름은 `quantum_lab`이다.

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

Windows에서 `python.exe`를 직접 실행하면 DLL 검색 경로가 달라질 수 있으므로, 가능하면 `conda activate quantum_lab` 또는 `conda run -n quantum_lab ...` 형식을 사용한다.

## 현재 학습 구성

- Level 0: 비트와 확률
- Level 1: 큐비트 입문
- Level 2: 측정
- Level 3: 양자 게이트
- Level 4: 간섭
- Level 5: 두 큐비트
- Level 6: 얽힘
- Level 7: 간단한 양자 알고리즘
- Level 8: 노이즈와 오류

각 레벨은 설명, 시뮬레이션, 자료실, 퀴즈로 구성된다. 설명 본문은 `content/lessons/{lang}/levelN.md`, 구조화 데이터는 `content/levels.json`과 `content/levels_en.json`, 자료 링크는 `content/resources.json`에서 관리한다.

## Photon Heist 배포 방식

`Photon Heist: 빛의 도둑`은 Streamlit 안에 iframe/custom component로 넣지 않는다. 게임은 별도 정적 HTML5 사이트로 배포하고, Streamlit 앱은 해당 게임을 여는 런처 페이지를 제공한다.

이 구조를 쓰는 이유:

- Streamlit iframe 안에서 클릭, 키보드, 높이 계산, 모바일 스크롤 문제가 반복되지 않는다.
- 게임은 순수 HTML/CSS/JavaScript 정적 사이트로 독립 배포할 수 있다.
- Streamlit Community Cloud는 학습 앱만 담당하고, 게임 호스팅은 Cloudflare Pages나 Netlify 같은 정적 호스팅이 담당한다.
- 한국어/영어 선택 상태는 게임 URL의 `?lang=ko` 또는 `?lang=en`으로 전달한다.

현재 게임 원본은 `games/photon_heist/`에 남겨 둔다. 배포가 안정되면 이 폴더를 별도 repo나 프로젝트 밖 폴더로 옮겨도 된다. 그 경우 Streamlit 앱은 게임 URL 설정만 새 주소로 바꾸면 된다.

권장 정적 배포 설정:

- Publish directory: `games/photon_heist`
- Build command: 없음
- Entry file: `hub.html` 권장, 또는 `index.html`
- 배포 후 Streamlit Cloud secrets 또는 실행 환경에 `PHOTON_HEIST_URL` 설정

예시:

```toml
PHOTON_HEIST_URL = "https://your-photon-heist-site.example/hub.html"
```

로컬에서 임시 확인할 때는 브라우저로 `games/photon_heist/hub.html`을 직접 열 수 있다. 최종 배포 확인은 정적 호스팅 URL을 만든 뒤 Streamlit의 `Photon Heist` 페이지에서 버튼으로 이동해 확인한다.

## Streamlit Cloud 배포 준비

Cloud 배포는 두 주소를 따로 준비한다.

1. Streamlit Community Cloud: 이 저장소의 `app.py`
2. 정적 호스팅: `games/photon_heist/hub.html`

Streamlit Cloud secrets에는 다음 값을 넣는다. 예시는 `.streamlit/secrets.toml.example`에도 있다.

```toml
PHOTON_HEIST_URL = "https://your-photon-heist-static-site.example/hub.html"
```

업로드 전 세부 확인은 `docs/cloud_deploy_checklist.md`를 따른다. 특히 루트에서 `git status`가 정상 동작하는지 확인한다. 현재 폴더가 Git 저장소로 인식되지 않는다면, GitHub에 올릴 깨끗한 저장소를 새로 만들거나 정상 clone 폴더에서 배포한다.

## 자료 추가 방식

- 설명 본문은 Markdown으로 관리한다.
- 레벨 목표, 퀴즈, 용어 정리처럼 구조화된 데이터는 JSON에서 관리한다.
- 로컬 그림은 `assets/images/`에 넣고 Markdown 또는 `content/resources.json`에서 연결한다.
- 영상, 기사, 외부 시뮬레이션은 실제 학습 페이지 URL로 연결한다.
- 영어 모드에서 한국어가 노출되지 않도록 `content/levels_en.json`, 영어 Markdown, 자료 링크를 함께 확인한다.

## 검증

```bash
conda run -n quantum_lab python -m compileall -q app.py core pages tests
conda run -n quantum_lab pytest -q
```

Photon Heist는 별도 정적 사이트이므로 Streamlit 테스트는 런처 페이지와 파일 구조를 검증한다. 게임 자체의 브라우저 조작 검증은 정적 호스팅 또는 로컬 HTML 실행 환경에서 별도로 확인한다.
