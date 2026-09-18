# research.remakeday.com

REMAKE DAY를 재현 가능한 Human–AI Interaction 실험환경으로 정의하고, 시스템 평가와 행동 관찰의 측정 결과를
쌓아 가는 연구 기록 사이트. 원칙 — **측정하지 않은 것은 주장하지 않는다.**

## 구조

```
index.md                              홈 — Abstract · 포지셔닝 · Contributions
testbed.md                            실험환경 설계 (Figure 1, 2층 평가)
experiments/model-selection.md        Exp 1 — E7/E6/외부 API (공개용 가공 스냅샷)
scripts/snapshot_model_eval.py        Exp 1 스냅샷 생성기
scripts/check_public.py               공개 금지어 검사
experiments/human-observations.md     Exp 2 — 기존 6판 집계와 후속 1판 별도 사례 (exploratory)
prereg.md                             사전등록 — Rationale A/B
limitations.md                        한계 · 재현성
lab-notes.md                          날짜별 실험 로그
```

## 로컬 실행

```bash
bundle install
python3 scripts/refresh_research_data.py
bundle exec jekyll serve
```

## 읽기 화면과 시각화

원문 Markdown은 전체 연구 기록으로 유지한다. `_data/reading.yml`과
`_includes/research/`가 쉬운 질문·설명·그림을 원문 앞에 붙이고,
`_layouts/page.html`이 원문을 그대로 표시한다. 홈의 전체 기록은 펼쳐 읽을 수 있고
기존 절 링크로 들어오면 해당 기록이 열린다. 사전등록 원문도 별도로 수정하지 않는다.

- UI: `assets/css/style.scss`, `assets/js/app.js`. Jekyll/Liquid와 기본 브라우저 기능을 사용한다.
- 읽기 요약: `_data/reading.yml`. 측정 조건·한계와 원문의 최신 상태를 함께 확인한다.
- 차트 데이터: `_data/research_figures.json`. 직접 수정하지 않는다.
  `python3 scripts/refresh_research_data.py`가 공개 Markdown의 표에서 수치를 읽는다.
- 원문 표의 형식이나 실험 조건이 바뀌면 생성기가 중단한다. 새 조건에 맞게 추출기와
  설명·캡션을 함께 검토한다. 여섯 판 집계/별도 사례, 검수 22문장/초기 30문장 반복은
  합치지 않는다. 생성 후 `--check`로 현재 원문과의 일치를 확인한다.
- 블렌더 그림: `assets/images/research-instrument.webp`. 재생성 방법과 편집 가능한
  장면은 [그림 제작 기록](docs/research-figures.md)에 있다. 그림의 설명은 웹 텍스트로 제공한다.

변경 검증:

```bash
python3 scripts/refresh_research_data.py --check
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/check_public.py
bundle exec jekyll build
python3 scripts/check_site.py _site
```

화면만 변경할 때는 변경 전 빌드를 남겨 원문과 기존 앵커의 보존을 대조할 수 있다.

```bash
python3 scripts/check_site.py _site --baseline /tmp/research-baseline-site
```

본문의 오류를 정정할 때는 `--anchor-baseline /tmp/research-baseline-site`로
기존 절 링크를 검사한다. 이 옵션은 문장 변경을 허용하지만 내부 링크 검사는 생략하지 않는다.

브라우저 검사는 Node 20 이상과 Chrome을 사용한다. 별도 npm 패키지는 필요하지 않다.
검사 전 `_site`를 `127.0.0.1:4173`에 제공하고, 전용 Chrome 프로필로 DevTools 포트를 연다.
Chrome의 기존 개인 프로필을 사용하지 않는다.

```bash
python3 -m http.server 4173 --bind 127.0.0.1 --directory _site
# 별도 터미널
google-chrome --headless --remote-debugging-port=9223 --user-data-dir=/tmp/research-browser-check
# 별도 터미널
node --experimental-websocket tests/browser.mjs
```

검사는 메뉴·원문 링크·모바일 목차·가로 넘침·JavaScript 없는 화면·인쇄를 확인하며,
화면 캡처를 `/tmp/research-ui-shots/`에 저장한다. `docs/`, `scripts/`, `tests/`,
`artwork/`는 사이트 빌드에서 제외된다.

## 운영 규칙

- Exp 1은 `com.remakeday/docs/model_evaluation.md`가 정본이고 이 사이트는 **공개용 가공 스냅샷**.
  정본 갱신 시 손으로 복사하지 말고 `python3 scripts/snapshot_model_eval.py`로 다시 뜬다
  (앱 저장소 `main` 기준, 제목 단계 조정·링크를 경로로·공개 범위 규칙 적용·금지어 검사·그림 데이터 갱신까지 한 번에).
  공개 검토 전인 추록은 로컬 공개 규칙의 `drop_section_prefixes`로 절 전체를 제외한다.
  지정한 절 제목이 정본에서 달라지면 생성이 중단되므로 공개 범위를 다시 확인한다.
  숫자 정정은 역할·실행 출처와 변경 이유를 정본에 먼저 기록한다.
  2026-09-18 정정본은 `--ref docs/research-review-20260918`로 생성했으며,
  이후 갱신도 공개 검토가 끝난 정본 커밋을 `--ref`로 명시한다.

## 공개 범위 (2026-09-17 확정)

심사에 설득력이 되는 설계 판단·측정은 드러내고, 공격에 쓸모 있는 운영 세부와 스포일러는 숨긴다.

- **공개**: 모델 선정 경위·평가 수치·게이트·탈락 사유, 판당 비용, 방어선이 있다는 사실(로그인·판 수 제한·지출 한도), 품질 한계, 표본이 작다는 명시
- **싣지 않음**: 운영 한도 수치와 그로부터 역산한 최대 비용, 프록시·IP 관련 미해결 경로, 개발 계정 로그인 세부, 인스펙터 토큰, 설정 키 이름·포트·인프라 식별자, 외부 의존 약점 서술, 시나리오 결말을 드러내는 식별자·정답 문장
- 치환표·금지어 목록은 그 자체가 스포일러라 `_private/public-rules.json`(gitignore)에만 둔다. 파일이 없으면 스냅샷·검사 스크립트가 멈춘다
- 커밋 전 `python3 scripts/check_public.py`(pre-commit 훅으로도 설치)가 금지어 0건을 확인한다
- 한계: 이전 커밋의 git 이력과 앱 저장소 정본에는 옛 내용이 남는다
- 사전등록 페이지는 데이터 수집 후 수정하지 않는다. 설계가 바뀌면 새 실험으로 등록.
- `REMAKE_DAY_*`, `TalkFile_*` 파일은 커밋·빌드 금지 (기획서 원문 비공개).

## 배포

GitHub Pages(저장소 `remakeday/com.remakeday.research`) + CNAME `research.remakeday.com`. DNS에 서브도메인 CNAME 레코드 필요.
