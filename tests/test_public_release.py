import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_NAMES = ("claim", "rule", "vocabulary", "corpus-source")
PUBLIC_SCHEMA_ROOT = (
    "https://raw.githubusercontent.com/domuk-k/preo/main/schemas"
)
APACHE_2_SHA256 = "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30"
CC_BY_4_SHA256 = "9e5f1b3c610b9c2da5c313bf81d577a7d1acec686bdb0384edefa6df0f90cd94"


def test_public_release_has_operational_license_and_contribution_files() -> None:
    required = (
        ROOT / "LICENSE",
        ROOT / "LICENSES" / "CC-BY-4.0.txt",
        ROOT / "LICENSES" / "README.md",
        ROOT / "CONTRIBUTING.md",
    )
    assert all(path.is_file() for path in required)


def test_license_policy_maps_code_and_project_content_without_pending_terms() -> None:
    policy = (ROOT / "LICENSES" / "README.md").read_text()
    assert "Apache License 2.0" in policy
    assert "Creative Commons Attribution 4.0 International" in policy
    assert "pending" not in policy.lower()
    assert "scripts/" in policy
    assert "tests/" in policy
    assert ".gitignore" in policy
    assert "docs/" in policy
    assert "research/" in policy
    assert "schemas/" in policy
    assert "standard/" in policy
    assert "비완전" in policy
    assert "저작권" in policy
    assert "면책" in policy


def test_license_texts_identify_the_selected_licenses() -> None:
    apache = (ROOT / "LICENSE").read_bytes()
    cc_by = (ROOT / "LICENSES" / "CC-BY-4.0.txt").read_bytes()
    assert hashlib.sha256(apache).hexdigest() == APACHE_2_SHA256
    assert hashlib.sha256(cc_by).hexdigest() == CC_BY_4_SHA256


def test_readme_declares_independence_from_asd_and_stemg() -> None:
    readme = (ROOT / "README.md").read_text().replace("\n> ", " ")
    assert "ASD 또는 STEMG와 제휴하거나 이들의 승인을 받은 프로젝트가 아닙니다" in readme
    assert "표준 원문이나 통제 사전을 재배포하지 않습니다" in readme


def test_contribution_terms_require_rights_and_apply_both_project_licenses() -> None:
    guide = (ROOT / "CONTRIBUTING.md").read_text()
    assert "right to submit" in guide
    assert "Apache License 2.0" in guide
    assert "CC BY 4.0" in guide
    assert "third-party standards" in guide
    assert "controlled dictionaries" in guide


def test_local_source_quarantine_tracks_only_its_policy_readme() -> None:
    tracked = subprocess.run(
        ["git", "ls-files", "research/sources"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    assert tracked == ["research/sources/README.md"]


def test_active_schema_ids_use_the_public_repository_namespace() -> None:
    for name in SCHEMA_NAMES:
        schema = json.loads((ROOT / "schemas" / f"{name}.schema.json").read_text())
        assert schema["$id"] == f"{PUBLIC_SCHEMA_ROOT}/{name}.schema.json"
