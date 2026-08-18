# KSTL Phase 0 Research Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a traceable Phase 0 research repository with verified evidence, cross-language comparisons, legally classified corpus candidates, machine-readable schemas, and at least ten Korean controlled-language rule candidates.

**Architecture:** Keep externally sourced facts in `research/`, KSTL-owned proposals in `standard/`, machine contracts in `schemas/`, and human workflows in `docs/`. A small Python test suite validates schemas, references, repository policy, and discoverability without implementing a language checker.

**Tech Stack:** Markdown, YAML 1.2-compatible data, JSON Schema Draft 2020-12, Python 3.11+, `uv`, PyYAML 6.x, jsonschema 4.x, pytest 8.x.

## Global Constraints

- Phase 0 does not implement a CLI, MCP server, LSP server, editor extension, or trained NLP model.
- Every factual research claim has one of these statuses: `verified`, `secondary`, `unverified`, `contradicted`.
- Only official institutional pages, primary academic texts, or repository bibliographic records can support `verified` claims.
- Search-result snippets alone cannot support `verified` claims.
- Do not commit ASD-STE100 PDFs, copyrighted dictionaries, paid books, paid papers, or third-party source archives.
- Do not present KSTL as endorsed, certified, or affiliated with ASD or STEMG.
- All Phase 0 rule data remains `candidate`; the schema may enumerate `experimental` and `deprecated` for later lifecycle stages. No vocabulary item is represented as approved.
- Unknown redistribution rights mean metadata-only handling; no source files are copied into the repository.
- Use stable lowercase IDs for sources, claims, and corpus records. Use stable uppercase `KSTL-*` IDs for standard rule and vocabulary records. Use ISO dates (`YYYY-MM-DD`) throughout machine-readable data.
- Keep each commit limited to the named task files; never stage with `git add .` or `git add -A`.

---

### Task 1: Reproducible research workspace and repository safeguards

**Files:**
- Create: `pyproject.toml`
- Create: `.gitignore`
- Create: `LICENSES/README.md`
- Create: `research/sources/README.md`
- Create: `tests/test_repository_policy.py`

**Interfaces:**
- Consumes: the design constraints in `docs/superpowers/specs/2026-08-08-phase-0-research-foundation-design.md`.
- Produces: `uv run pytest` as the common verification command; repository policy tests consumed by every later task.

- [ ] **Step 1: Add the Python and test configuration**

Create `pyproject.toml` with this content:

```toml
[project]
name = "kstl-research"
version = "0.0.0"
description = "Research data and validation for Korean Simplified Technical Language"
requires-python = ">=3.11"
dependencies = [
  "jsonschema>=4.23,<5",
  "PyYAML>=6.0,<7",
]

[dependency-groups]
dev = ["pytest>=8,<9"]

[tool.uv]
package = false

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra"
```

- [ ] **Step 2: Prevent accidental source redistribution**

Create `.gitignore` with explicit local-source and binary-document exclusions:

```gitignore
.worktrees/
.DS_Store
.venv/
__pycache__/
.pytest_cache/
*.py[cod]

# Third-party source material stays local. Only the policy README is tracked.
research/sources/*
!research/sources/README.md

# Do not commit copied standards, papers, books, or archives.
*.pdf
*.doc
*.docx
*.epub
*.zip
*.tar
*.tar.gz
```

- [ ] **Step 3: Write a failing repository-policy test**

Create `tests/test_repository_policy.py`:

```python
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_POLICY_FILES = (
    ROOT / "LICENSES" / "README.md",
    ROOT / "research" / "sources" / "README.md",
)
FORBIDDEN_SUFFIXES = {".pdf", ".doc", ".docx", ".epub", ".zip", ".tar", ".gz"}


def test_policy_files_exist() -> None:
    assert all(path.is_file() for path in REQUIRED_POLICY_FILES)


def test_no_forbidden_binary_sources_are_tracked() -> None:
    output = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout
    tracked = [ROOT / line for line in output.splitlines()]
    offenders = [path.relative_to(ROOT) for path in tracked if path.suffix in FORBIDDEN_SUFFIXES]
    assert offenders == []
```

- [ ] **Step 4: Run the policy test and verify the expected failure**

Run: `uv run pytest tests/test_repository_policy.py -v`

Expected: `test_policy_files_exist` fails because both policy README files are absent; the binary-source test passes.

- [ ] **Step 5: Add the licensing and local-source policies**

Create `LICENSES/README.md` with these decisions:

- Code is intended for Apache-2.0, pending repository-wide license confirmation before public release.
- KSTL-authored research notes and data are intended for CC BY 4.0, pending contributor-policy confirmation.
- A URL or citation does not grant redistribution rights.
- Each third-party source keeps its original terms.
- No ASD logo, ASD-STE100 PDF, controlled dictionary, paid paper, or paid book is redistributed.

Create `research/sources/README.md` with these rules:

- This directory is for local researcher copies only and is ignored by Git.
- Store only lawfully obtained files.
- Use source IDs from `research/bibliography.md` as local filenames when practical.
- Never infer repository redistribution permission from free download access.
- Record analysis in repository-authored Markdown or YAML rather than copying source passages.

- [ ] **Step 6: Run the policy test and verify it passes**

Run: `uv run pytest tests/test_repository_policy.py -v`

Expected: 2 tests pass.

- [ ] **Step 7: Commit the workspace foundation**

```bash
git add pyproject.toml uv.lock .gitignore LICENSES/README.md research/sources/README.md tests/test_repository_policy.py
git commit -m "chore: establish Phase 0 research workspace"
```

---

### Task 2: Machine-readable contracts and schema tests

**Files:**
- Create: `schemas/claim.schema.json`
- Create: `schemas/rule.schema.json`
- Create: `schemas/vocabulary.schema.json`
- Create: `schemas/corpus-source.schema.json`
- Create: `tests/test_schemas.py`

**Interfaces:**
- Consumes: JSON Schema Draft 2020-12 and the status enums fixed in the design.
- Produces: four schemas with `$id` values `https://kstl.dev/schemas/{claim,rule,vocabulary,corpus-source}.schema.json`; `load_schema(name: str) -> dict` for tests.

- [ ] **Step 1: Write schema behavior tests before the schemas exist**

Create `tests/test_schemas.py`:

```python
import json
from pathlib import Path

import jsonschema
import pytest


ROOT = Path(__file__).resolve().parents[1]


def load_schema(name: str) -> dict:
    return json.loads((ROOT / "schemas" / f"{name}.schema.json").read_text())


VALID_CASES = {
    "claim": {
        "id": "ste.issue-9.release-date",
        "claim": "ASD-STE100 Issue 9 was released on 2025-01-15.",
        "status": "verified",
        "source_ids": ["asd-ste-about"],
        "checked_on": "2026-08-08",
    },
    "rule": {
        "id": "KSTL-SYN-001",
        "title": "조건을 결과보다 먼저 쓴다",
        "purpose": "독자가 적용 조건을 먼저 확인하게 한다.",
        "scope": ["procedure", "description"],
        "normativity": "must",
        "status": "candidate",
        "automation": "heuristic",
        "approved_examples": ["온도가 80 °C를 넘으면 전원을 끈다."],
        "unapproved_examples": ["전원을 끈다(온도가 80 °C를 넘는 경우)."],
        "rewrite_guidance": "조건절을 주절 앞에 둔다.",
        "source_ids": ["hong-kim-2008"],
        "exceptions": [],
        "open_questions": ["조건절 표지의 허용 목록을 정해야 한다."],
    },
    "vocabulary": {
        "id": "KSTL-VOC-EXAMPLE-001",
        "lemma": "정지하다",
        "meaning": "기계의 작동을 멈추게 하다.",
        "part_of_speech": "verb",
        "allowed_forms": ["정지한다", "정지하십시오"],
        "discouraged_forms": ["스톱하다"],
        "preferred_replacements": {"스톱하다": "정지하다"},
        "examples": ["장비를 정지하십시오."],
        "domains": ["example"],
        "source_ids": [],
        "status": "example",
    },
    "corpus-source": {
        "id": "sample.public-manuals",
        "name": "공개 매뉴얼 예시",
        "provider": "예시 기관",
        "domains": ["public"],
        "url": "https://example.org/manuals",
        "formats": ["html"],
        "access_method": "manual-download",
        "copyright_notice": "이용 조건 확인 필요",
        "redistribution": "unknown",
        "derivatives": "unknown",
        "personal_data_risk": "low",
        "collection_status": "candidate",
        "checked_on": "2026-08-08",
    },
}


@pytest.mark.parametrize("name,instance", VALID_CASES.items())
def test_valid_examples(name: str, instance: dict) -> None:
    jsonschema.Draft202012Validator(load_schema(name)).validate(instance)


@pytest.mark.parametrize("name,instance", VALID_CASES.items())
def test_required_ids(name: str, instance: dict) -> None:
    invalid = dict(instance)
    invalid.pop("id")
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(load_schema(name)).validate(invalid)


def test_rule_rejects_accepted_status_during_phase_zero() -> None:
    invalid = dict(VALID_CASES["rule"], status="accepted")
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(load_schema("rule")).validate(invalid)
```

- [ ] **Step 2: Run the schema tests and verify the expected failure**

Run: `uv run pytest tests/test_schemas.py -v`

Expected: all cases fail with `FileNotFoundError` for files under `schemas/`.

- [ ] **Step 3: Implement `claim.schema.json`**

Use Draft 2020-12, `additionalProperties: false`, and these exact constraints:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://kstl.dev/schemas/claim.schema.json",
  "type": "object",
  "additionalProperties": false,
  "required": ["id", "claim", "status", "source_ids", "checked_on"],
  "properties": {
    "id": {"type": "string", "pattern": "^[a-z0-9]+(?:[._-][a-z0-9]+)*$"},
    "claim": {"type": "string", "minLength": 10},
    "status": {"enum": ["verified", "secondary", "unverified", "contradicted"]},
    "source_ids": {"type": "array", "items": {"type": "string"}, "uniqueItems": true},
    "checked_on": {"type": "string", "format": "date"},
    "notes": {"type": "string", "minLength": 1}
  }
}
```

- [ ] **Step 4: Implement the other three schemas with fixed field contracts**

All schemas use Draft 2020-12 and `additionalProperties: false`.

Create `rule.schema.json` with this field contract:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://kstl.dev/schemas/rule.schema.json",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "id", "title", "purpose", "scope", "normativity", "status", "automation",
    "approved_examples", "unapproved_examples", "rewrite_guidance", "source_ids",
    "exceptions", "open_questions"
  ],
  "properties": {
    "id": {"type": "string", "pattern": "^KSTL-[A-Z]{3}-[0-9]{3}$"},
    "title": {"type": "string", "minLength": 2},
    "purpose": {"type": "string", "minLength": 10},
    "scope": {
      "type": "array", "minItems": 1, "uniqueItems": true,
      "items": {"enum": ["procedure", "description", "warning", "all"]}
    },
    "normativity": {"enum": ["must", "should", "may"]},
    "status": {"enum": ["candidate", "experimental", "deprecated"]},
    "automation": {"enum": ["deterministic", "heuristic", "human"]},
    "approved_examples": {
      "type": "array", "minItems": 1, "uniqueItems": true,
      "items": {"type": "string", "minLength": 2}
    },
    "unapproved_examples": {
      "type": "array", "minItems": 1, "uniqueItems": true,
      "items": {"type": "string", "minLength": 2}
    },
    "rewrite_guidance": {"type": "string", "minLength": 5},
    "source_ids": {"type": "array", "items": {"type": "string"}, "uniqueItems": true},
    "exceptions": {"type": "array", "items": {"type": "string", "minLength": 1}},
    "open_questions": {"type": "array", "items": {"type": "string", "minLength": 1}}
  }
}
```

Create `vocabulary.schema.json` with this field contract:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://kstl.dev/schemas/vocabulary.schema.json",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "id", "lemma", "meaning", "part_of_speech", "allowed_forms",
    "discouraged_forms", "preferred_replacements", "examples", "domains",
    "source_ids", "status"
  ],
  "properties": {
    "id": {"type": "string", "pattern": "^KSTL-VOC-[A-Z0-9-]+$"},
    "lemma": {"type": "string", "minLength": 1},
    "meaning": {"type": "string", "minLength": 5},
    "part_of_speech": {"enum": ["noun", "verb", "adjective", "adverb", "determiner", "bound-noun", "other"]},
    "allowed_forms": {
      "type": "array", "minItems": 1, "uniqueItems": true,
      "items": {"type": "string", "minLength": 1}
    },
    "discouraged_forms": {
      "type": "array", "uniqueItems": true,
      "items": {"type": "string", "minLength": 1}
    },
    "preferred_replacements": {
      "type": "object", "additionalProperties": {"type": "string", "minLength": 1}
    },
    "examples": {
      "type": "array", "minItems": 1, "uniqueItems": true,
      "items": {"type": "string", "minLength": 2}
    },
    "domains": {
      "type": "array", "minItems": 1, "uniqueItems": true,
      "items": {"type": "string", "minLength": 1}
    },
    "source_ids": {"type": "array", "items": {"type": "string"}, "uniqueItems": true},
    "status": {"enum": ["example", "candidate", "deprecated"]}
  }
}
```

Create `corpus-source.schema.json` with this field contract:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://kstl.dev/schemas/corpus-source.schema.json",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "id", "name", "provider", "domains", "url", "formats", "access_method",
    "copyright_notice", "redistribution", "derivatives", "personal_data_risk",
    "collection_status", "checked_on"
  ],
  "properties": {
    "id": {"type": "string", "pattern": "^[a-z0-9]+(?:[._-][a-z0-9]+)*$"},
    "name": {"type": "string", "minLength": 2},
    "provider": {"type": "string", "minLength": 2},
    "domains": {
      "type": "array", "minItems": 1, "uniqueItems": true,
      "items": {"type": "string", "minLength": 1}
    },
    "url": {"type": "string", "format": "uri", "pattern": "^https://"},
    "formats": {
      "type": "array", "minItems": 1, "uniqueItems": true,
      "items": {"type": "string", "minLength": 1}
    },
    "access_method": {"type": "string", "minLength": 2},
    "copyright_notice": {"type": "string", "minLength": 2},
    "redistribution": {"enum": ["allowed", "metadata-only", "permission-required", "unknown"]},
    "derivatives": {"enum": ["allowed", "metadata-only", "permission-required", "unknown"]},
    "personal_data_risk": {"enum": ["none", "low", "medium", "high", "unknown"]},
    "collection_status": {"enum": ["candidate", "approved", "rejected", "collected"]},
    "checked_on": {"type": "string", "format": "date"}
  }
}
```

- [ ] **Step 5: Run all schema tests**

Run: `uv run pytest tests/test_schemas.py -v`

Expected: 9 tests pass.

- [ ] **Step 6: Commit the schemas**

```bash
git add schemas/claim.schema.json schemas/rule.schema.json schemas/vocabulary.schema.json schemas/corpus-source.schema.json tests/test_schemas.py
git commit -m "feat: define Phase 0 research schemas"
```

---

### Task 3: Evidence ledger and Korean controlled-language review

**Files:**
- Create: `research/bibliography.md`
- Create: `research/claims.yaml`
- Create: `research/korean-controlled-language.md`
- Create: `tests/test_research_integrity.py`
- Modify: `docs/HANDOFF.md`

**Interfaces:**
- Consumes: `schemas/claim.schema.json`; primary sources linked by stable source IDs.
- Produces: YAML list `research/claims.yaml`; bibliography headings of the form `## <source-id>`; `load_yaml(path: Path) -> object` test helper.

- [ ] **Step 1: Write failing evidence-integrity tests**

Create `tests/test_research_integrity.py`:

```python
import json
import re
from pathlib import Path

import jsonschema
import yaml


ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text())


def bibliography_ids() -> set[str]:
    text = (ROOT / "research" / "bibliography.md").read_text()
    return set(re.findall(r"^## ([a-z0-9]+(?:[._-][a-z0-9]+)*)$", text, re.MULTILINE))


def test_claims_validate_and_have_resolvable_sources() -> None:
    schema = json.loads((ROOT / "schemas" / "claim.schema.json").read_text())
    claims = load_yaml(ROOT / "research" / "claims.yaml")
    ids = bibliography_ids()
    assert len(claims) >= 12
    for claim in claims:
        jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker()).validate(claim)
        assert set(claim["source_ids"]) <= ids
        if claim["status"] == "verified":
            assert claim["source_ids"]


def test_claim_ids_are_unique() -> None:
    claims = load_yaml(ROOT / "research" / "claims.yaml")
    ids = [claim["id"] for claim in claims]
    assert len(ids) == len(set(ids))


def test_korean_review_covers_three_primary_texts() -> None:
    text = (ROOT / "research" / "korean-controlled-language.md").read_text()
    assert text.count("검증 상태: `verified`") >= 3
    for heading in ("연구 질문", "방법", "핵심 결과", "KSTL에 주는 시사점", "한계"):
        assert heading in text
```

- [ ] **Step 2: Run the research tests and verify the expected failure**

Run: `uv run pytest tests/test_research_integrity.py -v`

Expected: failures report missing `research/bibliography.md`, `research/claims.yaml`, and `research/korean-controlled-language.md`.

- [ ] **Step 3: Build the bibliography from primary records**

Give each source a heading ID and record title, authors or institution, publication, date, pages where applicable, canonical URL, source type, access date `2026-08-08`, access state, and reuse notes.

The minimum bibliography set is:

- `asd-ste-home`: ASD/STEMG official home page, <https://www.asd-ste100.org/>
- `asd-ste-about`: ASD/STEMG official explanation and Issue 9 summary, <https://www.asd-ste100.org/about_STE.html>
- `asd-ste-downloads`: official copy-request page, <https://www.asd-ste100.org/STE_downloads.html>
- `asd-ste-tools`: official tool limitations, <https://www.asd-ste100.org/STEsoftware.html>
- `hong-kim-2008`: Munpyo Hong and Chang-Hyun Kim, “Controlled Korean for Korean-English MT,” PACLIC 22, 2008, pages 391–396, <https://aclanthology.org/Y08-1040/>
- `ryu-im-jeong-2008`: 류수린, 임병화, 정동규, 「통제언어 모형개발의 필요성과 방향 — 기술문서에서 나타난 한국어 표현을 중심으로 —」, 『독어학』 17, 2008, 69–95, DOI `10.24814/kgds.2008..17.69`, <https://www.kci.go.kr/kciportal/landing/article.kci?arti_id=ART001261554>. KCI의 첫 저자 표기 `유수린`은 원문·KISS·RISS의 `류수린`과 다르다는 서지 메모를 남긴다.
- `im-nam-2009`: 임병화, 남유선, 「기술문서의 조건 부사어 통제1) — 번역성 제고 방안을 중심으로 —」, 『독어학』 20, 2009, 217–243, DOI `10.24814/kgds.2009..20.217`, <https://www.kci.go.kr/kciportal/landing/article.kci?arti_id=ART001405511>
- `choi-choi-2008`: 최지영, 최명원, 「통제언어의 관점에서 본 기술문서의 화행표현」, 『독어학』 17, 2008, 351–380, DOI `10.24814/kgds.2008..17.351`, <https://www.kci.go.kr/kciportal/landing/article.kci?arti_id=ART001264555>
- `gobbi-2014-thesis`: Ilaria Gobbi, doctoral thesis containing the Guía de Español Técnico Simplificado v.0, University of Bologna repository, <https://amsdottorato.unibo.it/id/eprint/6681/>
- `its-official`: COM&TEC’s official Italiano Tecnico Semplificato site, <https://www.italianotecnicosemplificato.it/>

Also record 권민재·남유선·홍우평 2008 「기술 커뮤니케이션과 통제언어」 (DOI `10.24814/kgds.2008..17.45`) and 함수진·류수린 2010 「기술문서의 한일기계번역 문제에 대한 통제언어 연구」 (DOI `10.15749/jts.2010.11.4.009`). Preserve the Korean authors’ published romanization only when the primary text supplies it; do not invent English translations for German parallel titles.

- [ ] **Step 4: Record atomic claims and corrections**

Create at least 12 claim records. Separate release date, standard status, rule count, dictionary size, tool limitations, Korean study existence, ETS structure, ITS ownership, and every challenged handoff statement into distinct records.

The following handoff claims remain `unverified` unless a primary source directly proves them:

- translation-cost reduction of 30–40 percent;
- an exact rule or dictionary count for ETS 2.0;
- an exact Italiano Tecnico Semplificato count based only on the paid book;
- a Français Rationalisé glossary-entry count;
- the claimed `sourdough-bread/asd-ste100-checker` repository if its canonical repository cannot be located.

Record the 2026 ETS 2.0 book itself as verified from the Aracne publisher catalog entry and ISBN `979-12-218-2466-7`; treat the more detailed 2026-02-13 release date and public description as secondary unless confirmed by the publisher. Record the publicly reported ITS values of 53 instructions and approximately 1,000 lemmas as `secondary`, not `verified`.

Use `contradicted` only when a stronger source directly supplies an incompatible fact; otherwise use `unverified`.

- [ ] **Step 5: Write structured summaries of at least three Korean studies**

For each primary text, include bibliographic ID, verification state, research question, method or data, core findings, relevance to KSTL, and limitations. The required summaries are `hong-kim-2008`, `ryu-im-jeong-2008`, `im-nam-2009`, and `choi-choi-2008`. For Hong and Kim 2008, explicitly record that their result concerns Korean-to-English MT and that the design must account for both Korean linguistic properties and the target MT system; do not generalize it into proven safety or readability gains.

- [ ] **Step 6: Correct the handoff’s certainty levels**

Modify `docs/HANDOFF.md` so verified claims link to bibliography IDs or canonical sources and uncertain numbers are labeled as unverified research leads. Preserve the original research direction while removing language that presents unsupported claims as settled facts.

- [ ] **Step 7: Run the research tests**

Run: `uv run pytest tests/test_research_integrity.py -v`

Expected: 3 tests pass.

- [ ] **Step 8: Commit the evidence ledger**

```bash
git add research/bibliography.md research/claims.yaml research/korean-controlled-language.md tests/test_research_integrity.py docs/HANDOFF.md
git commit -m "docs: verify Phase 0 evidence and Korean research"
```

---

### Task 4: Cross-language controlled-technical-language comparison

**Files:**
- Create: `research/language-comparison.md`
- Modify: `research/bibliography.md`
- Modify: `research/claims.yaml`
- Modify: `tests/test_research_integrity.py`

**Interfaces:**
- Consumes: bibliography and atomic claim IDs from Task 3.
- Produces: one evidence-scoped comparison row each for STE, ETS, ITS, and the French case; no unsupported numeric cells.

- [ ] **Step 1: Extend the tests with required comparison semantics**

Add this test:

```python
def test_language_comparison_covers_required_cases_and_uncertainty() -> None:
    text = (ROOT / "research" / "language-comparison.md").read_text()
    for term in (
        "ASD-STE100",
        "Español Técnico Simplificado",
        "Italiano Tecnico Semplificato",
        "Français",
    ):
        assert term in text
    assert "확인하지 못함" in text
    assert "단순 번역" in text
    assert "한국어 설계 시사점" in text
```

- [ ] **Step 2: Run the targeted test and verify the expected failure**

Run: `uv run pytest tests/test_research_integrity.py::test_language_comparison_covers_required_cases_and_uncertainty -v`

Expected: failure because `research/language-comparison.md` does not exist.

- [ ] **Step 3: Write the comparison from primary or official evidence**

Use columns for name, language, steward or author, first confirmed publication, latest confirmed version, publicly confirmed structure, relation to STE, access conditions, evidence status, and KSTL implication.

Apply these rules:

- STE facts come from ASD/STEMG pages and, where lawfully available for private study, Issue 9 analysis notes.
- For ETS, distinguish the 2014 thesis guide `Versión 0` from the 2015 book and the 2026 `Español Técnico Simplificado 2.0`. Record the v0 total of 59 numbered rules across sections 1–8 only after checking the thesis table of contents; do not apply that count to 2.0. Record the 2.0 rule and dictionary sizes as “확인하지 못함.”
- For ITS, record COM&TEC stewardship and the official `Istruzioni Linguistiche + Dizionario` structure. Record 53 instructions and approximately 1,000 lemmas as secondary values from the trained-practitioner page <https://free-edit.it/comunicatore-tecnico/its-italiano-tecnico-semplificato.html>, not as official-site values.
- For Français Rationalisé, record GIFAS stewardship, the 1999 second edition, seven sections and 50 rules when supported by Barthe et al. and page-specific academic analysis. Record the glossary entry count as “확인하지 못함,” because no official open guide or primary count was located.
- Do not infer that a language has a dictionary merely because its marketing page calls it controlled.

- [ ] **Step 4: Add new bibliography and claim records**

Every fact in the table must resolve to a source ID. Add atomic claims for each confirmed version and structure. Add unverified claims for each unsupported handoff number so future researchers can see what remains open.

- [ ] **Step 5: Explain the design inference**

Add a “한국어 설계 시사점” section that distinguishes observation from inference. State that KSTL should adapt control categories to Korean morphology and syntax, while cross-language machine-translation compatibility remains an evaluation hypothesis rather than a guaranteed outcome.

- [ ] **Step 6: Run the research suite and commit**

Run: `uv run pytest tests/test_research_integrity.py -v`

Expected: all tests pass.

```bash
git add research/language-comparison.md research/bibliography.md research/claims.yaml tests/test_research_integrity.py
git commit -m "docs: compare controlled technical languages"
```

---

### Task 5: Corpus acquisition policy and candidate registry

**Files:**
- Create: `docs/corpus-guide.md`
- Create: `research/corpus-sources.yaml`
- Create: `tests/test_corpus_sources.py`
- Modify: `research/bibliography.md`

**Interfaces:**
- Consumes: `schemas/corpus-source.schema.json` and official provider terms.
- Produces: at least 10 schema-valid corpus candidates spanning public, safety/mechanical, aviation/transport, and IT documentation.

- [ ] **Step 1: Write failing corpus registry tests**

Create `tests/test_corpus_sources.py`:

```python
import json
from pathlib import Path

import jsonschema
import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_corpus_registry_is_valid_and_diverse() -> None:
    schema = json.loads((ROOT / "schemas" / "corpus-source.schema.json").read_text())
    sources = yaml.safe_load((ROOT / "research" / "corpus-sources.yaml").read_text())
    assert len(sources) >= 10
    domains = set()
    ids = []
    for source in sources:
        jsonschema.Draft202012Validator(
            schema, format_checker=jsonschema.FormatChecker()
        ).validate(source)
        domains.update(source["domains"])
        ids.append(source["id"])
    assert len(ids) == len(set(ids))
    assert {"public", "safety-mechanical", "aviation-transport", "it"} <= domains


def test_unknown_rights_never_mark_collected() -> None:
    sources = yaml.safe_load((ROOT / "research" / "corpus-sources.yaml").read_text())
    offenders = [
        item["id"]
        for item in sources
        if item["redistribution"] == "unknown" and item["collection_status"] == "collected"
    ]
    assert offenders == []
```

- [ ] **Step 2: Run the corpus tests and verify the expected failure**

Run: `uv run pytest tests/test_corpus_sources.py -v`

Expected: both tests fail because `research/corpus-sources.yaml` is absent.

- [ ] **Step 3: Write the corpus guide**

Define this acquisition flow:

1. Discover the provider’s official landing page.
2. Record terms, copyright notice, public-license identifier, robots/API limits, and access date.
3. Classify redistribution and derivative rights independently.
4. Inspect samples for personal data, signatures, contact details, and security-sensitive content.
5. Approve metadata collection before any document download.
6. Keep source files outside Git under `research/sources/`.
7. Create derived text only when the license permits it.
8. Record extraction commands, checksums, normalization, and exclusions in a future corpus manifest.

Include rejection rules for unclear provenance, credentials or tokens in URLs, individually identifying maintenance records, and terms that prohibit automated access.

- [ ] **Step 4: Populate at least 10 official-source candidates**

Use only provider-controlled pages. Each record must quote no license text; paraphrase the operational result and link to the exact terms page in `copyright_notice` or the bibliography.

Create records for these ten concrete candidates and re-check each official page at implementation time:

| ID | Candidate and official landing page | Initial rights classification |
|---|---|---|
| `dtaq.ram-terms` | 국방기술품질원 RAM 용어 데이터, <https://www.data.go.kr/data/15149399/fileData.do> | `allowed` only if the page still states 이용허락범위 제한 없음; preserve attribution and metadata. |
| `molit.aim-quality-manual` | 항공정보 품질경영시스템 운영 매뉴얼, <https://law.go.kr/LSW/admRulInfoP.do?admRulSeq=2100000238114> | Administrative-rule text can be `allowed`; classify third-party attachments separately. |
| `molit.construction-standards` | 국가건설기준 KDS/KCS, <https://law.go.kr/LSW/admRulLsInfoP.do?admRulSeq=2100000201053> | Administrative-rule text can be `allowed`; exclude KS/ISO extracts and separately protected drawings. |
| `lh.specifications` | LH 전문시방서, <https://www.data.go.kr/data/15084347/fileData.do> | `allowed` only while the catalog states 이용허락범위 제한 없음; record the exact version. |
| `molit.environmental-cost-guide` | 환경관리비 산출기준 및 해설서, <https://www.data.go.kr/data/15035529/fileData.do> | `allowed` only while the catalog states 이용허락범위 제한 없음. |
| `kobaco.production-safety-guide` | 광고제작 현장 산업안전보건 가이드, <https://www.data.go.kr/data/15141914/fileData.do> | `allowed` only while the catalog states 이용허락범위 제한 없음. |
| `kubernetes.ko-docs` | Kubernetes 한국어 문서, <https://github.com/kubernetes/website/tree/main/content/ko> | `allowed` under CC BY 4.0 with attribution and change notice. |
| `python.ko-docs` | Python 한국어 문서, <https://github.com/python/python-docs-ko> and <https://docs.python.org/ko/3/license.html> | `allowed` only under the exact PSF/translation contribution terms recorded from the repositories; preserve notices. |
| `mdn.ko-content` | MDN 한국어 번역 문서, <https://github.com/mdn/translated-content/tree/main/files/ko> | `allowed` with content-type-specific terms; prose is CC BY-SA 2.5 and code snippets require separate handling. |
| `kdca.practice-guidelines` | 질병관리청 항목별 표준 실무지침, starting with <https://www.kdca.go.kr/kdca/2861/subview.do?enc=Zm5jdDF8QEB8JTJGYmJzJTJGa2RjYSUyRjU1JTJGMzA5NjA0JTJGYXJ0Y2xWaWV3LmRvJTNG> | `allowed` only for individual items displaying 공공누리 제1유형; never generalize one item’s mark to the entire site. |

If source files cannot be redistributed, set `redistribution: metadata-only` or `permission-required`. Use `allowed` only when the official license directly permits redistribution under the intended repository terms.

- [ ] **Step 5: Add provider and license sources to the bibliography**

Create one bibliography record per provider landing page and a separate record for each license or terms page when they differ. Set access date to `2026-08-08`.

- [ ] **Step 6: Run the corpus tests and commit**

Run: `uv run pytest tests/test_corpus_sources.py -v`

Expected: 2 tests pass.

```bash
git add docs/corpus-guide.md research/corpus-sources.yaml research/bibliography.md tests/test_corpus_sources.py
git commit -m "docs: define legal corpus acquisition and candidates"
```

---

### Task 6: Korean rule template, ten rule candidates, and vocabulary example

**Files:**
- Create: `docs/rule-template.md`
- Create: `standard/README.md`
- Create: `standard/rules/candidates.yaml`
- Create: `standard/vocabulary/entries.yaml`
- Create: `tests/test_standard_data.py`

**Interfaces:**
- Consumes: `schemas/rule.schema.json`, `schemas/vocabulary.schema.json`, and source IDs from `research/bibliography.md`.
- Produces: 10 or more schema-valid rule candidates with unique `KSTL-*` IDs; one explicitly non-approved vocabulary example.

- [ ] **Step 1: Write failing standard-data tests**

Create `tests/test_standard_data.py`:

```python
import json
from pathlib import Path
import re

import jsonschema
import yaml


ROOT = Path(__file__).resolve().parents[1]


def test_rule_candidates_validate_and_cover_ten_areas() -> None:
    schema = json.loads((ROOT / "schemas" / "rule.schema.json").read_text())
    rules = yaml.safe_load((ROOT / "standard" / "rules" / "candidates.yaml").read_text())
    bibliography = (ROOT / "research" / "bibliography.md").read_text()
    source_ids = set(re.findall(r"^## ([a-z0-9]+(?:[._-][a-z0-9]+)*)$", bibliography, re.MULTILINE))
    assert len(rules) >= 10
    ids = []
    automations = set()
    for rule in rules:
        jsonschema.Draft202012Validator(schema).validate(rule)
        assert rule["status"] == "candidate"
        assert rule["source_ids"]
        assert set(rule["source_ids"]) <= source_ids
        ids.append(rule["id"])
        automations.add(rule["automation"])
    assert len(ids) == len(set(ids))
    assert {"deterministic", "heuristic", "human"} <= automations


def test_vocabulary_is_labeled_as_non_approved_example() -> None:
    schema = json.loads((ROOT / "schemas" / "vocabulary.schema.json").read_text())
    entries = yaml.safe_load((ROOT / "standard" / "vocabulary" / "entries.yaml").read_text())
    assert entries
    for entry in entries:
        jsonschema.Draft202012Validator(schema).validate(entry)
        assert entry["status"] == "example"
```

- [ ] **Step 2: Run the tests and verify the expected failure**

Run: `uv run pytest tests/test_standard_data.py -v`

Expected: failures report missing rule and vocabulary YAML files.

- [ ] **Step 3: Write the authoring template and status policy**

In `docs/rule-template.md`, explain every schema field, give one complete YAML record, distinguish a linguistic requirement from a checker heuristic, and require meaning-preserving approved/unapproved example pairs.

In `standard/README.md`, state prominently:

- the directory is a proposal workspace, not a published standard;
- all rules are candidates;
- vocabulary entries are format examples, not approved words;
- rule acceptance requires corpus evidence, expert review, and comprehension evaluation;
- ASD-STE100 rules must not be copied verbatim.

- [ ] **Step 4: Create ten concrete Korean rule candidates**

Use these IDs and subjects:

| ID | Subject | Initial automation class |
|---|---|---|
| `KSTL-DOC-001` | one instruction action per sentence | heuristic |
| `KSTL-SYN-001` | state the condition before the result | heuristic |
| `KSTL-SYN-002` | avoid ambiguous omitted arguments | human |
| `KSTL-SYN-003` | restrict passive forms that hide responsibility | heuristic |
| `KSTL-SYN-004` | split independently testable conditions | heuristic |
| `KSTL-MOD-001` | reduce nested adnominal clauses | heuristic |
| `KSTL-TER-001` | use one term for one concept within a document | deterministic |
| `KSTL-REF-001` | use pronouns and demonstratives only with one referent | human |
| `KSTL-STY-001` | keep document-ending style consistent | deterministic |
| `KSTL-SAF-001` | state hazard, consequence, and avoidance action | human |

Each candidate must include at least one natural Korean approved example, one meaning-equivalent unapproved example, rewrite guidance, cited rationale, exceptions, and a concrete open research question. Do not assign sentence-length or modifier-count thresholds without corpus evidence.

- [ ] **Step 5: Add format-only vocabulary entries**

Add 3–5 entries that exercise verbs, nouns, discouraged synonyms, inflected forms, and domain tags. Use `status: example` for every entry and `example` as a domain tag. State in the file header comment that no entry is approved KSTL vocabulary.

- [ ] **Step 6: Run the standard-data tests and commit**

Run: `uv run pytest tests/test_standard_data.py -v`

Expected: 2 tests pass.

```bash
git add docs/rule-template.md standard/README.md standard/rules/candidates.yaml standard/vocabulary/entries.yaml tests/test_standard_data.py
git commit -m "docs: add Korean controlled-language rule candidates"
```

---

### Task 7: Phase 0 checklist, discoverability, and link validation

**Files:**
- Create: `docs/phase-0-checklist.md`
- Create: `scripts/validate_links.py`
- Create: `tests/test_docs.py`
- Modify: `README.md`
- Modify: `docs/HANDOFF.md`

**Interfaces:**
- Consumes: every artifact created in Tasks 1–6.
- Produces: `python scripts/validate_links.py` with exit code 0 for valid local Markdown links; a README index from which each Phase 0 artifact is reachable directly or through one intermediate index.

- [ ] **Step 1: Write failing documentation tests**

Create `tests/test_docs.py`:

```python
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_ARTIFACTS = (
    "docs/phase-0-checklist.md",
    "docs/rule-template.md",
    "docs/corpus-guide.md",
    "research/bibliography.md",
    "research/claims.yaml",
    "research/korean-controlled-language.md",
    "research/language-comparison.md",
    "research/corpus-sources.yaml",
    "standard/README.md",
    "standard/rules/candidates.yaml",
    "standard/vocabulary/entries.yaml",
    "schemas/claim.schema.json",
    "schemas/rule.schema.json",
    "schemas/vocabulary.schema.json",
    "schemas/corpus-source.schema.json",
)


def test_readme_links_phase_zero_artifacts() -> None:
    readme = (ROOT / "README.md").read_text()
    for artifact in EXPECTED_ARTIFACTS:
        assert artifact in readme


def test_local_markdown_links_resolve() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_links.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
```

- [ ] **Step 2: Run the docs tests and verify the expected failure**

Run: `uv run pytest tests/test_docs.py -v`

Expected: README artifact-link assertions fail and `scripts/validate_links.py` is missing.

- [ ] **Step 3: Implement the relative-link validator**

Create `scripts/validate_links.py`:

```python
from pathlib import Path
import re
import sys
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\[[^]]+\]\(([^)]+)\)")
IGNORED_PREFIXES = ("http://", "https://", "mailto:", "#")


def project_markdown_files() -> list[Path]:
    ignored_parts = {".git", ".venv", ".pytest_cache"}
    return sorted(
        path for path in ROOT.rglob("*.md") if not ignored_parts.intersection(path.parts)
    )


def missing_links(source: Path) -> list[str]:
    missing = []
    for match in LINK.finditer(source.read_text()):
        raw_target = match.group(1).strip().strip("<>")
        if raw_target.startswith(IGNORED_PREFIXES):
            continue
        path_part = unquote(raw_target.split("#", 1)[0])
        if not path_part:
            continue
        target = (source.parent / path_part).resolve()
        if not target.exists():
            missing.append(f"{source.relative_to(ROOT)}: {raw_target}")
    return missing


def main() -> int:
    failures = [item for source in project_markdown_files() for item in missing_links(source)]
    if failures:
        print("\n".join(failures))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Write an executable Phase 0 checklist**

For every success criterion in the design, record owner role, evidence file, verification command or manual review action, current status, and blocking condition. Mark only items proven by current files and test results as complete.

- [ ] **Step 5: Turn README into the documentation index**

Link all entries in `EXPECTED_ARTIFACTS`. Explain the four-directory boundary (`research`, `standard`, `schemas`, `docs`), the evidence-status vocabulary, quick verification command `uv run pytest`, and the prohibition on committing third-party source files.

- [ ] **Step 6: Reconcile handoff checkboxes with evidence**

Mark a handoff action complete only if its corresponding artifact and verification evidence exist. Keep the external Issue 9 request unchecked unless a human has actually submitted the official form and recorded receipt; a public URL to the request page is not proof of submission.

- [ ] **Step 7: Run documentation and full tests**

Run: `uv run pytest tests/test_docs.py -v`

Expected: 2 tests pass.

Run: `uv run pytest`

Expected: all repository tests pass.

- [ ] **Step 8: Commit discoverability and checklist changes**

```bash
git add docs/phase-0-checklist.md scripts/validate_links.py tests/test_docs.py README.md docs/HANDOFF.md
git commit -m "docs: publish Phase 0 research index and checklist"
```

---

### Task 8: Requirement-by-requirement Phase 0 completion audit

**Files:**
- Modify: `docs/phase-0-checklist.md`
- Modify: `research/claims.yaml` only if the audit finds incorrect status
- Modify: affected source or documentation files only when the audit finds a concrete defect

**Interfaces:**
- Consumes: the design’s seven success criteria and all repository tests.
- Produces: an evidence-backed checklist that distinguishes complete, incomplete, and externally blocked items.

- [ ] **Step 1: Map each design criterion to authoritative evidence**

Record these mappings in `docs/phase-0-checklist.md`:

1. STE claim sourcing → `research/claims.yaml`, `research/bibliography.md`, direct source review.
2. Three Korean studies → `research/korean-controlled-language.md`, primary-text links.
3. Four-language comparison → `research/language-comparison.md`, source IDs per row.
4. Corpus rights registry → `research/corpus-sources.yaml`, official terms links.
5. Machine contracts → four schema files and passing schema/data tests.
6. Ten Korean candidates → `standard/rules/candidates.yaml` and passing standard-data tests.
7. Discoverability → README links and passing documentation tests.

- [ ] **Step 2: Run mechanical verification from a clean environment**

Run:

```bash
uv sync --locked
uv run pytest -v
uv run python scripts/validate_links.py
git diff --check
git status --short
```

Expected: dependency sync succeeds; all tests pass; link validation exits 0; `git diff --check` prints nothing. Before the audit commit, only intentional audit corrections may appear in `git status --short`.

- [ ] **Step 3: Perform manual evidence sampling**

Open every source behind a `verified` claim. Confirm that the source directly supports the atomic claim and that the bibliography metadata matches the source. Downgrade any claim that relies on inference, a search snippet, or an inaccessible page.

Open every corpus terms link. Confirm that `allowed` is used only when the official terms clearly allow the intended redistribution. Downgrade uncertain records to `metadata-only`, `permission-required`, or `unknown`.

- [ ] **Step 4: Check for accidental copyrighted or sensitive material**

Run:

```bash
git ls-files | rg '\.(pdf|docx?|epub|zip|tar|gz)$' && exit 1 || true
git grep -nE 'ASD logo|BEGIN (RSA|OPENSSH|EC) PRIVATE KEY|api[_-]?key|password' -- . ':!docs/superpowers/plans/*'
```

Expected: the binary-material command succeeds without file matches; the content scan returns no credential material. Descriptive policy text mentioning ASD logos is acceptable after manual inspection.

- [ ] **Step 5: Resolve every audit failure**

For a failed test, fix the specific data or validator and rerun the narrow test before the full suite. For missing primary evidence, downgrade the affected claim rather than treating plausible secondary evidence as proof. For an unmet external action such as submitting the Issue 9 request form, leave the checklist incomplete and name the required human action.

- [ ] **Step 6: Commit the final audit state if files changed**

```bash
git add docs/phase-0-checklist.md research/claims.yaml
git commit -m "docs: record Phase 0 completion audit"
```

Do not create an empty commit. Do not call Phase 0 complete if any of the seven success criteria lacks direct evidence.
