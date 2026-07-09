# Photon Heist: 빛의 도둑

`Photon Heist`는 빛의 직진, 반사, 굴절을 다루는 HTML5 물리 퍼즐이다. Streamlit 앱 안에 직접 임베드하지 않고, 별도 정적 웹사이트로 배포한 뒤 Streamlit에서는 링크로 연다.

## 실행

브라우저에서 다음 파일을 직접 열 수 있다.

- `hub.html`: 챕터 선택과 진행 상황을 보여 주는 작전 허브
- `index.html`: Mirror Mission
- `glass.html`: Glass Route

정적 파일만 사용하므로 별도 서버나 빌드 과정은 필요 없다. 다만 실제 배포 검증은 Cloudflare Pages, Netlify 같은 정적 호스팅에서 확인하는 것이 좋다.

## 정적 배포

권장 설정:

- Publish directory: `games/photon_heist`
- Build command: 없음
- Entry file: `hub.html`

배포 후 Streamlit 앱에는 다음 값을 설정한다.

```toml
PHOTON_HEIST_URL = "https://your-photon-heist-site.example/hub.html"
```

Streamlit의 언어 선택은 게임 주소에 `?lang=ko` 또는 `?lang=en`으로 전달된다. 게임은 이 값을 읽어 `localStorage`에 저장한다.

## 현재 구성

- `hub.html`: 작전 허브
- `index.html`: Mirror Mission
- `glass.html`: Glass Route
- `styles/`: 화면 스타일
- `src/`: 게임 로직, 렌더링, 레벨 데이터, 언어 처리
- `docs/`: 설계 노트와 확장 로드맵
- `tests/`: 브라우저에서 직접 열어 확인하는 간단한 HTML 테스트

## 프로젝트 밖으로 옮길 때

배포가 안정되면 이 폴더를 별도 repo 또는 프로젝트 밖 폴더로 옮겨도 된다. 그때는 Streamlit 프로젝트에서 `games/photon_heist/`를 더 이상 소스 원본으로 들고 있을 필요가 없다.

현재 Streamlit 앱과 게임의 실행 결합은 끊겨 있다. Streamlit 쪽은 `PHOTON_HEIST_URL`만 읽고 외부 링크 버튼을 만든다. 따라서 정적 호스팅 URL이 확정된 뒤에는 이 폴더를 별도 저장소로 옮기는 것이 가장 관리하기 쉽다.

옮긴 뒤 확인할 것:

- 정적 사이트 URL이 정상 동작하는지 확인한다.
- Streamlit Cloud secrets의 `PHOTON_HEIST_URL`을 새 주소로 바꾼다.
- Streamlit 앱의 `Photon Heist` 페이지에서 한국어/영어 버튼 이동이 정상인지 확인한다.
- Streamlit 저장소에서는 `pages/10_photon_heist.py`와 README의 URL 설정 안내만 유지하면 된다.

## 향후 확장

현재 중심은 Mirror Mission과 Glass Route다. 이후 렌즈, 프리즘, 파동, 간섭, 양자정보 챕터를 단계적으로 추가할 수 있다.
