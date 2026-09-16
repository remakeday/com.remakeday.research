# research.remakeday.com

REMAKE DAY를 재현 가능한 Human–AI Interaction 실험환경으로 정의하고, 실측 기준으로
적립하는 연구 기록 사이트. 원칙 — **측정하지 않은 것은 주장하지 않는다.**

## 구조

```
index.md                              홈 — Abstract · 포지셔닝 · Contributions
testbed.md                            실험환경 설계 (Figure 1, 2층 평가)
experiments/model-selection.md        Exp 1 — E7/E6/외부 API (공개용 가공 스냅샷)
scripts/snapshot_model_eval.py        Exp 1 스냅샷 생성기
scripts/check_public.py               공개 금지어 검사
experiments/human-observations.md     Exp 2 — 사람 행동 관찰 (N=5+, exploratory)
prereg.md                             사전등록 — Rationale A/B
limitations.md                        한계 · 재현성
lab-notes.md                          날짜별 실험 로그
```

## 로컬 실행

```bash
bundle install
bundle exec jekyll serve
```

## 운영 규칙

- Exp 1은 `com.remakeday/docs/model_evaluation.md`가 정본이고 이 사이트는 **공개용 가공 스냅샷**.
  정본 갱신 시 손으로 복사하지 말고 `python3 scripts/snapshot_model_eval.py`로 다시 뜬다
  (앱 저장소 `main` 기준, 제목 단계 조정·링크를 경로로·공개 범위 규칙 적용·금지어 검사까지 한 번에).

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
