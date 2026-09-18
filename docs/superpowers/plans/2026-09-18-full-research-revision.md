# 리서치 전수 검토 반영 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development. Complete each scoped task and preserve its disposition ledger.

**Goal:** Apply every one of the 182 review findings to the research Jekyll, keeping the underlying evidence, historical decisions, and fixed preregistration intact.

**Architecture:** Edit the ordinary research articles directly. Edit Exp 1 in an isolated app documentation worktree and regenerate the public snapshot with the existing filter. Update the reading layer, navigation and figure extraction together; distinguish uncertain evidence from measured results.

**Tech Stack:** Markdown, Jekyll/Liquid, YAML, Python figure extraction, HTML/CSS/vanilla JS, existing headless Chrome checks.

**Spec:** `docs/reviews/full-audit/README.md`, the 182 records in the four `*-findings.json` files, and the user's approval to apply them to the research Jekyll using subagents.

## Global Constraints

- Work in `/tmp/research-full-revision-20260918`; app documentation source is `/tmp/remakeday-research-source-20260918/docs/model_evaluation.md`.
- Research baseline is `ff6afd0b3d0625b443cabbf5a2e9be34f9ac1037`; app worktree base is `f92001a7c1bbfdb8e85038eb59aad9cbae32198c`.
- Preserve facts, dates, model names, quoted participant speech, raw tables and existing section anchors unless an identified correction has supporting evidence. Correct prose in place rather than merely appending a generic caveat to contradictory prose.
- Keep `prereg.md` byte-for-byte unchanged. Explain missing operational definitions and version history outside its frozen content. Do not invent recruitment, exclusion, stopping, or analysis rules.
- Do not invent numerical corrections or portray unresolved raw questions as verified. Narrow the claim and identify the specific remaining evidence.
- Do not copy private prompts, responses, scenario answers, credentials, infrastructure details or `_private` rules into public files. Run the public checker.
- Do not change app runtime code or touch the user's dirty app worktree. App scope is evaluation documentation only.
- Every finding gets exactly one disposition `{id,status,files,summary,evidence_remaining}` in a task-specific JSON. Status is `corrected`, `clarified`, `qualified`, or `preserved_with_rationale`. A status does not mean missing raw evidence was obtained.
- No new external dependencies. Keep quantitative graphics in HTML/SVG; preserve the existing Blender concept image.
- No subagents from workers. Controller owns review and integration. Workers do not commit; the controller commits coherent verified changes after inspecting the diff.

### Task 1: Ordinary articles and fixed-protocol reading notes

**Files:** `index.md`, `statement.md`, `testbed.md`, `plain-summary.md`, `limitations.md`, `lab-notes.md`, `experiments/human-observations.md`; create `_includes/research/prereg-notes.html` and `docs/revisions/2026-09-18/other-articles-dispositions.json`.

**Consumes:** all 59 `OA-*` findings in `docs/reviews/full-audit/other-articles-findings.json`; exact original evidence in manifest and raw-evidence files.
**Produces:** corrected and readable original articles; a Liquid-free semantic HTML explanation include for the frozen protocol; dispositions for OA-01 through OA-59.

- [ ] Read the eight articles and all OA findings; retain the fixed protocol without changing it.
- [ ] Correct source contradictions, denominators and times; give each percentage its event/session denominator. Keep mixed-version six-session aggregate separate from the later case and distinguish free-text explanation from custom-rule selection.
- [ ] Make current model decisions dated and role-specific; keep documented old choices as dated history. State gate exceptions and unmeasured axes explicitly.
- [ ] Scope generic claims about human identity/CV, learning, reproducibility, causal effects, model behavior and cost to the available evidence. Add the two already verified primary literature citations where the field-wide absence claim is replaced.
- [ ] Add prereg-notes explaining what is fixed, what is not yet executed, the role of system controls versus future human A/B, exact missing operational definitions, and the rule for a dated future amendment. Do not fill missing research decisions with guesses.
- [ ] Preserve anchors when improving headings (explicit old ID aliases if necessary); avoid broad formatting churn.
- [ ] Record all 59 dispositions and unresolved evidence, read the diff, run `python3 scripts/check_public.py`. Figure extraction may wait until integration if prose changes its grammar; identify exact affected sections.

### Task 2: Model evaluation source correction

**Files:** app worktree `docs/model_evaluation.md` only; research `docs/revisions/2026-09-18/model-dispositions.json` and a report.

**Consumes:** all 46 `MF-*` and 68 `MD-*` findings, original manifest and raw-evidence records. Source app has an additional A.22 after the audited snapshot; preserve and review that section's interpretation when integrating, without copying private contents into reports.
**Produces:** corrected app source, 114 finding dispositions, summary of any A.22 qualification required, and exact corrected data rows for the controller's snapshot regeneration.

- [ ] Re-read the relevant source and each finding; implement the correction where the problem occurs.
- [ ] Put latest documented role-specific choices and the evidence boundary first. Preserve all dated intermediate decisions and original technical detail.
- [ ] Correct confirmed table arithmetic and omitted ties; attach role/stage/run to latency values. If the external comparison's intended baseline run is unknown, show the known advisor/evaluator values separately and identify the comparison gap rather than choosing an unexplained replacement.
- [ ] Separate planned and executed cases, calls, repeats, provider attempts, generated statements and judge comparisons. Explicitly separate raw timing, pacing-derived estimates, device memory and model residency.
- [ ] Narrow noninferiority, causal, deterministic, model-family, cost-upper-bound, concurrency, licensing and API quota claims to what was actually observed. Preserve practical adoption reasons and identify gate exceptions.
- [ ] Keep reviewed 22-item embedding data separate from the original 30-item repetitions; distinguish hit rate from ranking agreement and supported dimensions from measured dimensions.
- [ ] Handle QA nuances: MD-39 includes two gemma runs; MD-46 already includes estimated stopped-run costs; MD-60 must not merge 22/30 dimension comparisons.
- [ ] Apply local wording edits without changing direct quotes or standard terminology. Make citations and private artifacts' accessibility explicit.
- [ ] Record all 114 dispositions and remaining evidence, inspect the document diff, report exact old anchors or table formats changed. Do not edit the generated research snapshot or app code.

### Task 3: Reader summaries, graphics, and navigation

**Files:** `_data/reading.yml`, `_includes/research/*.html`, `_includes/research/figures/*.html`, `_layouts/page.html`, `_includes/sidebar.html`, `_config.yml`, `assets/css/style.scss`, `assets/js/app.js`; disposition `presentation-dispositions.json`.

**Consumes:** PR-01 through PR-09 and Task 1's `_includes/research/prereg-notes.html`. Current configuration is the documented decision, not a deployment assertion.
**Produces:** all nine PR dispositions, reachable protocol notes, model decision summary and four clear reading routes.

- [ ] Show a dated Core/NPC/embedding decision table with purpose, evidence link and exceptions before the long model record.
- [ ] Explain runner, co-residency and reviewer role without inventing whether an unidentified reviewer was a human or agent. Define the rule-selection types and keep acceptance distinct from trust.
- [ ] Label the trajectory as game total score; describe conditional monotonic locking accurately. Keep 0ms as the published rounded baseline and explain 0.1ms rounding rather than no measurement.
- [ ] Use distinct summary-figure numbering without breaking old original anchors. Translate rationale absent/present screen labels while preserving protocol variables.
- [ ] Provide Current decision / Method / Evidence / Dated history navigation on Exp 1, keep all original detailed content and hash links available. Use static links where possible instead of new JS behavior.
- [ ] Include the protocol notes only on `/prereg/`. Do not expose review IDs, internal correction workflow or JSON to site readers.
- [ ] Read the diff and record nine dispositions. No mirror tests for wording; integration uses the existing accessibility, anchor, figure and browser checks.

### Task 4: Source regeneration, full verification and publication

**Owner:** controller, with a final independent review.
**Files:** snapshot generator metadata if necessary; figure extraction and its focused tests if source grammar changes; generated `_data/research_figures.json`, `experiments/model-selection.md`; revision ledger/docs.

- [ ] Inspect each task diff against the 182 finding IDs. Ask targeted re-review for consequential research corrections and reader navigation.
- [ ] Commit the isolated app documentation change, regenerate the public snapshot from that exact commit and inspect the A.22 addition under the public filter. Preserve historical source anchors with aliases where required.
- [ ] Update snapshot metadata to describe role-specific evidence and exceptions accurately. Refresh figure data; if extraction behavior changes, first add a meaningful regression test and observe its expected failure, then make the minimal parser change.
- [ ] Validate 182 unique dispositions, no omitted IDs, fixed prereg hash, factual correction provenance, preserved headings/tables/quotes and public scope.
- [ ] Run `python3 -m unittest discover -s tests -p 'test_*.py'`, `python3 scripts/refresh_research_data.py --check`, `python3 scripts/check_public.py`, `bundle exec jekyll build --destination /tmp/research-revision-site`, `python3 scripts/check_site.py /tmp/research-revision-site` and existing headless browser checks.
- [ ] Have an independent reviewer inspect the full final diff and task reports. Address material findings and recheck only affected checks.
- [ ] Integrate the verified research change into the user's checkout without losing review artifacts or app work-in-progress. Continue the already authorized commit/push workflow and verify the live research pages after deployment; clearly report any external deployment limitation.
