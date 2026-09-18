# Model evidence follow-up: MF-15, MF-17, MD-34, MD-35, MD-39

Verified read-only on 2026-09-18 against the raw application workspace and the audit inputs. Counts below are aggregates only; no prompt, response, participant identifier, credential, endpoint, or database detail is reproduced.

## Findings

### MF-15 — what the 372 denominator counts

**Confirmed.** The formal Stage 2 artifact has four cells. Each cell records 66 advisor items, 9 planner items, 9 manager items, and 9 evaluator items: 93 role-item executions per cell and **372 role-item executions** overall. The expanded formula is `4 cells × (22 advisor + 3 planner + 3 manager + 3 evaluator) items × 3 repetitions = 372`.

The artifact's `calls` fields count those role-item rows, not literal provider requests. Of the 372 rows, 360 initiated an LLM request, 12 advisor meta rows had `attempts=0`, and nine regenerations produced **369 provider attempts**. All 372 rows ended without fallback. The later A.8 evaluator extension is separate: `4 cells × 14 cases × 3 repetitions = 168` rows and 168 provider attempts, with no regeneration or fallback.

Suggested wording:

> Stage 2 formal recorded 372 role-item executions: 4 cells × (22 advisor + 3 planner + 3 manager + 3 evaluator) × 3 repetitions. Of these, 360 initiated an LLM call; nine regeneration attempts brought the provider-attempt total to 369, while 12 meta items required no provider call. A.8 is a separate 168-call evaluator extension.

Do not call 372 “actual model/provider calls” without this qualification.

Primary sources:

- `docs/review-verification/2026-09-13-core-selection/stage2-formal-20260913T132023Z.json` — SHA-256 `559b8bb2768cdf6e46e5e12564bc75a4cbf4fc1f9d98cad11282e187cdf8716b`
- `docs/review-verification/2026-09-13-core-selection/stage2-formal-20260914T021635Z.json` — SHA-256 `fa85cbe48ad4c8ef42486e36a6f7c390466cd31536d83523c9ed167e4ef648a7`
- `backend/scripts/run_core_selection.py` — SHA-256 `8bf2edf1eb1d61890188cb6c2ff21e2b7fa4db1b1ed19c77461b9447875debaf`

### MF-17 — EGR is the intersection

**Confirmed.** The runner defines EGR as `has_detail AND has_evidence`. In each of the nine post-fix Gemma recovery runs, 11/12 question results had detail, 10/12 had evidence IDs, and **10/12 had both**, so EGR was `10/12 = 0.8333`. The initial failed run was 0/12 on all three counts. The 11/12 and 10/12 figures are marginal counts, not two EGR values.

Suggested wording:

> After the fix, 11/12 responses contained detail and 10/12 contained evidence IDs; 10/12 satisfied both conditions, so EGR was 0.8333. Before the fix, EGR was 0/12.

Gemma source artifacts, in time order:

- `real-model-artifacts/probes-20260909T035804Z.json` — SHA-256 `2979ac96b5052f12b16f55bf0b85136008008527832f1b7e8a4bc2c38922639b`
- `real-model-artifacts/probes-20260909T041723Z.json` — SHA-256 `56df6abb7e86857432b13505ae76e7a752061e1aee68707751007e85566c4f8b`
- `real-model-artifacts/probes-20260909T054143Z.json` — SHA-256 `ec0b66e7101ff0681aef8c75e1c9e34a6347eee515961e6f58925f69900230c2`
- `real-model-artifacts/probes-20260909T055416Z.json` — SHA-256 `e1d29431c8ed8f1d83debe7b735f47e28dddb13bcc60d64b9c2becb1e57fa78b`
- `real-model-artifacts/probes-20260909T061038Z.json` — SHA-256 `cb2be29b556162e630f2bf6b3ffc21e67da4e90f135e9c0b8cc0bb76a1d0e21e`
- `real-model-artifacts/probes-20260909T062838Z.json` — SHA-256 `049f9acd282d878416d59313c6d035c47e742d224c698a00444f0589cbc9dc3b`
- `real-model-artifacts/probes-20260909T063851Z.json` — SHA-256 `db8885673b0672ebfbd2f1fbfda1272aded4513d71e90ea36f0281a208a7e316`
- `real-model-artifacts/probes-20260909T064753Z.json` — SHA-256 `7c6b057b8913128f3b4ddcff9ed58d8e27a668e62d348229de1f7cbdd0f443a9`
- `real-model-artifacts/probes-20260909T071926Z.json` — SHA-256 `2f07c1fc432460e3601d086423b99170716b9709f1d396eabf3f5059f856b814`
- `real-model-artifacts/probes-20260909T073556Z.json` — SHA-256 `adf69d8b2df289aefdb964fb2aa6282417a76481ce5dc70b8495e13cdbb969a4`

All are under `docs/review-verification/2026-09-09-connected-implementation/` in the application workspace.

### MD-34 — intended local baseline for the external comparison

**Confirmed as a role mix-up.** The external comparison intentionally combines the accepted local advisor and evaluator baselines because its external run uses 22 advisor items plus 14 evaluator cases. The local advisor artifact supplies p50 **2,918 ms** and p95 **4,231 ms**. The local 14-case evaluator artifact supplies expected agreement **0.5714**, p50 **2,179 ms**, and p95 **2,735 ms**. No checked evaluator artifact supports 2,918 ms; that number exactly matches advisor p50.

Therefore the external table's `evaluator p50` cell should be **2,179 ms**. C13 remains a pass at 21,790 ms. Comparisons derived from 2,918 ms must also change: Sonnet n=1 evaluator p50 is about **46%** slower than the local evaluator baseline, and Opus n=1 is about **44%** slower, rather than about 9%.

Suggested wording:

> Local comparator: advisor p95 4,231 ms from the 22-item advisor run; evaluator expected agreement 0.5714 and evaluator p50 2,179 ms from the 14-case evaluator extension. These values come from separate role-specific runs.

Primary sources:

- `docs/review-verification/2026-09-13-core-selection/stage1-smoke-advisor-20260913T124645Z.json` — SHA-256 `70cc0a82a40d360305a000f4c8d00f4a3b34c7f696263b2656ea4f8d48b0ae27`
- `docs/review-verification/2026-09-13-core-selection/stage2-formal-20260914T021635Z.json` — SHA-256 `fa85cbe48ad4c8ef42486e36a6f7c390466cd31536d83523c9ed167e4ef648a7`
- `output/model-eval-2026-09-16-anthropic/core-age7-summary.md` — SHA-256 `bcfa1fb4971da705e08779b23b9e712078d35a36595a6eb47ebbafaba600afbe`

### MD-35 — Opus n=3 artifact

**No Opus n=3 artifact was found in the available application workspace.** The n=1 JSON contains Sonnet and Opus. The n=3 JSON and its log contain Sonnet only. The contemporaneous summary explicitly says both candidates stopped at n=1 at that checkpoint and later recommends Sonnet-only n=3; the resulting n=3 artifact is Sonnet-only. A workspace-wide content search found Opus only in the n=1 JSON and narrative/metrics documents.

This establishes absence from the inspected workspace, not universal nonexistence outside it.

Suggested wording:

> Sonnet passed the PCA/polarity/evaluator gates at n=1 and n=3. Opus passed those gates at n=1; no Opus n=3 artifact was found in the retained evaluation workspace.

Primary sources:

- `output/model-eval-2026-09-16-anthropic/stage2-formal-20260916T121314Z.json` — SHA-256 `71f7ee3f5424b35627fc19755797e00c3558a5798ab826018f04ca2eae4cb39f`
- `output/model-eval-2026-09-16-anthropic/stage2-formal-20260916T143841Z.json` — SHA-256 `88a99e5fa64db4cd95cb57ef1ed2ac4b5d7711db51c6414b50fad3ae1abdf630`
- `output/model-eval-2026-09-16-anthropic/core-sonnet5-n3.log` — SHA-256 `752cf21292dd58402c5ec149f1222d8b06c26a056e178da95328a6af1cfff465`
- `output/model-eval-2026-09-16-anthropic/core-age7-summary.md` — SHA-256 `bcfa1fb4971da705e08779b23b9e712078d35a36595a6eb47ebbafaba600afbe`

### MD-39 — Gemma regeneration 2 versus 0

**Both counts are correct for different runs.** The first five-loop local Core-control run has four advisor events, six advisor attempts, hence **two advisor regenerations**, and zero fallbacks. A later five-loop run with the Gemma player configuration has four advisor events and four attempts; all other recorded roles are also one attempt per event, so it has **zero regenerations and zero fallbacks**. The two runs must not be collapsed into one Gemma result.

Suggested wording:

> In the first local Core-control run, Gemma had two advisor regenerations and no fallback. In the later Gemma-player run, every recorded role completed without regeneration or fallback. The zero-regeneration statement refers only to the later run.

Primary sources:

- `scratchpad/inspector-gemma4.json` — SHA-256 `ffee0f0cef1c56c4c58bca3954a4883b9119caa21aa77054328186a794b089e8`
- `scratchpad/selfplay-core-gemma4.yml` — SHA-256 `42901729d582d57ea62df70bc1a975add8f1eeab3b5e5502b99690324b991fe9`
- `scratchpad/inspector-player-gemma4.json` — SHA-256 `0afcd341e238e1f0311ce71e402f98057d393751765aec385dd414aa03833c94`
- `output/gemma4-unify-2026-09-16/selfplay-player-gemma4.yml` — SHA-256 `a4a15e41f07ce60dd14095103495c53189b2c63c9b66f70050065344e2e407db`
- `output/gemma4-unify-2026-09-16/selfplay-player-gemma4.log` — SHA-256 `0b526e7067031ff6845bd7cd90d836205f27171422868387d39ee25e1ff13e60`

The three `scratchpad/` files are retained temporary raw artifacts in the existing evaluation scratch workspace; their hashes are supplied because they are not part of the application repository.

## Audit inputs checked first

- `docs/reviews/full-audit/model-foundations-findings.json` — SHA-256 `dd5e58ba6b0b2b5faebc157b7d0b9e50b4f3acc6c9591cbaa1e24f4522558a27`
- `docs/reviews/full-audit/model-decisions-findings.json` — SHA-256 `062cc468969145c5ba8f3b3dd9d521b13da51086df1d0454e208759831d062f5`
- `docs/reviews/full-audit/raw-evidence.json` — SHA-256 `b4e0b38d4eb5ae3dbcf9dccc4a0004aa4b188c223cf4666805d4d2a0ab00271c`

## Limits

- Provider-attempt counts are derived from each retained event's `attempts` field; no network or model run was performed.
- The Opus conclusion is limited to artifacts discoverable in the current application workspace.
- The MD-39 raw inspectors are temporary artifacts. Preserve or promote them before relying on their hashes as long-term public provenance.

## Additional check: `SD-reviewed-22` repeat provenance

**No three-run repeat set for the reviewed 22-item corpus was found.** The rule-alternatives output directory contains eight JSON artifacts: three 30-item timestamped draft runs, three named repeat files (also 30 items each), and only two 22-item files. The two 22-item files are separate single executions:

- `rule-alternatives-20260918T021836Z.json`: 22 items and six cells (`stem`, `qwen2560`, `qwen1536`, `bge`, `gemini`, `gemini2560`).
- `rule-alternatives-20260918T022248Z.json`: 22 items and four cells (`bge`, `gemini1024`, `gemini`, `qwen2560`).

The retained `rule-alternatives-rep1.json`, `rep2.json`, and `rep3.json` files each contain 30 items and the same six draft-corpus cells. RAW-03 confirms that their top-1/top-3 results and wrong-item positions match across the three runs. They do not support `repeat_n3_identical:true` on the six `SD-reviewed-22` rows in `docs/metrics.yml`.

The narrow correction is therefore to remove `repeat_n3_identical:true` from those six reviewed-22 rows and state separately that **the earlier 30-item draft corpus** was repeated three times with identical accuracy and wrong-item sets. Do not transfer that repeat claim to the 22-item reviewed corpus without new retained artifacts.

Latency values should remain unchanged during this correction. The 02:18:36 artifact is the only retained six-cell reviewed-22 run and is the natural coverage source for the six rows. The later 02:22:48 run remeasures only four cells and records nearby but distinct latency samples. The exact latency decimals in `docs/metrics.yml` do not all reproduce exactly from either retained JSON. Add execution-source notes and retain the published values pending a separate latency reconciliation; do not silently substitute one run's values for the other.

Suggested wording:

> Reviewed-22 accuracy source: `rule-alternatives-20260918T021836Z.json` (single six-cell run). A later partial rerun, `rule-alternatives-20260918T022248Z.json`, covers four cells and has separate latency samples. The retained n=3 repeat artifacts use the earlier 30-item agent-draft corpus, where all three runs had identical accuracy and wrong-item sets; no reviewed-22 n=3 artifact set was found.

Primary sources:

- `output/rule-alternatives-2026-09-18/rule-alternatives-20260918T021836Z.json` — SHA-256 `f1cb41964ac1c573ec9e6624d85be9986e184fbed02c5df9c995ceb766d03060`
- `output/rule-alternatives-2026-09-18/rule-alternatives-20260918T022248Z.json` — SHA-256 `81f05abaa657f56cd934b773f2ac3afa94c6fac40747cebf27d1f90049ab93ba`
- `output/rule-alternatives-2026-09-18/rule-alternatives-rep1.json` — SHA-256 `8906d1b2fa1cfeafb7d1bdfd5cd65de9ba0e778d301fd34b94e86d649ed26686`
- `output/rule-alternatives-2026-09-18/rule-alternatives-rep2.json` — SHA-256 `721436bb3089946f25cbfcd3a21f2aa0acb1cd7a97fc9e140de2355723d80ced`
- `output/rule-alternatives-2026-09-18/rule-alternatives-rep3.json` — SHA-256 `b58f101b85b53ac3662688f21be9735b4ee3e60be8c4ea06d1c111ffddc23680`
- `docs/metrics.yml` — SHA-256 `6ffe74f4f4f5d857891e41c53d5879f99081c579925d909f48fdb0f33ad87f7a`

## Additional check: who performed the Scenario Director review

**The project's declared provenance identifies the Scenario Director as human/user, not an evaluation agent.** Three repository statements align:

1. `backend/scripts/rule_alternatives_golden.yml` describes the corpus transition as an agent draft followed by a Scenario Director reviewed version.
2. `docs/teamprofile.md` assigns the Scenario Director role to a human team member and defines that role's content ownership.
3. `docs/model_evaluation.md` elsewhere explicitly refers to the Scenario Director as the user when recording a policy decision.

This is sufficient to describe the 22-item corpus as **human Scenario Director reviewed according to the project's own provenance**. It is not an independent audit trail: no separate signed review sheet, reviewer action record, or per-item approval artifact was found. Preserve that limit rather than claiming independently witnessed human review.

Suggested wording:

> The repository attributes the 22-item revision to the human Scenario Director: the golden file distinguishes the agent draft from the Scenario Director reviewed version, and project role documents identify the Scenario Director as a human/user. No separate signed per-item review record is retained.

Primary sources:

- `backend/scripts/rule_alternatives_golden.yml` — SHA-256 `97b8ab52ed853d05659cc082afd0d7d5c3c864e49ac663179705fc5afe060d61`
- `docs/teamprofile.md` — SHA-256 `d9b4b1760548267260752878b5f784db9a41272d474d50f6dc04776372023de5`
- `docs/model_evaluation.md` — SHA-256 `9705be5215bda36ed1e780ae26c9c369295fbdb5c96781ccf13cbb5e60b63f34`

## Additional check: Tester6 loops 3–5 submission content

**Independent content equality cannot be verified from retained artifacts.** The session record says the loop 3, 4, and 5 submissions were identical and reports a length of 266 characters for each. However, the record does not include the three submission strings or their hashes. Its directory contains only `tester6.md`; the session identifier appears nowhere else in the non-log application files; no linked JSON/export is named in the document; and repository history for that directory contains only the Markdown file. No new database query was performed.

Safe verification result:

```yaml
declared_same_text: true
observed_lengths: [266, 266, 266]
independently_verified: false
same_content: null
content_sha256:
  loop_3: unavailable
  loop_4: unavailable
  loop_5: unavailable
```

The declaration and independent verification must remain distinct. Equal length does not prove equal content, and no SHA-256 comparison can be reconstructed without the original strings. The graph should therefore not label loops 3–5 simply as “the same text” as an independently established fact.

Suggested graph wording:

> Loops 3–5: 266 characters each · content equality unverified

Suggested caution wording:

> The contemporaneous DB-review note describes loops 3–5 as the same submission, but the retained artifact preserves only equal lengths, not the texts or content hashes. Content equality is therefore unverified. The flat score must not be interpreted as learning or evaluator stability; monotonic-lock influence also cannot be tied to identical text independently from the retained evidence.

Primary source:

- `docs/review-verification/2026-09-16-tester6/tester6.md` — SHA-256 `5f863954fedb7029b65c9b7efc5128a9e34bf71a2d9bc73d63ceff04e5214840` (application commit `f92001a7c1bbfdb8e85038eb59aad9cbae32198c`)

## Ordinary-article follow-up evidence

- OA-42: the saved 2026-09-08 aggregate has 65 submitted attempts and two passes (2/65 = 3.1% rounded), recorded at 2026-09-08T05:05:41.686563+00:00. `docs/review-verification/2026-09-08/db-summary.json`, SHA-256 `bbf3e246668b0a1b1a807878643ce7a63826f92e708f0e123a2dde95ea16ee91`. Historical threshold and human/automatic composition remain unresolved.
- OA-53: the scoring code at public snapshot source commit `1568438` uses cause×0.35 + motive×0.35 + identity×0.30, rounded to one decimal, excluding side_effect. Subscores use confirmed=1, partial=0.5, none=0, threshold0.8 and a 100 cap. `scoring_rules.py` SHA-256 `210ed371ccd9603b268686194457178ed2c1b1437293e083150b17c80efe9dfc`, `game_constants.py` SHA-256 `07de7bf12e0c782ec6057535291084b165e0475babe0a5478443fc39194319af`. This does not prove the session's execution commit.
- OA-23: historical cost prose was checked against `docs/apiscenario.md`, SHA-256 `deaea2bc6338ef4003aa52ed652cd442c91036c8ca04304e0c0be9794da39e72`: character-to-token assumptions, separate input/output rates, exchange assumption and excluded calls are historic assumptions, not currently verified prices.

No new experiment, participant recruitment, paid model request or database query was performed for these corrections.
