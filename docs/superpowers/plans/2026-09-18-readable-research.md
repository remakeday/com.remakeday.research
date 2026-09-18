# Readable Research Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement the approved accessible paper-style Jekyll redesign with original content preserved and real Blender and data figures.

**Architecture:** Page layouts consume `_data/reading.yml` and `_includes/research/` to add a reading layer without editing articles. Quantitative figures use public source data with validation. A small progressive-enhancement script adds outline navigation, disclosures, glossary lookup, and mobile navigation.

**Tech Stack:** Jekyll/Liquid, SCSS, vanilla JavaScript, Python standard library, Blender, Chrome DevTools Protocol for browser verification.

**Spec:** `docs/superpowers/specs/2026-09-18-readable-research-design.md`

## Global Constraints

- Preserve all original article Markdown and existing URL/heading anchors.
- Assume no AI/statistics background; retain paper structure and nearby caveats.
- No runtime framework or chart dependency; no invented measurements.
- Do not edit preregistration, private data, or external development repository.
- Work within the supplied clean workspace; leave changes reviewable without publishing.
- Exclude plans, tooling and Blender source from the published site.

## Task 1: Blender instrument illustration

Files: `scripts/render_research_figure.py`, `assets/images/research-instrument.webp`, optional compact poster PNG, `docs/research-figures.md`.

Produces: a 1600px-wide landscape, orthographic clay-like game/AI/choice/record scene with warm neutral and sage palette, no rendered words or numerical claims. Four recognizable groups arranged left-to-right; subtle shadows and spacious composition. White/off-white world so it integrates with the paper UI. WebP below 450KB, reproducible Blender command. Source `.blend` may live under excluded `artwork/` if useful.

- [x] Author scene generation script and render using installed Blender.
- [x] Inspect image, correct composition, export optimized web asset.
- [x] Record command and conceptual nature, review image and asset weight.

## Task 2: Reading content and data figures

Files: `_data/reading.yml`, `_includes/research/overview.html`, `_includes/research/figures/*.html`, `scripts/check_research_data.py`, `tests/test_research_data.py`.

Consumes: existing articles; produces `site.data.reading[page.url]` with `section`, `label`, `question`, `summary`, `caution`, `figure`, optional `terms`. Overview include consumes this record and emits semantic content inside `.reading-overview`; original article rendering belongs to root layout task.

- [x] Define metadata for all nine existing pages, using plain Korean and accurate evidence status.
- [x] Add accessible system loop, model selection stages, rule-selection tiles, Tester 6 trajectory and A/B design. All figures have captions and source links; source table remains in original article.
- [x] Write failing behavior tests for source drift detection, unmeasured values, separate groups, denominator mismatch.
- [x] Implement source-derived/checked data and validation; ensure snapshot updates cannot silently publish stale figures.
- [x] Review evidence and source correspondence.

## Task 3: Layout, typography and reading interactions

Files: `_layouts/default.html`, `_layouts/page.html`, `_includes/head.html`, `_includes/sidebar.html`, `_includes/footer.html`, `_includes/research/home.html`, `_data/nav.yml`, `assets/css/style.scss`, `assets/js/app.js`, `_config.yml`.

Consumes: metadata and figures from Task 2; illustration from Task 1. Produces semantic main/article, persistent original rendered content, keyboard-operable navigation, glossary and outline.

- [x] Create warm paper design tokens and responsive layout, 17–18px body text, restrained sage accents and visible keyboard focus.
- [x] Add homepage abstract, instrument figure, linked contribution and evidence sections. Preserve original in a native source disclosure.
- [x] Add page introductions and static source records, persistent desktop outline and mobile section selector; all original IDs retained.
- [x] Add mobile navigation with ARIA state, Escape dismissal and focus return; source reveal on hash navigation; local glossary with visible definitions; no-JS fallbacks.
- [x] Exclude internal docs, scripts, tests, and artwork from published output. Update developer instructions for rebuild/check commands.

## Task 4: Integrated verification and review

Files: `scripts/check_site.py`, browser checks under `tests/`, `README.md`.

- [x] `bundle exec jekyll build --destination /tmp/research-redesign-site` succeeds.
- [x] `python3 scripts/check_public.py` reports no forbidden content.
- [x] Check article preservation against git baseline, original rendered text and IDs against `/tmp/research-baseline-site`, new internal links and assets, generated data consistency.
- [x] Use real Chrome at 1440px and 390px to verify home and both experiment pages, source anchors, glossary, mobile menu, keyboard, no page overflow and no console errors. Capture screenshots and inspect.
- [x] Request independent code/content review, fix meaningful findings and repeat only affected checks.
- [x] Summarize changes, validation and remaining publication step for user.

## Completion evidence (2026-09-18)

- Jekyll build succeeded in `/tmp/research-redesign-site`.
- All nine original article Markdown files remain unchanged. Built original text and heading anchors match `/tmp/research-baseline-site`; local links, image alternatives and publication exclusions pass.
- Public-content checker reports zero forbidden strings; generated figure data matches public sources.
- Ten Python tests pass, including changed-source rendering and incompatible measurement-header rejection.
- Thirty-four real Chrome checks pass at 320, 390, 768 and 1440px, including mobile navigation, source links, glossary, exact accessible values, no-JS reading, print and runtime errors.
- Screenshots in `/tmp/research-ui-shots/` were visually inspected. Flow connectors were corrected to a vertical sequence after the final visual review.
- Independent review is complete with no outstanding findings. Fixed no-JS mobile obstruction, secondary-text contrast, measurement-header interpretation and navigation timing.
- Blender illustration and editable scene are included, with regeneration instructions in `docs/research-figures.md`.
- Changes were completed and reviewed locally before the user requested commit and push.
