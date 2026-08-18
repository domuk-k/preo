# preo

<p align="center"><em>말은 없다. 한 문장 고친다. 읽힌다.</em></p>

한국어 기술문서의 꼬인 문장을 풉니다. 규칙은 후보입니다.

```
로드되어지면 → 로드되면
배포에 대한 절차 → 배포 절차
만료된 경우 → 만료되면
```

```
npx skills add domuk-k/preo
```

또는 `/plugin marketplace add domuk-k/preo` 후 `/plugin install preo@preo`.

“이 문서 풀어줘” · “검사만 해줘” · “풀어로 써줘”

스킬: [skill/preo/SKILL.md](skill/preo/SKILL.md). 규칙: [candidates.yaml](standard/rules/candidates.yaml).

```bash
uv sync --locked && uv run pytest && uv run python scripts/validate_links.py
```

[서지](research/bibliography.md) · [주장](research/claims.yaml) · [한국어 연구](research/korean-controlled-language.md) · [언어 비교](research/language-comparison.md) · [코퍼스](research/corpus-sources.yaml) · [표준](standard/README.md) · [어휘](standard/vocabulary/entries.yaml) · [주장 스키마](schemas/claim.schema.json) · [규칙 스키마](schemas/rule.schema.json) · [어휘 스키마](schemas/vocabulary.schema.json) · [코퍼스 스키마](schemas/corpus-source.schema.json) · [점검표](docs/phase-0-checklist.md) · [규칙 템플릿](docs/rule-template.md) · [코퍼스 가이드](docs/corpus-guide.md) · [인수인계](docs/HANDOFF.md)

> ASD 또는 STEMG와 제휴하거나 이들의 승인을 받은 프로젝트가 아닙니다.
> ASD-STE100은 참고자료입니다. 표준 원문이나 통제 사전을 재배포하지 않습니다.

[보관](research/sources/README.md) · [라이선스](LICENSES/README.md) · [Apache 2.0](LICENSE) · [CC BY 4.0](LICENSES/CC-BY-4.0.txt) · [기여](CONTRIBUTING.md)
