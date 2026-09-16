---
title: "사전등록 — Rationale → Acceptance"
permalink: /prereg/
eyebrow: "Preregistration · 설계 고정"
status: "미실행"
description: "결과를 보기 전에 가설·조건·측정값·판정 기준을 고정해 공개한다. Anchor Experiment: AI 제안에 이유(rationale)를 붙이면 수용률이 달라지는가."
---

<div class="callout">
  <div class="callout__title">사전등록의 의미</div>
  <p>이 페이지는 <strong>데이터를 보기 전에</strong> 실험 설계를 고정해 공개하는 기록이다.
  이후 결과가 어떻게 나오든 이 설계를 바꾸지 않으며 바뀌면 새 실험으로 등록한다.
  게시일 기준으로 본 실험은 <strong>미실행(NOT RUN)</strong> 상태다.</p>
</div>

## Research Questions

### RQ1 — Human Approval

> When humans receive AI-generated intervention suggestions after failure, how often
> do they accept the suggestions rather than create their own?

### RQ2 — Explanation Effect *(Anchor Experiment)*

> Does providing an explanation for an AI suggestion change the probability that
> humans accept it?

### RQ3 — Decision Quality

> How are different intervention strategies associated with subsequent understanding
> and side-effect recognition?

---

## Anchor Experiment 설계

### Independent Variable

```text
Rationale
A = absent   (AI suggestion only)
B = present  (AI suggestion + rationale)
```

### Primary Outcome

```text
AI suggestion acceptance rate
```

### Secondary Outcomes

```text
Δ Understanding Score
Side-effect Recognition
Custom Rule Selection
Cause-chain Question Hit Rate
```

### 배정

```text
Participants
    │
Random Assignment
    │
┌───┴───┐
│       │
A       B
│       │
No      With
Reason  Reason
│       │
└───┬───┘
    ↓
Acceptance Rate
```

표본이 작으면 억지로 유의성을 주장하지 않는다. 예: `N = 24, exploratory result`.

### 필수 로그

```text
monkey_paw_offer · intervention_options · answer_scored
intervention_question · rule_applied · session_end
```

---

## 사전등록 통제 (advisor_answer 의미 축)

기대 방향을 실험 전에 고정해 둔 통제 문항으로 기계 채점한다.
특히 **극성 쌍(PC3·PC4, SPC1·SPC2)은 반드시 함께 판정한다.** 한쪽만 통과하면
모델이 기록이 아니라 질문 표면을 읽고 있다는 뜻이다.

| 통제 | 기대 | 성격 |
|---|---|---|
| PC1·PC2·PC5 | supported | 기록에 있는 사실 |
| PC3 / PC4 | contradicted / supported | **극성 쌍**: 같은 사건, 반대 질문 |
| PC6·PC7·PC8 | unknown | 기록에 없는 것: 모른다고 답해야 함 |
| SPC1 / SPC2 | supported / contradicted | **합성 극성 쌍**: 기록을 뒤집은 fixture |

```text
PCA = 기대 방향과 일치한 통제 수 / 통제 문항 수
```

이 통제 세트는 [Exp 1]({{ '/experiments/model-selection/' | relative_url }})의
시스템 평가에서 이미 사용·검증되었다 (2026-09-09 코퍼스).

---

## 해석 원칙 (미리 고정)

- 인과 표현 금지: 랜덤 배정된 Rationale 축 외에는 전부 연관성으로 서술한다.
- 폴백은 성공으로 집계하지 않는다.
- 효과가 관찰되지 않으면 그대로 쓴다.
  *"We did not observe meaningful evidence that rationale presentation increased
  acceptance in our sample."* 이것도 결과다.

---

## Synthetic → Human (P1, 선택)

가능하다면 사람 실험 전에 LLM 플레이어로 in-silico pilot을 돌려 가설 후보를 생성한다.

> Synthetic agents were used for hypothesis generation and system stress-testing,
> **not** as validated substitutes for human participants.

비교 대상은 수치의 일치가 아니라 **방향성(directional regularity)의 보존**이다.
