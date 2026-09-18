#!/usr/bin/env python3
"""Audit built research pages, source preservation, local links and publication scope.

python3 scripts/check_site.py /tmp/research-redesign-site \
    --baseline /tmp/research-baseline-site
The optional baseline is a build from before a presentation-only change.
Use --anchor-baseline for content corrections that must keep historic links.
"""
import argparse
import collections
from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


class Node:
    def __init__(self, tag="root", attrs=()):
        self.tag, self.attrs, self.children = tag, dict(attrs), []

    def walk(self):
        yield self
        for child in self.children:
            if isinstance(child, Node):
                yield from child.walk()

    def text(self):
        return "".join(child.text() if isinstance(child, Node) else child for child in self.children)


class Document(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.root = Node()
        self.stack = [self.root]
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                self.stack = self.stack[:index]
                break

    def handle_data(self, text):
        self.stack[-1].children.append(text)


def normalized(text):
    return re.sub(r"\s+", " ", text).strip()


def page_path(url):
    return url.lstrip("/") + ("index.html" if url.endswith("/") else "")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site", type=Path)
    baselines = parser.add_mutually_exclusive_group()
    baselines.add_argument("--baseline", type=Path)
    baselines.add_argument("--anchor-baseline", type=Path)
    args = parser.parse_args()
    errors = []
    cache = {}

    def document(path):
        if path not in cache:
            cache[path] = Document(path.read_text()).root
        return cache[path]

    pages = []
    for source in [*ROOT.glob("*.md"), *ROOT.glob("experiments/*.md")]:
        match = re.search(r"^permalink:\s*(\S+)\s*$", source.read_text(), re.MULTILINE)
        if match:
            pages.append((source, page_path(match.group(1))))
    for source, relative in pages:
        path = args.site / relative
        if not path.is_file():
            errors.append(f"missing page: {relative}")
            continue
        tree = document(path)
        nodes = list(tree.walk())
        ids = collections.Counter(node.attrs["id"] for node in nodes if "id" in node.attrs)
        errors.extend(f"duplicate id: {relative} #{key}" for key, count in ids.items() if count > 1)
        originals = [node for node in nodes if "data-original-content" in node.attrs]
        if len(originals) != 1:
            errors.append(f"missing or duplicated original article: {relative}")
            continue
        baseline_links = set()
        baseline = args.baseline or args.anchor_baseline
        if baseline:
            old = document(baseline / relative)
            old_content = next(
                node for node in old.walk()
                if "data-original-content" in node.attrs
                or "content" in node.attrs.get("class", "").split()
            )
            if args.baseline and normalized(old_content.text()) != normalized(originals[0].text()):
                errors.append(f"original rendered text changed: {source.relative_to(ROOT)}")
            old_ids = {node.attrs["id"] for node in old_content.walk() if "id" in node.attrs}
            errors.extend(f"lost original anchor: {relative} #{key}" for key in old_ids - ids.keys())
            if args.baseline:
                baseline_links = {node.attrs["href"] for node in old.walk() if "href" in node.attrs}
        for node in nodes:
            if node.tag == "img" and not node.attrs.get("alt"):
                errors.append(f"image missing alt: {relative} {node.attrs.get('src')}")
            for attr in ("href", "src"):
                target = node.attrs.get(attr)
                if not target:
                    continue
                url = urlsplit(target)
                if url.scheme or url.netloc or target in baseline_links:
                    continue
                decoded_path = unquote(url.path)
                linked = args.site / decoded_path.lstrip("/") if decoded_path.startswith("/") else path.parent / decoded_path
                if not decoded_path:
                    linked = path
                elif decoded_path.endswith("/") or linked.is_dir():
                    linked = linked / "index.html"
                if not linked.is_file():
                    errors.append(f"missing local target: {relative} -> {target}")
                elif url.fragment and linked.suffix == ".html":
                    target_ids = {item.attrs.get("id") for item in document(linked).walk()}
                    if unquote(url.fragment) not in target_ids:
                        errors.append(f"missing anchor: {relative} -> {target}")
    for excluded in ("docs", "scripts", "tests", "artwork", "_private", ".superpowers"):
        if (args.site / excluded).exists():
            errors.append(f"internal material published: {excluded}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    preservation = "original text/anchors preserved" if args.baseline else (
        "historic anchors preserved" if args.anchor_baseline else "original records present"
    )
    print(f"PASS {len(pages)} pages: {preservation}, local links, alt text, publication scope")
    return subprocess.run([sys.executable, str(ROOT / "scripts/refresh_research_data.py"), "--check"], cwd=ROOT).returncode


if __name__ == "__main__":
    sys.exit(main())
