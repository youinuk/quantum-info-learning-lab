# Cloud Deploy Checklist

이 프로젝트는 두 부분으로 나누어 배포한다.

1. Streamlit Community Cloud: 양자정보 학습 앱
2. 정적 호스팅: `Photon Heist` HTML5 게임

## 1. Streamlit 앱 배포

- GitHub 저장소 루트가 `quantum_info_learning_lab`인지 확인한다.
- Streamlit Community Cloud의 main file path는 `app.py`로 설정한다.
- Python 패키지는 `requirements.txt`에서 설치된다.
- Cloud secrets에 `PHOTON_HEIST_URL`을 추가한다.

예시:

```toml
PHOTON_HEIST_URL = "https://quantum-info-learning-lab.youinuk.workers.dev/hub"
```

`PHOTON_HEIST_URL`은 로컬 파일 경로가 아니라 브라우저에서 직접 열 수 있는 `https://.../hub` 주소여야 한다.

## 2. Photon Heist 정적 배포

Cloudflare Pages, Netlify, GitHub Pages 같은 정적 호스팅을 사용한다.

권장 설정:

- Publish directory: `games/photon_heist`
- Build command: 비워 둠
- Entry file: `hub.html`

배포 뒤 다음 URL을 직접 확인한다.

- `https://.../hub?lang=ko`
- `https://.../hub?lang=en`
- `https://.../index.html?lang=ko`
- `https://.../glass.html?lang=ko`

## 3. 분리 상태

현재 Streamlit 앱은 게임을 iframe/custom component로 임베드하지 않는다. `pages/10_photon_heist.py`는 `PHOTON_HEIST_URL`을 읽어 외부 정적 게임 사이트로 이동하는 버튼만 제공한다.

따라서 게임 배포가 안정되면 `games/photon_heist/`는 별도 저장소나 프로젝트 밖 폴더로 옮겨도 된다. 그 경우 Streamlit 앱에서는 `PHOTON_HEIST_URL`만 새 주소로 바꾸면 된다.

## 4. 업로드 전 검증

```bash
conda run -n quantum_lab python -m compileall -q app.py core pages tests
conda run -n quantum_lab pytest -q
```

게임 런타임 프로브는 정적 호스팅 또는 로컬 HTTP 서버에서 확인한다.

- `games/photon_heist/tests/runtime_probe.html?lang=ko`
- `games/photon_heist/tests/hub_runtime_probe.html?lang=ko`
- `games/photon_heist/tests/glass_runtime_probe.html?lang=ko`

## 5. Git 확인

Cloud 배포는 GitHub 저장소 기준으로 동작한다. 업로드 전에 루트에서 다음 명령이 정상 동작해야 한다.

```bash
git status
```

현재 작업 폴더에서 `fatal: not a git repository`가 나오면, GitHub에 올릴 깨끗한 저장소를 새로 만들거나 정상 clone 폴더에서 파일을 옮긴 뒤 배포한다.
