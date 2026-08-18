# sulsul 스킬 v0 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `standard/rules/candidates.yaml`에서 결정론적으로 생성되는 Claude Code 스킬 sulsul(술술)을 만들고, 설치 매니페스트·동기화 테스트·파일럿 기록까지 갖춘다.

**Architecture:** 규칙 데이터(YAML)가 단일 원천이다. `scripts/generate_skill.py`가 `skill/sulsul/SKILL.md`(동작 규약)와 `skill/sulsul/references/rules.md`(규칙 상세)를 생성하고, `tests/test_skill_sync.py`가 생성물과 데이터의 byte 단위 일치를 강제한다. `.claude-plugin/` 매니페스트가 `/plugin install sulsul@kstl` 설치를 제공한다. 스킬 자체는 순수 마크다운이며 런타임 코드가 없다.

**Tech Stack:** Python 3.11+(stdlib + PyYAML — 이미 의존성에 있음), pytest 8(uv 실행), Claude Code plugin manifest(JSON).

**Spec:** `docs/superpowers/specs/2026-08-10-sulsul-skill-v0-design.md`

## Global Constraints

- 생성기는 결정론적이다: 같은 입력에서 byte 동일 출력. 타임스탬프·난수 금지.
- 새 런타임 의존성을 추가하지 않는다(`pyproject.toml` 무변경).
- 규칙 본문을 손으로 쓰지 않는다. 스킬의 규칙 내용은 전부 `candidates.yaml` 필드에서 나온다.
- `automation: human` 규칙(KSTL-SYN-002, KSTL-REF-001, KSTL-SAF-001)은 질문 게이트로 렌더링한다 — 조용히 고치지 않는다.
- 스킬 이름은 `sulsul`, 버전은 `0.1.0`, 마켓플레이스 이름은 `kstl`(설치 구문 `sulsul@kstl`).
- SKILL.md에 candidate 단계 고지와 `https://github.com/domuk-k/kstl` 링크를 넣는다.
- stats 규약: `~/.claude/sulsul/stats.jsonl`, 규칙 ID와 수치만 기록, 문서 내용·파일명·경로 비기록, 로컬 전용, 쓰기 실패 시 조용히 생략.
- 제3자 표준·사전·논문 본문을 저장소에 커밋하지 않는다. 외부 파일럿 기록은 규칙 히트 통계만 남기고 원문 문장을 재배포하지 않는다.
- 규칙은 16개다: 기존 10개 + 번역투·AI투 표현 규칙 KSTL-EXP-001~006 (2026-08-10 오피스아워 설계 반영). EXP 규칙의 automation 판정 규칙: 비승인 표현이 표면형 목록으로 열거 가능하고 예외가 유한하면 `heuristic`, 문맥 해석 없이 판정 불가면 `human`. EXP 규칙에 `deterministic`은 부여하지 않는다(기존 TER-001·STY-001은 유지). 6개 모두 `heuristic`이 되도록 후보 표현군을 고른다 — heuristic이 불가능한 표현군은 다른 후보로 교체한다.
- 신규 출처는 규칙 작성 전에 `research/bibliography.md`에 기존 항목 형식(`## <id>` 앵커, 제목/저자·기관/발행 정보/정식 URL/자료 유형/접근 상태/재사용 메모)으로 추가한다. `tests/test_standard_data.py`가 `source_ids ⊆ bibliography_ids`를 강제한다.
- 3자 비교·파일럿 기록에는 원문·산출문을 저장하지 않는다. 문단 인덱스, 선호 변형, 규칙 ID별 수락·거절 수 등 익명 통계만 남긴다.
- 모든 커밋 전에 `uv run pytest -q`와 `uv run python scripts/validate_links.py`가 통과해야 한다.
- 커밋 메시지에 작성 도구 트레일러(`Co-Authored-By`)를 붙인다. 세션 URL 등 개인 작업 환경 식별자는 저장소 문서에 남기지 않는다.

## File Structure

```text
research/bibliography.md            신규 출처 항목 추가(수정, Task 0)
standard/rules/candidates.yaml      KSTL-EXP-001~006 추가(수정, Task 0)
scripts/generate_skill.py           생성기(신규) — load/partition/render/generate
skill/sulsul/SKILL.md               생성물(신규) — 커밋함
skill/sulsul/references/rules.md    생성물(신규) — 커밋함
.claude-plugin/plugin.json          플러그인 매니페스트(신규)
.claude-plugin/marketplace.json     마켓플레이스 매니페스트(신규)
tests/test_skill_sync.py            단위 + 동기화 + 매니페스트 테스트(신규)
docs/pilot/2026-08-sulsul-dogfood.md   내부 파일럿 기록(신규)
docs/pilot/2026-08-sulsul-external.md  외부 파일럿 기록(신규)
README.md                           스킬 안내 한 단락(수정)
docs/HANDOFF.md                     상태 갱신 한 단락(수정)
```

---

### Task 0: 번역투·AI투 표현 규칙 팩 (서지 선행)

**Files:**
- Modify: `research/bibliography.md` (신규 출처 항목)
- Modify: `standard/rules/candidates.yaml` (KSTL-EXP-001~006, 파일 끝에 추가)
- Modify: 규칙 수를 고정하는 기존 테스트가 있으면 16으로 갱신

**Interfaces:**
- Consumes: 기존 서지 항목 형식, `schemas/rule.schema.json`(필수 14필드, additionalProperties false)
- Produces: KSTL-EXP-001~006 — Task 1의 `load_rules()`가 그대로 소비한다. 파일 끝에 추가하므로 `rules[-1]["id"] == "KSTL-EXP-006"`. 6개 모두 `automation: heuristic`.

이 태스크는 리서치 태스크다. 규칙 본문은 출처 검증 결과에 따라 확정되므로 아래는 절차·품질 게이트·완성 예시다.

- [ ] **Step 1: 출처 검증**

이미 서지에 있는 항목을 우선 재사용한다: `nikl-plain-language-guideline-2021`(국립국어원 2021 행정문서 표현 개선 지침), `nikl-easy-public-doc-guide`(쉬운 공문서 쓰기 길잡이). WebFetch로 각 자료(또는 그 공식 소개 페이지)가 다루는 다듬기 대상 표현을 확인하고, 후보 표현군 중 어느 것이 어느 출처에 근거하는지 표로 정리한다. 기존 서지로 부족한 표현군은 국립국어원 공공언어 자료(예: 「한눈에 알아보는 공공언어 바로 쓰기」, 다듬은 말 목록) 중 공식 페이지를 확인해 신규 서지 항목으로 추가한다. 원문 PDF는 커밋하지 않는다.

- [ ] **Step 2: 표현군 6개 선정과 규칙 작성**

후보 표현군(출처 확인되는 것 중 6개 선택, heuristic 판정이 가능한 것만):

1. 이중 피동 ("-되어지다", "-지게 되다")
2. "~에 대하여/대한" 남용
3. "~를/을 통해" 남용
4. "~에 있어서"
5. 명사화 남용 ("~함으로써", "~에 의한")
6. 영어식 복수 "-들" 남용
7. "~의 경우" 남용
8. AI 상투 수식어("다양한", "원활한", "성공적으로" 남용) — 공식 출처가 확보되는 경우에만

각 규칙은 필수 14필드를 전부 채운다: `id, title, purpose, scope, normativity, status, automation, approved_examples, unapproved_examples, example_invariants, rewrite_guidance, source_ids, exceptions, open_questions`. 형식 모델(첫 규칙 예시 — purpose·source_ids는 Step 1 검증 결과로 확정):

```yaml
- id: KSTL-EXP-001
  title: 이중 피동 표현을 쓰지 않는다
  purpose: >-
    (Step 1에서 확인한 출처가) 행정문서 표현 개선 대상으로 이중 피동을
    다룬다는 사실에 근거한 후보다. 개발자 문서에서의 가독성 효과는
    검증되지 않았으며 후속 파일럿에서 평가한다.
  scope: [description, procedure]
  normativity: should
  status: candidate
  automation: heuristic
  approved_examples:
    - 설정 파일이 로드되면 캐시가 갱신됩니다.
  unapproved_examples:
    - 설정 파일이 로드되어지면 캐시가 갱신되어집니다.
  example_invariants:
    - 두 예문 모두 설정 파일 로드 시 캐시가 갱신된다는 같은 조건-결과 관계를 진술한다.
  rewrite_guidance: >-
    "-되어지다", "-지게 되다" 형태를 찾아 단일 피동("-되다") 또는
    능동형으로 바꾼다. 인용문과 고유명사 안의 표기는 바꾸지 않는다.
  source_ids: [nikl-plain-language-guideline-2021]
  exceptions:
    - 원문 인용, 오류 메시지 문자열, 외부 API 응답 예시는 고치지 않는다.
  open_questions:
    - 개발자 문서 코퍼스에서 이중 피동의 출현 빈도와 수정 수락률은 어떠한가?
```

작성 규율: purpose는 "출처가 이 표현을 다듬기 대상으로 다룬다"는 사실만 진술하고 효과를 주장하지 않는다. 예문 쌍은 개발자 문서 장르(README·가이드·API 문서)로 자작한다. 출처 문헌의 예문을 옮겨 적지 않는다.

- [ ] **Step 3: 검증**

Run: `uv run pytest -q && uv run python scripts/validate_links.py`
Expected: 스키마·서지 참조 테스트 통과. 규칙 수를 고정하는 단언이 있어 실패하면 그 단언을 16으로 갱신하고 재실행한다.

- [ ] **Step 4: 커밋**

```bash
git add research/bibliography.md standard/rules/candidates.yaml tests/
git commit -m "feat: add KSTL-EXP translationese rule candidates with sources"
```

---

### Task 1: 생성기와 렌더링 테스트

**Files:**
- Create: `scripts/generate_skill.py`
- Test: `tests/test_skill_sync.py`

**Interfaces:**
- Consumes: `standard/rules/candidates.yaml` (규칙 16개, 각각 `id/title/purpose/scope/normativity/status/automation/approved_examples/unapproved_examples/example_invariants/rewrite_guidance/source_ids/exceptions/open_questions` 필드 보유)
- Produces (Task 2·3의 테스트와 실행이 의존):
  - `load_rules() -> list[dict]` — YAML 파일 순서 유지, id 중복 시 `ValueError`
  - `partition_rules(rules: list[dict]) -> tuple[list[dict], list[dict]]` — (고침 규칙, 질문 게이트 규칙). 알 수 없는 `automation` 값이면 `ValueError`
  - `render_skill_md(fix_rules: list[dict], gate_rules: list[dict]) -> str`
  - `render_rules_md(rules: list[dict]) -> str`
  - `generate(check: bool = False) -> int` — `check=False`면 파일 기록 후 0, `check=True`면 디스크와 비교해 일치 0 / 불일치 1
  - CLI: `uv run python scripts/generate_skill.py [--check]`
  - 모듈 상수: `SKILL_VERSION = "0.1.0"`, `SKILL_MD`, `RULES_MD` (Path)

- [ ] **Step 1: 실패하는 렌더링 테스트 작성**

`tests/test_skill_sync.py` 생성:

```python
"""sulsul 스킬 생성물이 규칙 데이터와 동기화되어 있는지 강제한다."""

import importlib.util
import json
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL_MD_PATH = ROOT / "skill" / "sulsul" / "SKILL.md"
RULES_MD_PATH = ROOT / "skill" / "sulsul" / "references" / "rules.md"
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
    assert "https://github.com/domuk-k/kstl" in text
    assert "~/.claude/sulsul/stats.jsonl" in text
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


def test_skill_md_render_has_write_mode_with_exp_rules_in_fix_table(gen, rules):
    text = gen.render_skill_md(*gen.partition_rules(rules))
    assert "## 쓰기 모드" in text
    fix_section = text.split("## 고침 규칙")[1].split("## 질문 게이트 규칙")[0]
    for n in range(1, 7):
        assert f"KSTL-EXP-00{n}" in fix_section
```

- [ ] **Step 2: 실패 확인**

Run: `uv run pytest tests/test_skill_sync.py -q`
Expected: 전 테스트 ERROR — `scripts/generate_skill.py`가 없어 `_load_generator`가 실패한다.

- [ ] **Step 3: 생성기 구현**

`scripts/generate_skill.py` 생성(전문):

```python
#!/usr/bin/env python3
"""standard/rules/candidates.yaml에서 skill/sulsul/ 산출물을 생성한다.

결정론적이다: 같은 입력에서 byte 동일 출력을 낸다. 타임스탬프를 쓰지 않는다.
--check는 디스크의 산출물이 최신 생성 결과와 일치하는지 검사한다(불일치 시 1).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
RULES_PATH = ROOT / "standard" / "rules" / "candidates.yaml"
SKILL_MD = ROOT / "skill" / "sulsul" / "SKILL.md"
RULES_MD = ROOT / "skill" / "sulsul" / "references" / "rules.md"

SKILL_VERSION = "0.1.0"
REPO_URL = "https://github.com/domuk-k/kstl"
STATS_PATH = "~/.claude/sulsul/stats.jsonl"
GENERATED_NOTICE = (
    "<!-- scripts/generate_skill.py가 standard/rules/candidates.yaml에서"
    " 생성한 파일이다. 직접 수정하지 말 것. -->"
)

FIX_AUTOMATION = {"deterministic", "heuristic"}
GATE_AUTOMATION = {"human"}


def load_rules() -> list[dict]:
    rules = yaml.safe_load(RULES_PATH.read_text(encoding="utf-8"))
    ids = [rule["id"] for rule in rules]
    if len(ids) != len(set(ids)):
        raise ValueError("candidates.yaml에 중복된 규칙 id가 있다")
    return rules


def partition_rules(rules: list[dict]) -> tuple[list[dict], list[dict]]:
    fix_rules: list[dict] = []
    gate_rules: list[dict] = []
    for rule in rules:
        automation = rule["automation"]
        if automation in FIX_AUTOMATION:
            fix_rules.append(rule)
        elif automation in GATE_AUTOMATION:
            gate_rules.append(rule)
        else:
            raise ValueError(f"{rule['id']}: 알 수 없는 automation 값 {automation!r}")
    return fix_rules, gate_rules


def render_skill_md(fix_rules: list[dict], gate_rules: list[dict]) -> str:
    fix_table = "\n".join(
        f"| {r['id']} | {r['title']} | {r['automation']} |" for r in fix_rules
    )
    gate_table = "\n".join(f"| {r['id']} | {r['title']} |" for r in gate_rules)
    return f"""---
name: sulsul
description: >-
  한국어 기술문서를 술술 읽히게 고치고, 쓸 때부터 술술 읽히게 쓰는 스킬.
  "술술하게 해줘", "이 문서 검사만 해줘" 같은 교정 요청과 "KSTL로 써줘",
  "술술 문체로 써줘" 같은 한국어 문서 작성 요청, 한국어 README·가이드·API
  문서를 다루는 작업에 사용한다. KSTL 규칙 후보에 근거해 고치고, 요청 시
  이유를 설명한다.
version: {SKILL_VERSION}
---

{GENERATED_NOTICE}

# sulsul — 한국어 기술문서를 술술 읽히게

이 스킬의 규칙은 [KSTL]({REPO_URL}) 규칙 후보다. 모든 규칙은 candidate
단계이며 아직 확정 표준이 아니다. 규칙 본문의 단일 원천은 KSTL 저장소의
`standard/rules/candidates.yaml`이다.

## 동작

1. 기본 동작은 고치기다. 문서에서 고침 규칙에 걸리는 문장을 재작성한다.
2. 고치기 전에 [references/rules.md](references/rules.md)를 읽고 각 규칙의
   예문 쌍과 예외를 판정 기준으로 삼는다.
3. 고친 결과를 보여준 뒤 마지막에 한 줄로 요약한다. 형식:
   `SYN-001 ×2 · TER-001 ×1 고침 · 나머지 이미 좋음`.
4. 걸린 문장이 적으면 "이미 잘 읽힙니다 — N곳만 고쳤습니다"라고 말하고
   억지로 고치지 않는다.
5. "검사만" 요청이면 고치지 않고 걸린 문장, 규칙 ID, 위치만 보고한다.
6. "왜 바꿨어?" 요청이면 그때만 규칙 ID, 근거, 연구 출처를 설명한다.
   근거는 references/rules.md의 근거 메모에서 가져온다.
7. 질문 게이트 규칙에 걸리는 문장은 조용히 고치지 않는다. 가능한 해석
   후보를 담아 한 줄로 묻는다. 예: "센서 설치, 누가 합니까? ① 작업자
   ② 정비사".
8. 범위와 강도 조정은 자연어로 받는다. "이 문단만"이면 그 범위만
   처리하고, "가볍게"면 확실한 위반만 고친다. 별도 플래그는 없다.

## 쓰기 모드

사용자가 한국어 문서 작성을 요청하며 "KSTL로", "술술 문체로" 등을
언급하면 고치기가 아니라 쓰기에 규칙을 적용한다.

1. 작성 전에 [references/rules.md](references/rules.md)의 고침 규칙을
   읽고 작성 제약으로 삼는다.
2. 초안을 문장 단위로 자기 검사해 규칙 위반을 작성 중에 제거한다.
3. 산출물 끝에 한 줄 요약을 붙인다. 형식: `적용: EXP-001 ×2 · SYN-001 ×1`.
4. 질문 게이트 규칙에 해당하는 정보(예: 행위자)가 입력에 없으면
   추측하지 않고 묻는다.

## 보존 보장

- 코드 블록, 셸 명령, URL, 파일 경로, 숫자와 단위, 오류 문자열은 byte
  단위로 보존한다.
- 재작성은 문장의 행위자, 대상, 조건, 순서, 양태를 바꾸지 않는다.
- 원문에 없는 정보를 추가하지 않는다. 확실하지 않으면 묻는다.

## 고침 규칙

| ID | 규칙 | 자동화 |
|---|---|---|
{fix_table}

## 질문 게이트 규칙

| ID | 규칙 |
|---|---|
{gate_table}

규칙별 예문, 재작성 지침, 예외, 근거는
[references/rules.md](references/rules.md)에 있다.

## 통계

- 실행을 마치면 `{STATS_PATH}`에 JSON 한 줄을 추가한다. 형식:
  `{{"date": "YYYY-MM-DD", "checked": 검사한 문장 수, "fixed": 고친 문장 수,
  "hits": {{"KSTL-SYN-001": 2}}}}`.
- checked는 검사한 문장 수, fixed는 재작성한 문장 수, hits는 규칙별로
  걸린 문장 수다. 한 문장이 여러 규칙에 걸리면 각 규칙에 1씩 세므로
  hits 합계는 fixed보다 클 수 있다.
- 문서 내용, 파일명, 경로는 기록하지 않는다. 통계는 로컬 파일에만 남고
  외부로 전송하지 않는다. 삭제하려면 파일을 지우면 된다.
- "통계 보여줘" 요청이면 파일을 읽어 누적 고친 문장 수, 최다 발동 규칙,
  공유용 한 줄("sulsul이 두 번 읽게 만드는 문장 N개를 없앴습니다")을
  출력한다.
- 통계 파일을 쓸 수 없으면 조용히 건너뛰고 기록만 생략한다.
"""


def render_rules_md(rules: list[dict]) -> str:
    sections = []
    for rule in rules:
        mode = "질문 게이트" if rule["automation"] in GATE_AUTOMATION else "고침"
        approved = "\n".join(f"  - {ex}" for ex in rule["approved_examples"])
        unapproved = "\n".join(f"  - {ex}" for ex in rule["unapproved_examples"])
        invariants = "\n".join(f"  - {inv}" for inv in rule["example_invariants"])
        exceptions = "\n".join(f"  - {ex}" for ex in rule["exceptions"])
        sources = ", ".join(rule["source_ids"])
        sections.append(
            f"""## {rule['id']} — {rule['title']}

- 처리: {mode} ({rule['automation']})
- 적용 범위: {', '.join(rule['scope'])}
- 승인 예문:
{approved}
- 비승인 예문:
{unapproved}
- 의미 불변식:
{invariants}
- 재작성 지침: {rule['rewrite_guidance'].strip()}
- 예외:
{exceptions}
- 근거 메모({sources}): {rule['purpose'].strip()}"""
        )
    body = "\n\n".join(sections)
    return f"""{GENERATED_NOTICE}

# sulsul 규칙 상세

모든 규칙은 KSTL candidate 단계다. 근거 메모는 각 규칙이 아직 검증
가설임을 설명한다. 재작성 판정은 승인/비승인 예문 쌍을 기준으로 한다.

{body}
"""


def generate(check: bool = False) -> int:
    rules = load_rules()
    fix_rules, gate_rules = partition_rules(rules)
    outputs = {
        SKILL_MD: render_skill_md(fix_rules, gate_rules),
        RULES_MD: render_rules_md(rules),
    }
    if check:
        stale = [
            str(path.relative_to(ROOT))
            for path, content in outputs.items()
            if not path.exists() or path.read_text(encoding="utf-8") != content
        ]
        if stale:
            print("생성물이 오래되었다. scripts/generate_skill.py를 실행할 것:")
            for name in stale:
                print(f"  {name}")
            return 1
        return 0
    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"생성함: {path.relative_to(ROOT)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return generate(check=args.check)


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: 테스트 통과 확인**

Run: `uv run pytest tests/test_skill_sync.py -q`
Expected: 7 passed (렌더링은 메모리에서 검증되므로 파일 생성 전에도 통과한다.)

- [ ] **Step 5: 전체 스위트 확인 후 커밋**

Run: `uv run pytest -q`
Expected: Task 0 완료 시점 스위트 + 신규 7개 = 91 passed (Task 0에서 기존 개수가 84에서 변했다면 그만큼 보정)

```bash
git add scripts/generate_skill.py tests/test_skill_sync.py
git commit -m "feat: add deterministic sulsul skill generator"
```

---

### Task 2: 산출물 생성·커밋과 동기화 테스트

**Files:**
- Create: `skill/sulsul/SKILL.md` (생성기로 생성)
- Create: `skill/sulsul/references/rules.md` (생성기로 생성)
- Modify: `tests/test_skill_sync.py` (동기화 테스트 추가)

**Interfaces:**
- Consumes: Task 1의 `generate(check=True)`, `SKILL_MD_PATH`/`RULES_MD_PATH` 상수
- Produces: 커밋된 `skill/sulsul/` 산출물 — Task 3 매니페스트와 Task 4·5 파일럿이 이 파일을 참조한다

- [ ] **Step 1: 실패하는 동기화 테스트 추가**

`tests/test_skill_sync.py` 끝에 추가:

```python
def test_generated_files_exist_and_match_generator_output(gen):
    assert SKILL_MD_PATH.exists(), "skill/sulsul/SKILL.md가 없다"
    assert RULES_MD_PATH.exists(), "skill/sulsul/references/rules.md가 없다"
    assert gen.generate(check=True) == 0, (
        "생성물이 candidates.yaml과 어긋난다. "
        "uv run python scripts/generate_skill.py를 실행할 것"
    )


def test_skill_md_frontmatter_declares_name_and_version(gen):
    frontmatter = yaml.safe_load(SKILL_MD_PATH.read_text(encoding="utf-8").split("---")[1])
    assert frontmatter["name"] == "sulsul"
    assert frontmatter["version"] == gen.SKILL_VERSION
```

- [ ] **Step 2: 실패 확인**

Run: `uv run pytest tests/test_skill_sync.py -q`
Expected: 신규 2개 FAIL — 산출물 파일이 아직 없다.

- [ ] **Step 3: 생성기 실행**

Run: `uv run python scripts/generate_skill.py`
Expected: `생성함: skill/sulsul/SKILL.md`, `생성함: skill/sulsul/references/rules.md`

- [ ] **Step 4: 산출물 육안 확인**

`skill/sulsul/SKILL.md`를 열어 확인한다: frontmatter(name/description/version), 고침 규칙 표 13행(KSTL-EXP-001~006 포함), 질문 게이트 표 3행(KSTL-SYN-002·KSTL-REF-001·KSTL-SAF-001), 쓰기 모드 섹션, 통계 섹션. `references/rules.md`에 규칙 16개 섹션과 예문 쌍이 있는지 확인한다.

- [ ] **Step 5: 테스트·링크 검증 통과 확인 후 커밋**

Run: `uv run pytest -q && uv run python scripts/validate_links.py`
Expected: 93 passed, 링크 검증 통과

```bash
git add skill/ tests/test_skill_sync.py
git commit -m "feat: generate sulsul skill artifacts from rule candidates"
```

---

### Task 3: 플러그인 매니페스트와 저장소 문서 반영

**Files:**
- Create: `.claude-plugin/plugin.json`
- Create: `.claude-plugin/marketplace.json`
- Modify: `tests/test_skill_sync.py` (매니페스트 테스트 추가)
- Modify: `README.md` (「빠른 확인」 섹션에 한 줄 추가)
- Modify: `docs/HANDOFF.md` (상태 한 단락 추가)

**Interfaces:**
- Consumes: Task 2의 커밋된 SKILL.md frontmatter(name `sulsul`, version `0.1.0`)
- Produces: `/plugin marketplace add domuk-k/kstl` → `/plugin install sulsul@kstl` 설치 경로

- [ ] **Step 1: 실패하는 매니페스트 테스트 추가**

`tests/test_skill_sync.py` 끝에 추가:

```python
def test_plugin_manifest_matches_skill_frontmatter(gen):
    plugin = json.loads(PLUGIN_JSON_PATH.read_text(encoding="utf-8"))
    frontmatter = yaml.safe_load(SKILL_MD_PATH.read_text(encoding="utf-8").split("---")[1])
    assert plugin["name"] == frontmatter["name"] == "sulsul"
    assert plugin["version"] == frontmatter["version"] == gen.SKILL_VERSION
    assert plugin["skills"] == ["./skill/sulsul"]


def test_marketplace_manifest_serves_sulsul_at_kstl():
    marketplace = json.loads(MARKETPLACE_JSON_PATH.read_text(encoding="utf-8"))
    assert marketplace["name"] == "kstl"
    entries = {p["name"]: p for p in marketplace["plugins"]}
    assert entries["sulsul"]["source"] == "./"
```

- [ ] **Step 2: 실패 확인**

Run: `uv run pytest tests/test_skill_sync.py -q`
Expected: 신규 2개 FAIL — 매니페스트 파일이 없다.

- [ ] **Step 3: 매니페스트 작성**

`.claude-plugin/plugin.json` 생성:

```json
{
  "name": "sulsul",
  "version": "0.1.0",
  "description": "한국어 기술문서를 술술 읽히게 고치는 스킬. KSTL 규칙 후보에서 생성된다.",
  "author": { "name": "KSTL project" },
  "homepage": "https://github.com/domuk-k/kstl",
  "skills": ["./skill/sulsul"]
}
```

`.claude-plugin/marketplace.json` 생성:

```json
{
  "name": "kstl",
  "owner": { "name": "domuk-k" },
  "plugins": [
    {
      "name": "sulsul",
      "source": "./",
      "description": "한국어 기술문서를 술술 읽히게 고치는 스킬. KSTL 규칙 후보에서 생성된다."
    }
  ]
}
```

- [ ] **Step 4: 테스트 통과 확인**

Run: `uv run pytest tests/test_skill_sync.py -q`
Expected: PASS (누적 13개)

- [ ] **Step 5: README와 HANDOFF 반영**

`README.md`의 「빠른 확인」 목록 끝에 추가:

```markdown
- 스킬: [skill/sulsul/SKILL.md](skill/sulsul/SKILL.md) —
  `standard/rules/candidates.yaml`에서 생성되는 한국어 기술문서 교정 스킬.
  설치는 `/plugin marketplace add domuk-k/kstl` 후 `/plugin install sulsul@kstl`.
```

`docs/HANDOFF.md`의 첫 인용 블록(문서 상태 요약) 끝에 한 문장 추가:

```markdown
> 2026-08-10에 규칙 후보에서 생성되는 sulsul 스킬 v0을 추가했다. 설계는
> `docs/superpowers/specs/2026-08-10-sulsul-skill-v0-design.md`, 구현 계획은
> `docs/superpowers/plans/2026-08-10-sulsul-skill-v0.md`에 있다.
```

(HANDOFF의 실제 블록 인용 형식에 맞춰 이어 붙인다. 기존 문장은 수정하지 않는다.)

- [ ] **Step 6: 전체 검증 후 커밋**

Run: `uv run pytest -q && uv run python scripts/validate_links.py`
Expected: 95 passed, 링크 검증 통과

```bash
git add .claude-plugin/ tests/test_skill_sync.py README.md docs/HANDOFF.md
git commit -m "feat: add sulsul plugin manifests and repo docs links"
```

---

### Task 4: 내부 dogfood와 3자 비교 준비

**Files:**
- Create: `docs/pilot/2026-08-sulsul-dogfood.md`
- Create: `docs/pilot/2026-08-sulsul-comparison.md`

**Interfaces:**
- Consumes: Task 2의 `skill/sulsul/references/rules.md` (판정 기준, 규칙 16개)
- Produces: 스펙 성공 기준의 dogfood 기록과, 사람 평가자가 수행할 3자 비교의
  프로토콜·기록 양식. Task 6의 성공 기준 대조가 두 파일을 확인한다.

이 태스크는 코드가 아니라 스킬 리허설과 실험 준비다. 실제 3자 비교 평가는
사람(동료 3명 이상)이 수행하므로 이 태스크는 준비물까지만 만든다.

- [ ] **Step 1: dogfood 기록 파일 골격 작성**

`docs/pilot/2026-08-sulsul-dogfood.md` 생성:

```markdown
# sulsul 내부 dogfood 기록 (2026-08)

sulsul v0의 규칙(skill/sulsul/references/rules.md)을 KSTL 저장소 자체
문서에 적용한 기록이다. 목적은 규칙 후보의 오탐·정탐 경향 관찰이다.
문서를 실제로 수정하지는 않는다.

## 대상

- README.md 전체
- docs/HANDOFF.md 1절, 2절

## 판정 기록

| 위치 | 문장 요지 | 규칙 | 판정 | 메모 |
|---|---|---|---|---|

판정 값: 정탐(규칙 위반이 맞고 고치면 나아짐), 오탐(걸렸지만 고치면
어색하거나 의미가 바뀜), 게이트(질문 게이트 규칙에 걸림).

## 집계

- 검사 문장 수:
- 규칙별 히트: (규칙 16개 전부를 `규칙ID ×N`으로, 0 포함)
- 오탐 수와 원인 메모:

## 관찰

(규칙 표현을 조정할 필요가 보이면 여기 적는다. 조정 자체는 별도 작업으로
standard/rules/candidates.yaml에서 한다.)
```

- [ ] **Step 2: README.md 판정 수행**

`README.md`의 한국어 문장을 위에서부터 규칙 16개에 대조한다. 걸리는 문장마다 판정 기록 표에 한 행을 추가한다. 위치는 `README.md:줄번호` 형식으로 적는다.

- [ ] **Step 3: HANDOFF 1·2절 판정 수행**

같은 방식으로 `docs/HANDOFF.md` 1절과 2절을 판정하고 표에 추가한다.

- [ ] **Step 4: 집계 작성**

검사 문장 수(공백·표 제외 서술 문장 기준), 규칙별 히트 수(16개 전부, 0 포함), 오탐 수를 집계 섹션에 채운다.

- [ ] **Step 5: 3자 비교 프로토콜·기록 양식 작성**

`docs/pilot/2026-08-sulsul-comparison.md` 생성:

```markdown
# sulsul 3자 비교 파일럿 — 프로토콜과 기록 양식 (2026-08)

같은 한국어 기술문서 문단을 세 방식으로 만들어 한국어 화자가 블라인드로
비교한다: ① vanilla Claude ② Matt Pocock writing-for-agents 적용
③ sulsul 적용. 목적은 sulsul 규칙 팩이 실제 선호를 얻는지 확인하는 것이다.

## 프로토콜

1. 소스: 동료가 Claude로 작성한 실제 문서에서 문단 20개를 고른다.
   문서 제공자의 동의를 먼저 받는다.
2. 변형 생성: 문단마다 세 변형을 만든다. 생성 프롬프트는 세 변형 모두
   같고, 적용 스킬만 다르다.
3. 블라인딩: 문단마다 세 변형을 무작위 순서로 A/B/C 라벨을 붙여 제시한다.
   평가자는 어느 라벨이 어느 방식인지 모른다. 라벨-방식 대응표는 평가가
   끝날 때까지 진행자만 본다.
4. 평가: 평가자 3명 이상. 문단당 "가장 자연스러운 한국어" 1표.
   sulsul 변형의 편집 각각에 수락/거절도 표시한다.
5. 저장: 원문과 산출문은 이 저장소에 저장하지 않는다. 아래 양식의
   익명 통계만 기록한다.

## 기록 양식

- 평가 일자:
- 평가자 수:
- 문단 수:
- 선호 집계: vanilla ___표 / writing-for-agents ___표 / sulsul ___표
- sulsul 편집 수락/거절 (규칙별): (예: EXP-001 수락 4 / 거절 1)
- 관찰 메모: (문장 인용 없이 경향만)

## 판정

- sulsul이 선호 다수를 얻으면: 규칙 팩 유지, 공개 데모 검토.
- 얻지 못하면: 거절이 많은 규칙부터 candidates.yaml에서 개정하고 재실험.
- 평가자가 3명 미만이면 판정 불가로 기록하고 통과 처리하지 않는다.
```

- [ ] **Step 6: 검증 후 커밋**

Run: `uv run pytest -q && uv run python scripts/validate_links.py`
Expected: 95 passed, 링크 검증 통과

```bash
git add docs/pilot/
git commit -m "docs: record internal sulsul dogfood and comparison pilot protocol"
```

---

### Task 5: 외부 문서 파일럿

**Files:**
- Create: `docs/pilot/2026-08-sulsul-external.md`

**Interfaces:**
- Consumes: Task 2의 `skill/sulsul/references/rules.md` (판정 기준)
- Produces: 스펙 성공 기준 5의 외부 파일럿 기록(규칙 히트 통계만).

권리 제약: 외부 문서의 문장을 저장소에 옮겨 적지 않는다. 기록은 URL,
섹션 제목, 규칙 히트 수, 판정 메모(문장 인용 없이 요지만)로 한정한다.

- [ ] **Step 1: 대상 문서 2개 선정과 확보**

공개 한국어 개발자 문서에서 2개를 고른다. 1순위 후보(접근 실패 시 같은 성격의 공개 한국어 기술문서로 대체하고 기록에 사유를 남긴다):

1. Kubernetes 한국어 문서의 개념 페이지 1개 — `https://kubernetes.io/ko/docs/concepts/overview/`
2. React 한국어 문서의 학습 페이지 1개 — `https://ko.react.dev/learn`

WebFetch로 본문을 가져와 작업 메모리에서만 사용한다. 로컬 파일로 저장하지 않는다.

- [ ] **Step 2: 판정 수행**

각 문서의 산문 문장을 규칙 16개에 대조한다. 문서당 최소 30문장을 검사한다. 30문장이 안 되면 같은 사이트의 인접 페이지를 추가하고 기록에 명시한다.

- [ ] **Step 3: 기록 작성**

`docs/pilot/2026-08-sulsul-external.md` 생성:

```markdown
# sulsul 외부 문서 파일럿 기록 (2026-08)

공개 한국어 개발자 문서에 sulsul v0 규칙을 적용한 규칙 히트 통계다.
원문 문장은 이 저장소에 옮겨 적지 않는다. 원문은 각 URL에서 확인한다.

## 문서 1

- URL: (실제 URL)
- 접근일: (실제 날짜)
- 검사 문장 수:
- 규칙별 히트: (모든 규칙을 `규칙ID ×N`으로, 0 포함)
- 게이트 발동 수:
- 메모: (오탐 경향, 문서 장르 특성 — 문장 인용 없이)

## 문서 2

(같은 형식)

## 종합 관찰

- 내부 dogfood(docs/pilot/2026-08-sulsul-dogfood.md)와 비교한 규칙 히트
  분포 차이:
- 규칙 후보 조정이 필요해 보이는 항목:
```

- [ ] **Step 4: 검증 후 커밋**

Run: `uv run pytest -q && uv run python scripts/validate_links.py`
Expected: 95 passed, 링크 검증 통과

```bash
git add docs/pilot/2026-08-sulsul-external.md
git commit -m "docs: record external sulsul pilot statistics"
```

---

### Task 6: 성공 기준 대조와 마무리

**Files:**
- Modify: `docs/superpowers/specs/2026-08-10-sulsul-skill-v0-design.md` (성공 기준에 달성 표시 추가)

**Interfaces:**
- Consumes: Task 1~5의 모든 산출물
- Produces: v0 완료 판정

- [ ] **Step 1: 스펙 성공 기준 5개 대조**

스펙 3절의 기준을 하나씩 확인한다:

1. 매니페스트가 있고 SKILL.md description에 자연어 트리거가 있다 → Task 3 산출물 확인
2. `uv run python scripts/generate_skill.py --check`가 0으로 종료한다
3. `uv run pytest tests/test_skill_sync.py -q`가 통과한다(게이트 분류 포함)
4. `docs/pilot/2026-08-sulsul-dogfood.md`에 판정 표와 집계가 채워져 있다
5. `docs/pilot/2026-08-sulsul-external.md`에 문서 2개 이상의 통계가 있다

- [ ] **Step 2: 스펙에 달성 기록 추가**

스펙 3절 아래에 추가:

```markdown
### 달성 기록 (구현 완료 시점)

구현 커밋: (Task 1~5의 커밋 해시 나열). 성공 기준 1~5를 위 기준의 확인
방법으로 검증했다. 미달 항목: (없으면 "없음", 있으면 항목과 사유).
```

- [ ] **Step 3: 최종 전체 검증**

Run: `uv run pytest -q && uv run python scripts/validate_links.py && uv run python scripts/generate_skill.py --check`
Expected: 95 passed, 링크 검증 통과, 생성물 동기화 확인 종료 코드 0

- [ ] **Step 4: 커밋**

```bash
git add docs/superpowers/specs/2026-08-10-sulsul-skill-v0-design.md
git commit -m "docs: record sulsul v0 success criteria verification"
```
