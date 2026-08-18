from __future__ import annotations

from markdown_it import MarkdownIt
from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_links.py"
README_ENTRY_POINTS = (
    "standard/README.md",
    "research/bibliography.md",
)
MARKDOWN = MarkdownIt("commonmark")


def markdown_targets(text: str) -> set[str]:
    return {
        target.attrGet("href").split("#", 1)[0]
        for token in MARKDOWN.parse(text)
        if token.type == "inline" and token.children
        for target in token.children
        if target.type == "link_open" and target.attrGet("href") is not None
    }


def copy_validator(repository: Path) -> Path:
    assert VALIDATOR.is_file(), "링크 검증기가 아직 없습니다."
    destination = repository / "scripts" / "validate_links.py"
    destination.parent.mkdir(exist_ok=True)
    shutil.copy2(VALIDATOR, destination)
    return destination


def copy_tracked_repository(destination: Path) -> Path:
    """Build a clean fixture from the repository's tracked files only."""
    output = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    for raw_path in output.split(b"\0"):
        if not raw_path:
            continue
        relative_path = Path(raw_path.decode())
        source = ROOT / relative_path
        target = destination / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    return destination


def run_validator(repository: Path) -> subprocess.CompletedProcess[str]:
    validator = copy_validator(repository)
    return subprocess.run(
        [sys.executable, str(validator)],
        cwd=repository,
        capture_output=True,
        text=True,
        check=False,
    )


def test_readme_links_standard_and_research_entry_points() -> None:
    targets = markdown_targets((ROOT / "README.md").read_text())
    assert set(README_ENTRY_POINTS) <= targets


def test_local_markdown_links_resolve_in_clean_repository_copy(tmp_path: Path) -> None:
    repository = copy_tracked_repository(tmp_path / "repository")
    result = run_validator(repository)
    assert result.returncode == 0, result.stdout + result.stderr


def test_clean_repository_copy_excludes_ignored_trees_and_keeps_source_policy(
    tmp_path: Path,
) -> None:
    repository = copy_tracked_repository(tmp_path / "repository")

    assert not (repository / ".superpowers").exists()
    assert not (repository / ".pytest_cache").exists()
    assert (repository / "research" / "sources" / "README.md").is_file()


def test_validator_checks_local_image_targets(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "present.png").write_bytes(b"image fixture")
    (tmp_path / "README.md").write_text(
        "![present](docs/present.png)\n![missing](docs/missing.png)\n"
    )

    result = run_validator(tmp_path)

    assert result.returncode == 1
    assert result.stdout.splitlines() == ["README.md: docs/missing.png"]


def test_validator_ignores_fragment_only_links(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("# Heading\n\n[heading](#heading)\n")

    result = run_validator(tmp_path)

    assert result.returncode == 0, result.stdout + result.stderr


def test_validator_rejects_relative_target_that_escapes_repository(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    repository.mkdir()
    (repository / "README.md").write_text("[escape](../outside.md)\n")
    (tmp_path / "outside.md").write_text("outside\n")
    result = run_validator(repository)
    assert result.returncode == 1
    assert "README.md: ../outside.md" in result.stdout


def test_validator_ignores_fenced_code_inline_code_and_html_comments(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text(
        "```md\n[code](missing.md)\n```\n`[inline](also-missing.md)`\n"
        "<!-- [comment](comment-missing.md) -->\n"
    )
    result = run_validator(tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr


