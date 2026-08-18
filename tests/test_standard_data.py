import json
from pathlib import Path
import re

import jsonschema
import yaml


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_RULE_AUTOMATION = {
    "KSTL-DOC-001": "heuristic",
    "KSTL-SYN-001": "heuristic",
    "KSTL-SYN-002": "human",
    "KSTL-SYN-003": "heuristic",
    "KSTL-SYN-004": "heuristic",
    "KSTL-MOD-001": "heuristic",
    "KSTL-TER-001": "deterministic",
    "KSTL-REF-001": "human",
    "KSTL-STY-001": "deterministic",
    "KSTL-SAF-001": "human",
}


def bibliography_ids() -> set[str]:
    bibliography = (ROOT / "research" / "bibliography.md").read_text()
    return set(
        re.findall(
            r"^## ([a-z0-9]+(?:[._-][a-z0-9]+)*)$",
            bibliography,
            re.MULTILINE,
        )
    )


def test_rule_candidates_validate_and_cover_required_areas() -> None:
    schema = json.loads((ROOT / "schemas" / "rule.schema.json").read_text())
    rules = yaml.safe_load(
        (ROOT / "standard" / "rules" / "candidates.yaml").read_text()
    )
    source_ids = bibliography_ids()

    assert len(rules) >= 10
    ids = [rule["id"] for rule in rules]
    assert len(ids) == len(set(ids))
    assert set(REQUIRED_RULE_AUTOMATION) <= set(ids)

    for rule in rules:
        jsonschema.Draft202012Validator(schema).validate(rule)
        assert rule["status"] == "candidate"
        if rule["id"] in REQUIRED_RULE_AUTOMATION:
            assert rule["automation"] == REQUIRED_RULE_AUTOMATION[rule["id"]]
        assert rule["source_ids"]
        assert set(rule["source_ids"]) <= source_ids
        assert rule["example_invariants"]
        assert rule["exceptions"]
        assert rule["open_questions"]

    assert {rule["automation"] for rule in rules} == {
        "deterministic",
        "heuristic",
        "human",
    }

    by_id = {rule["id"]: rule for rule in rules}
    terminology_invariants = " ".join(by_id["KSTL-TER-001"]["example_invariants"])
    assert all(
        term in terminology_invariants
        for term in ("전원 차단기", "메인 브레이커", "동일한 개념")
    )
    reference_invariants = " ".join(by_id["KSTL-REF-001"]["example_invariants"])
    assert all(term in reference_invariants for term in ("이것", "제어기", "작성자 의도"))


def test_ter_001_does_not_fail_surface_synonymy_without_term_table() -> None:
    rules = yaml.safe_load(
        (ROOT / "standard" / "rules" / "candidates.yaml").read_text()
    )
    ter = next(rule for rule in rules if rule["id"] == "KSTL-TER-001")
    text = " ".join([ter["rewrite_guidance"], *ter["exceptions"]])
    assert ter["automation"] == "deterministic"
    assert "용어표" in text
    assert "실패로 단정하지" in text
    assert "불명" in text


def test_saf_001_binds_to_safety_hazard_not_admonition_box() -> None:
    rules = yaml.safe_load(
        (ROOT / "standard" / "rules" / "candidates.yaml").read_text()
    )
    saf = next(rule for rule in rules if rule["id"] == "KSTL-SAF-001")
    text = " ".join([saf["title"], saf["rewrite_guidance"], *saf["exceptions"]])
    assert "안전 위험" in text
    assert "#### 경고" in text
    assert "패키지" in text
    assert "번역 고지" in text


def test_vocabulary_is_labeled_as_non_approved_example() -> None:
    schema = json.loads((ROOT / "schemas" / "vocabulary.schema.json").read_text())
    entries = yaml.safe_load(
        (ROOT / "standard" / "vocabulary" / "entries.yaml").read_text()
    )

    assert 3 <= len(entries) <= 5
    ids = [entry["id"] for entry in entries]
    assert len(ids) == len(set(ids))

    for entry in entries:
        jsonschema.Draft202012Validator(schema).validate(entry)
        assert entry["status"] == "example"
        assert "example" in entry["domains"]
        assert set(entry["source_ids"]) <= bibliography_ids()

    assert {"noun", "verb"} <= {entry["part_of_speech"] for entry in entries}
    assert all(
        any(form != entry["lemma"] for form in entry["allowed_forms"])
        for entry in entries
    )
    assert all(entry["discouraged_forms"] for entry in entries)
    assert all(entry["preferred_replacements"] for entry in entries)
    for entry in entries:
        assert set(entry["preferred_replacements"]) <= set(entry["discouraged_forms"])
