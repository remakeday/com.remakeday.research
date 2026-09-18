# 모델 의사결정 전체 검토 — A.9–A.21·변경 이력

대상은 공개 스냅샷 `experiments/model-selection.md:985–1811`의 **226개 블록 전부**다. 입력 원장의 `F09-U301`부터 `F09-U526`까지 표·목록·제목·구획선·마지막 원칙을 하나씩 확인했다. 표본을 뽑아 검토하지 않았으며, 공개 원문과 앱 정본을 수정하지 않았다. 이 파일과 같은 이름의 JSON 발견 목록, 블록별 판정 JSON만 작성했다.

심사위원과 AI·통계 비전공 개발자가 읽는 연구 기록이라는 조건으로 검토했다. 사용자가 지정한 `im-not-ai`의 한국어 skill과 quick-rules를 적용하되 사실·수치·모델명·코드·실제 발화 인용·필요한 불확실성을 보존했다. AI 작성 여부나 AI 작성률은 판정하지 않는다. 기술 용어·학술 표·기능적인 소제목을 AI 문체로 간주하지 않았다.

**68건**: 높음 22건, 중간 44건, 낮음 2건. 블록별 판정은 keep 94, copy_edit 3, clarify 69, verify 51, restructure 9다. 여러 블록에서 같은 문제가 반복되면 하나의 발견에 모았고, 한 블록에 독립적인 문제가 있으면 여러 발견을 연결했다. 따라서 발견 수와 수정 대상 블록 수는 다르다.

문체 규칙으로 직접 분류한 것은 **MD-68 / C-11**이다. 나머지는 독해·정보 구조·집계 정의·주장 범위의 별도 검토다. 특히 `verify`와 주장 범위를 좁히는 제안은 의미 불변 윤문이 아니라 정본 저자가 근거를 확인한 뒤 적용할 내용 정정이다. `before`는 지정 블록 안에서 정확히 일치하는 짧은 인용으로 검사했다.

확인 수준: `public_document` 18건은 공개 본문 내부 대조, `raw_checked` 7건은 연결된 원시 파일의 제한된 집계 확인을 포함한다. `needs_source` 43건은 실제 오류로 확정한 것이 아니라 필요한 근거·분모·조건을 명시한 확인 요청이다. 원시 확인 범위와 한계는 [raw-evidence.json](raw-evidence.json)의 RAW-01~06에 있으며, 비공개 발화나 운영 비밀은 이 검토서에 옮기지 않았다. 원시 일부 확인을 전체 실험 재검증으로 해석하지 않는다.

## 먼저 확인할 정정

- **MD-29**: 원시 A/B 요약에서 페르소나·관련성의 무승부가 각각 1건 확인됐다. 공개 표에는 무승부 열이 없다.
- **MD-34·35**: 연결된 원시 집계는 advisor p50 2,918ms/evaluator p50 2,179ms이고, 확인한 n=3 파일은 Sonnet만 포함한다. 다른 실행을 의도했는지는 추가 확인이 필요하다.
- **MD-08·13**: 공개 수치상 20~28초/5초는 4~5.6배이며 OFF 표는 5셀이다. 10배·OFF 10셀의 근거를 확인한다.
- **MD-54·55·60·61**: top-3 정답 적중은 추천 목록의 동일성이 아니다. 차원별 비교와 반복은 22문장/30문장을 분리하고 실제 측정한 범위로 제한한다.
- **MD-39·44·49**: 재생성 수는 gemma4 실행별로 구분하고 누설 미측정과 전체 게이트 통과를 분리한다. 과거의 2슬롯·결정 대기와 최종 3슬롯 안내를 연결한다.

## 전체 발견 목록

### MD-01 · 중간 · 교대 상주 실험의 측정 범위와 용어

분류: `readability` · 확인: `public_document` · 반영 위치: `either` · im-not-ai: 해당 없음

대상 블록: F09-U302, F09-U304, F09-U306, F09-U310, F09-U316, F09-U367, F09-U370, F09-U431, F09-U437, F09-U507, F09-U517

**문제.** 상주·축출·오프로드, 셀·콜·스냅샷, 스모크·Core/NPC/플레이어가 한꺼번에 등장한다. 표의 무축출은 매 콜 직후 관찰한 표본 구간에 한정되는데 독자는 동시 실행의 장시간 안정성으로 읽기 쉽다.

**근거.** `experiments/model-selection.md:987` · `experiments/model-selection.md:992` · `experiments/model-selection.md:999` · `experiments/model-selection.md:1007` · `experiments/model-selection.md:1024` · `experiments/model-selection.md:1165` · `experiments/model-selection.md:1173` · `experiments/model-selection.md:1342` · `experiments/model-selection.md:1357` · `experiments/model-selection.md:1715` · `experiments/model-selection.md:1757`

**원문.**

> **두 후보 모두 교대 구간에서 축출 없이 공존한다.**

**수정 제안 또는 필요한 근거.** 해설층 첫 용례에 “상주는 모델을 GPU 메모리에 유지하는 상태, 축출은 다른 모델을 올리려고 내리는 일이다. 이 검사는 NPC와 Core를 번갈아 호출한 뒤 총 6개 스냅샷을 확인했다”를 둔다. Core/NPC는 서비스 역할, 플레이어는 테스트 입력 생성 역할, judge는 평가 역할로 구분한다. 결과 문장은 “교대 구간의 6스냅샷에서 두 모델의 동시 상주를 확인했다”로 범위를 명시한다.

**보존할 내용.** 모델명·think 설정·교대 3라운드·6스냅샷·메모리값·측정의 단시간 한계

### MD-02 · 중간 · 초기 축출 원인과 운영 영향의 추론

분류: `claim` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U308

**문제.** NPC 초기 축출 1건과 GPU 감소는 관측이지만 원인을 스케줄러 메모리 추정으로 돌리고 운영 영향을 1회·약 1초로 한정하는 것은 추가 추론이다. 재현 가능성 표현도 1건의 범위를 넘는다.

**근거.** `experiments/model-selection.md:1003`

**원문.**

> 운영 영향은 Core 교체 시점의 NPC 1회 재로드(~1초)로 제한적이지만

**수정 제안 또는 필요한 근거.** “이번 실행에서는 Core 초기 로드 뒤 NPC가 1회 재로드됐고 약 1초가 걸렸다. 스케줄러의 메모리 추정이 원인일 가능성은 있으나 확인하지 않았다. 다른 로드 순서·반복 실행에서의 영향은 미측정이다”로 관측과 추론을 나누거나, 로드 순서별 반복·스케줄러 로그 근거를 추가한다.

**보존할 내용.** 초기 축출 1건·5,117→4,419 MiB·1,007ms·교대 게이트 통과

### MD-03 · 중간 · 논리 호출·Core 콜·시도 수의 분모

분류: `data` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U318, F09-U319, F09-U323

**문제.** Core 콜 14/15, 전체 서버 콜 17, attempts 17/19의 집계 단위가 달라 표를 가로로 합산할 수 없다. 역할별 목록의 non-NPC 합은 14여서 e4b Core 15가 재시도를 포함하는지 설명해야 한다.

**근거.** `experiments/model-selection.md:1031` · `experiments/model-selection.md:1036` · `experiments/model-selection.md:1044`

**원문.**

> | **`gemma4:e4b-N`** | O | 0 | **0 / 17** | 15 | 17 (19) | 0자 | 35.6s | **통과** |

**수정 제안 또는 필요한 근거.** 각 열을 “논리 호출 수 / 모델 실제 시도 수 / debug 누계” 등 실제 집계 정의로 명명하고, 15=14+advisor 재시도 1인지 러너에서 확인해 주석을 단다. 폴백 0/17과 재시도 2를 같은 분모로 섞지 않는다.

**보존할 내용.** 기존 14·15·17·19·역할별 콜 수·폴백과 재생성 구분

### MD-04 · 중간 · 다른 문서의 절과 축약 출처의 참조

분류: `structure` · 확인: `public_document` · 반영 위치: `either` · im-not-ai: 해당 없음

대상 블록: F09-U314, F09-U348, F09-U353, F09-U358, F09-U360, F09-U362, F09-U365, F09-U373, F09-U381, F09-U387, F09-U395, F09-U399, F09-U402, F09-U420, F09-U442, F09-U492, F09-U359

**문제.** “방식(a)”, “부록 E6 §6”, “§3.1/§4/§7.3/§8/§11”, “같은 디렉토리”, 생략된 파일명이 서로 다른 문서의 절을 가리킨다. 특히 A.21의 “§8”은 본문 E6 §8과 A.21 내부 8절을 혼동시킨다.

**근거.** `experiments/model-selection.md:1020` · `experiments/model-selection.md:1106` · `experiments/model-selection.md:1128` · `experiments/model-selection.md:1144` · `experiments/model-selection.md:1148` · `experiments/model-selection.md:1152` · `experiments/model-selection.md:1161` · `experiments/model-selection.md:1179` · `experiments/model-selection.md:1200` · `experiments/model-selection.md:1216` · `experiments/model-selection.md:1238` · `experiments/model-selection.md:1246` · `experiments/model-selection.md:1255` · `experiments/model-selection.md:1306` · `experiments/model-selection.md:1374` · `experiments/model-selection.md:1638` · `experiments/model-selection.md:1146`

**원문.**

> §7.3 문장 3형

**수정 제안 또는 필요한 근거.** 외부 설계의 절은 “E6 설계 §7.3”, 이 페이지 부록 안의 절은 “A.21.8”처럼 문서명과 부록 번호를 함께 쓴다. 원문 파일은 최초 출처 디렉토리로 이동하는 명시적 링크와 전체 파일명 목록을 제공한다. “방식(a)”은 뒤에 이미 있는 HTTP 실서버 설명만으로 이해되게 정리한다.

**보존할 내용.** 기존 문서·파일명·절 번호의 실제 대상과 역사 기록

### MD-05 · 중간 · 첫 실행 두 판의 완주 근거

분류: `claim` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U326

**문제.** 게임 두 판 정상 완주를 확인했다고 쓰지만 괄호 안 DB 근거는 12b 폴백 0/17만 제시한다. 정상 완주·폴백 0·수집기 실패는 다른 관측이다.

**근거.** `experiments/model-selection.md:1050`

**원문.**

> **게임 자체는 두 판 모두 정상 완주였다**(DB 이벤트 로그로 확인: 12b 판 폴백 0/17)

**수정 제안 또는 필요한 근거.** 두 시도의 종료 상태와 모델별 폴백 집계를 출처 필드로 분리해 제시한다. e4b 첫 실행의 완주 근거가 없으면 확인한 범위만 쓴다. 잘못된 gate_pass=false와 재실행 정본의 관계는 유지한다.

**보존할 내용.** 실제 게임과 계측기 예외의 구별·정본 파일명·삭제 metrics 2줄 이력

### MD-06 · 중간 · 단시간 프로브로 추정한 티어와 한도

분류: `claim` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U332, F09-U334, F09-U336

**문제.** 55.4초 연속 요청의 429 부재만으로 티어·공칭 RPM 범위를 추정한다. 후속 사용자 확인은 유료 여부를 뒷받침하지만 정확한 Tier 1·150~300 RPM과 11번째 콜 제한은 이 관측만으로 정해지지 않는다.

**근거.** `experiments/model-selection.md:1066` · `experiments/model-selection.md:1070` · `experiments/model-selection.md:1074`

**원문.**

> **이 키는 결제 계정이 연결된 유료 티어(Tier 1, 공칭 150~300 RPM)로 판단된다.**

**수정 제안 또는 필요한 근거.** 40콜/55.4초·429 0건은 실측으로 남기고, 유료 여부는 A.11의 사용자 확인으로 분리한다. 티어·RPM은 당시 모델/프로젝트별 콘솔 기록 또는 당시 공식 한도 문서가 있어야 적는다. 문구 예: “이 실행에서는 40콜 동안 429가 발생하지 않았다. 이후 사용자가 유료 키임을 확인했다.”

**보존할 내용.** 측정값·사용자 확인·무료 기준 10 RPM을 유지한 결정

### MD-07 · 중간 · 30 RPM 운영 안전성과 합성 지연

분류: `claim` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U337, F09-U338

**문제.** 30 RPM을 “안전한 운영값” 후보로 둔 근거가 1분 미만 단독 실측과 추정 티어다. 표는 max(raw,간격)의 합성 계산이며 장시간·동시 요청 운영 보장을 측정한 것이 아니다.

**근거.** `experiments/model-selection.md:1076` · `experiments/model-selection.md:1082`

**원문.**

> **30 RPM**이 안전한 운영값 후보다.

**수정 제안 또는 필요한 근거.** “단독 프로브와 게이트 산식만 보면 30 RPM을 검토할 수 있으나 운영 안정성은 미측정이다”로 좁힌다. 게이트 표에는 합성 계산·순차 10콜·첫 요청 대기 처리·공유 페이싱의 가정을 적는다. 최종 10 RPM 유지 결정은 그대로 둔다.

**보존할 내용.** ≥12·≥20·30 RPM·표의 raw/eff 계산·당시의 가정적 시나리오

### MD-08 · 높음 · 20~28초를 5초의 10배로 쓴 계산

분류: `data` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U344, F09-U345

**문제.** 공개된 초소형 호출 20~28초와 C11=5초의 비는 4~5.6배다. “raw 지연만으로 10배 이상”은 제시된 수치와 맞지 않는다.

**근거.** `experiments/model-selection.md:1096` · `experiments/model-selection.md:1098`

**원문.**

> raw 지연만으로 C11(5초)을 10배 이상 초과한다

**수정 제안 또는 필요한 근거.** 원시 6콜의 raw·timeout·wall time를 확인한다. 50초 이상 raw 근거가 없다면 정정 기록을 남기고 “공개된 20~28초 호출은 C11(5초)의 4~5.6배였다”로 고친다. 초소형 프로브 지연을 실제 advisor p95로 부르지 않는다.

**보존할 내용.** 20~28초·C11 5초·503·30초 타임아웃·6콜/131초·무료 운영 후보 제외 이력

### MD-09 · 낮음 · 실험 날짜와 요일의 불일치

분류: `data` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U345

**문제.** A.11 날짜 2026-09-14는 월요일인데 추록은 일요일 13시대라고 한다. 날짜 또는 측정 요일 중 하나가 맞지 않는다.

**근거.** `experiments/model-selection.md:1098` · `experiments/model-selection.md:1062`

**원문.**

> 시점 한정 측정(일요일 13시대

**수정 제안 또는 필요한 근거.** 실험 파일 타임스탬프의 시간대와 원문 작성 날짜를 확인한 뒤 요일 또는 날짜를 정정한다. 어느 쪽도 임의로 선택하지 않는다.

**보존할 내용.** 원문 실험 시점·시점 한정이라는 제한

### MD-10 · 중간 · 생성 모델 무료 한도의 역할별 범위

분류: `claim` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U344, F09-U345, F09-U454, F09-U471

**문제.** 짧은 무료 키 실험에서 관찰한 지연·daily cap을 “무료 기준 온라인 대안 없음” 또는 “어떤 역할로도 운영 후보가 아니다”로 확장한다. 생성 모델의 한도는 A.21 임베딩 서비스와 같은 제약이라고 단정할 수 없다.

**근거.** `experiments/model-selection.md:1096` · `experiments/model-selection.md:1098` · `experiments/model-selection.md:1448` · `experiments/model-selection.md:1529`

**원문.**

> 무료 키는 어떤 역할로도 운영 후보가 아니다(하루 20요청).

**수정 제안 또는 필요한 근거.** “이번에 시험한 프로젝트·키의 gemini-3-flash-preview NPC 구성은 해당 시점 하루 20요청 상한으로 제외했다”처럼 모델·역할·시점을 명시한다. A.11의 Core 결론과 A.19의 NPC 결론을 구분하고, A.21 Gemini 임베딩 채택은 별도 모델·한도라고 연결한다.

**보존할 내용.** 무료 키 후보 제외 당시 결정·20요청·14/80 성공·66실패·임베딩 최종 채택

### MD-11 · 중간 · 혼합 양자화가 보수적이라는 가정

분류: `claim` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U350

**문제.** 0.8b만 Q8_0인 혼재를 “정밀도가 높으므로 하강 결론에 보수적”이라고 정리한다. 높은 양자화 정밀도가 해당 행동 지표를 한 방향으로 바꾼다는 자료는 제시하지 않는다.

**근거.** `experiments/model-selection.md:1111`

**원문.**

> 정밀도가 더 높은 쪽 — 하강 결론에 보수적

**수정 제안 또는 필요한 근거.** Q4 태그 부재와 Q8_0 사용은 그대로 보고한다. “양자화가 달라 크기 효과만 분리할 수 없다”를 추가하고 보수적 방향의 단정은 별도 동일모델 Q4/Q8 비교 근거가 있을 때만 남긴다.

**보존할 내용.** 0.8b Q8_0·9b/4b/2b Q4_K_M·재pull 이력·관측 수치

### MD-12 · 높음 · 5개 관측 항목과 실제 게이트의 구분

분류: `data` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U352, F09-U353, F09-U355, F09-U358, F09-U360, F09-U392, F09-U405, F09-U425, F09-U457, F09-U460, F09-U461

**문제.** E6 표의 items는 5항목 통과 개수인데 항목3은 판정 제외라고 한다. 판정 축 4개·5/5 절대 축·후기 4/5 게이트가 함께 쓰여 같은 숫자가 같은 기준처럼 보인다. 각 rate·D3·누설·스키마의 분모도 표에서 빠졌다.

**근거.** `experiments/model-selection.md:1120` · `experiments/model-selection.md:1128` · `experiments/model-selection.md:1132` · `experiments/model-selection.md:1144` · `experiments/model-selection.md:1148` · `experiments/model-selection.md:1226` · `experiments/model-selection.md:1261` · `experiments/model-selection.md:1318` · `experiments/model-selection.md:1458` · `experiments/model-selection.md:1473` · `experiments/model-selection.md:1479`

**원문.**

> 항목 3(3턴 망각)은 판정 축이 아니라 관측치다

**수정 제안 또는 필요한 근거.** 표 주석에 rate=해당 항목 통과 응답/n, items=5개 관측 항목 중 기준을 넘은 수, 실제 선택 게이트의 항목 목록을 분리한다. D3 전원일치의 응답 수, 누설 0/몇 회, 스키마 성공/시도 수도 적는다. A.12의 5항목 전부≥0.7과 A.19의 4/5 기준이 언제·왜 바뀌었는지 문서화한다.

**보존할 내용.** 모든 rate·items 값·0.7 임계값·망각 항목의 당시 지위·변경 시점

### MD-13 · 높음 · OFF 10셀과 표의 5셀

분류: `data` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U357

**문제.** A.12 정책 OFF 표는 모델 5개인데 해석은 OFF 10셀이라고 한다. ON/OFF 전체 10셀과 OFF 5셀을 혼동한 것으로 보인다.

**근거.** `experiments/model-selection.md:1142`

**원문.**

> OFF 10셀 중 collapse=none이 없다.

**수정 제안 또는 필요한 근거.** 러너의 ON/OFF 조건 수를 확인하고 OFF가 표의 5개라면 “OFF 5셀 중 collapse=none은 없었다”로 정정한다. 10은 ON/OFF 전체 조건 수로만 남긴다.

**보존할 내용.** 5모델·ON/OFF 전체 10셀·각 모델의 collapse 분류

### MD-14 · 높음 · 연령 능력·모델 크기 하한으로의 일반화

분류: `claim` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U357, F09-U358, F09-U524

**문제.** “자연히 7세인 크기 없음”, “프롬프트가 살릴 수 있는 하한이 2B와 4B 사이”는 제한된 모델·문항·프롬프트 결과를 일반적인 연령 능력과 크기 인과로 확장한다. 실제 아동 검증이 아니라 운영 정의를 검사한 실험이다.

**근거.** `experiments/model-selection.md:1142` · `experiments/model-selection.md:1144` · `experiments/model-selection.md:1781`

**원문.**

> 프롬프트가 살릴 수 있는 하한이 2B와 4B 사이에 있다.

**수정 제안 또는 필요한 근거.** “이번 qwen3.5 후보·정책·문항에서 2B는 기준에 미달했고 4B는 통과했다. 두 크기 사이는 측정하지 않았다”로 범위를 좁힌다. “7세/3세/어른화”는 실험의 행동 분류 이름임을 명시한다. 하한·연령 일반화는 별도 실증이 필요하다.

**보존할 내용.** 모델 크기·패밀리·ON/OFF 관측·정책과 하네스 조건·사용자 정의의 역사

### MD-15 · 중간 · 약한 기준선과 비열등이라는 표현

분류: `readability` · 확인: `public_document` · 반영 위치: `either` · im-not-ai: 해당 없음

대상 블록: F09-U360, F09-U407

**문제.** “비열등 참”, “형해화”, “절대 축”은 기준선이 약해서 형식상 통과해도 실제 채택하지 않았다는 핵심을 숨긴다. 통계적 비열등 검정을 한 것처럼 읽힐 수도 있다.

**근거.** `experiments/model-selection.md:1148` · `experiments/model-selection.md:1268`

**원문.**

> §4 기준이 사실상 형해화됐다

**수정 제안 또는 필요한 근거.** “기준선이 실제 판정 항목 4개 중 1개만 통과했으므로, 그 항목을 유지하는 조건만으로는 후보의 정책 수행 능력을 충분히 구별하지 못했다”로 풀고 실제 판정 기준 링크를 붙인다. 비열등은 문서의 운영 규칙이며 통계 검정 결과가 아니라는 설명을 한 번 둔다.

**보존할 내용.** 기준선의 낮은 통과 수·형식 통과/최종 비채택 구별·p95/VRAM 수치

### MD-16 · 중간 · 정책 검수를 실제 아동 문체 검증으로 해석

분류: `claim` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U362, F09-U394

**문제.** 전사문 전수 검수와 judge 만장일치는 정책 분류를 확인하는 근거다. “실제 7세 문체”, “판정 정당”, “실제 현상”은 실제 아동 언어 검증이나 judge 타당성 검증으로 읽힐 수 있다.

**근거.** `experiments/model-selection.md:1152` · `experiments/model-selection.md:1236`

**원문.**

> PASS 응답은 실제 7세 문체

**수정 제안 또는 필요한 근거.** “PASS 응답은 이 실험의 7세 정책 기준에 맞는지 전수 검수했다”로 범위를 명시한다. 검수 주체·기준·응답 수를 적고 실제 발화 인용은 그대로 둔다. A.15의 재판정 결과는 v2에서도 동일 분류였다는 범위로 쓴다.

**보존할 내용.** 전수 검수·v2 판정 결과·직접 인용·다수결 및 만장일치 수치

### MD-17 · 중간 · 동일 응답의 문자 혼입 재집계

분류: `data` · 확인: `public_document` · 반영 위치: `either` · im-not-ai: 해당 없음

대상 블록: F09-U362, F09-U379, F09-U381, F09-U410, F09-U429

**문제.** A.12와 A.14는 같은 transcripts를 재사용한다. 한자 혼입 2/25를 “일치하는 재확인”이라고 하면 독립 재현으로 오해할 수 있고 한자/비한글/외국 문자 지표의 검사 범위도 흔들린다.

**근거.** `experiments/model-selection.md:1152` · `experiments/model-selection.md:1196` · `experiments/model-selection.md:1200` · `experiments/model-selection.md:1279` · `experiments/model-selection.md:1337`

**원문.**

> 한자 혼입 8%는 A.12 관측(2/25)과 일치하는 재확인이다.

**수정 제안 또는 필요한 근거.** “A.12와 같은 25개 응답에서 한자 혼입 2건을 다시 집계했다”로 적는다. 검사 대상이 한자·영문·모든 비한글 중 무엇인지, 분모가 발화 25개인지 문자 수인지 정의한다.

**보존할 내용.** 동일 원문 재사용·2/25=8%·영문만 검사하던 하네스·원 인용

### MD-18 · 중간 · 순서 교환 불일치와 위치 편향

분류: `claim` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U376, F09-U384, F09-U417, F09-U428

**문제.** 순서를 바꿔 판정이 달라지면 전부 위치 편향으로 처리한다. 순서 변화 외에도 확률적 judge 변동이 있을 수 있어 원인까지 식별했다고 보기 어렵다.

**근거.** `experiments/model-selection.md:1185` · `experiments/model-selection.md:1206` · `experiments/model-selection.md:1297` · `experiments/model-selection.md:1330`

**원문.**

> 불일치는 위치 편향으로 무효 처리

**수정 제안 또는 필요한 근거.** “순서를 바꾼 두 다수결 판정이 다른 쌍은 비교 집계에서 제외했다. 위치 영향과 판정 변동을 분리하지는 않았다”로 쓴다. 표의 무효 열도 “순서 교환 불일치”로 정의하고 제외 규칙은 유지한다.

**보존할 내용.** 스왑 2회·각 3표·무효 처리 정책·모든 승수와 무효수

### MD-19 · 중간 · A/B 승수의 유효 분모와 우세 범위

분류: `claim` · 확인: `public_document` · 반영 위치: `either` · im-not-ai: 해당 없음

대상 블록: F09-U378, F09-U381, F09-U382, F09-U409, F09-U410, F09-U414, F09-U433

**문제.** 승수로 우세한 방향은 읽을 수 있지만 표본 25·단일 judge·항목별 무효 수가 다른 상황에서 큰 차이·비등·강점 등 강한 요약을 쓴다. 유효 쌍 분모가 요약과 함께 보이면 범위가 분명해진다.

**근거.** `experiments/model-selection.md:1189` · `experiments/model-selection.md:1200` · `experiments/model-selection.md:1202` · `experiments/model-selection.md:1272` · `experiments/model-selection.md:1279` · `experiments/model-selection.md:1287` · `experiments/model-selection.md:1346`

**원문.**

> **발화 품질 3개 항목에서 exaone이 큰 차이로 우세하다**

**수정 제안 또는 필요한 근거.** “유효 판정에서 exaone 승수가 더 많았다(자연스러움 18:3, 관련성 18:3, 페르소나 14:2)”로 표본 범위를 붙인다. 항목별 유효 n·무효·무승부를 함께 제시하며 통계적 유의성·동등성은 주장하지 않는다는 기존 제한을 유지한다.

**보존할 내용.** 원 승수·측정항목·E6 정책과 A/B 품질의 별도 지위

### MD-20 · 중간 · 응답 길이와 말투 평가의 인과

분류: `claim` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U381, F09-U410

**문제.** 단답/장문의 평균 길이와 7세 말투 점수의 연관을 원인처럼 쓴다. 길이를 통제한 실험이나 judge 편향 분리 측정은 없다.

**근거.** `experiments/model-selection.md:1200` · `experiments/model-selection.md:1279`

**원문.**

> 장광설(83.5자) 탓에 7세 말투 최하이고

**수정 제안 또는 필요한 근거.** “2.4b는 평균 83.5자로 가장 길었고, 7세 말투 승수도 낮았다. 길이의 영향을 분리하지는 않았다”로 쓴다. 4b 9.1자의 원인 추정 역시 가능성으로 남기고 새 확신을 추가하지 않는다.

**보존할 내용.** 83.5·35.0·9.1자·승수·편향 가능성·원문 한계

### MD-21 · 중간 · collapse 분류와 어른화 신호

분류: `data` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U382, F09-U414

**문제.** exaone 정책 ON의 collapse 값은 toddler인데 결정 요약은 “어른화”만 표시한다. 실제로 항목1 사실·항목2/5가 모두 미달해 둘은 충돌 없이 설명할 수 있으나 분류값과 별도 신호를 구분해야 한다.

**근거.** `experiments/model-selection.md:1202` · `experiments/model-selection.md:1287` · `experiments/model-selection.md:1122` · `experiments/model-selection.md:1266`

**원문.**

> `exaone`은 7세 정책 1/5(어른화 신호)

**수정 제안 또는 필요한 근거.** 표에 “collapse=toddler(사실 항목 우선 판정); 어른화 관련 항목도 미달”처럼 공식 분류와 보조 관찰을 구분한다. exaone2.4b를 처음 양방향 프로필이라고 부른 A.16과도 판정 규칙·대상을 대조한다.

**보존할 내용.** 기존 collapse 값·1/5·어른화 항목 실패·분류 우선순위

### MD-22 · 중간 · v2 개정 기준과 왜=몰라 표머리글

분류: `readability` · 확인: `public_document` · 반영 위치: `either` · im-not-ai: 해당 없음

대상 블록: F09-U389, F09-U390, F09-U392, F09-U394, F09-U395, F09-U396, F09-U399, F09-U405, F09-U425, F09-U457, F09-U460

**문제.** v2는 이유 지어내기를 일부 허용하지만 표 머리글은 계속 “왜=몰라”다. “관대해진/완화”는 0.8b가 더 엄격하게 재분류된 사실과 함께 읽기 어렵다.

**근거.** `experiments/model-selection.md:1220` · `experiments/model-selection.md:1222` · `experiments/model-selection.md:1226` · `experiments/model-selection.md:1236` · `experiments/model-selection.md:1238` · `experiments/model-selection.md:1240` · `experiments/model-selection.md:1246` · `experiments/model-selection.md:1261` · `experiments/model-selection.md:1318` · `experiments/model-selection.md:1458` · `experiments/model-selection.md:1473`

**원문.**

> 왜=몰라

**수정 제안 또는 필요한 근거.** 원 식별자는 보존하되 “항목2(v2: 아이다운 이유·모름·딴 이야기 허용)” 설명을 붙인다. “관대해진 기준” 대신 “개정한 v2 기준”으로 지칭해 일부는 상승하고 일부는 하락한 재분류를 정확히 나타낸다. 실제 사용자 인용은 고치지 않는다.

**보존할 내용.** 항목 번호·v1/v2 구분·모든 재판정 수치·사용자 발화

### MD-23 · 높음 · v1 OFF와 v2 ON의 비교 범위

분류: `data` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U399, F09-U404, F09-U405, F09-U407

**문제.** A.15는 기존 모델 ON 항목2만 v2로 재판정했고 OFF는 v1이라고 명시한다. A.16은 ON/OFF 전체가 v2인데 “기존 셀과 비교 가능”을 포괄적으로 쓴다.

**근거.** `experiments/model-selection.md:1246` · `experiments/model-selection.md:1259` · `experiments/model-selection.md:1261` · `experiments/model-selection.md:1268`

**원문.**

> A.15 재판정과 동일 기준이라 기존 셀과 비교 가능

**수정 제안 또는 필요한 근거.** “정책 ON의 항목2는 A.15 v2 재판정과 비교 가능하다. 기존 OFF는 v1이므로 OFF의 직접 비교는 제한한다”로 범위를 명시한다. 정책 ON/OFF 차이를 모델 간 비교하려면 기준을 통일한 재판정이 필요하다.

**보존할 내용.** ON/OFF 원자료·응답 재생성 여부·v2 적용 범위·n=5

### MD-24 · 높음 · exaone 두 크기에서 패밀리로의 일반화

분류: `claim` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U406, F09-U407, F09-U415, F09-U524

**문제.** 두 exaone 크기의 제한된 조건에서 나온 실패를 “패밀리 성질로 확인”이라고 일반화한다. A.16의 “처음 나온 양방향 프로필”도 A.12 exaone7.8b의 사실0.60·왜0.40·문자0.40과 대조해야 한다.

**근거.** `experiments/model-selection.md:1266` · `experiments/model-selection.md:1268` · `experiments/model-selection.md:1293` · `experiments/model-selection.md:1781`

**원문.**

> 어른화는 크기 하강으로 사라지지 않았다 — exaone 패밀리 성질로 확인.

**수정 제안 또는 필요한 근거.** “이번 조건에서 시험한 exaone 7.8B와 2.4B 모두 어른화 관련 항목에 미달했다”로 관측 범위를 제한한다. “처음”을 남기려면 양방향 정의와 기존7.8b 제외 이유를 제시한다. 변경 이력의 동일 일반화도 함께 정정하되 당시 해석이었다는 기록을 남긴다.

**보존할 내용.** 두 크기의 수치·측정 조건·후보 부적격 결정·역사 이력

### MD-25 · 중간 · 통과 항목 수 차이 0과 효과 부재

분류: `claim` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U355, F09-U358, F09-U407

**문제.** ON−OFF의 items 개수 차이0을 정책 “순효과가 없다”로 해석한다. 같은 통과 항목 수라도 항목별 rate는 변하며 작고 반복된 표본만으로 효과 부재를 확인할 수 없다.

**근거.** `experiments/model-selection.md:1132` · `experiments/model-selection.md:1144` · `experiments/model-selection.md:1268`

**원문.**

> 정책 프롬프트 순효과가 없다.

**수정 제안 또는 필요한 근거.** “통과 항목 수는 ON/OFF 모두1로 같았다. 항목별 rate 차이는 표와 같으며 정책 효과 부재를 입증한 것은 아니다”로 제한한다. 4b의 +2와 2b의0도 항목 수 차이임을 머리글에 명시한다.

**보존할 내용.** ON−OFF 집계값·개별 rate·비열등 형식 판정·n=5

### MD-26 · 중간 · A.16 A/B 무승부·무효의 누락

분류: `data` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U409

**문제.** A.16 A/B 표는 각25쌍이라고 하지만 승수만 남겨 합계가25가 아닌 행들의 무승부·무효 수를 볼 수 없다. 유효율이 다르면 15:4와10:4의 의미도 달라진다.

**근거.** `experiments/model-selection.md:1272`

**원문.**

> | 한국어 자연스러움 | **15 : 4** | 9 : 10 (비등) |

**수정 제안 또는 필요한 근거.** 각 비교를 A.14와 같은 승/패/무승부/무효 형식으로 펼친다. 원자료에서 누락된 범주를 확인해 채우며 25에서 단순 차감해 모두 무효로 간주하지 않는다.

**보존할 내용.** 모든 승수·25쌍·순서 교환 규칙

### MD-27 · 높음 · 라이선스 판단의 버전·조건·출처

분류: `claim` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U421, F09-U422, F09-U423, F09-U433, F09-U524

**문제.** 라이선스 기록이 “연구 전용 확정”, “상업 가능”, “문제없음”으로 압축되어 어떤 버전의 어떤 조항과 배포 조건을 확인했는지 본문에서 검증하기 어렵다. 이번 읽기 검토는 현재 법적 허용 여부를 재판정하지 않는다.

**근거.** `experiments/model-selection.md:1308` · `experiments/model-selection.md:1310` · `experiments/model-selection.md:1312` · `experiments/model-selection.md:1346` · `experiments/model-selection.md:1781`

**원문.**

> Core `gemma4:12b`·`gemma4:e4b`는 **Apache 2.0(Gemma 4부터)** — 문제없음.

**수정 제안 또는 필요한 근거.** 2026-09-14 조사 당시의 모델별 공식 LICENSE URL·리비전/열람일·해당 조항·적용 범위를 붙인다. 원문 인용은 그대로 보존하고 “이 조사에서는 ○조건의 배포 후보로 분류했다”처럼 당시 결정과 해석임을 표시한다. 이후 EXAONE 롤백은 연구·개발용이라는 본문의 제한도 연결한다.

**보존할 내용.** 라이선스명·당시 조사·직접 인용·상업 배포 후보 제외 및 채택 이력

### MD-28 · 중간 · 항목1만 미달이라는 판정 범위

분류: `readability` · 확인: `public_document` · 반영 위치: `either` · im-not-ai: 해당 없음

대상 블록: F09-U425, F09-U426

**문제.** 세 후보가 “항목1에서만 미달”이라고 하지만 gemma e4b·midm은 항목3도0.7 미만이다. 항목3이 관측 전용이어서 판정 항목 중에서는 사실일 수 있으나 지금 문장은 모든5항목을 말하는 것처럼 보인다.

**근거.** `experiments/model-selection.md:1318` · `experiments/model-selection.md:1324`

**원문.**

> **항목 1(사실대로)에서만 미달**

**수정 제안 또는 필요한 근거.** “판정에 쓰는 항목 중에서는 항목1만 미달했다. 관측 전용 항목3은 e4b0.4·midm0.6이었다”처럼 판정/관측 범위를 명시한다. 민감 사실 회피의 원인 설명은 원응답 관찰이라는 수준으로 유지한다.

**보존할 내용.** 각 rate·0.7 기준·항목3 비판정 지위·같은 실패케이스 인용

### MD-29 · 높음 · A.17 A/B 무승부 열 누락

분류: `data` · 확인: `raw_checked` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U428

**문제.** 25쌍 A/B 표에서 페르소나7+4+13=24, 관련성14+5+5=24다. 두 행의 한 건씩이 어느 범주인지 빠져 있다. 원시 summary에서도 두 행 각각 ties=1이 확인됐다.

**근거.** `experiments/model-selection.md:1330` · `com.remakeday/docs/review-verification/2026-09-14-npc-descent/npc-quality-ab-20260914T112712Z.json:summary` · `docs/reviews/full-audit/raw-evidence.json#RAW-06`

**원문.**

> | 페르소나 적합 | 7 | 4 | 13 |

**수정 제안 또는 필요한 근거.** 무승부 열을 복원해 페르소나 7/4/1/13, 관련성 14/5/1/5(승/패/무승부/무효)로 보고한다. 자연스러움·7세 말투의 무승부는 0이다. 모든 행 합계 25를 검산한다.

**보존할 내용.** 25쌍·현재 승수·무효수·실제 무승부가 확인되면 그 값

### MD-30 · 중간 · 자연스러움 9:7을 동등성으로 해석

분류: `claim` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U428, F09-U429, F09-U433, F09-U524

**문제.** 자연스러움9:7에 무효9건인 표를 “사실상 대등권”이라고 요약한다. 검정·허용차 기준 없이 동등성을 입증한 것처럼 보일 수 있다.

**근거.** `experiments/model-selection.md:1330` · `experiments/model-selection.md:1337` · `experiments/model-selection.md:1346` · `experiments/model-selection.md:1781`

**원문.**

> **사실상 대등권**

**수정 제안 또는 필요한 근거.** “자연스러움 유효16쌍에서 exaone9승·kanana7승, 무효9쌍이었다”로 제시하고 동등성 입증 여부는 별개라고 적는다. 채택 이유는 수치와 실제 운영 판단으로 설명한다.

**보존할 내용.** 9·7·9·25쌍·단일judge·kanana 채택 결정

### MD-31 · 중간 · 워밍업 아티팩트와 실제 초기 축출

분류: `data` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U368, F09-U431

**문제.** A.13/A.17의 warm 시점 아티팩트는 아직 Core를 로드하지 않았으므로 축출로 세면 안 되는 사례다. A.9 e4b의 실제 초기 NPC 언로드와 “동류”로 묶으면 서로 다른 현상을 혼동시킨다.

**근거.** `experiments/model-selection.md:1169` · `experiments/model-selection.md:1342`

**원문.**

> A.9의 초기 로드 관측과 동류

**수정 제안 또는 필요한 근거.** “이1건은 Core 로드 전 스냅샷을 축출로 집계한 러너 아티팩트다. A.9의 실제 초기 NPC 언로드와는 구별한다”로 정리하고 스냅샷 시점·판정 규칙 근거를 붙인다.

**보존할 내용.** 원 기록의evictions1·교대구간0·초기로드실제축출 관측

### MD-32 · 중간 · 루프의 16콜·21발화 분모

분류: `data` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U438, F09-U439

**문제.** 루프 표는 전체16콜·NPC agent3콜과 별개로 회피0/21발화·평균11.4자를 보고한다. 21의 수집 범위와 평균 표본을 제시하지 않아 서비스 호출·대화 발화·플레이어 발화를 혼동할 수 있다.

**근거.** `experiments/model-selection.md:1359` · `experiments/model-selection.md:1368`

**원문.**

> | 관리 항목 ① 회피성 응답 | 0 / 21 발화 |

**수정 제안 또는 필요한 근거.** 21발화에 들어가는 대화 경로와 플레이어 출력 포함 여부를 명시한다. 문자 혼입0과 평균11.4자의 분모, 회피 판정 주체·기준을 붙인다. 게이트 통과는 이1회차 스모크 범위로 유지한다.

**보존할 내용.** 16콜 역할합·21발화·11.4자·0관측·61.4s·점수8.8

### MD-33 · 중간 · 비공개 원문과 공개 검증 가능한 요약

분류: `structure` · 확인: `public_document` · 반영 위치: `either` · im-not-ai: 해당 없음

대상 블록: F09-U442, F09-U482, F09-U521

**문제.** 비공개·gitignore 원시 파일을 여러 개 열거한 뒤 이 부록을 정본이라고 한다. 독자는 실행 조건·집계 분모·수치 산식을 공개 자료만으로 재확인하기 어렵다. 민감 로그를 그대로 공개할 필요는 없다.

**근거.** `experiments/model-selection.md:1374` · `experiments/model-selection.md:1592` · `experiments/model-selection.md:1772`

**원문.**

> gitignore — 이 부록이 정본

**수정 제안 또는 필요한 근거.** 공개 가능한 실행 요약을 붙인다: 실행일·코드ref·모델·역할·반복단위·집계/제외규칙·파싱실패/폴백 수·표생성 방법. 비공개 원문은 비공개라고 표시하고 공개 요약이 재현 원자료 전체는 아니라는 범위를 적는다. 개인 발화·키·운영 세부값은 추가 공개하지 않는다.

**보존할 내용.** 원시 출처의 존재·정본/스냅샷 지위·공개 가능한 집계값

### MD-34 · 높음 · 로컬 evaluator p50 역할 혼선

분류: `data` · 확인: `raw_checked` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U444, F09-U445

**문제.** A.19 로컬 evaluator p50=2,918은 A.8의2,179와 다르며2,918은 A.6 advisor p50에도 나온다. 재측정 출처인지 역할 혼입인지 확인 전 숫자를 바꾸면 안 된다. RAW-01에서 연결된 advisor 원시 p50은 2,918ms, evaluator는 2,179ms임을 확인했다. 별도 새 기준선 의도는 아직 확인하지 않았다.

**근거.** `experiments/model-selection.md:1389` · `experiments/model-selection.md:1396` · `experiments/model-selection.md:787` · `experiments/model-selection.md:941` · `docs/reviews/full-audit/raw-evidence.json#RAW-01`

**원문.**

> | 로컬 기준 gemma4:12b-N | 0.90 | O | 0.57 | 4,231 | 2,918 | O | O |

**수정 제안 또는 필요한 근거.** 로컬 기준행의 역할·실행파일·표본·통제세트를 원시 결과와 대조한다. 재측정이면 날짜와 출처를 추가하고 오기면 정정 이력을 남긴다. C13 합성값 및 외부모델 대비 지연 설명도 같은 기준으로 다시 계산한다.

**보존할 내용.** 표의 모델·PCA·극성·eval·원 측정값·정정 근거

### MD-35 · 높음 · Opus까지 포함한 n=3 통과 서술

분류: `data` · 확인: `raw_checked` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U444, F09-U445, F09-U524

**문제.** 표에는 Sonnet n=1/n=3와 Opus n=1만 있는데 본문과 변경이력은 “n=1·n=3 모두 Sonnet·Opus 둘 다PASS”라고 쓴다. 실행하지 않은 조건까지 포함한 것처럼 읽힌다. RAW-05의 연결된 두 파일도 n=1은 두 모델, n=3은 Sonnet만 포함한다. 다른 파일의 존재 여부는 단정하지 않는다.

**근거.** `experiments/model-selection.md:1389` · `experiments/model-selection.md:1396` · `experiments/model-selection.md:1781` · `docs/reviews/full-audit/raw-evidence.json#RAW-05`

**원문.**

> **PCA·극성·eval 게이트는 n=1·n=3
> 모두 Sonnet·Opus 둘 다 PASS**

**수정 제안 또는 필요한 근거.** 추가 Opus n=3 원자료가 없으면 “Sonnet은 n=1·n=3에서, Opus는 n=1에서 PCA·극성·eval 게이트를 통과했다”로 정정한다. 모델별 반복단위 n과 실제 advisor/evaluator 호출 수도 함께 적는다.

**보존할 내용.** Sonnet n=1/n=3·Opus n=1 공개행·각PASS결과·66/42콜

### MD-36 · 높음 · 외부 API 지연의 원인 추정

분류: `claim` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U445, F09-U471

**문제.** 동시 로컬 GPU 작업과 외부 API 지연의 인과는 확인되지 않았다. 조건별 표본이 작은 상황에서 Opus의 지연 차이를 모델 자체의 속도로 확정하기도 어렵다.

**근거.** `experiments/model-selection.md:1396` · `experiments/model-selection.md:1529`

**원문.**

> 모델 자체가 느리다

**수정 제안 또는 필요한 근거.** “이번 실행의 Opus advisor p95는 로컬 기준보다 38% 높았다. API·네트워크·동시 작업의 영향을 분리하지 않았다”로 쓴다. Sonnet의 n=1/n=3 변화는 관측으로 남기고 동시 GPU 작업은 교란 가능성으로 표시한다.

**보존할 내용.** p95·38%·C11/C13 판정·측정 당시 동시 작업

### MD-37 · 중간 · 합성 C13과 미구현 묶음 호출

분류: `claim` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U445

**문제.** evaluator p50×10은 실제 연속 10콜 시간이나 그 p95와 다른 합성 지표다. 호출을 묶으면 1회라는 미구현 변경을 현재 외부 API의 불리함을 설명하는 근거로 섞는다.

**근거.** `experiments/model-selection.md:1396`

**원문.**

> 채점 호출을 묶으면 실제 호출은 1회가 되고

**수정 제안 또는 필요한 근거.** 현재 지표 정의와 호출 수를 먼저 적고, 묶음 호출은 “별도 설계안이며 품질·지연 미측정”으로 분리한다. 실제 밤 채점 벽시계 시간과 합성값을 비교하려면 동일 시도에서 둘을 기록한다.

**보존할 내용.** p50×10·30초 임계값·현행 10콜·미측정 설계의 지위

### MD-38 · 중간 · Core·NPC·플레이어 역할의 혼선

분류: `readability` · 확인: `needs_source` · 반영 위치: `either` · im-not-ai: 해당 없음

대상 블록: F09-U447, F09-U448, F09-U449

**문제.** 완주 표에 Core만 쓰고 플레이어 모델이 빠져 있으며 다음 문단은 “Core gemma4 플레이어(Core gemma4...)”로 역할명이 뒤엉킨다. 플레이어 변경과 GPU 경합을 구별해야 한다.

**근거.** `experiments/model-selection.md:1406` · `experiments/model-selection.md:1412` · `experiments/model-selection.md:1418`

**원문.**

> Core gemma4 플레이어(Core gemma4, NPC kanana)

**수정 제안 또는 필요한 근거.** 완주 표에 Core/NPC/플레이어/think/페르소나/동시 작업 열 또는 주석을 둔다. “플레이어에 gemma4를 사용한 추가 1판(Core gemma4, NPC kanana)”처럼 역할을 분리한다. 실제 모델은 실행 설정을 확인해 채운다.

**보존할 내용.** 1판 5회차·점수·결말·시간·모델 역할·확률적 점수의 제한

### MD-39 · 높음 · gemma4 두 실행의 재생성 요약

분류: `data` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U447, F09-U448, F09-U471, F09-U524

**문제.** 표의 gemma4 대조군에는 advisor 재생성 2가 있지만, 이어지는 gemma4 플레이어 추가 실행은 전 역할 재생성 0이다. 판정 요약의 gemma4 대조군 0 재생성이 어느 실행을 가리키는지 불명확하다. Sonnet의 재생성≤로컬 판정도 전체 합인지 역할별인지 밝혀야 한다.

**근거.** `experiments/model-selection.md:1406` · `experiments/model-selection.md:1412` · `experiments/model-selection.md:1529` · `experiments/model-selection.md:1781`

**원문.**

> Opus·gemma4 대조군 0 재생성·0 폴백

**수정 제안 또는 필요한 근거.** 요약이 가리키는 실행 ID와 Core/NPC/플레이어 구성을 먼저 확인한다. 표의 대조 실행을 요약한 것이라면 advisor 재생성 2·폴백 0을 반영하고, 추가 실행을 뜻한다면 그 실행임을 명시한다. 두 실행을 합쳐 0 또는 2로 단정하지 않는다. Sonnet 비교도 planner끼리 등 역할별 기준을 적는다.

**보존할 내용.** 상세 표 재생성 2·Sonnet planner 재생성 2/폴백 1·최종 조합 재생성 1/폴백 0

### MD-40 · 높음 · 선별 의미 검토와 비열등 결론

분류: `claim` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U453, F09-U471

**문제.** 10케이스를 선별한 사람 검토의 일부 개선으로 NPC “비열등 이상”을 결론낸다. 문서 상단의 재생성 0 게이트는 Haiku 2·Sonnet 1로 만족하지 않아 의미 평가와 전체 게이트의 구별이 필요하다.

**근거.** `experiments/model-selection.md:1440` · `experiments/model-selection.md:1529` · `experiments/model-selection.md:46`

**원문.**

> Haiku·Sonnet 둘 다 로컬 대비 비열등 이상

**수정 제안 또는 필요한 근거.** “선별한 10케이스의 사람 검토에서 방금 들음/기억 구분 개선을 관찰했다”로 범위를 적고 선정법·검토자·항목별 판정을 제공한다. 재생성 0 조건의 미충족과 Sonnet의 남은 실패를 별도로 보고한다. 채택은 사용자 판단이며 모든 게이트 통과와 같지 않다.

**보존할 내용.** 사람 검토 10케이스·모델별 실패 사례·재생성 수·채택 결정

### MD-41 · 중간 · 80/82턴과 러너 수정 전후의 분모

분류: `data` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U450, F09-U451, F09-U452

**문제.** 20케이스×repeat 2가 80평가턴이 되는 추가 턴 구조와 kanana 82턴의 차이가 표에서 설명되지 않는다. 성공 요청 80과 하네스 재시도 2는 서로 다른 집계다.

**근거.** `experiments/model-selection.md:1425` · `experiments/model-selection.md:1427` · `experiments/model-selection.md:1435`

**원문.**

> 20케이스 × repeat 2 = 구조상 80평가턴

**수정 제안 또는 필요한 근거.** 케이스당 평가 대상 턴 수와 82가 된 이유를 원러너에서 확인한다. 논리 턴·NPC 호출 시도·분류기 시도·성공 응답·미복구 폴백을 나눈 집계 정의를 둔다. 수정 전후 Haiku 지연을 별도 실행 행으로 나누면 비교가 명확해진다.

**보존할 내용.** 80·82·14/80·66실패·NPC 재시도와 스텁 결함 구별

### MD-42 · 높음 · 파싱 실패와 VRAM 원인 단정

분류: `claim` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U458, F09-U462, F09-U471, F09-U524

**문제.** 재채점 성공과 단발 API 성공은 앞선 실패가 VRAM 때문이라는 확정이나 어댑터 결함의 배제를 뒷받침하지 못한다. 1·2차는 응답 재생성 여부·채점기·실행 환경 등 여러 요소가 바뀌었다.

**근거.** `experiments/model-selection.md:1465` · `experiments/model-selection.md:1484` · `experiments/model-selection.md:1529` · `experiments/model-selection.md:1781`

**원문.**

> 원인이 채점기
> 자체가 아니라 당시 VRAM 경합으로 판단

**수정 제안 또는 필요한 근거.** 파싱 실패·멈춤·재채점 결과는 관측으로 쓰고 VRAM/계정/네트워크는 미확정 원인 가설로 분리한다. “어댑터 결함은 배제”를 “단발 호출에서는 재현되지 않았다”로 좁힌다. 원인 확인에는 같은 입력·같은 채점기에서 GPU 경합만 바꾼 비교와 오류 로그가 필요하다.

**보존할 내용.** 0/20 파싱 실패·3.31초 진단·32/24분 정지·원인 추정의 제한

### MD-43 · 중간 · 채점기 재판정·일치율의 분모

분류: `data` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U462

**문제.** 20발화를 두 채점기로 각 2회 채점했는데 파싱 실패 0/20·자기일치 20/20·채점기 간 19/20의 계산 단위가 서로 다르다. 원시 판정 80개와 비교쌍 20개를 구분해야 한다.

**근거.** `experiments/model-selection.md:1484`

**원문.**

> 각 2회 재채점한 결과 파싱 실패 0/20(양쪽 다)

**수정 제안 또는 필요한 근거.** 각 모델 20발화×2회=40판정인지 확인하고 파싱 실패는 실제 판정 건수, 자기일치와 모델 간 일치는 비교쌍 수로 표기한다. 모델 간 일치가 어느 회차·집계 규칙 기준인지 적는다.

**보존할 내용.** 20발화·2회·19/20=95%·유일한 불일치 원인용

### MD-44 · 높음 · 4/5 통과와 누설 미측정 게이트

분류: `data` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U457, F09-U460, F09-U461, F09-U471

**문제.** A.19는 4/5로 게이트 통과라 쓰지만 상단 게이트는 4/5 이상과 누설 0이다. 본문은 누설 측정 범위 밖이라고 명시하므로 전체 게이트 통과로 읽히면 안 된다.

**근거.** `experiments/model-selection.md:1458` · `experiments/model-selection.md:1473` · `experiments/model-selection.md:1479` · `experiments/model-selection.md:1529` · `experiments/model-selection.md:47`

**원문.**

> **세 모델 전부 4/5로 게이트를 통과한다.**

**수정 제안 또는 필요한 근거.** “세 모델은 5항목 중 4항목 기준을 통과했다. 누설 0 조건은 이 러너에서 미측정이다”로 분리한다. 별도 누설 실험을 연결할 때는 모델·프롬프트·실행 버전이 같은지 확인한다.

**보존할 내용.** 모든 rate·4/5·Sonnet 메타 발화·누설 미측정

### MD-45 · 중간 · 모델·어댑터·평가 러너 결함의 구분

분류: `readability` · 확인: `public_document` · 반영 위치: `either` · im-not-ai: 해당 없음

대상 블록: F09-U465, F09-U466, F09-U467, F09-U494

**문제.** 어댑터 수정·러너 스텁·서버 입력 상한·judge thinking이 한 목록에 섞여 모델 실패와 계측 실패를 독자가 다시 분류해야 한다. SDK 동작 진술도 특정 1.6.0 환경에 묶어야 한다.

**근거.** `experiments/model-selection.md:1494` · `experiments/model-selection.md:1500` · `experiments/model-selection.md:1502` · `experiments/model-selection.md:1650`

**원문.**

> **Anthropic SDK 1.6.0 `temperature` 인자 소실**

**수정 제안 또는 필요한 근거.** 모델 응답 위반(planner), 어댑터 호환(Haiku), 평가 러너 결함(분류기·thinking), selfplay 입력 결함을 표로 구분한다. 각 행에 영향을 받은 실행·수정 커밋·재실행 여부를 붙인다. temperature 설명은 당시 SDK·모델 설정 기준이라고 한정한다.

**보존할 내용.** 커밋·버전·코드 식별자·실패 인용·수정 전후 응답·하네스 기록

### MD-46 · 높음 · 문자수 비용 추정을 상한으로 해석

분류: `claim` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U468, F09-U469

**문제.** 문자수×1토큰은 실측이 아닌 가정이며 상한이라는 증거가 없다. Sonnet 정지 시도 2건의 ~$0.13은 포함되어 있지만 이 비용도 추정이고, NPC 대화 점검·재측정 일부 축의 실제 토큰 사용량은 집계하지 않았다. 이 부분 추정으로 총 $10 미만을 확정할 수 없다.

**근거.** `experiments/model-selection.md:1519` · `experiments/model-selection.md:1521`

**원문.**

> 문자수 × 1.0토큰 가정 — 상한 추정

**수정 제안 또는 필요한 근거.** “문자수×1.0토큰을 가정한 부분 비용 추정”으로 표기한다. 실제 상한·총지출 판정에는 프로바이더 usage·청구 내역 또는 모든 입력·출력·재시도·실패 과금 범위를 포함한 검증된 상한식이 필요하다. ~$1.06은 해당 실행 범위의 추정으로 보존한다.

**보존할 내용.** ~$1.06·항목별 비용·~$4 배정·$10 목표·실측 정산이 아니라는 제한

### MD-47 · 중간 · 작성 당시 대화 화자와 리뷰 등급

분류: `readability` · 확인: `public_document` · 반영 위치: `either` · im-not-ai: 해당 없음

대상 블록: F09-U374, F09-U403, F09-U421, F09-U469, F09-U492, F09-U507

**문제.** “사용자 프레임”, “내 몫”, “오늘”, “결정은 사용자”, “sonnet 최종 검토 B등급”은 대화 참여자와 작업 시점을 알아야 이해된다. 코드 리뷰 등급이 실험 모델 성능 등급처럼 보일 수 있다.

**근거.** `experiments/model-selection.md:1181` · `experiments/model-selection.md:1257` · `experiments/model-selection.md:1308` · `experiments/model-selection.md:1521` · `experiments/model-selection.md:1638` · `experiments/model-selection.md:1715`

**원문.**

> 내 몫 예산(~$4) 안.

**수정 제안 또는 필요한 근거.** “이 실행분에 배정된 예산(~$4) 안”처럼 집계 범위를 주어로 쓴다. 오늘은 기록일로, sonnet 최종 검토 B등급은 구현 코드 검토 등급(B)으로 명시한다. 사용자와 Scenario Director가 같은 역할인지는 정본에서 정의하고 실제 발화 인용은 보존한다.

**보존할 내용.** 역할·예산·당시 결정 대기·코드 리뷰 등급·직접 발화

### MD-48 · 중간 · 후보 절단 제거와 임베딩 정확도

분류: `claim` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U474, F09-U475, F09-U476

**문제.** 채점 캘리브레이션은 임베딩 모델 자체의 우열보다 후보 top-3 절단과 전체 8개 전달의 차이다. 유사도 랭킹을 쓰지 않는 쪽이 정확하다는 주장은 그 조건의 결과로 제한해야 한다.

**근거.** `experiments/model-selection.md:1550` · `experiments/model-selection.md:1553` · `experiments/model-selection.md:1565`

**원문.**

> 유사도 랭킹을 쓰지 않는 쪽이 채점에 더 정확했기 때문이다.

**수정 제안 또는 필요한 근거.** “당시 골든 세트에서 top-3 후보만 전달하는 경로보다 전체 8개를 전달하는 경로의 채점 결과가 나았다”로 적는다. 후보 선정 대상(정답 주장/유저 주장)과 분모를 원코드에서 확인해 일관되게 설명한다. 임베딩 비교 미실행 결정은 남긴다.

**보존할 내용.** 65.3→100.0·25.7→19.4·2회 반복·0.0%p·09-06 경로 삭제

### MD-49 · 높음 · 과거 두 슬롯과 최종 세 슬롯의 안내

분류: `structure` · 확인: `public_document` · 반영 위치: `either` · im-not-ai: 해당 없음

대상 블록: F09-U310, F09-U474, F09-U477, F09-U478, F09-U479, F09-U480, F09-U483, F09-U492, F09-U498, F09-U512, F09-U519, F09-U524

**문제.** 같은 날 A.20은 호출 0·2슬롯을 정본으로 선언하고 A.21은 3슬롯을 최종 확정한다. 앞의 임베딩 폴백 가정·중간 qwen/Gemini 양자택일·마지막 변경 이력의 결정 대기가 현재 상태처럼 남는다.

**근거.** `experiments/model-selection.md:1007` · `experiments/model-selection.md:1550` · `experiments/model-selection.md:1569` · `experiments/model-selection.md:1571` · `experiments/model-selection.md:1580` · `experiments/model-selection.md:1583` · `experiments/model-selection.md:1596` · `experiments/model-selection.md:1638` · `experiments/model-selection.md:1671` · `experiments/model-selection.md:1739` · `experiments/model-selection.md:1766` · `experiments/model-selection.md:1781`

**원문.**

> 현재 구성은 **Core·NPC 2슬롯뿐**임을 이 부록이 정본으로 정한다.

**수정 제안 또는 필요한 근거.** 역사 문장은 삭제하지 않고 “이후 변경: A.21.8” 안내를 붙인다. 읽기층에 2026-09-18 최종 제출/로컬 구성을 표로 보이고 각 결정 절 링크를 둔다. A.21 중간 2560 결정과 bge 1024 최종 결정을 시점으로 구별하며 변경 이력에 최종 확정 행을 추가한다.

**보존할 내용.** 모든 날짜·당시 판단·A.20 실사·A.21 복원·최종 Gemini 2560/bge 1024

### MD-50 · 중간 · 추천 기능 격리와 무해성의 구별

분류: `claim` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U483

**문제.** 추천을 플레이어가 선택한다는 사실로 오추천이 게이트에 무해하다고 단정한다. 채점 코드 직접 격리는 확인 가능하지만 추천이 선택·게임 진행에 미치는 간접 영향은 다른 문제다.

**근거.** `experiments/model-selection.md:1596`

**원문.**

> 틀려도 게이트에 무해한 자리

**수정 제안 또는 필요한 근거.** “추천 순위를 정하며 최종 선택은 플레이어가 한다. 채점·NPC 기억·단서 해금에는 직접 호출하지 않는다”로 구현 범위를 쓴다. 사용자 경험에 해가 없다는 판정은 오추천을 포함한 플레이 검증이 필요하다.

**보존할 내용.** 직접 쓰기 대안 3개·Strategy·예외 폴백·직접 격리·자매 프로젝트 참고

### MD-51 · 높음 · 실행 후 골든 검수의 조건

분류: `claim` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U482, F09-U501, F09-U502, F09-U521

**문제.** 30문장 중 8개를 모델 실행 후 제외하고 2개를 수정한 22문장 집합을 정본으로 채택했다. 기준 수정 필요성은 설명했지만 검수자가 모델 결과를 봤는지가 불명확해 사후 선택의 영향을 평가하기 어렵다.

**근거.** `experiments/model-selection.md:1592` · `experiments/model-selection.md:1682` · `experiments/model-selection.md:1686` · `experiments/model-selection.md:1772`

**원문.**

> **에이전트 작성·Scenario Director 미검수**

**수정 제안 또는 필요한 근거.** 30→22 변경 이력을 유지하고 검수 시점·검수자가 본 정보·제외/수정 기준·ID별 변경 목록을 공개 가능한 범위로 기록한다. 22문장 결과는 사후 검수 집합임을 표시하며 일반화가 필요하면 별도 미사용 검증 세트를 쓴다.

**보존할 내용.** 원 30문장·제외 8/수정 2·22문장·17쌍·검수 인용

### MD-52 · 높음 · 429 부재와 전역 풀 원인 단정

분류: `claim` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U486

**문제.** 30/30 성공·429 없음에서 429가 키 쿼터가 아니라 전역 풀 문제라고 결론낼 수 없다. 자매 프로젝트 실측도 이 프로젝트 한도의 원인을 대체하지 못한다.

**근거.** `experiments/model-selection.md:1615`

**원문.**

> 429는 키 쿼터가 아니라 베이스 모델 전역 풀

**수정 제안 또는 필요한 근거.** “이번 30요청에서는 429가 없었다”까지 실측으로 쓴다. 원인 진술을 남기려면 당시 Gemini 오류의 quota metric/scope와 공식 정의·실제 프로젝트 한도 근거가 필요하다. 임베딩 일일 상한 미측정 기록은 유지한다.

**보존할 내용.** 30/30 성공·429 없음·별도 503·미측정 상한

### MD-53 · 중간 · 적중률·추천 일치도·순위 통계의 정의

분류: `readability` · 확인: `needs_source` · 반영 위치: `either` · im-not-ai: 해당 없음

대상 블록: F09-U485, F09-U489, F09-U497, F09-U502, F09-U503, F09-U510, F09-U511

**문제.** top-1/3 적중률, top-1 일치, Jaccard, Kendall τ가 모두 인접해 있다. 분모·집계법·순위 방향·동률 처리가 없어 비전공 독자가 정확도와 모델 간 일치를 혼동하기 쉽다.

**근거.** `experiments/model-selection.md:1607` · `experiments/model-selection.md:1623` · `experiments/model-selection.md:1664` · `experiments/model-selection.md:1686` · `experiments/model-selection.md:1695` · `experiments/model-selection.md:1726` · `experiments/model-selection.md:1732`

**원문.**

> | 쌍 | top-1 일치 | top-3 Jaccard | Kendall τ |

**수정 제안 또는 필요한 근거.** 표 주석에 적중률=정답 행동 포함 문장 수/전체 문장 수, top-1 일치=두 모델의 첫 추천이 같은 비율, Jaccard=상위 3개 집합의 겹침, τ=전체 순서의 일치라고 설명한다. Jaccard·τ의 문장별 평균 여부와 동률 처리는 러너 기준으로 적는다. 0.909=20/22 같은 건수를 주요 행에 병기한다.

**보존할 내용.** 모든 수치·n=30/n=22·행동 목록·일치와 정확도의 구별

### MD-54 · 높음 · 차원 절단 손실을 지운 해석

분류: `claim` · 확인: `raw_checked` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U485, F09-U489, F09-U490, F09-U524

**문제.** qwen 2560→1536의 top-1은 0.933→0.867로 30문장 중 2건 감소했다. τ 0.918만 보고 잃는 게 없다거나 절단이 무해하다고 하면 손실을 지운다.

**근거.** `experiments/model-selection.md:1607` · `experiments/model-selection.md:1623` · `experiments/model-selection.md:1632` · `experiments/model-selection.md:1781` · `docs/reviews/full-audit/raw-evidence.json#RAW-03`

**원문.**

> 1536 호환 규격을 써도 잃는 게 없다.

**수정 제안 또는 필요한 근거.** “2560→1536에서 전체 순위 일치 τ는 0.918이었고 top-3 적중률은 유지됐다. 다만 top-1 정답은 28/30에서 26/30으로 2건 줄었다”로 지표별 효과를 분리한다. 변경 이력의 절단 무해도 함께 정정한다.

**보존할 내용.** 차원·τ·top-1/top-3·오답 수·역사적 차원 선택

### MD-55 · 높음 · 같은 정답 적중과 같은 추천 목록

분류: `claim` · 확인: `public_document` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U490, F09-U492, F09-U498, F09-U504, F09-U512, F09-U524

**문제.** 정답이 top-3에 있다는 적중률 1.000을 같은 추천 3개·같은 순서로 해석한다. Jaccard 0.627/0.600과 τ<1은 추천 목록·전체 순위에 차이가 있음을 이미 보여 준다.

**근거.** `experiments/model-selection.md:1632` · `experiments/model-selection.md:1638` · `experiments/model-selection.md:1671` · `experiments/model-selection.md:1703` · `experiments/model-selection.md:1739` · `experiments/model-selection.md:1781`

**원문.**

> 플레이어가 보는 결과는 사실상 같다.

**수정 제안 또는 필요한 근거.** “두 모델 모두 정답을 상위 3개에 포함했으나 추천 목록과 순서는 같지 않다”로 구분한다. 아무것도 바뀌지 않음·어느 차원이든 같은 순위도 어떤 지표가 같은지 명시한다. 노출 결과의 동일성을 주장하려면 정렬된 추천 3개의 완전 일치율을 별도로 계산한다.

**보존할 내용.** top-3 적중률 1.000·Jaccard·τ·차원별 top-1·원순위 측정

### MD-56 · 중간 · 순위 비일치를 무의미로 해석

분류: `claim` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U490, F09-U504

**문제.** 다른 모델과 τ≈0이라는 이유로 어간 순서가 무의미하다고 할 수 없다. 모델 간 비일치는 정답 기준 평가와 다르며 어간 top-3도 0.833/0.818이다.

**근거.** `experiments/model-selection.md:1632` · `experiments/model-selection.md:1703`

**원문.**

> 어간 겹침은 순서가 무의미

**수정 제안 또는 필요한 근거.** “어간 순위는 임베딩 순위와 일치도가 낮았고 정답 top-1 적중률은 30문장에서 0.300, 22문장에서 0.364였다”로 지표를 분리한다. 무의미하다는 해석은 내용 정정 대상으로 다루며 자동 윤문하지 않는다.

**보존할 내용.** τ·어간 top-1/top-3·기존 폴백 역할

### MD-57 · 중간 · 판정·구현 검증·중간 후보의 배치

분류: `structure` · 확인: `public_document` · 반영 위치: `either` · im-not-ai: 해당 없음

대상 블록: F09-U492

**문제.** 판정 목록에 게이트·코드 리뷰·예외 처리·테스트 960개·최종 provider·초기 후보·설정 오타가 섞여 있다. 서로 다른 시점의 항목을 독자가 재구성해야 한다.

**근거.** `experiments/model-selection.md:1638`

**원문.**

> sonnet 최종 검토(B등급)

**수정 제안 또는 필요한 근거.** A.21.3을 실험 판정, 구현 검증, 당시 후보의 세 문단으로 나누고 최종 구성은 A.21.8로 안내한다. B등급은 구현 리뷰 결과임을 표시하며 960 passed를 모델 성능 검증 점수로 쓰지 않는다. “설정 파일는”은 “설정 파일은”으로 바꾼다.

**보존할 내용.** Critical/Major 수·코드 수정·960 passed·당시 후보·최종 결정

### MD-58 · 중간 · 공개 문서에 없는 A.22 예정 참조

분류: `structure` · 확인: `needs_source` · 반영 위치: `either` · im-not-ai: 해당 없음

대상 블록: F09-U494

**문제.** A.22를 예정 참조하지만 이 공개 문서에는 A.22가 없다. 완료한 후속 코드 수정과 아직 공개하지 않은 실험이 같은 단락에 있다.

**근거.** `experiments/model-selection.md:1650`

**원문.**

> 같은 날 밤 실행 예정(A.22).

**수정 제안 또는 필요한 근거.** “이후 실행 예정이며 이 스냅샷에는 결과 미포함”으로 표시한다. 결과가 이미 있다면 정본의 실행 출처·실측 절을 확인한 뒤 공개 스냅샷을 갱신한다. 예정을 임의로 완료로 바꾸지 않는다.

**보존할 내용.** 당시 예정일·provider 러너 반영·완료한 958 passed 수정

### MD-59 · 중간 · 차원 비교의 n=15와 n=30

분류: `data` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U497, F09-U498

**문제.** Gemini 2560 표는 재실행 30/30인데 3072↔2560 τ는 n=15라고 한다. 서로 다른 실행·표본 수를 같은 조건으로 읽으면 안 된다.

**근거.** `experiments/model-selection.md:1664` · `experiments/model-selection.md:1671`

**원문.**

> gemini3072↔gemini2560(n=15) τ 0.942

**수정 제안 또는 필요한 근거.** 15건은 503으로 중단한 실행의 공통 문장인지 명시한다. 가능하면 완료한 30건의 같은 ID로 일치도를 재집계한다. 재집계하지 않으면 표에 실행 ID·비교 분모·부분 실행임을 붙인다.

**보존할 내용.** 503 첫 중단·30/30 재실행·기존 n=15 값·τ 0.942

### MD-60 · 높음 · 지원 차원 전체와 실제 측정 범위

분류: `claim` · 확인: `raw_checked` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U498, F09-U512

**문제.** 측정한 Gemini 차원은 1024·1536·2560·3072인데 지원 범위 128~3072 전체가 차원 무관하다고 쓴다. 순위 τ만으로 모델 공간 자체가 더 가깝다고 할 수도 없다. RAW-04에서 확인한 8개 파일에도 128차원 조건은 없었다.

**근거.** `experiments/model-selection.md:1671` · `experiments/model-selection.md:1739` · `docs/reviews/full-audit/raw-evidence.json#RAW-04`

**원문.**

> 128~3072 전 구간에서 이 과제는 차원 무관

**수정 제안 또는 필요한 근거.** “검수한 22문장에서는 Gemini 1024·1536·2560의 top-1 적중률이 0.955로 같았다. 초기 30문장의 1536·2560·3072 비교는 별도로 보고한다”로 표본을 분리한다. 같은 차원도 실행 시점·표본이 다르면 조건을 표시한다. 모델 공간이 가깝다는 주장은 “이 22문장과 행동 목록의 순위 일치 τ는 bge가 qwen보다 높았다”로 쓰고 τ 비율을 유사성의 배수로 해석하지 않는다.

**보존할 내용.** 지원 차원 범위·실제 비교 차원·τ·top-1·bge 채택 결정

### MD-61 · 중간 · 30문장 반복과 22문장 검수의 구분

분류: `claim` · 확인: `raw_checked` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U499, F09-U505, F09-U519

**문제.** 제목은 검수 골든 22문장·반복 n=3처럼 묶이지만 반복은 초기 30문장이다. 세 번 같은 적중률·오답 집합만으로 전체 순위의 결정론이나 반복의 의미를 일반화한다. RAW-03에서도 반복 파일 3개가 모두 30문장임을 확인했다.

**근거.** `experiments/model-selection.md:1678` · `experiments/model-selection.md:1706` · `experiments/model-selection.md:1766` · `docs/reviews/full-audit/raw-evidence.json#RAW-03`

**원문.**

> 임베딩 순위는 결정론적이라 반복은 지연에만 의미가 있다

**수정 제안 또는 필요한 근거.** 제목·요약에서 검수 골든 22문장 결과와 초기 30문장 반복 검사를 분리한다. “30문장 3회에서 top-1·top-3·오답 집합이 같았다”로 관측을 한정한다. 전체 순위 일치도 확인했다면 추가 근거를 명시한다.

**보존할 내용.** n=30/n=22·3회·동일 오답 집합·지연 변동·원인 미확정

### MD-62 · 중간 · 로컬 최적의 판단 기준

분류: `claim` · 확인: `raw_checked` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U504, F09-U507, F09-U519

**문제.** qwen 2560을 로컬 최적이라고 하지만 bge와 22문장 top-1이 같고 메모리는 bge가 작다. 최적화 목표·비교 범위 없이 최종 승자로 오해할 수 있다.

**근거.** `experiments/model-selection.md:1703` · `experiments/model-selection.md:1715` · `experiments/model-selection.md:1766` · `experiments/model-selection.md:132` · `docs/reviews/full-audit/raw-evidence.json#RAW-02`

**원문.**

> 로컬 최적은 qwen@2560

**수정 제안 또는 필요한 근거.** “이번 후보 중 qwen 2560은 top-1이 bge와 동률이고 p50이 더 짧았다. 동시 상주 조건에서는 bge를 채택했다”로 선택 축을 명시한다. 단독 실행 지연 우위 등 정확한 범위를 붙여 문서 자체의 최적 표현 금지와 맞춘다.

**보존할 내용.** 동률 0.909·86/109ms·동주 불가·bge 채택

### MD-63 · 중간 · GPU 메모리 단위와 집계 범위

분류: `data` · 확인: `needs_source` · 반영 위치: `source_of_truth` · im-not-ai: 해당 없음

대상 블록: F09-U507, F09-U509, F09-U512, F09-U516, F09-U517, F09-U518

**문제.** GB·GiB·MiB가 섞이고 13,402MiB를 13.4GB로 다뤄 합계 14.1GB를 만든다. 여유 16,311−14,187=2,124MiB≈2.07GiB를 ~2.1GB라고 쓴다. 각 모델 상주량과 장치 전체 사용량도 다르다.

**근거.** `experiments/model-selection.md:1715` · `experiments/model-selection.md:1723` · `experiments/model-selection.md:1739` · `experiments/model-selection.md:1755` · `experiments/model-selection.md:1757` · `experiments/model-selection.md:1764`

**원문.**

> 13.4+0.66=14.1GB 상주 가능

**수정 제안 또는 필요한 근거.** 장치 전체 사용량과 모델별 바이트를 같은 단위로 환산한다. “장치 여유 2,124MiB(약 2.07GiB)”처럼 원시 바이트 확인 후 쓴다. 모델 합계와 런타임 오버헤드를 포함한 장치 총량은 별도 열로 둔다.

**보존할 내용.** 원 MiB·상주 바이트·추정과 실측·16GB 제품명·최종 상주 성공

### MD-64 · 중간 · 동주 예산 추정과 최종 실측

분류: `claim` · 확인: `public_document` · 반영 위치: `either` · im-not-ai: 해당 없음

대상 블록: F09-U507, F09-U509, F09-U512, F09-U514, F09-U517, F09-U518

**문제.** A.21.6/7은 bge 동주 가능을 실측 전 단정하고 .8에서 추정이었다고 밝힌다. qwen 2/2 축출도 모든 로컬 구성의 불가능보다 해당 설정의 결과로 한정해야 한다.

**근거.** `experiments/model-selection.md:1715` · `experiments/model-selection.md:1723` · `experiments/model-selection.md:1739` · `experiments/model-selection.md:1747` · `experiments/model-selection.md:1757` · `experiments/model-selection.md:1764`

**원문.**

> **VRAM 동주 — 로컬 구성에서는 동주 불가.**

**수정 제안 또는 필요한 근거.** “이번 gemma4+kanana 설정에서 qwen 임베딩 호출 2/2에 두 모델이 축출됐다”로 쓴다. .6/.7의 bge는 예산 추정, .8은 실측 확인 단계라고 앞에서 명시한다. 유일 후보는 이번 시험 후보 범위로 한정한다.

**보존할 내용.** 2/2·실측 최종 3모델 상주·초기 로딩/후속 지연·사용자 선택 이력

### MD-65 · 중간 · HTTP 배선 검사와 추천 의미 정확도

분류: `readability` · 확인: `public_document` · 반영 위치: `either` · im-not-ai: 해당 없음

대상 블록: F09-U501, F09-U515

**문제.** 검수에서 밥 나눠주지 마≠배급을 남긴다를 제외한 뒤 서버 검증은 유사 문장을 배급을 남긴다로 출력한 사례를 보인다. 서버·계산 일치 검사이지 의미 정확도 통과 사례가 아니다.

**근거.** `experiments/model-selection.md:1682` · `experiments/model-selection.md:1749`

**원문.**

> "채연이한테 밥 나눠주지 말라고 해" → 배급을 남긴다

**수정 제안 또는 필요한 근거.** “배선·순위 반환 일치 검사용이며 추천의 의미 정답 판정은 아님”을 명시한다. 22문장 정확도 시험과 HTTP·폴백 동작 검사를 별도 축으로 표시하고 원응답은 그대로 둔다.

**보존할 내용.** 원입력·추천 3개·서버와 로컬의 일치·검수 제외 사유·지연

### MD-66 · 중간 · 설정 요청 차원과 실제 반환 차원

분류: `readability` · 확인: `public_document` · 반영 위치: `either` · im-not-ai: 해당 없음

대상 블록: F09-U496, F09-U498, F09-U509, F09-U515, F09-U519

**문제.** 설정 차원 기본 2560을 bge가 무시해 실제 1024를 반환하며 최종 설정은 provider 한 줄만 바꾸라고 한다. 요청 차원·실제 차원·모델 기본값이 분리되어야 재현할 수 있다.

**근거.** `experiments/model-selection.md:1661` · `experiments/model-selection.md:1671` · `experiments/model-selection.md:1723` · `experiments/model-selection.md:1749` · `experiments/model-selection.md:1766`

**원문.**

> 차원 기본 2560

**수정 제안 또는 필요한 근거.** 최종 구성 표에 provider/model/요청 dimensions/실제 반환 dimensions를 구분한다. bge는 이번 서빙에서 2560 요청에도 1024를 반환했다고 설명한다. 한 줄 변경은 bge 모델 기본값이 반영된 코드 버전 기준임을 붙인다.

**보존할 내용.** 2560 요청·1024 반환·Gemini 2560·bge 기본값 변경·날짜·실서버 관측

### MD-67 · 중간 · 변경 이력의 순서와 최종 확정 상태

분류: `structure` · 확인: `public_document` · 반영 위치: `either` · im-not-ai: 해당 없음

대상 블록: F09-U524

**문제.** 변경 이력은 09-16 뒤에 09-14가 끼고 마지막 행은 초기 30문장과 provider 대기 상태로 끝난다. 긴 행에 실험 수치·코드 수정·결정·과제가 섞여 변경 순서를 확인하기 어렵다.

**근거.** `experiments/model-selection.md:1781`

**원문.**

> 프로덕션 provider는 사용자 결정 대기.

**수정 제안 또는 필요한 근거.** 기존 행은 보존하고 같은 날 후속 22문장 검수·동주 실측·최종 bge/Gemini 결정 행을 추가한다. 날짜순으로 정렬하거나 기록 추가순임을 명시한다. 읽기층에는 요약과 부록 링크를 두고 사후 수치 정정은 별도 정정 행으로 기록한다.

**보존할 내용.** 모든 날짜·원채택 순서·이전 결정과 보류·측정 한계

### MD-68 · 낮음 · 연결어미 뒤 쉼표의 국소 윤문

분류: `style` · 확인: `public_document` · 반영 위치: `source_of_truth` · im-not-ai: C-11

대상 블록: F09-U306, F09-U307, F09-U308, F09-U310, F09-U336, F09-U343, F09-U362, F09-U374, F09-U381, F09-U397, F09-U406, F09-U410, F09-U415, F09-U421, F09-U445, F09-U453, F09-U458, F09-U483, F09-U498, F09-U512, F09-U524

**문제.** 연결어미 직후 쉼표가 반복된다. im-not-ai C-11에 직접 매핑되며 대부분 쉼표 하나만 삭제해 의미·격식·수치를 보존할 수 있다. 실제 발화 인용의 쉼표는 제외한다.

**근거.** `experiments/model-selection.md:999` · `experiments/model-selection.md:1001` · `experiments/model-selection.md:1003` · `experiments/model-selection.md:1007` · `experiments/model-selection.md:1074` · `experiments/model-selection.md:1094` · `experiments/model-selection.md:1152` · `experiments/model-selection.md:1181` · `experiments/model-selection.md:1200` · `experiments/model-selection.md:1242` · `experiments/model-selection.md:1266` · `experiments/model-selection.md:1279` · `experiments/model-selection.md:1293` · `experiments/model-selection.md:1308` · `experiments/model-selection.md:1396` · `experiments/model-selection.md:1440` · `experiments/model-selection.md:1465` · `experiments/model-selection.md:1596` · `experiments/model-selection.md:1671` · `experiments/model-selection.md:1739` · `experiments/model-selection.md:1781`

**원문.**

> 후보와 NPC가 동시 상주했고, 부분 CPU 오프로드도 0이다.

**수정 제안 또는 필요한 근거.** “후보와 NPC가 동시 상주했고 부분 CPU 오프로드도 0이다.”처럼 이고,/보이며,/했고, 뒤 쉼표만 국소 삭제한다. 1236행 “알 수 있고, 준비할 수 있잖아”와 1266행 인용 “활동하고, 그로 인해”는 실제 발화라 그대로 둔다. 내용 정정과 별도 검토 단위로 취급한다.

**보존할 내용.** 접속 관계·문장 격식·수치·유보 강도·발화 인용·기술 용어

## 보존 판정과 적용 경로

keep 94개도 모두 읽었다. 날짜별 실험 제목, 프로토콜과 결과의 구분, 작은 표본·점수 비교 불가·초기 실패와 재실행 이력, 출처, 마지막의 측정 범위 원칙은 연구 기록의 기능을 수행한다. 무엇을 보존한 것인지는 [model-decisions-ledger.json](model-decisions-ledger.json)에 블록별 사유로 남겼다. 불확실한 원인을 추정으로 남긴 표현을 단정으로 바꾸지 않는다.

source_of_truth는 앱 정본 `com.remakeday/docs/model_evaluation.md`에서 확인·정정할 사항이다. reading_layer는 공개 사이트의 해설·탐색 안내이며 either는 양쪽에서 문맥에 맞춰 다룰 수 있다. 역사 기록은 삭제하지 말고 이후 변경 링크·정정 이유·최종 상태를 덧붙인다. 공개 스냅샷만 임의 수정하면 다음 갱신 때 정본과 갈라지므로 이 검토에서는 적용하지 않았다.

검사 결과: 입력 226개와 판정 226개의 ID가 정확히 일치하고 중복·누락이 없다. 모든 인용은 대상 블록에서 정확히 검색되며, 모든 발견 ID와 원장 연결을 검사했다. 원문의 226개 블록 내용과 SHA-256은 입력 원장과 같아 변경되지 않았다. 이 검사는 검토 산출물의 누락·참조·원문 불변성을 확인하며 연구 결론 전체의 타당성을 보증하지 않는다.
