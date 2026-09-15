# research.remakeday.com

REMAKE DAY를 재현 가능한 Human–AI Interaction 실험환경으로 정의하고, 실측 기준으로
적립하는 연구 기록 사이트. 원칙 — **측정하지 않은 것은 주장하지 않는다.**

## 구조

```
index.md                              홈 — Abstract · 포지셔닝 · Contributions
testbed.md                            실험환경 설계 (Figure 1, 2층 평가)
experiments/model-selection.md        Exp 1 — E7/E6 (정본 스냅샷)
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

- Exp 1은 `com.remakeday/docs/model_evaluation.md`가 정본이고 이 사이트는 스냅샷.
  정본 갱신 시 스냅샷을 다시 떠온다.
- 사전등록 페이지는 데이터 수집 후 수정하지 않는다. 설계가 바뀌면 새 실험으로 등록.
- `REMAKE_DAY_*`, `TalkFile_*` 파일은 커밋·빌드 금지 (기획서 원문 비공개).

## 배포

GitHub Pages + CNAME `research.remakeday.com`. DNS에 서브도메인 CNAME 레코드 필요.
