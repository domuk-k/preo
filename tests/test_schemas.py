import json
from pathlib import Path

import jsonschema
import pytest


ROOT = Path(__file__).resolve().parents[1]


def load_schema(name: str) -> dict:
    return json.loads((ROOT / "schemas" / f"{name}.schema.json").read_text())


def validate_schema(name: str, instance: dict) -> None:
    validator = jsonschema.Draft202012Validator(
        load_schema(name), format_checker=jsonschema.FormatChecker()
    )
    validator.validate(instance)


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
        "example_invariants": ["온도 조건과 전원 차단 결과를 동일하게 유지한다."],
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
        "estimated_size": "고정 스냅숏 미정으로 문서 수 미측정",
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
    validate_schema(name, instance)


@pytest.mark.parametrize("name,instance", VALID_CASES.items())
def test_required_ids(name: str, instance: dict) -> None:
    invalid = dict(instance)
    invalid.pop("id")
    with pytest.raises(jsonschema.ValidationError):
        validate_schema(name, invalid)


def test_rule_rejects_accepted_status_during_phase_zero() -> None:
    invalid = dict(VALID_CASES["rule"], status="accepted")
    with pytest.raises(jsonschema.ValidationError):
        validate_schema("rule", invalid)


def test_claim_rejects_invalid_checked_on_date() -> None:
    invalid = dict(VALID_CASES["claim"], checked_on="2026-02-30")
    with pytest.raises(jsonschema.ValidationError):
        validate_schema("claim", invalid)


def test_corpus_source_rejects_invalid_checked_on_date() -> None:
    invalid = dict(VALID_CASES["corpus-source"], checked_on="2026-02-30")
    with pytest.raises(jsonschema.ValidationError):
        validate_schema("corpus-source", invalid)


def test_corpus_source_requires_nonempty_estimated_size() -> None:
    invalid = dict(VALID_CASES["corpus-source"])
    invalid.pop("estimated_size")
    with pytest.raises(jsonschema.ValidationError):
        validate_schema("corpus-source", invalid)

    whitespace_only = dict(VALID_CASES["corpus-source"], estimated_size="   ")
    with pytest.raises(jsonschema.ValidationError):
        validate_schema("corpus-source", whitespace_only)
