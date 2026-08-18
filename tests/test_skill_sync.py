"""preo 스킬 생성물이 규칙 데이터와 동기화되어 있는지 강제한다."""

import importlib.util
import json
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL_MD_PATH = ROOT / "skill" / "preo" / "SKILL.md"
RULES_MD_PATH = ROOT / "skill" / "preo" / "references" / "rules.md"
PLUGIN_JSON_PATH = ROOT / ".claude-plugin" / "plugin.json"
MARKETPLACE_JSON_PATH = ROOT / ".claude-plugin" / "marketplace.json"

HUMAN_RULE_IDS = {"KSTL-SYN-002", "KSTL-REF-001", "KSTL-SAF-001"}


def _load_generator():
    spec = importlib.util.spec_from_file_location(
        "generate_skill", ROOT / "scripts" / "generate_skill.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def gen():
    return _load_generator()


@pytest.fixture(scope="module")
def rules(gen):
    return gen.load_rules()


def test_load_rules_returns_sixteen_rules_in_file_order(rules):
    assert len(rules) == 16
    assert rules[0]["id"] == "KSTL-DOC-001"
    assert rules[-1]["id"] == "KSTL-EXP-006"


def test_partition_splits_human_rules_into_question_gate(gen, rules):
    fix_rules, gate_rules = gen.partition_rules(rules)
    assert {r["id"] for r in gate_rules} == HUMAN_RULE_IDS
    assert len(fix_rules) == 13
    assert not HUMAN_RULE_IDS & {r["id"] for r in fix_rules}


def test_partition_rejects_unknown_automation(gen):
    with pytest.raises(ValueError):
        gen.partition_rules([{"id": "X-1", "automation": "magic"}])


def test_skill_md_render_contains_all_rule_ids_and_notice(gen, rules):
    text = gen.render_skill_md(*gen.partition_rules(rules))
    for rule in rules:
        assert rule["id"] in text
    assert "candidate" in text
    assert "https://github.com/domuk-k/preo" in text
    assert "~/.claude/preo/stats.jsonl" in text
    assert "기록하지 않는다" in text


def test_skill_md_render_gates_human_rules(gen, rules):
    text = gen.render_skill_md(*gen.partition_rules(rules))
    fix_section = text.split("## 고침 규칙")[1].split("## 질문 게이트 규칙")[0]
    gate_section = text.split("## 질문 게이트 규칙")[1].split("## 통계")[0]
    for rule_id in HUMAN_RULE_IDS:
        assert rule_id not in fix_section
        assert rule_id in gate_section


def test_rules_md_render_contains_examples_and_guidance(gen, rules):
    text = gen.render_rules_md(rules)
    for rule in rules:
        assert rule["id"] in text
        assert rule["approved_examples"][0] in text
        assert rule["unapproved_examples"][0] in text


def test_skill_md_render_puts_meaning_before_fluency_and_forbids_scores(gen, rules):
    text = gen.render_skill_md(*gen.partition_rules(rules))
    assert "뜻을 읽힘보다 앞에" in text
    assert "바꿔 말한다" in text
    assert "Accuracy" in text
    assert "부분 점수를 주지 않는다" in text
    assert "BLEU" in text
    assert "이해되는지 봐줘" in text


def test_skill_md_render_has_write_mode_with_exp_rules_in_fix_table(gen, rules):
    text = gen.render_skill_md(*gen.partition_rules(rules))
    assert "## 쓰기 모드" in text
    fix_section = text.split("## 고침 규칙")[1].split("## 질문 게이트 규칙")[0]
    for n in range(1, 7):
        assert f"KSTL-EXP-00{n}" in fix_section


def test_generated_files_exist_and_match_generator_output(gen):
    assert SKILL_MD_PATH.exists(), "skill/preo/SKILL.md가 없다"
    assert RULES_MD_PATH.exists(), "skill/preo/references/rules.md가 없다"
    assert gen.generate(check=True) == 0, (
        "생성물이 candidates.yaml과 어긋난다. "
        "uv run python scripts/generate_skill.py를 실행할 것"
    )


def test_skill_md_frontmatter_declares_name_and_version(gen):
    frontmatter = yaml.safe_load(SKILL_MD_PATH.read_text(encoding="utf-8").split("---")[1])
    assert frontmatter["name"] == "preo"
    assert frontmatter["version"] == gen.SKILL_VERSION


def test_plugin_manifest_matches_skill_frontmatter(gen):
    plugin = json.loads(PLUGIN_JSON_PATH.read_text(encoding="utf-8"))
    frontmatter = yaml.safe_load(SKILL_MD_PATH.read_text(encoding="utf-8").split("---")[1])
    assert plugin["name"] == frontmatter["name"] == "preo"
    assert plugin["version"] == frontmatter["version"] == gen.SKILL_VERSION
    assert plugin["skills"] == ["./skill/preo"]


def test_marketplace_manifest_serves_preo_at_preo():
    marketplace = json.loads(MARKETPLACE_JSON_PATH.read_text(encoding="utf-8"))
    assert marketplace["name"] == "preo"
    entries = {p["name"]: p for p in marketplace["plugins"]}
    assert entries["preo"]["source"] == "./"
