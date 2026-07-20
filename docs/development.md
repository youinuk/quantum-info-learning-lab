# Development Notes

이 문서는 배포판 README에 둘 필요 없는 개발·운영 메모를 모아 둔다.

## 문서 역할

- `README.md`: GitHub 기본 화면에 표시되는 영문 프로젝트 안내
- `README_KR.md`: 영문 README와 함께 갱신하는 한국어 프로젝트 안내
- `curriculum_roadmap.md`: 교육 순서, Level 13-18 구현 범위, Advanced 과정
- `photon_heist_roadmap.md`: 게임 Chapter 3 이후 확장 계획
- `experiment_registry.md`: 실험 ID와 코드·원고·그림 연결
- `quantum_conventions.md`: 회로 연산자, 상태벡터와 SDK 비트 순서
- `content_style_guide.md`: 학습 설명 문체, 수식 전개, 한영 동기화 기준
- `cloud_deploy_checklist.md`: Python 환경, Cloud 설정, 배포 직전 확인 항목

## 공개 문서와 비공개 메모

`docs/`의 로드맵, 실험 레지스트리, 표기 규약, 개발 및 배포 문서는 기여자가 설계 의도와 재현 방법을 이해하는 데 필요하므로 공개 저장소에서 버전 관리한다. 내부 개발용이라는 말이 곧 비밀 문서라는 뜻은 아니다.

다음 정보는 공개 문서에 넣지 않는다.

- API 토큰, 계정 키, 실제 Streamlit secret
- 개인 PC의 절대 경로와 계정 정보
- 공개 전 콘텐츠, 개인 메모, 외부에 공유할 수 없는 자료

로컬에서만 볼 메모는 `.gitignore`에 등록된 `docs/private/`에 둔다. 공개 문서에는 환경 변수 이름과 예시 값은 둘 수 있지만 실제 비밀 값은 넣지 않는다.

README를 수정할 때는 `README.md`와 `README_KR.md`의 배포 주소, Level 목록, 실행 명령, 문서 링크를 함께 갱신한다.

## 로컬 Streamlit 실행 원칙

로컬 앱은 프로젝트당 한 프로세스만 실행한다. 여러 Streamlit 프로세스가 같은
포트를 공유하면 새 페이지 코드와 이전 `core` 모듈이 한 화면에서 섞여 보일 수
있다. 앱을 사용하는 동안 실행 터미널을 열어 둔다. 재실행할 때는 기존 터미널에서
`Ctrl+C`로 종료한 뒤 `python -m streamlit run app.py`를 다시 실행한다.

`.streamlit/config.toml`은 `fileWatcherType = "poll"`을 사용한다. 이는 소스 변경을
감지하면서 native watchdog 의존성을 피한다. 새 페이지가 최근 추가된 공통 API를
사용할 때는 페이지별 `importlib.reload`를 만들지 않고 `core.runtime_modules`의
`ensure_module_api`에서 필요한 공개 함수 목록을 선언한다.

## Git과 릴리스

현재 개인 개발 흐름은 `main` 단일 장기 브랜치를 사용한다. 짧은 실험이나 큰 변경이 필요할 때만 `feature/...` 브랜치를 만들고 병합 후 삭제한다.

기본 순서:

1. 로컬에서 컴파일, 테스트, 주요 페이지를 확인한다.
2. `main`에 커밋하고 `git push origin main`으로 자동 배포한다.
3. Streamlit과 Cloudflare의 공개 주소를 확인한다.
4. 공개 기준선으로 남길 버전만 주석 태그를 만들고 푸시한다.

예시:

```bash
git add -A
git diff --cached --check
git commit -m "Add Level 13 quantum teleportation"
git push origin main

git tag -a v0.5.0 -m "Add quantum teleportation level"
git push origin v0.5.0
```

태그는 배포 확인 전의 임시 커밋보다 실제 공개 상태와 대응하는 커밋에 붙인다.

## 배포 구조

서비스는 두 부분으로 나누어 배포한다.

1. Streamlit Cloud: 양자정보 학습 앱
2. Cloudflare 정적 호스팅: `Photon Heist` HTML5 게임

Streamlit 앱은 게임을 iframe/custom component로 임베드하지 않는다. `pages/10_photon_heist.py`는 외부 게임 사이트로 이동하는 링크 버튼만 제공한다. 이 방식이 클릭, 키보드 입력, 높이 계산, 모바일 스크롤 문제를 줄인다.

## Photon Heist 연결

Streamlit 페이지에는 기본 게임 URL이 있으며, secret 또는 환경 변수 `PHOTON_HEIST_URL`로 덮어쓸 수 있다. 언어 선택은 `?lang=ko` 또는 `?lang=en`으로 전달된다. 실제 URL, publish directory, 런타임 버전은 [Cloud 배포 체크리스트](cloud_deploy_checklist.md)에서 한 번만 관리한다.

## 게임 파일 분리

현재 게임 원본은 `games/photon_heist/`에 같이 둔다. 나중에 게임 배포가 안정되면 별도 저장소나 프로젝트 밖 폴더로 옮겨도 된다. 그 경우 Streamlit 앱에서는 `PHOTON_HEIST_URL`만 새 주소로 바꾸면 된다.

## 캐시 버전

게임 HTML은 JS/CSS에 `?v=YYYYMMDDx` 형식의 캐시 버전을 붙인다. 게임 소스나 스타일을 수정해 Cloudflare에 배포할 때는 이 값을 올려 브라우저가 오래된 파일을 잡지 않게 한다.

현재 버전: `20260710c`

## 검증

기본 명령은 README의 검증 절을 따르고, 실제 배포 전에는 [Cloud 배포 체크리스트](cloud_deploy_checklist.md)를 순서대로 확인한다.

새 레벨을 추가할 때는 `docs/curriculum_roadmap.md`, `docs/experiment_registry.md`, README의 레벨 범위를 함께 갱신한다. 게임 Chapter를 추가할 때는 `docs/photon_heist_roadmap.md`도 갱신한다.

게임 런타임 프로브:

- `games/photon_heist/tests/hub_runtime_probe.html?lang=ko`
- `games/photon_heist/tests/runtime_probe.html?lang=ko`
- `games/photon_heist/tests/glass_runtime_probe.html?lang=ko`

브라우저에서 확인할 때는 한국어/영어 전환, 허브에서 거울 작전 진입, 유리 작전 진입, 첫 스테이지 조작이 정상인지 본다.
