# 리서치 전체 문장·독해 검토

> 1차 요약 보관본입니다. 후속 전수 검토와 원시 집계 확인 결과는 [전체 검토 — 775개 단위와 수정·확인 제안](full-audit/README.md)을 기준으로 읽으세요.

검토일: 2026-09-18. 대상 커밋: `ff6afd0b3d0625b443cabbf5a2e9be34f9ac1037`.

**요약 화면은 읽기 쉬워졌지만, 상세 본문에는 현재 결론을 찾기 어려운 누적 기록과 근거보다 강한 해석이 남아 있다.** 심사위원과 AI·통계에 익숙하지 않은 개발자에게는 말투를 고치는 것보다 이 부분을 먼저 정리하는 편이 도움이 된다. 일부 문장은 가볍게 윤문할 수 있지만, 수치의 출처와 주장의 범위는 별도로 확인해야 한다.

사용자가 지정한 [im-not-ai의 humanize-korean 스킬](https://github.com/epoko77-ai/im-not-ai/blob/9747f036cdc28a1a8aea4dc71fef1f7846eb96f7/codex/skills/humanize-korean/SKILL.md)과 같은 커밋의 `quick-rules.md`를 읽어 적용했다. 제공된 `metrics_v2.py`도 실행했다. 서브에이전트 3명이 범위를 나눠 원문을 모두 읽었고, 주 검토자가 주요 발견을 공개 소스와 다시 대조했다. 아래에서 **문체 규칙에 해당하는 지적**과 **추가 독해·근거 검토**를 구분한다. 원문과 사이트 문구는 수정하지 않았다.

## 먼저 확인할 근거와 상태

다음 항목은 의미를 그대로 두는 윤문만으로 해결되지 않는다. 수치는 원시 결과를 확인하기 전에 바꾸지 않고, 해석을 좁히는 제안은 연구 내용 정정으로 다룬다. ‘높음’은 이번 검토의 수정 우선순위이며 im-not-ai의 S1/S2 분류나 AI 작성 가능성을 뜻하지 않는다.

### R01 · 높음 · 외부 API 비교표의 로컬 지연 기준 출처 확인

[Exp 1:1389](/home/kimchungsik/projects/research.remakeday.com/experiments/model-selection.md:1389)의 열 이름은 `evaluator p50(ms)`이고, 로컬 모델 행에는 **2,918ms**가 들어 있다. 그러나 [A.8:941](/home/kimchungsik/projects/research.remakeday.com/experiments/model-selection.md:941)의 같은 모델 `evl p50`은 **2,179ms**다. **2,918ms**는 [A.6:787](/home/kimchungsik/projects/research.remakeday.com/experiments/model-selection.md:787)의 `advisor_answer` 측정값과 일치한다.

역할이 다른 지연을 옮긴 것인지, 다른 조건으로 다시 측정한 값인지 공개 설명만으로 확정할 수 없다. 비교표의 역할·측정일·실행 결과 출처를 정본과 대조해야 한다. **2,179로 자동 교체하라는 지적은 아니다.** 현재 두 수치를 대조해 확인할 이유가 있다는 뜻이다.

### R02 · 높음 · 검수 22문장과 미검수 30문장의 반복 검증 구분

[Lab Notes:17](/home/kimchungsik/projects/research.remakeday.com/lab-notes.md:17)은 검수한 22문장의 적중률 뒤에 “반복 n=3 적중률·오답 집합 완전 동일”을 붙인다. 읽는 사람은 22문장을 세 번 반복했다고 받아들일 수 있다. [정본 스냅샷:1706](/home/kimchungsik/projects/research.remakeday.com/experiments/model-selection.md:1706)은 반복 검사를 **1차 골든**, 즉 미검수 30문장 대상으로 명시한다.

문장 보완 예: “별도로, 미검수 1차 골든 30문장의 n=3 반복에서는 적중률과 오답 집합이 같았다.” 검수 22문장의 수치는 그대로 둔다. [Exp 1:1678](/home/kimchungsik/projects/research.remakeday.com/experiments/model-selection.md:1678)의 긴 절 제목도 두 검사가 같은 세트인 것처럼 읽히지 않게 구분하면 좋다. 새 차트 캡션은 이미 두 세트를 정확히 구분하고 있다.

### R03 · 높음 · ‘수정 전후 세션을 합산하지 않는다’와 실제 집계 상태

[한계:34](/home/kimchungsik/projects/research.remakeday.com/limitations.md:34)는 수정 전후 세션을 합산하지 않는다고 서술한다. 반면 [Exp 2:72](/home/kimchungsik/projects/research.remakeday.com/experiments/human-observations.md:72)는 기존 6판 집계에 기구 버전이 섞였으며 버전별 분리 집계가 후속 작업이라고 명시한다.

분리 원칙과 현재 남은 예외를 함께 써야 한다. 예: “수정 전후 세션은 분리해 해석하는 것을 원칙으로 한다. 다만 기존 6판 집계에는 기구 버전이 섞여 있어 경향 주장에 쓰지 않으며, 버전별 분리 집계는 후속 작업으로 남아 있다.” 기존 집계나 후속 Tester 6 사례의 값을 바꾸는 제안은 아니다.

### R04 · 높음 · top-3 적중률과 같은 추천 목록은 다르다

[Exp 1:1634](/home/kimchungsik/projects/research.remakeday.com/experiments/model-selection.md:1634)는 “top-3가 양쪽 다 1.000이라 플레이어가 보는 결과는 사실상 같다”고 해석한다. 하지만 바로 위 [순위 일치도 표:1625](/home/kimchungsik/projects/research.remakeday.com/experiments/model-selection.md:1625)의 Gemini↔Qwen top-3 Jaccard는 **0.627 / 0.600**이다.

정답이 상위 3개 안에 있다는 사실과, 보여 주는 세 대안이 같다는 사실을 구분해야 한다. 해석 정정 후보: “두 모델 모두 정답을 top-3 안에 포함했다. 추천 목록과 순서의 일치도는 Jaccard와 Kendall τ로 따로 확인한다.” 실제 사용자 경험이 같다는 결론도 이 표만으로 추가하지 않는다.

### R05 · 높음 · 지원 차원 범위를 측정 범위로 확대하지 않기

[Exp 1:1739](/home/kimchungsik/projects/research.remakeday.com/experiments/model-selection.md:1739)는 “128~3072 전 구간에서 … 차원 무관”이라고 쓴다. 128은 [지원 범위 설명:1661](/home/kimchungsik/projects/research.remakeday.com/experiments/model-selection.md:1661)에 나오며, 공개 비교표에는 1024·1536·2560·3072의 일부 조건만 제시된다. 이 조건들도 초기 30문장과 검수 22문장으로 나뉜다. [Lab Notes:19](/home/kimchungsik/projects/research.remakeday.com/lab-notes.md:19)의 “0.955(1024~3072 전 차원 동일)”에도 같은 범위 확인이 필요하다.

정정 시에는 **세트별로 실제 비교한 차원과 지표**를 적는다. 적중률이 같았다는 설명을 전체 순위가 같다는 뜻으로 넓히지 않는다. [1736행](/home/kimchungsik/projects/research.remakeday.com/experiments/model-selection.md:1736)의 τ도 1.000이 아닌 0.964다.

### R06 · 높음 · 세 번의 일치를 모델 일반 성질로 단정하지 않기

[Exp 1:877](/home/kimchungsik/projects/research.remakeday.com/experiments/model-selection.md:877)의 “우연이 아니라 모델의 성질이다”는 n=3에서 판정이 같았다는 관찰보다 넓은 주장이다. 같은 절은 뒤에서 통계적 유의성을 주장하지 않는다고 제한한다.

해석 정정 후보: “이번 통제 문항의 n=3 반복에서는 판정이 달라지지 않았다.” 값과 반복 수는 보존한다. [892행](/home/kimchungsik/projects/research.remakeday.com/experiments/model-selection.md:892)의 오류 부재 단정과 [1268행](/home/kimchungsik/projects/research.remakeday.com/experiments/model-selection.md:1268)의 모델 계열 성질 단정도 같은 방식으로 측정 조건 안에 한정할 필요가 있다.

### R07 · 높음 · 프로젝트의 기여와 분야 전체의 부재·최상급 구분

[Statement:15](/home/kimchungsik/projects/research.remakeday.com/statement.md:15)의 “측정할 방법이 없습니다”, [25행](/home/kimchungsik/projects/research.remakeday.com/statement.md:25)과 [52행](/home/kimchungsik/projects/research.remakeday.com/statement.md:52)의 “가장 빠른”은 관련 연구 검토나 대안과의 속도 비교가 필요한 주장이다. 사이트에 있는 하루 단위 모델 평가 기록만으로는 그 범위를 뒷받침하지 못한다.

저자가 주장을 좁히기로 한다면 “저희는 AI 제안의 수용·거부를 반복해서 측정할 게임 환경을 만들었습니다”, “이 환경에서 모델 교체를 하루 단위 실측으로 결정했습니다”처럼 실제 수행 범위를 쓸 수 있다. 이는 원문의 의미를 유지하는 단순 윤문이 아니다. 이번 검토에서 외부 연구의 존재 여부나 최속 여부를 조사한 것은 아니다.

### R08 · 높음 · 과거 결정과 최신 구성으로 가는 안내

[Exp 1:627](/home/kimchungsik/projects/research.remakeday.com/experiments/model-selection.md:627)의 “미착수”, [1588행](/home/kimchungsik/projects/research.remakeday.com/experiments/model-selection.md:1588)의 “현재 … 2슬롯”, [1805행](/home/kimchungsik/projects/research.remakeday.com/experiments/model-selection.md:1805)의 “결정 대기”를 갱신하는 완료·변경·채택 기록도 같은 문서에 있다. 날짜가 붙은 과거 기록 자체는 보존할 가치가 있지만, 독자가 이를 현재 상태로 읽기 쉽다.

공개 문서의 최종 명시값은 [2026-09-17 제출 모델 결정:1536](/home/kimchungsik/projects/research.remakeday.com/experiments/model-selection.md:1536)과 [2026-09-18 최종 구성:1766](/home/kimchungsik/projects/research.remakeday.com/experiments/model-selection.md:1766)에서 찾을 수 있다. 요약 첫머리에 해당 절로 연결되는 현재 구성표를 두고, 과거 절에는 후속 결정 링크를 붙이는 편이 좋다.

[Statement:46](/home/kimchungsik/projects/research.remakeday.com/statement.md:46)의 `kanana → gemma4:12b` 교체 기록과 [Testbed:87](/home/kimchungsik/projects/research.remakeday.com/testbed.md:87)의 로컬 `kanana` 표도 적용 날짜·평가 정책을 함께 밝혀야 한다. 두 값을 보고 임의로 하나를 지우거나 실제 실행 설정이 무엇인지 확정하지 않는다. 원문의 날짜별 결정이 바뀌었다는 사실을 독자가 따라갈 수 있게 만드는 작업이다.

### R09 · 보통 · 선택 70%의 분모와 ‘믿음’의 의미

[Statement:35](/home/kimchungsik/projects/research.remakeday.com/statement.md:35)의 “6판 … AI 계열 70%”에는 규칙 선택 **20회**라는 분모가 바로 붙어야 한다. “6판에서 규칙을 선택한 20번 중 AI 계열 14번(70%), 직접 작성 6번(30%)”으로 쓰면 참가자 70%라는 오독을 줄인다. 20번을 독립된 참가자 20명처럼 해석하지 않게 하고, AI 계열은 두 종류의 선택을 합한 값이라는 설명도 연결한다.

[쉬운 요약:34](/home/kimchungsik/projects/research.remakeday.com/plain-summary.md:34)의 “로봇을 믿는가”는 [용어집:5](/home/kimchungsik/projects/research.remakeday.com/_includes/research/glossary.html:5)가 구분한 **선택 행동과 믿는 마음**을 다시 합친다. 실제 측정 질문을 “카드를 받아들이는가”로 맞추거나, 믿음은 연구 동기이고 직접 센 것은 선택이라는 문장을 붙이는 편이 정확하다. 블록탑 비유 전체는 유지한다.

## 문장과 읽는 순서 개선

**R10 · 보통 — 요약에서 원문으로 넘어갈 때 난이도가 급격히 올라간다.** [Exp 1:22](/home/kimchungsik/projects/research.remakeday.com/experiments/model-selection.md:22)의 첫 설명에 역할·모델·평가 약어·지연·메모리가 한꺼번에 등장한다. [홈 원문:63](/home/kimchungsik/projects/research.remakeday.com/index.md:63)의 `operationalize`, `explanation exposure`, `deterministic domain logic`, [Testbed:75](/home/kimchungsik/projects/research.remakeday.com/testbed.md:75)의 역할 표도 분야 지식을 요구한다. 기술 용어 자체는 im-not-ai B-2의 광고성 용어로 분류하지 않았다. 첫 등장 풀이와 역할 설명이 필요한 독해 문제다.

추천 읽기 순서는 **연구 질문 → 역할별 최종 구성·선택 이유·남은 한계 → 평가 절차 → 보조 기능인 임베딩 비교 → 전체 실측 이력**이다. 현재 모델 페이지의 대표 차트는 보조 임베딩 비교라서 Core/NPC를 어떻게 골랐는지는 원문 깊은 곳에서 찾아야 한다. 원문·설정·테스트 기록은 보존하면서 결론으로 가는 안내를 보완할 수 있다.

추가 설명 후보는 다음과 같다. 전문 이름을 없애거나 사실을 새로 만드는 예시는 아니다.

| 위치 | 현재 표현 | 설명을 보완한 예시 |
|---|---|---|
| [reading.yml:23](/home/kimchungsik/projects/research.remakeday.com/_data/reading.yml:23) | 같은 러너와 통과 기준 | 같은 러너(평가 실행 도구)와 통과 기준 |
| [reading.yml:50](/home/kimchungsik/projects/research.remakeday.com/_data/reading.yml:50) | GPU 동주 조건 | 여러 모델을 GPU 메모리에 함께 올리는 조건(동주) |
| [reading.yml:65](/home/kimchungsik/projects/research.remakeday.com/_data/reading.yml:65) | 같은 제출문과 단조 잠금 구간 | 같은 제출문에 더 낮은 점수를 주지 않는 처리인 단조 잠금이 적용된 구간 |
| [Exp 1:266](/home/kimchungsik/projects/research.remakeday.com/experiments/model-selection.md:266) | 셀당 25콜. 9셀 × n. | 모델과 thinking 설정을 묶은 한 조건(셀)마다 25번 호출한다. 9셀을 각각 n회 반복한다. |
| [그림 4B:26](/home/kimchungsik/projects/research.remakeday.com/_includes/research/figures/human-observations.html:26) | 회차별 관찰 점수 | 회차별 게임 총점 |

추가로 [Lab Notes:15](/home/kimchungsik/projects/research.remakeday.com/lab-notes.md:15)의 긴 불릿은 한 항목 안에서 문장을 나누면 된다. 날짜별 목록을 모두 산문으로 바꿀 필요는 없다. [Exp 1:1522](/home/kimchungsik/projects/research.remakeday.com/experiments/model-selection.md:1522)의 “내 몫 예산”처럼 작성 당시 대화 상대를 알아야 하는 표현은 담당 범위를 확인해 적는다. [1640행](/home/kimchungsik/projects/research.remakeday.com/experiments/model-selection.md:1640)의 코드 검토 “B등급”은 모델 성능 평가 등급과 구분하는 안내가 필요하다.

**R11 · 보통 — 고정 사전등록 밖에 한글 설명 보완.** [사전등록:18](/home/kimchungsik/projects/research.remakeday.com/prereg.md:18)의 연구 질문과 [51행](/home/kimchungsik/projects/research.remakeday.com/prereg.md:51)의 보조 측정값은 영어로만 제시된다. 이미 있는 A/B 안내에 RQ3와 이해도 점수 변화 등 보조 측정값의 풀이를 더하면 좋다. 고정 프로토콜 자체를 윤문하지 않고, 앞의 독자 안내에서 원문으로 연결한다. 측정 척도·문턱을 임의로 보충하지 않는다.

[Exp 2:167](/home/kimchungsik/projects/research.remakeday.com/experiments/human-observations.md:167)의 “더 큰 연관성이 관찰되었다”는 문장은 문맥상 서술 예시다. 예시임을 더 뚜렷하게 표시하면 실제 분석 결과처럼 인용되는 일을 줄일 수 있다. 이미 인과를 주장한 문장이라고 오진해서는 안 된다.

**R12 · 낮음 — 확실한 문체 규칙만 국소 적용.** 아래 두 사례는 실제 im-not-ai 규칙에 연결된다. 다른 지적에 억지로 AI 문체 ID를 붙이지 않았다.

| 규칙 | 위치와 원문 | 의미를 유지하는 후보 |
|---|---|---|
| C-11: 연결어미 뒤 쉼표 | [reading.yml:59](/home/kimchungsik/projects/research.remakeday.com/_data/reading.yml:59) “출처를 세었고, 이후 …” | “출처를 세었고 이후 …” |
| I-2: 형식적인 강조 도입 | [Exp 1:915](/home/kimchungsik/projects/research.remakeday.com/experiments/model-selection.md:915) “주목할 점은 방향이다. gemma4 두 모델이 기준선보다 엄격하다.” | “판정 방향을 보면 gemma4 두 모델이 기준선보다 엄격하다.” |

C-8의 부정 대구는 일부 도입부에서 반복을 줄일 후보지만, “인과가 아니라 연관성”, “NOT RUN은 0이라는 뜻이 아니다” 같은 구분은 연구의 의미 자체다. 이를 모두 지우거나 더 강한 단정으로 바꾸면 안 된다. 문장 길이를 일부러 들쭉날쭉하게 만들거나 논문을 구어체 블로그로 바꾸는 것도 권하지 않는다.

## 전 페이지 검토 범위

원문은 9개 파일 **2,612행 전체**를 읽었다. 표·코드·영문 초록도 문맥·정합성 검토에서 확인했으며, 한글 자동 문체 집계에서는 제외했다. 추가로 `_data/reading.yml`, 랜딩 본문, 용어집, 네 종류의 그림 include와 공통 본문 안내를 검토했다.

| 페이지 | 원문 행 수 | 주요 판단 |
|---|---:|---|
| 연구 개요 | 85 | 새 요약은 명확하다. 원문의 기여 설명에 첫 용어 풀이가 필요하다. |
| 왜 게임인가 | 52 | 부재·최상급 주장, 선택 비율 분모, 모델 교체 시점을 우선 정리한다. |
| 실험환경 설계 | 121 | 역할 표·영어 지표 풀이와 구성 기준일을 보완한다. 흐름도는 유지한다. |
| 비유로 읽는 요약 | 59 | 블록탑 비유는 유지하고 수용 행동과 믿음을 구분한다. |
| 한계와 재현 | 74 | 기존 혼재 집계와 분리 원칙의 예외를 정확히 적는다. |
| 사전등록 | 129 | 고정 원문은 보존하고 그 밖에 한글 측정 안내를 붙인다. |
| 날짜별 연구 기록 | 114 | 검수 세트·반복 세트 구분, 조건별 수치, 긴 불릿을 정리한다. |
| AI 모델 선정 | 1,811 | A.1–A.21 전부 검토. 최신 결론 안내와 지표·해석 범위 확인이 가장 시급하다. |
| 사람의 선택 관찰 | 167 | 한계 설명은 적절하다. 단조 잠금 풀이와 서술 예시 표지를 보완한다. |

## 자동 검사 실행과 해석 범위

사용한 도구 커밋은 `9747f036cdc28a1a8aea4dc71fef1f7846eb96f7`이다. `metrics_v2.compute_all_v2(text, genre='report')`를 **원문 9개 + 읽기 안내 9개**에 각각 실행했다. Jekyll 결과에서 한국어가 포함된 제목·문단·목록·캡션을 추출했고, 코드·표·SVG·탐색 메뉴·한국어 없는 블록은 자동 집계에서 제외했다. 읽기 안내에는 공통 용어집도 포함되므로 페이지 간 수치를 더해 고유 문제 수라고 해석하지 않는다.

다음 값은 추출한 **원문의 후보 패턴 수**다. 확정된 문체 위반 건수가 아니며 문서 길이를 보정한 점수도 아니다.

| 페이지 | 자동 집계 입력 문자 수 | 부정 대구 후보 | 연결어미 뒤 쉼표 후보 |
|---|---:|---:|---:|
| 연구 개요 | 602 | 0 | 1 |
| 왜 게임인가 | 1,114 | 2 | 2 |
| 실험환경 설계 | 986 | 1 | 1 |
| 비유로 읽는 요약 | 974 | 1 | 2 |
| 한계와 재현 | 908 | 1 | 0 |
| 사전등록 | 753 | 2 | 0 |
| 날짜별 연구 기록 | 3,931 | 2 | 3 |
| AI 모델 선정 | 43,475 | 27 | 61 |
| 사람의 선택 관찰 | 3,239 | 2 | 4 |

두 층을 합쳐 검사한 입력은 68,424자다. 이중 피동과 이중 조사 후보는 이 입력에서 0건이었다. 그러나 코드가 “게임을 만들었다”도 have/make 직역 후보로 잡는 등 문맥상 오탐이 있다. 부정 대구 개수 역시 원래 도구에서 절대치만으로 판정하지 말라고 명시한다.

v2 기준 데이터에는 `report` 항목이 없어 `essay`로 대체되고, 14개 지표 셀에는 임시 기준 표시가 있다. 따라서 자동 위험 점수·z-score·AI 작성 확률·윤문 등급을 이 연구의 품질 판정에 쓰지 않았다. 이 검토는 윤문 전후 비교가 아니므로 변경률이나 탐지 감소율도 제시하지 않는다.

실행 입력의 해시·선택한 원시 집계·기준 버전은 [검사 기록](2026-09-18-humanize-korean-metrics.json)에 있다. 세부 근거와 보존 판단은 [개요·실험환경 검토](2026-09-18-humanize-overview-detail.md), [모델 선정 검토](2026-09-18-humanize-model-detail.md), [행동·사전등록·한계 검토](2026-09-18-humanize-evidence-detail.md)에 남겼다.

## 유지할 것과 반영 순서

작은 표본, 기구 버전 혼재, 측정하지 않은 항목, 인과 해석의 한계는 과도한 완곡 표현이 아니다. 차트의 22문장/30문장 구분, 기존 집계/단일 사례 구분, p50·ms 설명, 실제 게임 화면과 Blender 개념 모형의 구분도 유지한다. 모델명·표준 약어·직접 인용·코드·값·날짜를 자연스러운 표현이라는 이유로 바꾸지 않는다.

반영 순서는 **지표 출처·집계 범위 확인 → 주장과 현재 상태 정리 → 본문 진입 난이도 개선 → 국소 윤문**을 권한다. Exp 1은 앱 저장소의 `docs/model_evaluation.md`가 정본이므로, 확인한 정본과 ref를 수정한 뒤 `scripts/snapshot_model_eval.py`로 공개 스냅샷과 그림 데이터를 갱신해야 한다. 사전등록 해설은 고정 원문 밖에서 보완한다.

이번 작업은 공개 소스 내부 대조와 문장·독해 검토다. 비공개 실행 결과·참가자 DB·현재 앱 설정·외부 연구 문헌을 재검증하지 않았다. 특히 R01의 정정 숫자와 실제 런타임 모델 구성은 확정하지 않았다. 검토 보고서만 추가했으며 사이트 원문·데이터·UI 변경이나 커밋·푸시는 하지 않았다.
