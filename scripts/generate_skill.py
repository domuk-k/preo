#!/usr/bin/env python3
"""standard/rules/candidates.yaml에서 skill/preo/ 산출물을 생성한다.

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
SKILL_MD = ROOT / "skill" / "preo" / "SKILL.md"
RULES_MD = ROOT / "skill" / "preo" / "references" / "rules.md"

SKILL_VERSION = "0.2.0"
STATS_PATH = "~/.preo/stats.jsonl"
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
    fix_table = "\n".join(f"| {r['id']} | {r['title']} |" for r in fix_rules)
    gate_table = "\n".join(f"| {r['id']} | {r['title']} |" for r in gate_rules)
    return f"""---
name: preo
description: >
  Use when rewriting or reviewing Korean README, guide, or API docs that
  read like translationese or chatbot prose; when the user says 풀어줘,
  검사만 해줘, 이해되는지 봐줘, 바꿔 말해봐, or 풀어로 써줘.
version: {SKILL_VERSION}
---

{GENERATED_NOTICE}

# preo

풀어. 한국어 기술문서의 꼬인 문장을 고친다. 규칙은 candidate다.
`KSTL-`는 규칙 ID 접두사다.

## 쓰지 않을 때

시, 채팅, 영어 전용 문서. 사람 문체로만 다듬는 일(humanize). 가독성
점수나 등급을 매기는 일.

## 잠금

문장마다 행위자·대상·조건·순서·양태·부정을 잠근다. 코드 블록, 셸 명령,
URL, 경로, 숫자와 단위, 오류 문자열은 byte 단위로 둔다. 원문에 없는
정보는 묻는다.

## 고치기

기본 경로. 끝난 때: 모든 문장이 유지이거나 교체이고, 잠금이 그대로다.

1. 문장마다 잠근다.
2. 걸린 규칙 ID만 [references/rules.md](references/rules.md)에서 연다.
3. 고침 규칙이 걸리면 예문 쌍을 기준으로 재작성한다.
4. 한 줄로 바꿔 말한다. 잠금과 다르면 되돌린다.
5. 절차·경고는 다음 행동이 하나인지 본다. 둘이면 나누거나 게이트로 묻는다.
6. 더 뻣뻣하거나 번역투·챗봇·말투가 깨지면 되돌린다. 이유:
   `번역투` · `챗봇` · `말투` · `두 번 읽음` · `불필요`.
7. 게이트 규칙은 묻는다. 예: "센서 설치, 누가 합니까? ① 작업자 ② 정비사".

출력:

```
(고친 문서)

뜻 유지 · SYN-001 ×2 · 거절 Style ×1
```

걸린 규칙이 없으면:

```
이미 읽힘 · 0곳
```

"왜"이면 그때만 연 규칙의 근거 메모를 말한다. "이 문단만"이면 그 범위만.

## 검사만

`검사만` · `이해되는지` · `바꿔 말해봐`. 고치지 않는다. 끝난 때: 모든
문장에 통과 또는 실패가 있다.

- 설명: 바꿔 말한 한 줄.
- 절차·경고: 다음 행동 한 줄.
- 실패 코드: Accuracy · Terminology · Style · Conventions · Audience ·
  Markup + 규칙 ID.

## 쓰기

`풀어로 써줘`. 초안에 같은 잠금을 적용한다. 끝 줄:

```
적용: EXP-001 ×2 · 뜻 유지
```

행위자가 없으면 추측하지 않고 묻는다.

## 고침 규칙

| ID | 규칙 |
|---|---|
{fix_table}

## 질문 게이트

| ID | 규칙 |
|---|---|
{gate_table}

## 실수

- 예쁜데 뜻이 바뀜 → 되돌린다 (Accuracy).
- 검사만인데 고침 → 출력은 통과/실패만.
- 코드·명령을 손댐 → 되돌린다 (Markup).
- 점수·등급·BLEU를 붙임 → 출력 형식에 그 칸이 없다.

## 통계

요청할 때만 `{STATS_PATH}`를 읽고 쓴다. 한 줄:
`{{"date":"YYYY-MM-DD","checked":N,"fixed":N,"hits":{{"KSTL-SYN-001":2}},"fail_meaning":0,"reject":{{"Style":1}}}}`.
문서 내용·경로를 쓰지 않는다. 쓰기 실패는 생략한다.
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

# preo 규칙 상세

SKILL.md가 가리킨 규칙 ID만 연다. 전수 읽지 않는다. 재작성 판정은
승인/비승인 예문 쌍을 기준으로 한다. 모든 규칙은 candidate다.

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
