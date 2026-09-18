# 원시 집계·선행연구 대조 기록

연결된 로컬 집계·선택 행·측정 스크립트 대조. 실험 재실행이나 모든 원시 이벤트/비공개 자료 검증이 아니다.

앱 현재 커밋: `f92001a7c1bbfdb8e85038eb59aad9cbae32198c`. 공개 스냅샷의 앱 기준 커밋: `1568438`.

파일의 SHA-256과 실제 확인한 집계는 [기계 판독 기록](raw-evidence.json)에 보관했다. `tracked: false`는 로컬 결과 파일로, 앱 커밋만으로 재현되지 않음을 뜻한다.

## RAW-01

공개 비교표의 evaluator 2,918ms는 advisor 원시 집계와 일치하고, 연결된 evaluator 원시 집계는 2,179ms다.

확인 한계: 다른 날짜의 별도 측정값을 의도했을 가능성은 작성자가 확인해야 한다. 역할·실행 식별자 확인 없이 숫자만 자동 교체하지 않는다.

근거 파일:

- `docs/review-verification/2026-09-13-core-selection/stage1-smoke-advisor-20260913T124645Z.json`
- `docs/review-verification/2026-09-13-core-selection/stage2-formal-20260914T021635Z.json`

## RAW-02

그림의 검수 22문장 적중 수 8·20·18·20·21·21은 개별 행에서 다시 센 값과 일치한다. Qwen1536은 Qwen2560보다 이 세트에서 두 문장을 덜 맞혔다.

확인 한계: 검수자의 판단 자체를 독립 재검수한 것은 아니다. 원시 입력 문장·정답·후보 대사는 보고서에 복사하지 않았다.

근거 파일:

- `output/rule-alternatives-2026-09-18/rule-alternatives-20260918T021836Z.json`

## RAW-03

반복 3회 파일은 모두 초기 30문장 세트다. 같은 문장 순서에서 적중률과 top-1 오답 위치가 동일했다. 검수 22문장 반복 결과로 표기하면 안 된다.

확인 한계: 세 번의 일치를 확률적 변동 부재나 전체 모델의 불변 성질로 확대하지 않는다.

근거 파일:

- `output/rule-alternatives-2026-09-18/rule-alternatives-rep1.json`
- `output/rule-alternatives-2026-09-18/rule-alternatives-rep2.json`
- `output/rule-alternatives-2026-09-18/rule-alternatives-rep3.json`

## RAW-04

확인한 8개 결과 파일의 측정 조건은 1024·1536·2560·3072 중 일부다. 128차원 측정은 이 파일들에 없고 22문장과30문장 조건도 다르다.

확인 한계: 저장소 밖의 추가 파일이 전혀 없다고 단정하지 않는다. 지원 범위를 전 구간 실측으로 쓰려면 추가 근거가 필요하다.

근거 파일:

- `output/rule-alternatives-2026-09-18/rule-alternatives-20260918T012519Z.json`
- `output/rule-alternatives-2026-09-18/rule-alternatives-20260918T014146Z.json`
- `output/rule-alternatives-2026-09-18/rule-alternatives-20260918T014215Z.json`
- `output/rule-alternatives-2026-09-18/rule-alternatives-20260918T021836Z.json`
- `output/rule-alternatives-2026-09-18/rule-alternatives-20260918T022248Z.json`
- `output/rule-alternatives-2026-09-18/rule-alternatives-rep1.json`
- `output/rule-alternatives-2026-09-18/rule-alternatives-rep2.json`
- `output/rule-alternatives-2026-09-18/rule-alternatives-rep3.json`

## RAW-05

확인한 n=1 파일은 Sonnet5·Opus5, n=3 파일은 Sonnet5만 포함한다. 두 모델 모두 n=3을 통과했다는 설명에는 Opus5의 별도 근거가 필요하다.

확인 한계: 이 두 파일 밖에 Opus5 n=3 측정이 존재하지 않는다는 단정은 하지 않는다.

근거 파일:

- `output/model-eval-2026-09-16-anthropic/stage2-formal-20260916T121314Z.json`
- `output/model-eval-2026-09-16-anthropic/stage2-formal-20260916T143841Z.json`

## RAW-06

A.17의 페르소나·관련성 행에는 무승부가 각각1개 빠져 있다. 각행25쌍은 승A+승B+무승부+invalid로 합산해야 한다.

확인 한계: 유효쌍과 판정불가를 분리해야 하며 invalid를 패배로 재분류하지 않는다.

근거 파일:

- `docs/review-verification/2026-09-14-npc-descent/npc-quality-ab-20260914T112712Z.json`

## RAW-07

Tester6의 공개5회 총점과 동일 제출문 길이는 앱 저장소의 DB 집계 보고서와 일치한다.

확인 한계: DB에 다시 접속해 원시 이벤트를 조회한 검증은 아니다. 기존6판 전체의 참여자 분류·CV·작성 이벤트 분류는 확인 자료가 더 필요하다.

근거 파일:

- `docs/review-verification/2026-09-16-tester6/tester6.md`

## RAW-08

어간 겹침 기준선도 실행 시간을 측정한다. 0.0ms는 한 자리 반올림된 요약값이며 시간 측정 생략이나 정확한0을 뜻하지 않는다.

확인 한계: 이 값으로 타이머의 실제 유효 분해능이나 다른 환경의 성능까지 추정하지 않는다.

근거 파일:

- `backend/scripts/run_rule_alternatives_eval.py`

## 관련 연구에 비추어 주장 범위 점검

AI 제안을 받아들이는 행동을 실험으로 관찰한 선행 사례가 있다. Buçinca 등은 199명이 참여한 실험에서 AI 제안의 과수용과 여러 개입 조건을 비교했다. [Buçinca et al. (2021)](https://arxiv.org/abs/2102.09692).

Lai와 Tan은 속임수 탐지 실험환경에서 모델 예측과 설명을 제시하는 방식을 달리해 인간 판단을 관찰했다. [Lai & Tan (2019)](https://arxiv.org/abs/1811.07901).

이 자료에 근거한 검토 판단: “측정할 방법이 없다”는 분야 전체의 부재 주장보다, 이번 프로젝트가 구현한 반복 실패–규칙 수정 환경과 기록 방식의 기여를 구체화해야 한다. 같은 게임 장치의 신규성까지 이 두 논문으로 판정하지 않는다.

논문 초록과 저자·연도·출판정보를 확인한 두 선행사례다. 체계적 문헌 고찰이나 REMAKE DAY와 동일한 게임기구의 존재 증명은 아니다.
