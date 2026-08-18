import json
from pathlib import Path

import jsonschema
import yaml


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_SOURCE_IDS = {
    "dtaq.ram-terms",
    "molit.aim-quality-manual",
    "molit.construction-standards",
    "lh.specifications",
    "molit.environmental-cost-guide",
    "kobaco.production-safety-guide",
    "kubernetes.ko-docs",
    "python.ko-docs",
    "mdn.ko-content",
    "kdca.practice-guidelines",
}
REQUIRED_DOMAINS = {"public", "safety-mechanical", "aviation-transport", "it"}


def load_sources() -> list[dict]:
    return yaml.safe_load((ROOT / "research" / "corpus-sources.yaml").read_text())


def test_corpus_registry_is_schema_valid_with_unique_ids() -> None:
    schema = json.loads((ROOT / "schemas" / "corpus-source.schema.json").read_text())
    sources = load_sources()
    ids = []
    for source in sources:
        jsonschema.Draft202012Validator(
            schema, format_checker=jsonschema.FormatChecker()
        ).validate(source)
        ids.append(source["id"])
    assert len(ids) == len(set(ids))


def test_corpus_registry_has_all_required_candidates_and_domains() -> None:
    sources = load_sources()
    ids = {source["id"] for source in sources}
    domains = {domain for source in sources for domain in source["domains"]}
    assert len(sources) >= 10
    assert REQUIRED_SOURCE_IDS <= ids
    assert REQUIRED_DOMAINS <= domains


def test_all_corpus_candidates_record_a_nonempty_estimated_size() -> None:
    missing_or_empty = [
        source["id"]
        for source in load_sources()
        if not str(source.get("estimated_size", "")).strip()
    ]
    assert missing_or_empty == []


def test_all_phase_zero_sources_remain_candidates() -> None:
    offenders = [
        source["id"]
        for source in load_sources()
        if source["collection_status"] != "candidate"
    ]
    assert offenders == []


def test_uninspected_payloads_remain_metadata_only_with_unknown_derivatives() -> None:
    sources = {source["id"]: source for source in load_sources()}
    required_rights = {
        "molit.construction-standards": {
            "redistribution": "metadata-only",
            "derivatives": "unknown",
        },
        "lh.specifications": {
            "redistribution": "metadata-only",
            "derivatives": "unknown",
        },
        "molit.environmental-cost-guide": {
            "redistribution": "metadata-only",
            "derivatives": "unknown",
        },
    }
    actual_rights = {
        source_id: {
            "redistribution": sources[source_id]["redistribution"],
            "derivatives": sources[source_id]["derivatives"],
        }
        for source_id in required_rights
    }
    assert actual_rights == required_rights


def test_unclear_rights_never_mark_collected() -> None:
    offenders = [
        source["id"]
        for source in load_sources()
        if source["collection_status"] == "collected"
        and (
            source["redistribution"] == "unknown"
            or source["derivatives"] == "unknown"
        )
    ]
    assert offenders == []
