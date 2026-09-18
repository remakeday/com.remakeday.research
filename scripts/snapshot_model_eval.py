#!/usr/bin/env python3
"""Exp 1 스냅샷 — 앱 저장소 정본 model_evaluation.md를 공개용으로 가공해 싣는다.

  python3 scripts/snapshot_model_eval.py [--ref main] [--app ../com.remakeday]

처리 순서
  1. 정본을 git ref에서 읽는다(작업 트리의 미커밋 변경을 섞지 않는다).
  2. 첫 H1 제목을 버리고, 첫 번째 `# ` 절부터 제목 단계를 한 칸씩 내린다
     (사이트 페이지 제목이 H1이므로).
  3. 앱 저장소 문서로 가는 링크는 걸지 않고 경로만 남긴다.
  4. 공개 범위 규칙(_private/public-rules.json, 비공개)의 절 제외·치환·줄 삭제를 적용한다.
  5. front matter·안내 상자(HEAD)를 붙이고 스냅샷 기준 커밋을 적는다.

마지막에 scripts/check_public.py로 금지어 검사를 돌린다.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "experiments" / "model-selection.md"
RULES = ROOT / "_private" / "public-rules.json"
SRC_PATH = "docs/model_evaluation.md"

HEAD = """---
title: "Exp 1 — Model Selection (E7 · E6 · 외부 API)"
permalink: /experiments/model-selection/
eyebrow: "System Evaluation · 실측과 채택 기록"
status: "역할별 실측 · 일부 근거 확인 중"
description: Core·NPC·임베딩 모델의 역할별 측정과 채택 근거를 기록합니다. 통과한 기준, 예외를 둔 결정, 미측정 항목을 구분한 공개용 스냅샷입니다.
---

<div class="callout">
  <div class="callout__title">이 문서의 위치</div>
  <p>정본은 앱 저장소 <code>com.remakeday/docs/model_evaluation.md</code>이고,
  이 페이지는 <strong>공개용으로 가공한 스냅샷</strong>입니다. 공개한 절의 수치·판정·결정은 아래 기준 커밋의 정본을 따릅니다.
  시나리오 결말을 드러내는 문장과 운영 세부(설정 키·포트·로그인 경로 등)는 가리거나 뺐고,
  공개 검토 전인 후속 추록은 포함하지 않았습니다. 앱 저장소 문서는 링크 대신 경로로 적었습니다.<br>
  <strong>스냅샷 기준:</strong> 앱 저장소 <code>{ref}</code> <code>{commit}</code></p>
</div>
"""


def git(app: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(app), *args], capture_output=True, text=True, check=True
    ).stdout


def shift_headings(lines: list[str]) -> list[str]:
    out, shifted, fence = [], False, False
    for line in lines:
        if line.startswith("```"):
            fence = not fence
        if not fence and re.match(r"^#{1,5} ", line):
            if line.startswith("# "):
                shifted = True
            if shifted:
                line = "#" + line
        out.append(line)
    return out


def unlink(body: str) -> str:
    """[텍스트](앱 저장소 문서) → 텍스트(`경로`). 외부 URL 링크는 그대로 둔다."""
    app_blob = r"https://github\.com/remakeday/com\.remakeday/blob/[^/]+/"

    def repl(m: re.Match) -> str:
        text, target = m.group(1), m.group(2)
        if re.match(app_blob, target):
            path = re.sub(app_blob, "", target)
        elif target.startswith("../"):
            path = target[3:]
        elif not re.match(r"(https?:|#|/)", target):
            path = "docs/" + target
        else:
            return m.group(0)
        return f"{text}(`{path}`)"

    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", repl, body)


def apply_rules(body: str, rules: dict) -> str:
    section_prefixes = set(rules.get("drop_section_prefixes", []))
    matched = set()
    kept, skipped_level, fence = [], None, None
    for line in body.split("\n"):
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
        heading = re.match(r"^(#{1,6})\s+", line) if fence is None else None
        if heading:
            level = len(heading.group(1))
            if skipped_level is not None and level <= skipped_level:
                skipped_level = None
            exclusions = {p for p in section_prefixes if line.startswith(p)}
            if exclusions:
                matched.update(exclusions)
                skipped_level = level if skipped_level is None else min(level, skipped_level)
        if skipped_level is None and not any(line.startswith(p) for p in rules["drop_line_prefixes"]):
            kept.append(line)
    if section_prefixes - matched:
        raise ValueError("section exclusion did not match; review public scope before generating")
    body = "\n".join(kept)
    for old, new in rules["replace"]:
        body = body.replace(old, new)
    return body


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", default="main")
    ap.add_argument("--app", default=str(ROOT.parent / "com.remakeday"))
    args = ap.parse_args()

    if not RULES.exists():
        print(f"공개 범위 규칙 파일이 없다: {RULES}", file=sys.stderr)
        return 1
    rules = json.loads(RULES.read_text())
    app = Path(args.app)

    src = git(app, "show", f"{args.ref}:{SRC_PATH}")
    commit = git(app, "rev-parse", "--short", args.ref).strip()

    body = "\n".join(shift_headings(src.split("\n")[1:])).lstrip("\n")
    try:
        body = apply_rules(unlink(body), rules)
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 1

    PAGE.write_text(HEAD.format(ref=args.ref, commit=commit) + "\n" + body)
    print(f"스냅샷 갱신: {PAGE.relative_to(ROOT)} ← {args.ref} {commit}")

    public_check = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_public.py")]
    ).returncode
    if public_check:
        return public_check
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "refresh_research_data.py")]
    ).returncode


if __name__ == "__main__":
    sys.exit(main())
