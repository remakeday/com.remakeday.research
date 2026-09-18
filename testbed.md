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
   └─ 규칙 선택 출처 집계·게임 점수 사례 기록
      이해도·부작용 인지·질문 품질은 정의/분석 미완료
```

즉, **게임은 연구를 보여주기 위한 포장물이 아니라 실험환경 자체**다.

REMAKE DAY의 정의:

> REMAKE DAY는 반복적인 실패–설명–수정–재실행 과정에서 사람이 AI의 제안을 언제 수용하고
> 언제 거부하며 그 선택이 이후의 문제 이해와 어떤 관계인지를 연구하기 위한
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

실패 원인을 설명하는 단계와 AI 제안에 이유를 붙이는 Rationale A/B는 다르다.
Rationale A/B는 아직 실행하지 않았다.

플레이어가 신의개입에서 마주하는 추천·직접 작성 선택 구조:

```text
원숭이손 제안 → 수락 / 거절

신의개입 규칙 선택
├─ AI Option 1 / AI Option 2 / AI Option 3
└─ Human-written Rule (직접 작성)
   └─ 거부될 때 대안 후보 순위 제시
```

AI Option 1–3는 신의개입에서 제시되는 규칙 후보이고 Human-written Rule은 직접 작성
경로다. 원숭이손 제안의 수락/거절, 추천 옵션 선택, 직접 작성은 별도 행동으로 읽는다.
직접 쓴 규칙이 거부될 때의 대안 순위에는 9/18 임베딩 변경이 추가됐다.

정의된 event-level trace(이벤트별 기록) 종류에는 `monkey_paw_offer`(원숭이손 제안),
`intervention_options`(추천 후보), `answer_scored`(밤 제출 채점),
`intervention_question`(신의 질문), `rule_applied`(규칙 적용), `session_end`(판 종료)가 있다.
수락·거절·직접 작성의 분기는 이벤트와 `rules.source`를 함께 읽어야 한다.
이 목록이 모든 내적 판단을 기록하거나 각 선택과 1:1 대응함을 뜻하지는 않는다.
이벤트 누락 검사 범위와 단계별 매핑의 공개 검증은 남아 있다.

---

## 시스템 구성

| 구성 | 역할 |
|---|---|
| Planner | 하루 전체 행동 구조 생성 |
| Agent / NPC | 인물 발화 |
| Manager | 비트(하루 안의 장면 진행 단위) 진행 판정 · 원숭이손 제안 |
| Advisor | 밤 질문 응답 · 기록 근거가 부족할 때 단정을 억제하도록 설계 |
| Evaluator | 의미 동치 판정 · 채점 |
| Domain Logic | 같은 입력에 같은 결과를 내는 게임 규칙(deterministic), LLM 판단과 분리 |
| Trace | 정의된 이벤트를 추가 전용(append-only)으로 기록 |
| Harness | 응답 형식 검사 · 재시도 · 위반 기록 도구 |

### 모델 구성 — 평가 구성과 서빙 구성

지원 어댑터의 호환성 검증과 필요한 수정이 끝난 뒤에는 provider·모델 설정으로 전환한다.
이번 외부 API 평가에서는 어댑터·러너와 출력 상한 처리도 수정했다. 같은 평가 체계를
사용하되 수정 전후 조건을 구분해야 한다. A.19 §5는 어댑터 수정 커밋 `6a02a13`을
기록하며 모든 러너·출력 상한 수정의 전후 커밋 연결은 추가 확인이 필요하다.

아래는 **2026-09-17 Core·NPC 구성 기록**이다. 9/14 kanana 채택, 9/15 gemma4 교체,
9/17 kanana 개발 구성 사이 복귀 결정·적용 시점과 정책 버전은 아직 연결 확인이 필요하다.

| 슬롯 | 2026-09-17 기록의 로컬 개발 구성 | 제출 서빙 구성 (2026-09-17 확정) |
|---|---|---|
| Core (채점·관리자 검사·신의 질문·계획·발화 분류) | `ollama:gemma4:12b` (think off) | `anthropic:claude-sonnet-5` |
| NPC (인물 대화) | `ollama:kanana1.5:8b` | `anthropic:claude-haiku-4-5` |

2026-09-18 임베딩 채택은 **서빙 `gemini-embedding-001` 2560차원, 로컬 `bge-m3`
1024차원**이다. 역할은 직접 작성 규칙이 거부될 때 제시할 대안의 순위이며 채점용
임베딩과 구분한다. → [Exp 1 · A.21]({{ '/experiments/model-selection/' | relative_url }}#a21)

서빙 전환의 기록상 이유는 이번 로컬 구성에서 동시 플레이 1명을 전제로 운영한 조건과
가용성 제약이다. GPU 한 장의 일반적인 동시 처리 한계를 뜻하지 않으며 부하 실측과
제한 정책의 근거는 추가 확인이 필요하다. 측정한 의미 품질 게이트는 통과했지만 지연
게이트는 1회·3회 반복에서 엇갈렸다. 비열등은 통계적 검정이 아닌 사전 통과선에 따른
운영 판정이다. 원숭이손·채점 캘리브레이션·누설 평가는 남아 있다.
→ [Exp 1 · A.19]({{ '/experiments/model-selection/' | relative_url }}#a19)

---

## Evaluation은 두 층으로 분리한다

### 1층 — System Evaluation

> **실험기구가 제대로 작동하는가?**

Schema pass rate · Fallback rate · Latency · Identity leak · Judge consistency 등.
→ [Exp 1 — 모델 선정]({{ '/experiments/model-selection/' | relative_url }})에서
모델·러너별로 측정했으며 항목마다 완료·미측정 상태가 다르다. Identity leak,
메타 표현 한 건의 관찰, 금칙어 누설율의 정식 측정은 구분한다.
[A.19의 남은 평가]({{ '/experiments/model-selection/' | relative_url }}#a19)도 함께 읽는다.

### 2층 — Behavioral Evaluation

> **그 실험기구 안에서 실제 사람에게 어떤 행동이 관찰되는가?**

| 항목 | 2026-09-18 공개 상태 |
|---|---|
| AI suggestion acceptance · Custom rule rate | 기존 6판의 적용 규칙 출처 20건 집계; 원숭이손 수락은 6/9로 별도 |
| Understanding trajectory | 게임 점수 사례 제시; 검증된 이해도 변화 척도는 미확정 |
| Side-effect recognition | NOT RUN; 현 기구의 측정 가능성 미해결 |
| Rationale effect | 사전등록·미실행; 설명 표시 여부(explanation exposure)를 비교할 계획 |
| Question quality | 조작적 정의·분석 미완료 |

→ [Exp 2 — 행동 관찰]({{ '/experiments/human-observations/' | relative_url }})와
[사전등록 읽기 안내]({{ '/prereg/' | relative_url }})를 구분해 읽는다.

```text
Instrument Validation
        ↓
Behavioral Experiment
```

시스템 검증은 반복 실행·기록 기능을 점검한다. 시스템 게이트 통과만으로 사람의
이해도·신뢰·부작용 인지 척도의 타당도나 행동 결과의 독립 재현까지 보장하지 않는다.
