---
title: "Testbed — 실험환경으로서의 REMAKE DAY"
permalink: /testbed/
eyebrow: "System Design"
description: 게임은 연구를 보여주기 위한 포장물이 아니라 실험환경 자체다. 반복 가능한 실패–수정 루프와 측정 인프라.
---

## 게임과 연구의 관계

```text
REMAKE DAY
│
├─ Game
│  └─ 실제로 플레이 가능한 추리·대화형 게임
│
├─ Experimental Testbed
│  └─ 반복 가능한 실패·수정 환경
│
└─ Behavioral Measurement
   └─ AI 제안 수용, 직접 작성, 이해도 변화,
      부작용 인지, 질문 품질 등을 계측
```

즉, **게임은 연구를 보여주기 위한 포장물이 아니라 실험환경 자체**다.

REMAKE DAY의 정의:

> REMAKE DAY는 반복적인 실패–설명–수정–재실행 과정에서 사람이 AI의 제안을 언제 수용하고
> 언제 거부하며, 그 선택이 이후의 문제 이해와 어떤 관계인지를 측정하는
> **게임 기반 Human–AI Interaction Testbed**다.

---

## Figure 1 — System Loop

```text
Human Player
    ↓
Observe / Talk / Infer
    ↓
Explain Failure
    ↓
AI Advisor
    ↓
Accept / Reject / Write
    ↓
Apply Rule
    ↓
Re-execute
    ↓
Next Loop
```

플레이어가 매 회차 마주하는 선택 구조 (신의개입):

```text
AI Option 1
AI Option 2
AI Option 3
Human-written Rule
```

이 선택 하나하나가 event-level trace로 기록된다: `monkey_paw_offer`,
`intervention_options`, `answer_scored`, `intervention_question`,
`rule_applied`, `session_end`.

---

## 시스템 구성

| 구성 | 역할 |
|---|---|
| Planner | 하루 전체 행동 구조 생성 |
| Agent / NPC | 인물 발화 |
| Manager | 비트 진행 판정 · 원숭이손 제안 |
| Advisor | 밤 질문 응답, 근거 기반 억제 |
| Evaluator | 의미 동치 판정 · 채점 |
| Domain Logic | deterministic, LLM 판단과 분리 |
| Trace | 모든 이벤트 append-only 기록 |
| Harness | 스키마 검증 · 재생성 · 위반 계측 |

---

## Evaluation은 두 층으로 분리한다

### 1층 — System Evaluation

> **실험기구가 제대로 작동하는가?**

Schema pass rate · Fallback rate · Latency · Identity leak · Judge consistency 등.
→ [Exp 1 — 모델 선정]({{ '/experiments/model-selection/' | relative_url }})에서 실측 완료.

### 2층 — Behavioral Evaluation

> **그 실험기구 안에서 실제 사람에게 어떤 행동이 관찰되는가?**

AI suggestion acceptance · Custom rule rate · Rationale effect · Side-effect
recognition · Question quality · Understanding trajectory.
→ [Exp 2 — 행동 관찰]({{ '/experiments/human-observations/' | relative_url }})에서 적립 중.

```text
Instrument Validation
        ↓
Behavioral Experiment
```

기구 검증 없이 행동 결과를 주장하지 않는다. 순서가 곧 방법론이다.
