# Contributing to preo

preo(풀어) is an experimental, independently maintained controlled-language project.
Issues and contributions are welcome, but no contribution becomes an approved
standard rule or vocabulary entry merely because it is merged.

## Before contributing

- Open or reference a GitHub issue that states the problem, evidence, and
  intended scope.
- Do not attach or commit third-party standards, controlled dictionaries,
  papers, books, manuals, private corpora, credentials, or personal data.
- Link to external sources and record their provenance and reuse conditions.
  Free access is not permission to redistribute.
- State when AI or an automated agent materially helped produce a contribution.
  A human contributor remains responsible for checking facts, rights, safety,
  and meaning preservation.

## Validation

Run the repository checks before submitting a change:

```bash
uv sync --locked
uv run pytest
uv run python scripts/validate_links.py
```

Rule and vocabulary changes must preserve the candidate or experimental status
unless the repository's documented evidence and governance process explicitly
authorizes another state. Automatic findings must not be presented as semantic
proof or as a substitute for expert review.

## Contribution licensing

By submitting a contribution, you represent that you have the right to submit
it and agree that it is licensed according to the repository's
[`LICENSES/README.md`](LICENSES/README.md) file-scope policy:

- code is contributed under the Apache License 2.0;
- project-authored documentation, research records, schemas, standard proposals,
  and data are contributed under CC BY 4.0.

Do not submit material whose license is incompatible with those terms. If a
contribution needs an exception, discuss it in an issue before sending it.
