#!/usr/bin/env python3
"""Derive public figure data from the immutable research Markdown.

The checked-in JSON is the only numeric input used by the figure includes. Run
without arguments to refresh it, or with --check to fail when the public source
and checked artifact no longer agree.
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "_data" / "research_figures.json"
SOURCE_PATHS = (
    "testbed.md",
    "prereg.md",
    "experiments/model-selection.md",
    "experiments/human-observations.md",
)


class SourceError(ValueError):
    """The public record no longer has the shape required by a figure."""


def read_source(root: Path, relative_path: str) -> str:
    path = root / relative_path
    if not path.exists():
        raise SourceError(f"missing public source: {relative_path}")
    return path.read_text(encoding="utf-8")


def require(pattern: str, text: str, description: str, flags: int = 0) -> re.Match[str]:
    match = re.search(pattern, text, flags)
    if not match:
        raise SourceError(f"public source changed: could not derive {description}")
    return match


def section(text: str, start: str, end: str | None = None) -> str:
    start_match = require(start, text, "section start", re.MULTILINE)
    remainder = text[start_match.end() :]
    if end is None:
        return remainder
    end_match = re.search(end, remainder, re.MULTILINE)
    return remainder[: end_match.start()] if end_match else remainder


def source_entry(root: Path, relative_path: str) -> dict[str, str]:
    raw = (root / relative_path).read_bytes()
    return {"path": relative_path, "sha256": hashlib.sha256(raw).hexdigest()}


def parse_human_observations(text: str) -> dict[str, Any]:
    aggregate_date = require(
        r"^## 세션 분리 — DB 전수 판별 \((\d{4}-\d{2}-\d{2})\)$",
        text,
        "six-session aggregation date",
        re.MULTILINE,
    ).group(1)
    aggregate_text = section(
        text,
        r"^## 집계 결과 \(확정 \+ 유력 6판, exploratory\)$",
        r"^## 케이스 기록",
    )
    ai_match = require(
        r"AI 계열 규칙 선택 \| \*\*(\d+)/(\d+) \(70%\)\*\*: 원숭이손 수락 (\d+) \+ AI 추천 옵션 선택 (\d+)",
        aggregate_text,
        "six-session rule-selection counts",
    )
    custom_match = require(
        r"직접 작성 규칙 \| \*\*(\d+)/(\d+) \(30%\)\*\*",
        aggregate_text,
        "six-session custom-rule count",
    )
    mixed_instruments = "기구 버전 혼재 주의" in aggregate_text
    if not mixed_instruments:
        raise SourceError("public source changed: mixed-instrument caveat is missing")

    ai_total, ai_denominator, intervention, recommendation = map(int, ai_match.groups())
    custom, custom_denominator = map(int, custom_match.groups())
    if ai_total != intervention + recommendation:
        raise SourceError("source denominator mismatch: AI total differs from its two sources")
    if ai_denominator != custom_denominator:
        raise SourceError("source denominator mismatch: aggregate rows use different totals")

    tester_heading = require(
        r"^### Case — Tester 6 \((\d{4}-\d{2}-\d{2})\) · 5회차 완주$",
        text,
        "Tester 6 measurement date",
        re.MULTILINE,
    )
    tester_date = tester_heading.group(1)
    tester_text = section(
        text,
        r"^### Case — Tester 6 \(\d{4}-\d{2}-\d{2}\) · 5회차 완주$",
        r"^### Tester 7",
    )
    trajectory: list[dict[str, float | int]] = []
    for round_number, score in re.findall(
        r"^\| ([1-5]) \| ([0-9.]+) \|", tester_text, re.MULTILINE
    ):
        trajectory.append({"round": int(round_number), "score": float(score)})
    if [item["round"] for item in trajectory] != [1, 2, 3, 4, 5]:
        raise SourceError("public source changed: Tester 6 trajectory must contain rounds 1–5")

    tester_rules = require(
        r"이 판에서는 AI 계열 (\d+)/(\d+), 직접 작성 (\d+)/(\d+)다",
        tester_text,
        "Tester 6 rule-selection counts",
    )
    tester_ai, tester_denominator, tester_custom, tester_custom_denominator = map(
        int, tester_rules.groups()
    )
    if tester_denominator != tester_custom_denominator:
        raise SourceError("source denominator mismatch: Tester 6 rows use different totals")
    same_text = require(
        r"(\d+)~(\d+)회차 제출문은 같은 (\d+)자였고",
        tester_text,
        "Tester 6 repeated-submission caveat",
    )
    same_text_start, same_text_end, same_text_length = map(int, same_text.groups())
    if "단조 잠금" not in tester_text:
        raise SourceError("public source changed: Tester 6 scoring caveat is missing")

    return {
        "source_path": "experiments/human-observations.md",
        "aggregate": {
            "group": "six-session-aggregate",
            "measured_on": aggregate_date,
            "sessions": 6,
            "denominator": ai_denominator,
            "ai_total": ai_total,
            "instrument_versions": "mixed",
            "selections": [
                {"id": "intervention", "label": "AI 개입 수락", "count": intervention},
                {"id": "recommendation", "label": "AI 추천 선택", "count": recommendation},
                {"id": "custom", "label": "직접 작성", "count": custom},
            ],
            "source_anchor": "집계-결과-확정--유력-6판-exploratory",
        },
        "tester6": {
            "group": "separate-case",
            "measured_on": tester_date,
            "session_id": "2338ec9f",
            "denominator": tester_denominator,
            "ai_selections": tester_ai,
            "custom_selections": tester_custom,
            "trajectory": trajectory,
            "same_text_rounds": list(range(same_text_start, same_text_end + 1)),
            "same_text_length": same_text_length,
            "monotonic_scoring_lock": True,
            "source_anchor": "case--tester-6-2026-09-16--5회차-완주",
        },
    }


def parse_embedding(text: str) -> dict[str, Any]:
    measurement_date = require(
        r"^### A\.21 (\d{4}-\d{2}-\d{2}) · 임베딩 부활",
        text,
        "embedding evaluation date",
        re.MULTILINE,
    ).group(1)
    reviewed = section(
        text,
        r"^#### 6\. 정본 수치 — Scenario Director 검수 골든\(22문장\)",
        r"^#### 7\.",
    )
    preliminary_repetitions = int(
        require(
            r"\*\*반복 n=(\d+)\(1차 골든, 조용한 GPU\)",
            reviewed,
            "preliminary embedding repetition count",
        ).group(1)
    )
    require(
        r"^#### 1\. 셀 결과 \(n=30, 각 1회,",
        text,
        "preliminary 30-item embedding set",
        re.MULTILINE,
    )
    expected_header = ["셀", "dims", "top-1", "top-3", "p50 ms", "top-1 오답"]
    header_cells = None
    for line in reviewed.splitlines():
        if line.startswith("| 셀 |"):
            header_cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            break
    if header_cells != expected_header:
        raise SourceError(
            "public source changed: reviewed embedding table header must remain "
            + " | ".join(expected_header)
        )
    rows = []
    for line in reviewed.splitlines():
        if not line.startswith("|") or "---" in line:
            continue
        cells = [cell.strip().replace("**", "") for cell in line.strip().strip("|").split("|")]
        if len(cells) != 6 or cells[0] == "셀":
            continue
        try:
            top1 = float(cells[2])
            latency = float(cells[4].replace(",", ""))
        except ValueError:
            continue
        label = cells[0].replace("`", "")
        dims = cells[1].replace("`", "")
        if label.startswith("stem"):
            condition_id = "stem"
            short_label = "어간 겹침"
        elif "qwen3" in label:
            condition_id = f"qwen-{dims}"
            short_label = "Qwen"
        elif "bge-m3" in label:
            condition_id = "bge-1024"
            short_label = "bge-m3"
        elif "gemini" in label:
            condition_id = f"gemini-{dims}"
            short_label = "Gemini"
        else:
            continue
        rows.append(
            {
                "id": condition_id,
                "label": short_label,
                "dimensions": None if dims == "—" else int(dims),
                "top1_correct": round(top1 * 22),
                "top1_rate": top1,
                "latency_p50_ms": latency,
            }
        )
    expected_ids = [
        "stem",
        "qwen-2560",
        "qwen-1536",
        "bge-1024",
        "gemini-1536",
        "gemini-2560",
    ]
    if [row["id"] for row in rows] != expected_ids:
        raise SourceError("public source changed: reviewed 22-item embedding table is incomplete")
    return {
        "source_path": "experiments/model-selection.md",
        "source_anchor": "6-정본-수치--scenario-director-검수-골든22문장--반복-n3--서버-실경로--vram-동주",
        "source_section": "A.21 §6",
        "measured_on": measurement_date,
        "reviewed_items": 22,
        "repeat_check": {
            "items": 30,
            "review_status": "unreviewed",
            "repetitions": preliminary_repetitions,
            "applies_to_reviewed_table": False,
        },
        "conditions": rows,
        "latency_context": "후보 문구를 미리 준비한 뒤, 대안 순서를 한 번 계산하는 시간",
    }


def build_dataset(root: Path = ROOT) -> dict[str, Any]:
    sources = {path: read_source(root, path) for path in SOURCE_PATHS}
    testbed = sources["testbed.md"]
    prereg = sources["prereg.md"]
    model = sources["experiments/model-selection.md"]

    for phrase in ("Human Player", "AI Advisor", "Accept / Reject / Write", "Re-execute"):
        if phrase not in testbed:
            raise SourceError(f"public source changed: system loop lacks {phrase!r}")
    for stage in range(5):
        require(rf"\| \*\*{stage}\*\* `[^`]+`", model, f"model-selection Stage {stage}")
    if "A = absent" not in prereg or "B = present" not in prereg:
        raise SourceError("public source changed: preregistered A/B conditions are missing")
    if "미실행(NOT RUN)" not in prereg:
        raise SourceError("public source changed: preregistration is no longer marked NOT RUN")

    return {
        "schema_version": 1,
        "sources": [source_entry(root, path) for path in SOURCE_PATHS],
        "system_loop": {
            "source_path": "testbed.md",
            "source_anchor": "figure-1--system-loop",
            "steps": [
                "관찰·대화·추론",
                "실패 설명",
                "AI 조언",
                "수용·거부·직접 작성",
                "규칙 적용",
                "재실행",
            ],
        },
        "model_selection": {
            "source_path": "experiments/model-selection.md",
            "stages": [
                {"number": 0, "id": "protocol", "label": "응답 형식 확인"},
                {"number": 1, "id": "smoke", "label": "기본 동작 확인"},
                {"number": 2, "id": "formal", "label": "역할별 정식 평가"},
                {"number": 3, "id": "concurrency", "label": "메모리에 함께 올리기"},
                {"number": 4, "id": "loop", "label": "실제 게임 실행"},
            ],
            "stages_source_anchor": "41-funnel",
            "embedding": parse_embedding(model),
        },
        "human_observations": parse_human_observations(
            sources["experiments/human-observations.md"]
        ),
        "preregistration": {
            "status": "NOT RUN",
            "conditions": [
                {"id": "A", "rationale": "absent", "label": "AI 제안만"},
                {"id": "B", "rationale": "present", "label": "AI 제안 + 이유"},
            ],
            "primary_outcome": "AI 제안 수용률",
            "source_path": "prereg.md",
            "source_anchor": "anchor-experiment-설계",
        },
    }


def validate_dataset(
    data: dict[str, Any], root: Path = ROOT, expected: dict[str, Any] | None = None
) -> list[str]:
    errors: list[str] = []
    source_entries = {entry.get("path"): entry.get("sha256") for entry in data.get("sources", [])}
    for path in SOURCE_PATHS:
        actual = source_entry(root, path)["sha256"]
        if source_entries.get(path) != actual:
            errors.append(f"source drift: {path} hash does not match the public record")

    aggregate = data.get("human_observations", {}).get("aggregate", {})
    if aggregate.get("group") != "six-session-aggregate":
        errors.append("six-session observations must remain in their own aggregate group")
    selections = aggregate.get("selections", [])
    count_sum = sum(item.get("count", 0) for item in selections)
    denominator = aggregate.get("denominator")
    if denominator != 20 or count_sum != denominator:
        errors.append(
            f"denominator mismatch: six-session selections sum to {count_sum}, denominator is {denominator}"
        )

    tester6 = data.get("human_observations", {}).get("tester6", {})
    if tester6.get("group") != "separate-case":
        errors.append("Tester 6 must remain a separate case, outside the six-session aggregate")
    if tester6.get("ai_selections", 0) + tester6.get("custom_selections", 0) != tester6.get(
        "denominator"
    ):
        errors.append("denominator mismatch: Tester 6 rule-selection counts do not sum to five")

    prereg = data.get("preregistration", {})
    allowed_prereg_keys = {
        "status",
        "conditions",
        "primary_outcome",
        "source_path",
        "source_anchor",
    }
    if prereg.get("status") != "NOT RUN" or set(prereg).difference(allowed_prereg_keys):
        errors.append("NOT RUN preregistration must not contain measured result values")

    embedding = data.get("model_selection", {}).get("embedding", {})
    reviewed_items = embedding.get("reviewed_items")
    if reviewed_items != 22:
        errors.append("embedding figure must use the reviewed 22-item source")
    for condition in embedding.get("conditions", []):
        correct = condition.get("top1_correct")
        if not isinstance(correct, int) or correct < 0 or correct > 22:
            errors.append(f"invalid measured top-1 count for {condition.get('id')}")

    if expected is not None and data != expected and not errors:
        errors.append("generated data drift: checked artifact differs from current public sources")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="verify without writing")
    args = parser.parse_args()
    try:
        expected = build_dataset(ROOT)
    except SourceError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    errors = validate_dataset(expected, ROOT)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    serialized = json.dumps(expected, ensure_ascii=False, indent=2) + "\n"
    if args.check:
        if not OUTPUT.exists():
            print(f"generated data missing: {OUTPUT.relative_to(ROOT)}", file=sys.stderr)
            return 1
        if OUTPUT.read_text(encoding="utf-8") != serialized:
            print(
                "generated data drift: run python3 scripts/refresh_research_data.py",
                file=sys.stderr,
            )
            return 1
        print("research figure data: current")
        return 0

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(serialized, encoding="utf-8")
    print(f"research figure data refreshed: {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
