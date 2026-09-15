---
title: "Limitations & Reproducibility"
permalink: /limitations/
eyebrow: "부록"
description: 이 연구가 주장할 수 없는 것들과, 같은 결과를 다시 만드는 방법.
---

## Limitations

### Small Sample Size

해커톤 기간 내 제한된 참가자 수 (세션 5건 이상 수준). 모든 행동 결과는 exploratory다.

### Selection Bias

AI 제안 선택 vs 직접 작성은 참가자의 자발적 선택이다. 랜덤 배정된 Rationale 축 외에는
인과 해석을 하지 않는다.

### Synthetic Agents Are Not Human Simulators

일반 LLM self-play는 인간 대체 모델로 검증되지 않았다. 가설 생성과 시스템
스트레스 테스트 용도로만 쓴다.

### Single Scenario

한 시나리오에서 관찰된 패턴이 다른 도메인으로 일반화되는지는 미검증이다.

### Repeated-game Learning

후반 회차 행동에는 treatment뿐 아니라 학습 효과가 섞일 수 있다.

### Instrument Changes During Observation

관찰 기간 중 실험기구(모델·프롬프트·채점기)가 수정되었다. 수정 전후 세션은
합산하지 않고 각 세션에 당시 기구 버전을 병기한다.

---

## Reproducibility

| 대상 | 위치 |
|---|---|
| 시스템 평가 러너 | `com.remakeday/backend/scripts/run_core_selection.py` |
| NPC 대화 평가 | `com.remakeday/backend/scripts/run_npc_dialogue_check.py` |
| 수치 적립 | `com.remakeday/docs/metrics.yml` |
| 원문 raw | `com.remakeday/docs/review-verification/<date>-<experiment>/` |
| 모델 평가 정본 | `com.remakeday/docs/model_evaluation.md` |

재현 원칙:

- 조건(모델·양자화·thinking·프롬프트)을 하나라도 바꾸면 새 실험이다.
- 후보 모델의 답을 Ground Truth로 쓰지 않는다. 결정적 게이트와 사전등록 통제로만 판정한다.
- `NOT RUN`은 부끄러운 표기가 아니라 이 사이트의 신뢰 단위다.
