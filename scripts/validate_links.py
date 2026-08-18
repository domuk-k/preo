"""Validate local Markdown links without making network requests."""

from __future__ import annotations

from collections.abc import Iterator
from markdown_it import MarkdownIt
from pathlib import Path
import sys
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN = MarkdownIt("commonmark")
IGNORED_PREFIXES = ("http://", "https://", "mailto:", "//", "#")
IGNORED_PARTS = frozenset(
    {
        ".git",
        ".venv",
        ".pytest_cache",
        ".superpowers",
        "__pycache__",
        ".mypy_cache",
        ".ruff_cache",
        ".tox",
        ".nox",
        "node_modules",
        "build",
        "dist",
        "coverage",
        "htmlcov",
    }
)


def project_markdown_files(root: Path = ROOT) -> list[Path]:
    """Return project Markdown files, excluding generated and local-only trees."""
    return sorted(
        path
        for path in root.rglob("*.md")
        if not IGNORED_PARTS.intersection(path.relative_to(root).parts)
    )


def is_ignored_target(raw_target: str) -> bool:
    normalized_target = raw_target.strip().strip("<>").lower()
    return normalized_target.startswith(IGNORED_PREFIXES)


def target_path(raw_target: str) -> str:
    """Extract the decoded local path portion of a Markdown target."""
    return unquote(raw_target.strip().strip("<>").split("#", 1)[0])


def is_within_root(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root.resolve())
    except ValueError:
        return False
    return True


def markdown_targets(text: str) -> Iterator[str]:
    """Yield actual Markdown link and image destinations in document order."""
    for token in MARKDOWN.parse(text):
        if token.type != "inline" or not token.children:
            continue
        for child in token.children:
            if child.type == "link_open":
                target = child.attrGet("href")
            elif child.type == "image":
                target = child.attrGet("src")
            else:
                continue
            if target is not None:
                yield target


def missing_links(source: Path, root: Path = ROOT) -> list[str]:
    """Report missing or repository-escaping local targets in one Markdown file."""
    failures = []
    for raw_target in markdown_targets(source.read_text(encoding="utf-8")):
        if is_ignored_target(raw_target):
            continue

        path_part = target_path(raw_target)
        if not path_part:
            continue

        target = (source.parent / path_part).resolve()
        if not is_within_root(target, root) or not target.exists():
            failures.append(f"{source.relative_to(root)}: {raw_target}")
    return failures


def main() -> int:
    failures = [
        failure
        for source in project_markdown_files()
        for failure in missing_links(source)
    ]
    if failures:
        print("\n".join(failures))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
