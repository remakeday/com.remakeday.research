---
title: "AI 제안 수용 측정을 위한 게임 기반 Human–AI 상호작용 실험환경의 설계 및 검증"
short_title: "REMAKE DAY Research"
permalink: /
eyebrow: "Research Report · 작성 중"
status: "탐색적 관찰 · 기존 집계 6판(확정 5·유력 1), 후속 사례 1판 별도"
description: "REMAKE DAY: A Game-Based Testbed for Measuring Human Reliance on AI Suggestions in Iterative Failure-Recovery Loops"
---

## Abstract

규칙 선택 출처는 기존 6판의 적용 규칙 20건을 집계했고 게임 점수는 사례로 제시했다.
부작용 인지율은 `NOT RUN`이며 측정 가능성부터 미해결이다. Rationale A/B는 사전등록·미실행이고
질문 품질·이해도 변화는 조작적 정의와 분석이 아직 확정되지 않았다.

Agentic systems increasingly place humans in loops where AI suggests interventions
and humans accept, reject, or revise them. However, this reliance is difficult
to observe repeatedly under controlled and reproducible conditions.

We introduce **REMAKE DAY**, a game-based experimental testbed that reproduces an
execution–failure–explanation–revision loop. The environment records defined
choice, submission, and rule-application events.
We report exploratory counts of applied-rule sources and game-score case records.
Rationale effects, side-effect recognition, question quality, and understanding
change remain unmeasured or require operational definitions.

The game supports repeated execution and behavioral recording for studying
human–AI decision making. Independent reproduction of behavioral results and
validation of psychological measures remain to be established.

---

## 포지셔닝

이 프로젝트가 보여주려는 것은 "AI를 이용해 게임을 만들었다"가 아니다.

> **AI Agent가 개입하는 반복적 실패–수정 환경을 만들고 그 안에서 사람이 AI의 제안을
> 수용·거절하고 규칙을 선택했는지를 행동 기록으로 관찰했다.**

> *We built a repeatable game environment that records defined choices about
> AI-generated interventions; the current behavioral evidence is exploratory.*

```text
                    REMAKE DAY

┌──────────────────────────────────────────┐
│ 1. GAME                                  │
│ 실제 플레이 가능한 제품                  │
└──────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────┐
│ 2. EXPERIMENT DASHBOARD                  │
│ Acceptance / Rationale / Understanding   │
│ Side-effect / Question Quality           │
└──────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────┐
│ 3. RESEARCH REPORT                       │
│ Question → Hypothesis → Method           │
│ → Results → Limitations                  │
└──────────────────────────────────────────┘
```

---

## Contributions

**C1 — Experimental Environment.** 실패 → 설명 → AI 제안 → Human Approval → 규칙 수정 →
재실행 과정을 반복 가능한 게임환경에서 실행·기록할 수 있도록 구현했다(operationalize).

**C2 — Behavioral Measurement.** 정의한 선택·제출·규칙 적용을
event-level trace(이벤트별 기록)로 남겼다. AI 계열 규칙과 직접 작성 규칙의 출처를
6판 20건에서 집계했다. explanation exposure(설명 표시 여부)는 향후 Rationale A/B의
조건이며 질문 품질·이해 변화·부작용 인지는 로그 보유만으로 측정 완료라고 하지 않는다.

**C3 — Reproducible Evaluation.** LLM 판단과 deterministic domain logic(같은 입력에
같은 결과를 내는 게임 규칙)을 분리했다. 반복 실행과 행동 기록을 지원하며 공개한 집계는
명시된 수집 시점·기구 조건의 기록을 기준으로 한다. 독립 재현 묶음과 행동 척도의 타당도는
별도 과제다. → [재현 범위와 한계]({{ "/limitations/" | relative_url }})

---

## 현재 상태

| 트랙 | 상태 | 페이지 |
|---|---|---|
| System Evaluation — 모델 선정 (E7/E6) | **역할별 실측·채택**: Funnel 5단계 실행과 Core·NPC 채택 기록. manager_paw 등 미측정 축은 Exp 1에서 별도 확인 | [Exp 1]({{ '/experiments/model-selection/' | relative_url }}) |
| System Evaluation — 외부 API 서빙 (A.19) | **2026-09-17 채택**: Core Sonnet 5 · NPC Haiku 4.5. 측정한 의미 품질 게이트 통과, 지연 게이트는 1회·3회 반복에서 엇갈림. 남은 평가: 원숭이손·채점 캘리브레이션·누설 | [Exp 1 · A.19]({{ '/experiments/model-selection/' | relative_url }}#a19) |
| Behavioral Observation — 사람 플레이 | **진행 중**: 기존 집계 6판(확정 5·유력 1, 기구 버전 혼재), 9/16 후속 5회차 완주 사례 1판 별도. 판수는 고유 참가자 수가 아님 | [Exp 2]({{ '/experiments/human-observations/' | relative_url }}) |
| Rationale A/B (Anchor Experiment) | **사전등록·미실행**: 공개 원문 고정, 배정·분모·분석 등 미정 항목은 읽기 안내 참조 | [사전등록]({{ '/prereg/' | relative_url }}) |

이 사이트의 원칙은 하나다. **측정하지 않은 것은 주장하지 않는다.**
미측정 항목은 `NOT RUN`으로 표기하고 표본이 작으면 작다고 쓴다.
