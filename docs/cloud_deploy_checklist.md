# Cloud Deploy Checklist

배포 직전에 확인할 항목만 모아 둔 체크리스트다. 자세한 개발 운영 메모는 `docs/development.md`를 본다.

## Streamlit Cloud

- Repository: 이 프로젝트의 GitHub 저장소
- Main file path: `app.py`
- Requirements: `requirements.txt`
- Python: `3.12.x`
- App URL: `https://quantum-info-learning-lab.streamlit.app`

`runtime.txt`와 Streamlit Cloud Advanced settings의 Python 버전을 모두 확인한다. 의존성이나 Python 버전을 바꾼 뒤에는 Cloud 로그에서 `requirements.txt` 설치가 끝나고 앱 프로세스가 정상적으로 유지되는지 본다.

선택 사항으로 다음 secret을 둘 수 있다. 값이 없으면 앱 코드의 기본 Cloudflare 주소를 사용한다.

```toml
PHOTON_HEIST_URL = "https://quantum-info-learning-lab.youinuk.workers.dev/hub"
```

## Cloudflare

- Game URL: `https://quantum-info-learning-lab.youinuk.workers.dev/hub`
- Publish directory: `games/photon_heist`
- Build command: 없음 또는 `exit 0`

확인 URL:

- `https://quantum-info-learning-lab.youinuk.workers.dev/hub?lang=ko`
- `https://quantum-info-learning-lab.youinuk.workers.dev/hub?lang=en`
- `https://quantum-info-learning-lab.youinuk.workers.dev/index.html?lang=ko`
- `https://quantum-info-learning-lab.youinuk.workers.dev/glass.html?lang=ko`

## 업로드 전 검증

```bash
conda run -n quantum_lab python -m compileall -q app.py core pages tests
conda run -n quantum_lab pytest -q
```

## Git 확인

```bash
git branch --show-current
git status --short
git diff --check
git push origin main
```

- 현재 브랜치가 `main`인지 확인한다.
- 의도하지 않은 임시 스크린샷, 브라우저 프로필, secret 파일이 포함되지 않았는지 확인한다.
- Streamlit Cloud 배포가 끝난 뒤 Home과 변경된 레벨을 확인한다.
- 릴리스 태그는 배포 확인이 끝난 커밋에 붙인다.
