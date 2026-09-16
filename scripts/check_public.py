#!/usr/bin/env python3
"""공개 범위 금지어 검사 — 사이트 소스에 스포일러·운영 세부가 남았는지 확인한다.

  python3 scripts/check_public.py        # 걸리면 종료 코드 1

금지어 목록은 _private/public-rules.json(비공개)에 있다. pre-commit 훅으로도 쓴다.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RULES = ROOT / "_private" / "public-rules.json"
SKIP_DIRS = {"_site", "_private", ".git", ".jekyll-cache", "vendor", ".bundle", "node_modules"}
EXTS = {".md", ".html", ".yml", ".yaml", ".scss", ".js", ".py", ".txt"}


def main() -> int:
    if not RULES.exists():
        print(f"공개 범위 규칙 파일이 없다: {RULES}", file=sys.stderr)
        return 1
    pattern = re.compile("|".join(json.loads(RULES.read_text())["forbidden"]))

    hits = 0
    for path in sorted(ROOT.rglob("*")):
        rel = path.relative_to(ROOT)
        if not path.is_file() or path.suffix not in EXTS or SKIP_DIRS & set(rel.parts):
            continue
        for n, line in enumerate(path.read_text(errors="ignore").split("\n"), 1):
            m = pattern.search(line)
            if m:
                hits += 1
                print(f"{rel}:{n}: [{m.group(0)}] {line.strip()[:120]}")

    if hits:
        print(f"\n공개 금지어 {hits}건 — 고친 뒤 다시 검사한다.", file=sys.stderr)
        return 1
    print("공개 금지어 0건")
    return 0


if __name__ == "__main__":
    sys.exit(main())
