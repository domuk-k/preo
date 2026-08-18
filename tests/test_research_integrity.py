import json
import re
from collections import Counter
from pathlib import Path

import jsonschema
import yaml


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_KOREAN_SOURCE_IDS = {
    "hong-kim-2008",
    "ryu-im-jeong-2008",
    "im-nam-2009",
    "choi-choi-2008",
}
REQUIRED_ATOMIC_CLAIM_IDS = {
    "ste.issue-9.section-count",
    "ste.issue-9.rule-count",
    "ste.issue-9.copy-cost",
    "ste.issue-9.copy-access",
    "ste.tools.writer-limit",
    "ste.tools.standard-limit",
    "ste.tools.automation-limit",
    "korean.hong-kim.translation-direction",
    "korean.hong-kim.application-domain",
    "korean.hong-kim.review-pair-count",
    "korean.hong-kim.error-type-count",
    "korean.hong-kim.sentences-per-type",
    "korean.ryu-im-jeong.lexicon-model",
    "korean.ryu-im-jeong.grammar-model",
    "korean.im-nam.document-count",
    "korean.im-nam.conditional-instance-count",
    "korean.im-nam.translation-route",
    "korean.choi-choi.first-survey-item-count",
    "korean.choi-choi.first-survey-participant-count",
    "korean.choi-choi.second-survey-item-count",
    "korean.choi-choi.second-survey-participant-count",
    "korean.choi-choi.sipsio-directive-rate",
    "korean.choi-choi.seumnida-directive-rate",
    "korean.kwon-nam-hong.scope",
    "korean.ham-ryu.scope",
    "ets.v0.corpus-basis",
    "ets.v0.rules-component",
    "ets.v0.dictionary-component",
    "ets.v2.publisher",
    "ets.v2.release-date",
    "ets.v2.print-isbn",
    "ets.v2.rule-count",
    "ets.v2.dictionary-size",
    "its.instruction-count",
    "its.dictionary-size",
    "its.rights.trademark-protection",
    "its.rights.copyright-protection",
    "its.access.print-availability",
    "its.access.digital-availability",
    "oss.sourdough-checker.repository",
    "oss.sourdough-checker.checker",
    "oss.sourdough-checker.mcp",
    "oss.sourdough-checker.lsp",
    "oss.sourdough-checker.agent-skill",
}
FORBIDDEN_COMPOSITE_CLAIM_IDS = {
    "ste.issue-9.official-copy",
    "ste.tools.limitations",
    "korean.hong-kim.scope",
    "korean.hong-kim.method",
    "korean.ryu-im-jeong.model",
    "korean.im-nam.corpus",
    "korean.im-nam.rules",
    "korean.choi-choi.method",
    "korean.choi-choi.ending-result",
    "korean.additional-studies",
    "ets.v0.structure",
    "ets.v2.book",
    "ets.v2.exact-counts",
    "its.public-counts",
    "its.rights-status",
    "oss.sourdough-checker",
}


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text())


def bibliography_ids() -> set[str]:
    text = (ROOT / "research" / "bibliography.md").read_text()
    return set(re.findall(r"^## ([a-z0-9]+(?:[._-][a-z0-9]+)*)$", text, re.MULTILINE))


def bibliography_blocks() -> dict[str, str]:
    text = (ROOT / "research" / "bibliography.md").read_text()
    return {
        match.group(1): match.group(2)
        for match in re.finditer(
            r"^## ([a-z0-9]+(?:[._-][a-z0-9]+)*)\n(.*?)(?=^## |\Z)",
            text,
            re.MULTILINE | re.DOTALL,
        )
    }


def korean_review_blocks() -> dict[str, str]:
    text = (ROOT / "research" / "korean-controlled-language.md").read_text()
    blocks = {}
    for match in re.finditer(
        r"^## [^\n]+\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL
    ):
        block = match.group(1)
        source_match = re.search(r"^- 서지 ID: `([^`]+)`$", block, re.MULTILINE)
        if source_match:
            blocks[source_match.group(1)] = block
    return blocks


def test_claims_validate_and_have_resolvable_sources() -> None:
    schema = json.loads((ROOT / "schemas" / "claim.schema.json").read_text())
    claims = load_yaml(ROOT / "research" / "claims.yaml")
    ids = bibliography_ids()
    assert len(claims) >= 12
    for claim in claims:
        jsonschema.Draft202012Validator(
            schema, format_checker=jsonschema.FormatChecker()
        ).validate(claim)
        assert set(claim["source_ids"]) <= ids
        if claim["status"] == "verified":
            assert claim["source_ids"]


def test_claim_ids_are_unique() -> None:
    claims = load_yaml(ROOT / "research" / "claims.yaml")
    ids = [claim["id"] for claim in claims]
    assert len(ids) == len(set(ids))


def test_claim_inventory_and_status_counts_are_pinned() -> None:
    claims = load_yaml(ROOT / "research" / "claims.yaml")
    assert len(claims) == 106
    assert Counter(claim["status"] for claim in claims) == {
        "verified": 96,
        "secondary": 3,
        "unverified": 5,
        "contradicted": 2,
    }


def test_reviewed_facts_have_atomic_claim_records() -> None:
    claims = load_yaml(ROOT / "research" / "claims.yaml")
    ids = {claim["id"] for claim in claims}
    assert REQUIRED_ATOMIC_CLAIM_IDS <= ids
    assert FORBIDDEN_COMPOSITE_CLAIM_IDS.isdisjoint(ids)


def test_korean_review_covers_all_required_primary_texts() -> None:
    assert REQUIRED_KOREAN_SOURCE_IDS <= korean_review_blocks().keys()


def test_each_korean_review_has_verified_state_and_required_sections() -> None:
    blocks = korean_review_blocks()
    required_sections = {"연구 질문", "방법", "핵심 결과", "KSTL에 주는 시사점", "한계"}
    for source_id in REQUIRED_KOREAN_SOURCE_IDS:
        block = blocks[source_id]
        assert "- 검증 상태: `verified`" in block
        sections = set(re.findall(r"^### (.+)$", block, re.MULTILINE))
        assert required_sections <= sections


def test_verified_claims_use_only_primary_or_institutional_sources() -> None:
    claims = load_yaml(ROOT / "research" / "claims.yaml")
    blocks = bibliography_blocks()
    for claim in claims:
        if claim["status"] != "verified":
            continue
        for source_id in claim["source_ids"]:
            source_type = re.search(
                r"^- 자료 유형: (.+)$", blocks[source_id], re.MULTILINE
            ).group(1)
            assert "2차 자료" not in source_type
            assert any(
                marker in source_type
                for marker in ("공식", "기관", "학술 논문", "학술대회 논문")
            )


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


def test_language_comparison_preserves_version_count_and_reference_semantics() -> None:
    text = (ROOT / "research" / "language-comparison.md").read_text()
    rows = {}
    for line in text.splitlines():
        if not line.startswith("| **"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        name = re.sub(r"\*\*| \([^)]*\)", "", cells[0])
        rows[name] = cells

    assert set(rows) == {
        "ASD-STE100 Simplified Technical English",
        "Español Técnico Simplificado",
        "Italiano Tecnico Semplificato",
        "Français Rationalisé",
    }
    assert all(len(cells) == 10 for cells in rows.values())

    ste = " ".join(rows["ASD-STE100 Simplified Technical English"])
    assert all(value in ste for value in ("Issue 9", "53개", "9개 섹션", "약 900개"))
    assert all(
        claim_id in ste
        for claim_id in (
            "ste.issue-9.rule-count",
            "ste.issue-9.section-count",
            "ste.issue-9.dictionary-size",
        )
    )

    ets = rows["Español Técnico Simplificado"]
    ets_first_edition = ets[3]
    ets_latest_edition = ets[4]
    ets_structure = ets[5]
    ets_evidence_status = ets[8]

    assert "`Versión 0`" in ets_first_edition
    assert "ets.v0.version-label" in ets_first_edition
    assert "Español Técnico Simplificado 2.0" in ets_latest_edition
    assert "ets.v2.release-date" in ets_latest_edition

    structure_summary, structure_evidence = ets_structure.split(
        "<br>근거:", maxsplit=1
    )
    v0_structure, v2_structure = structure_summary.split("2.0:", maxsplit=1)
    assert all(value in v0_structure for value in ("v0:", "59개"))
    assert "확인하지 못함" in v2_structure
    assert all(
        claim_id in structure_evidence
        for claim_id in (
            "ets.v0.rule-count",
            "ets.v2.rule-count",
            "ets.v2.dictionary-size",
        )
    )
    assert all(
        value in ets_evidence_status
        for value in (
            "v0 구조·59개: `verified`",
            "2.0 정확한 계수: `unverified`",
        )
    )

    its = " ".join(rows["Italiano Tecnico Semplificato"])
    assert all(value in its for value in ("판본 번호", "확인하지 못함", "53개", "약 1,000개"))
    assert all(
        claim_id in its
        for claim_id in ("its.latest-version-label", "its.instruction-count", "its.dictionary-size")
    )

    french = " ".join(rows["Français Rationalisé"])
    assert all(value in french for value in ("제2판", "1999", "7개 섹션", "50개", "확인하지 못함"))
    assert all(
        claim_id in french
        for claim_id in (
            "francais-rationalise.second-edition-year",
            "francais-rationalise.section-count",
            "francais-rationalise.rule-count",
            "francais-rationalise.glossary-size",
        )
    )
    assert "fr-barthe-1999" not in french

    claims = {claim["id"]: claim for claim in load_yaml(ROOT / "research" / "claims.yaml")}
    assert {
        claim_id: claims[claim_id]["status"]
        for claim_id in (
            "ets.v0.rule-count",
            "ets.v2.rule-count",
            "ets.v2.dictionary-size",
            "its.instruction-count",
            "its.dictionary-size",
            "francais-rationalise.glossary-size",
        )
    } == {
        "ets.v0.rule-count": "verified",
        "ets.v2.rule-count": "unverified",
        "ets.v2.dictionary-size": "unverified",
        "its.instruction-count": "secondary",
        "its.dictionary-size": "secondary",
        "francais-rationalise.glossary-size": "unverified",
    }
    assert claims["francais-rationalise.stewardship"]["source_ids"] == [
        "gobbi-2014-thesis"
    ]
    assert claims["francais-rationalise.second-edition-year"]["source_ids"] == [
        "gobbi-2014-thesis"
    ]

    claim_refs = set(re.findall(r"`([a-z][a-z0-9-]*(?:\.[a-z0-9-]+)+)`", text))
    assert claim_refs <= claims.keys()

    bibliography = bibliography_ids()
    source_refs = {
        source_id
        for cells in rows.values()
        for cell in cells
        for segment in cell.split("<br>")
        if "출처:" in segment
        for source_id in re.findall(r"`([^`]+)`", segment.split("출처:", 1)[1])
    }
    assert source_refs <= bibliography
