---
title: "AI 제안 수용 측정을 위한 게임 기반 Human–AI 상호작용 실험환경의 설계 및 검증"
short_title: "REMAKE DAY Research"
permalink: /
eyebrow: "Research Report · 작성 중"
status: "Exploratory · 사람 세션 6판"
description: "REMAKE DAY: A Game-Based Testbed for Measuring Human Reliance on AI Suggestions in Iterative Failure-Recovery Loops"
---

## Abstract

Agentic systems increasingly place humans in loops where AI suggests interventions
and humans accept, reject, or revise them. However, this reliance is difficult
to observe repeatedly under controlled and reproducible conditions.

We introduce **REMAKE DAY**, a game-based experimental testbed that reproduces an
execution–failure–explanation–revision loop. The environment records human choices
between AI-generated and self-written interventions, explanation exposure,
side-effect recognition, and subsequent understanding.

We demonstrate how a game environment can function not only as an AI product, but
as a **reproducible behavioral testbed** for studying human–AI decision making.

---

## 포지셔닝

이 프로젝트가 보여주려는 것은 "AI를 이용해 게임을 만들었다"가 아니다.

> **AI Agent가 개입하는 반복적 실패–수정 환경을 만들고, 그 안에서 사람이 AI의 제안을
> 어떻게 판단하는지를 실제 행동 데이터로 측정했다.**

> *We did not build a game only to demonstrate an AI agent. We built a reproducible
> environment in which human decisions about AI-generated interventions can be measured.*

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
재실행을 반복 가능한 게임환경으로 operationalize했다.

**C2 — Behavioral Measurement.** AI 제안 수락/거부, 직접 작성, explanation exposure,
질문 품질, 이해 변화, 부작용 인지를 event-level trace로 측정한다.
사람 테스터 세션이 이벤트 단위로 기록되어 있다.

**C3 — Reproducible Evaluation.** LLM 판단과 deterministic domain logic을 분리하고
동일 trace에서 system evaluation과 human behavioral evaluation을 재현한다.

---

## 현재 상태

| 트랙 | 상태 | 페이지 |
|---|---|---|
| System Evaluation — 모델 선정 (E7/E6) | **완료**: Funnel 5단계 실측, Core·NPC 슬롯 채택 | [Exp 1]({{ '/experiments/model-selection/' | relative_url }}) |
| Behavioral Observation — 사람 플레이 | **진행 중**: DB 전수 판별로 사람 세션 6판 분리, RQ1 예비 집계 완료 | [Exp 2]({{ '/experiments/human-observations/' | relative_url }}) |
| Rationale A/B (Anchor Experiment) | **사전등록**: 설계 고정, 미실행 | [사전등록]({{ '/prereg/' | relative_url }}) |

이 사이트의 원칙은 하나다. **측정하지 않은 것은 주장하지 않는다.**
미측정 항목은 `NOT RUN`으로 표기하고 표본이 작으면 작다고 쓴다.
