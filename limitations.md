---
title: "Limitations & Reproducibility"
permalink: /limitations/
eyebrow: "부록"
description: 이 연구가 주장할 수 없는 것들과, 같은 결과를 다시 만드는 방법.
---

## Limitations

### Small Sample Size

사람 플레이 세션이 적다. 2026-09-18 재집계 기준 사람 판 14판(5회차 완주 10판)이고
기존 6판(확정 5·유력 1) 집계는 병기한다. 판수는 고유 참가자 수가 아니며(팀 내부 참가자
포함) 같은 판의 반복 선택은 독립 참가자 관측값이 아니다. 모든 행동 결과는 exploratory다.

### Selection Bias

AI 제안 선택 vs 직접 작성은 참가자의 자발적 선택이다. 현재 관찰에는 무작위 배정이
없어 인과 효과를 주장하지 않는다. 별도 사전등록한 Rationale A/B는 미실행이다.

### Synthetic Agents Are Not Human Simulators

일반 LLM self-play는 인간 대체 모델로 검증되지 않았다. 가설 생성과 시스템
스트레스 테스트 용도로만 쓴다.

### Single Scenario

한 시나리오에서 관찰된 패턴이 다른 도메인으로 일반화되는지는 미검증이다.

### Repeated-game Learning

현재 관찰의 후반 회차에는 반복 학습이 영향을 주었을 수 있다. 아직 실행하지 않은
Rationale A/B에서도 회차 효과를 고려해야 한다. 게임 점수는 검증된 학습효과 척도가 아니다.

### Instrument Changes During Observation

관찰 기간 중 실험기구(모델·프롬프트·채점기)가 수정되었다. 수정 전후 세션을
구분하는 것을 원칙으로 한다. 다만 기존 6판 집계에는 버전이 섞여 있어 경향 주장에
쓰지 않으며 버전별 분리는 후속 작업이다. 확인 가능한 수정 전후 구분과 미확인
모델·프롬프트·커밋은 [세션별 기구 기록]({{ '/experiments/human-observations/' | relative_url }}#instrument-versions)에 적었다.

### Serving Configuration ≠ Observation Configuration

사람 세션은 로컬 모델 구성(ollama, NPC 모델은 시기에 따라 다름)에서 수집됐다.
제출·심사 서빙은 외부 API(Core `claude-sonnet-5` · NPC `claude-haiku-4-5`)로 한다.
외부 API는 같은 평가 체계로 비교해 측정한 의미 품질 게이트를 통과했으나 지연
게이트는 1회·3회 반복에서 엇갈렸다. 이 운영상 비열등 판정은 통계적 비열등성
검정이 아니다. 원숭이손·채점 캘리브레이션·누설 평가는 남아 있다.
[Exp 1 · A.19]({{ '/experiments/model-selection/' | relative_url }}#a19)의 채택 결정이
사람 행동의 동일성을 보장하지는 않는다. 서빙 구성 세션은 로컬 구성과 구분해야 한다.

### Judge Model Change

7세 정책 채점기를 2026-09-16에 `gemma3:12b`에서 `gemma4:12b`(think off)로 바꿨다.
Haiku 1차 로그에서 고른 같은 발화 20건을 두 채점기로 각각 2회 재채점했을 때
채점기 간 일치는 19/20(95%)이었다. 분모 20은 발화 수이며 두 번 반복했다고 40개의
독립 발화가 되지는 않는다. 모든 정책·모델에서의 동등성을 뜻하지 않는다.
교체 전후 수치는 채점기를 병기해 따로 읽는다. 상세 조건은
[Exp 1 · A.19 §4]({{ '/experiments/model-selection/' | relative_url }}#a19)를 따른다.

<span id="scoring-stability"></span>

### Scoring Stability Is Not Established

같은 자유서술(md5 동일) 제출이 4→5회차에서 67.9 → 53.3으로 채점된 이력이 있다
(테스터3, 2026-09-10). 2026-09-14에 넣은 단조 잠금은 앞 회차에서 인정된 문장이 그대로
남으면 판정을 낮추지 않는 장치다. 잠금 도입 뒤 완주 6판에서 4→5회차 하락은 0건, 도입 전
4판은 모두 하락했다. 이는 잠금이 작동했다는 뜻이지 채점기가 같은 입력에 같은 판정을
낸다는 증거가 아니다. partial 판정 경계의 정량 정의와 조건을 고정한 재생 검증은 남아 있다.
[Exp 2 · 14판 집계]({{ '/experiments/human-observations/' | relative_url }}#aggregate-14)

<span id="fun-and-completion"></span>

### Fun and Completion Are Not Measured as a Gate

재미 게이트(외부 참가자·1회차·제한 시간)는 돌리지 않았다. 완주율(14판 중 10판)과 이탈
지점은 DB 기록으로 셀 수 있지만 재미의 측정값이 아니다. 참가자 모집 경로가 공개돼 있지
않아 외부 표본이라고 주장하지 않는다. 첫 회차 총점은 0.0~55.4로 낮게 시작한 판이 많았고
난이도가 높다는 피드백이 반복됐다. 난이도·재미의 목표 구간은 미정이다.

### Cost Figures Are Estimates

외부 API 판당 비용($0.68~0.97, 사람 5회차 완주 판 기준)은 기록된 입출력 문자 수에
**1자 = 0.7~1.0토큰**이라는 환산 가정과 모델별 입력·출력 단가를 적용한 추정이다.
2026-09-17 계산 기록은 100만 토큰당 Sonnet 5 입력 $2·출력 $10, Haiku 4.5 입력 $1·출력 $5,
환율 1,400원/$를 썼다. 이는 당시 계산에 쓴 미국 달러 단가이며 현재 가격 검증이 아니다.
원 단가 참조표의 기준일은 2026-06-24로 기록돼 있다.

산식은 모델별 `(입력 문자 × 환산계수 × 입력 단가 + 출력 문자 × 환산계수 × 출력 단가) / 1,000,000`의 합이다.
thinking 토큰·재생성·임베딩은 제외했다. 9/18 추가된 임베딩 비용까지 포함한 추정으로
읽지 않는다. 전체 비용의 87~94%와 Core 입력량의 56~68%는 각각 비용·입력량의 비율이다.
어댑터가 `response.usage`를 기록하지 않아 실측 토큰 정산은 아직 없다.
공개 근거는 [Exp 1 · A.19 §6]({{ '/experiments/model-selection/' | relative_url }}#a19),
산식 정본은 앱 저장소의 `docs/apiscenario.md` 최종 예상 비용·§1.2다.

---

## Reproducibility

이 사이트는 **공개 스냅샷의 근거 위치**를 제공한다. 아래 앱 저장소 내부 경로는
독립 실행 가능한 공개 재현 묶음을 뜻하지 않는다. 입력 fixture·환경·고정 버전·실행
명령·기대 산출물을 함께 묶은 공개 패키지는 아직 없다. 비공개 원문 로그·프롬프트·
시나리오 자료는 공개 접근 범위 밖이며 이 문서에서 공개를 전제하지 않는다.
일부 로컬 산출물은 git에 포함되지 않아 앱 커밋만으로 복구할 수도 없다.

공개 독자는 [Exp 1]({{ '/experiments/model-selection/' | relative_url }})의 조건별
집계와 [Exp 2]({{ '/experiments/human-observations/' | relative_url }})의 수집 시점·
기구 변경 기록을 검토할 수 있다. 시스템 평가 통과가 행동 척도의 구성타당도까지
검증했다는 뜻은 아니다.

| 대상 | 앱 저장소 내부 근거 위치 |
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
