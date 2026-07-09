# Development Notes

이 문서는 배포판 README에 둘 필요 없는 개발·운영 메모를 모아 둔다.

## 배포 구조

서비스는 두 부분으로 나누어 배포한다.

1. Streamlit Cloud: 양자정보 학습 앱
2. Cloudflare 정적 호스팅: `Photon Heist` HTML5 게임

Streamlit 앱은 게임을 iframe/custom component로 임베드하지 않는다. `pages/10_photon_heist.py`는 외부 게임 사이트로 이동하는 링크 버튼만 제공한다. 이 방식이 클릭, 키보드 입력, 높이 계산, 모바일 스크롤 문제를 줄인다.

## Photon Heist URL

현재 기본 게임 URL은 코드에 들어 있다.

```toml
PHOTON_HEIST_URL = "https://quantum-info-learning-lab.youinuk.workers.dev/hub"
```

Streamlit Cloud secret 또는 환경 변수에 `PHOTON_HEIST_URL`을 넣으면 기본값을 덮어쓴다. 언어 선택은 `?lang=ko` 또는 `?lang=en`으로 전달된다.

## Cloudflare 설정

- Publish directory: `games/photon_heist`
- Build command: 없음 또는 `exit 0`
- 권장 진입 주소: `/hub`

Cloudflare는 clean URL을 사용하므로 `/hub.html`이 `/hub`로 리다이렉트될 수 있다. Streamlit 쪽에는 `/hub` 주소를 쓰는 편이 깔끔하다.

## 게임 파일 분리

현재 게임 원본은 `games/photon_heist/`에 같이 둔다. 나중에 게임 배포가 안정되면 별도 저장소나 프로젝트 밖 폴더로 옮겨도 된다. 그 경우 Streamlit 앱에서는 `PHOTON_HEIST_URL`만 새 주소로 바꾸면 된다.

## 캐시 버전

게임 HTML은 JS/CSS에 `?v=YYYYMMDDx` 형식의 캐시 버전을 붙인다. 게임 소스나 스타일을 수정해 Cloudflare에 배포할 때는 이 값을 올려 브라우저가 오래된 파일을 잡지 않게 한다.

현재 버전: `20260710b`

## 검증

기본 검증:

```bash
conda run -n quantum_lab python -m compileall -q app.py core pages tests
conda run -n quantum_lab pytest -q
```

게임 런타임 프로브:

- `games/photon_heist/tests/hub_runtime_probe.html?lang=ko`
- `games/photon_heist/tests/runtime_probe.html?lang=ko`
- `games/photon_heist/tests/glass_runtime_probe.html?lang=ko`

브라우저에서 확인할 때는 한국어/영어 전환, 허브에서 거울 작전 진입, 유리 작전 진입, 첫 스테이지 조작이 정상인지 본다.
