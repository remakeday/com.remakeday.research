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

### Serving Configuration ≠ Observation Configuration

사람 세션은 로컬 모델 구성(ollama, NPC 모델은 시기에 따라 다름)에서 수집됐다.
제출·심사 서빙은 외부 API(Core `claude-sonnet-5` · NPC `claude-haiku-4-5`)로 한다.
외부 API는 같은 러너·같은 게이트로 비열등을 확인했지만(Exp 1 A.19) 게이트 통과가
사람 행동의 동일성을 보장하지는 않는다. 서빙 구성에서 들어온 세션은 로컬 구성 세션과
합산하지 않는다.

### Judge Model Change

7세 정책 채점기를 2026-09-16에 `gemma3:12b`에서 `gemma4:12b`(think off)로 바꿨다.
두 채점기의 일치율은 19/20(95%)이다. 교체 전후 수치는 채점기를 병기해 따로 읽는다.

### Cost Figures Are Estimates

외부 API 판당 비용($0.68~0.97, 사람 5회차 완주 판 기준)은 입출력 문자 수에 단가를
곱한 추정이다. 어댑터가 `response.usage`를 기록하지 않아 실측 토큰 정산은 아직 없다.

---

## Reproducibility

| 대상 | 위치 |
|---|---|
| 시스템 평가 러너 | `com.remakeday/backend/scripts/run_core_selection.py` |
| NPC 대화 평가 | `com.remakeday/backend/scripts/run_npc_dialogue_check.py` |
| NPC 7세 정책 평가 | `com.remakeday/backend/scripts/run_age7_check.py` |
| 종단간 self-play | `com.remakeday/backend/scripts/run_selfplay.py` |
| 외부 API 비용 추정 | `com.remakeday/docs/apiscenario.md` |
| 수치 적립 | `com.remakeday/docs/metrics.yml` |
| 원문 raw | `com.remakeday/docs/review-verification/<date>-<experiment>/` |
| 모델 평가 정본 | `com.remakeday/docs/model_evaluation.md` |

재현 원칙:

- 조건(provider·모델·양자화·thinking·프롬프트·채점기)을 하나라도 바꾸면 새 실험이다.
- 후보 모델의 답을 Ground Truth로 쓰지 않는다. 결정적 게이트와 사전등록 통제로만 판정한다.
- `NOT RUN`은 부끄러운 표기가 아니라 이 사이트의 신뢰 단위다.
