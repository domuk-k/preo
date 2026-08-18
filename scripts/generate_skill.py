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

SKILL_VERSION = "0.1.1"
REPO_URL = "https://github.com/domuk-k/preo"
STATS_PATH = "~/.claude/preo/stats.jsonl"
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
name: preo
description: >-
  한국어 기술문서의 꼬인 문장을 풀어 읽히게 고치고, 쓸 때부터 풀어서 쓰는
  스킬. "풀어줘", "이 문서 풀어줘", "이 문서 검사만 해줘", "이해되는지
  봐줘", "바꿔 말해봐" 같은 교정·이해 검사 요청과 "풀어로 써줘" 같은
  한국어 문서 작성 요청, 한국어 README·가이드·API 문서를 다루는 작업에
  사용한다. 뜻 보존을 읽힘보다 앞에 두고, 규칙 후보에 근거해 고친다.
  한글 이름은 풀어, 설치 이름은 preo다.
version: {SKILL_VERSION}
---

{GENERATED_NOTICE}

# preo — 풀어, 한국어 기술문서를 읽히게

이 스킬의 규칙은 [preo]({REPO_URL}) 규칙 후보다. 모든 규칙은 candidate
단계이며 아직 확정 표준이 아니다. 규칙 본문의 단일 원천은 저장소의
`standard/rules/candidates.yaml`이다. 규칙 ID의 `KSTL-` 접두사는 식별자일
뿐 제품 이름이 아니다.

## 동작

1. 기본 동작은 고치기다. 고치기 전에 [references/rules.md](references/rules.md)를
   읽고 예문 쌍과 예외를 판정 기준으로 삼는다.
2. 뜻을 읽힘보다 앞에 둔다. 문장마다 행위자·대상·조건·순서·양태·부정을
   잠근 뒤에만 고친다. 자연스러운데 뜻이 바뀌면 그 문장은 실패다. 되돌린다.
3. 고친 뒤 한 줄로 바꿔 말한다. 잠근 뜻과 다르면 그 편집을 버린다.
4. 절차문·경고문은 "읽고 할 일"이 하나인지 본다. 두 동작이 되면 나누거나
   게이트로 묻는다. 설명문에는 이 검사를 하지 않는다.
5. 고친 문장이 더 뻣뻣하거나, 번역투·챗봇처럼 들리거나, 의도한 말투가
   깨지면 그 편집을 버린다. `+`/`−`로만 기억한다. `−` 이유 코드:
   `번역투` · `챗봇` · `말투` · `두 번 읽음` · `불필요`.
6. 문장은 통째로 통과 또는 실패다. 부분 점수를 주지 않는다.
7. 고친 결과를 보여준 뒤 한 줄로 요약한다. 형식:
   `뜻 유지 · SYN-001 ×2 · 거절 Style ×1 · 나머지 이미 좋음`.
8. 걸린 문장이 적으면 "이미 잘 읽힙니다 — N곳만 고쳤습니다"라고 말하고
   억지로 고치지 않는다.
9. "검사만" 또는 "이해되는지 봐줘"이면 고치지 않는다. 문장마다 이진
   통과/실패와 이유만 보고한다. 설명문은 바꿔 말한 한 줄, 절차·경고는
   "다음 행동" 한 줄. 실패 이유 코드는 Accuracy · Terminology · Style ·
   Conventions · Audience · Markup 중 하나와 규칙 ID다.
10. "왜 바꿨어?"이면 그때만 규칙 ID, 근거, 연구 출처를 설명한다.
    근거는 references/rules.md의 근거 메모에서 가져온다.
11. 질문 게이트 규칙에 걸리는 문장은 조용히 고치지 않는다. 가능한 해석
    후보를 담아 한 줄로 묻는다. 예: "센서 설치, 누가 합니까? ① 작업자
    ② 정비사".
12. 범위와 강도 조정은 자연어로 받는다. "이 문단만"이면 그 범위만
    처리하고, "가볍게"면 확실한 위반만 고친다. 별도 플래그는 없다.
13. 이독성 점수, 등급, BLEU·COMET 같은 표면 유사 점수를 만들지 않는다.

## 쓰기 모드

사용자가 한국어 문서 작성을 요청하며 "풀어로", "풀어 문체로" 등을
언급하면 고치기가 아니라 쓰기에 규칙을 적용한다.

1. 작성 전에 [references/rules.md](references/rules.md)의 고침 규칙을
   읽고 작성 제약으로 삼는다.
2. 초안을 문장 단위로 자기 검사해 규칙 위반을 작성 중에 제거한다.
3. 쓴 뒤에도 바꿔 말하기와 "다음 행동" 검사를 한다. 뜻이 흔들리거나
   할 일이 두 개면 다시 쓴다.
4. 산출물 끝에 한 줄 요약을 붙인다. 형식:
   `적용: EXP-001 ×2 · SYN-001 ×1 · 뜻 유지`.
5. 질문 게이트 규칙에 해당하는 정보(예: 행위자)가 입력에 없으면
   추측하지 않고 묻는다.

## 보존 보장

- 코드 블록, 셸 명령, URL, 파일 경로, 숫자와 단위, 오류 문자열은 byte
  단위로 보존한다. 깨지면 Markup 실패다.
- 재작성은 문장의 행위자, 대상, 조건, 순서, 양태를 바꾸지 않는다.
  깨지면 Accuracy 실패다.
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
  "hits": {{"KSTL-SYN-001": 2}}, "fail_meaning": 0,
  "reject": {{"Style": 1}}}}`.
- checked는 검사한 문장 수, fixed는 재작성해 남긴 문장 수, hits는 규칙별로
  걸린 문장 수다. fail_meaning은 뜻 깨져서 되돌린 수, reject는 과교정으로
  버린 편집을 이유 코드별로 센 것이다. 한 문장이 여러 규칙에 걸리면 각
  규칙에 1씩 세므로 hits 합계는 fixed보다 클 수 있다.
- 문서 내용, 파일명, 경로는 기록하지 않는다. 통계는 로컬 파일에만 남고
  외부로 전송하지 않는다. 삭제하려면 파일을 지우면 된다.
- "통계 보여줘" 요청이면 파일을 읽어 누적 고친 문장 수, 최다 발동 규칙,
  공유용 한 줄("preo가 두 번 읽게 만드는 문장 N개를 없앴습니다")을
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

# preo 규칙 상세

모든 규칙은 candidate 단계다. 근거 메모는 각 규칙이 아직 검증
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
