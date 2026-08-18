from pathlib import Path
import subprocess

import pytest


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_POLICY_FILES = (
    ROOT / "LICENSES" / "README.md",
    ROOT / "research" / "sources" / "README.md",
)
FORBIDDEN_SUFFIXES = {
    ".pdf",
    ".doc",
    ".docx",
    ".epub",
    ".hwp",
    ".hwpx",
    ".odt",
    ".rtf",
    ".pages",
    ".ppt",
    ".pptx",
    ".xls",
    ".xlsx",
    ".zip",
    ".tar",
    ".gz",
    ".7z",
    ".rar",
}
MIXED_CASE_FORBIDDEN_FILENAMES = (
    "source.PdF",
    "source.DoC",
    "source.dOcX",
    "source.EpUb",
    "source.HwP",
    "source.hWpX",
    "source.OdT",
    "source.RtF",
    "source.PaGeS",
    "source.PpT",
    "source.pPtX",
    "source.XlS",
    "source.xLsX",
    "source.ZiP",
    "source.TaR",
    "source.Gz",
    "source.7Z",
    "source.RaR",
)


def test_policy_files_exist() -> None:
    assert all(path.is_file() for path in REQUIRED_POLICY_FILES)


def test_no_forbidden_binary_sources_are_tracked() -> None:
    output = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout
    tracked = [ROOT / line for line in output.splitlines()]
    offenders = [
        path.relative_to(ROOT)
        for path in tracked
        if path.suffix.lower() in FORBIDDEN_SUFFIXES
    ]
    assert offenders == []


@pytest.mark.parametrize("filename", MIXED_CASE_FORBIDDEN_FILENAMES)
def test_gitignore_blocks_copied_source_formats_case_insensitively(
    filename: str,
) -> None:
    result = subprocess.run(
        ["git", "check-ignore", "--no-index", "--quiet", filename], cwd=ROOT
    )
    assert result.returncode == 0


@pytest.mark.parametrize("filename", ["source.json", "source.md", "source.py"])
def test_gitignore_allows_repository_text_and_source_formats(filename: str) -> None:
    result = subprocess.run(
        ["git", "check-ignore", "--no-index", "--quiet", filename], cwd=ROOT
    )
    assert result.returncode == 1


@pytest.mark.parametrize(
    "suffix",
    [
        ".PDF",
        ".DOCX",
        ".ZIP",
        ".HWP",
        ".HWPX",
        ".ODT",
        ".PPTX",
        ".XLSX",
        ".7Z",
        ".RAR",
    ],
)
def test_uppercase_forbidden_binary_extensions_are_detected(
    monkeypatch: pytest.MonkeyPatch, suffix: str
) -> None:
    result = subprocess.CompletedProcess(
        args=["git", "ls-files"], returncode=0, stdout=f"source{suffix}\n", stderr=""
    )
    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: result)

    with pytest.raises(AssertionError):
        test_no_forbidden_binary_sources_are_tracked()
