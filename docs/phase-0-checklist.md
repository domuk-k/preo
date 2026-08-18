# Phase 0 완료 점검표

Task 8 감사일은 2026-08-08이다. 아래의 `완료`는 산출물, 직접 원문 검토,
권리 검토와 자동 검증으로 확인되었다는 뜻이지 규칙·어휘가 표준으로
승인되었거나 체커가 구현되었다는 뜻이 아니다.

## 감사 표본과 결과

- 주장 레코드 95개의 상태는 `verified` 80개, `secondary` 3개, `unverified` 11개, `contradicted` 1개이며 이 정확한 재고를 자동 검사로 고정했다. `verified` 80개는 전수 검사했다. 감사 전에는 고유 근거 출처가 17개였으나, 원문을 열지 않은 메타데이터 전용 `fr-barthe-1999`를 두 Français Rationalisé 내용 주장과 비교표에서 제거한 뒤 **80개 주장 / 고유 출처 16개**가 되었다. 현재 80개 모두 연결된 본문이 원자적 주장을 직접 뒷받침한다.
- 전수 검사한 16개 출처 ID는 `asd-ste-home`, `asd-ste-about`, `asd-ste-downloads`, `asd-ste-tools`, `hong-kim-2008`, `ryu-im-jeong-2008`, `im-nam-2009`, `choi-choi-2008`, `kwon-nam-hong-2008`, `ham-ryu-2010`, `gobbi-2014-thesis`, `ets-2-publisher`, `its-official`, `its-official-structure`, `its-comtec-2016`, `fr-le-bris-2016`이다. ASD/STEMG 공식 페이지 4개에서 STE 주장 12/12를, 공식·기관 원문에서 한국어 연구 주장 30/30을 확인했다. KCI 원문은 공식 랜딩 페이지의 PDF 흐름으로 재현 가능하지만 원시 다운로드 주소는 세션·리퍼러에 의존한다.
- 코퍼스 후보 10/10의 정확한 제공 페이지와 적용 조건을 다시 확인했다. 10개 모두 비어 있지 않은 `estimated_size`를 기록한다. LH 후보의 PDF 53건은 카탈로그 설명에 근거하고 현재 연결 대상과의 동일성 미확인을 함께 표시했으며, 나머지는 고정 스냅숏이나 원문을 확보하지 않아 측정하지 못한 단위와 이유를 명시했다. `allowed/allowed`는 `dtaq.ram-terms`, 행정규칙 인라인 본문으로 한정한 `molit.aim-quality-manual`, 제3자 자료를 제외한 `kobaco.production-safety-guide`, `kubernetes.ko-docs`, 콘텐츠 유형을 분리한 `mdn.ko-content` 5개이다. 나머지 5개는 보수적으로 `metadata-only/unknown`이다. KDCA 항목은 제0유형 링크와 표시의 긴장을 해소할 제공기관 확인 전까지 보수 상태를 유지한다. 안전하지 않은 `allowed` 항목은 없다.
- 규칙 후보의 허용·비허용 예문 10쌍을 행위자·대상·행동·조건·결과·순서·양태 기준으로 전수 대조했다. `KSTL-TER-001`의 두 용어가 같은 개념이라는 의도와 `KSTL-REF-001`의 `이것`이 `제어기`라는 작성자 의도를 포함해 각 쌍의 `example_invariants`에 수동 판단 경계를 기록했다. 자동 검사는 의미 동일성을 증명하지 않는다.

## 일곱 성공 기준

| 설계 성공 기준 | 담당 역할 | 직접 증거 | 정확한 검증 명령 또는 수동 작업 | 감사 상태 | 남은 경계 |
| --- | --- | --- | --- | --- | --- |
| 1. ASD-STE100 핵심 주장에 ASD/STEMG 공식 출처 연결 | 연구 증거 담당자 | [주장 레코드](../research/claims.yaml), [서지](../research/bibliography.md), [무결성 테스트](../tests/test_research_integrity.py), ASD/STEMG 공식 페이지 4개 | `uv run pytest tests/test_research_integrity.py -v`; **수동:** STE `verified` 주장 12개와 4개 공식 본문을 원자 단위로 전수 대조 | **완료 — 12/12 직접 지지** | Issue 9 요청·수령은 아래 별도 외부 행동이며 이 기준의 공개 페이지 주장 검증과 섞지 않는다. |
| 2. 한국어 통제언어 연구 3편 이상 식별 및 확보 원문의 구조화 요약 | 한국어 언어 연구자 | [원문 검토](../research/korean-controlled-language.md), [서지](../research/bibliography.md), [주장](../research/claims.yaml) | `uv run pytest tests/test_research_integrity.py -v`; **수동:** 네 원문의 연구 질문·방법·결과·한계를 PDF와 전수 대조 | **완료 — 4/4 구조화 검토, 관련 주장 30/30 직접 지지** | 연구 결과는 해당 번역 방향·시스템·표본에 한정하며 후보 효과를 일반화하지 않는다. |
| 3. STE·ETS·ITS·Français Rationalisé의 공개 확인 구조 비교 | 비교 연구 담당자 | [언어 비교표](../research/language-comparison.md), [주장](../research/claims.yaml), [서지](../research/bibliography.md) | `uv run pytest tests/test_research_integrity.py -v`; **수동:** 네 행의 버전·공식/2차 계수·미확인 계수·구조·접근·근거 ID를 원문과 대조 | **완료 — 4/4 언어 행과 버전/계수 경계 확인** | ETS 2.0 계수와 ITS 공식 계수, FR Glossaire 계수는 각각 `unverified`/`secondary`/`unverified`로 유지한다. |
| 4. 코퍼스 후보별 출처·분야·형식·예상 규모·권리·개인정보·수집 방법 기록 | 코퍼스 권리·개인정보 담당자 | [코퍼스 레지스트리](../research/corpus-sources.yaml), [확보 가이드](corpus-guide.md), [코퍼스 테스트](../tests/test_corpus_sources.py), 후보별 공식 제공·라이선스 페이지 | `uv run pytest tests/test_corpus_sources.py -v`; **수동:** 후보 10/10의 정확한 항목 범위, 규모 근거 또는 미측정 이유, 재배포·파생물 권리, 제3자 제외와 개인정보 위험을 전수 대조 | **완료 — 10/10 비어 있지 않은 `estimated_size`와 메타데이터·권리 경계 확인, 불안전한 `allowed` 0개** | 모두 `candidate`이며 실제 수집 직전에 고정 스냅숏의 규모, 버전·약관·payload 동일성을 다시 확인한다. |
| 5. 규칙·어휘 JSON Schema 초안과 유효성 검사 | 데이터 계약 담당자 | [규칙 스키마](../schemas/rule.schema.json), [어휘 스키마](../schemas/vocabulary.schema.json), [코퍼스 스키마](../schemas/corpus-source.schema.json), [주장 스키마](../schemas/claim.schema.json), [스키마 테스트](../tests/test_schemas.py) | `uv run pytest tests/test_schemas.py tests/test_research_integrity.py tests/test_corpus_sources.py tests/test_standard_data.py -v` | **완료 — 스키마 4/4와 현재 데이터 검증** | 이후 데이터 모델 변경 시 스키마와 데이터를 같은 변경으로 검증한다. |
| 6. 근거·예문·자동 검사 가능성을 갖춘 한국어 규칙 후보 10개 이상 | 한국어 규칙 설계자 | [규칙 후보](../standard/rules/candidates.yaml), [규칙 템플릿](rule-template.md), [어휘 예시](../standard/vocabulary/entries.yaml), [표준 데이터 테스트](../tests/test_standard_data.py) | `uv run pytest tests/test_standard_data.py tests/test_schemas.py -v`; **수동:** 예문 쌍 10/10의 의미 불변식과 근거·자동화 상한을 전수 검토 | **완료 — 후보 10개, 예문 10/10 수동 대조; 자동화 2 deterministic / 5 heuristic / 3 human** | 모든 규칙은 `candidate`, 어휘는 형식 `example`이다. 의미 보존·규칙 효과·최종 위반 판정은 자동 검증 완료를 뜻하지 않는다. |
| 7. README에서 두 번 이하 링크 이동으로 모든 Phase 0 산출물 도달 | 문서 유지관리자 | [문서 색인](../README.md), 이 점검표, [문서 테스트](../tests/test_docs.py), [링크 검증기](../scripts/validate_links.py) | `uv run pytest tests/test_docs.py -v`; `uv run python scripts/validate_links.py`; **수동:** README의 Phase 0 대상 15/15와 이동 수 확인 | **완료 — 15/15 대상이 README에서 한 번에 연결되고 로컬 링크 검증 통과** | 외부 URL의 현재 내용·권리·사실성은 로컬 링크 검사 범위가 아니므로 사람이 다시 검토한다. |

일곱 저장소 성공 기준은 **7/7 완료**이다. 이는 Phase 0 연구 기반의 완료 판정이며, 공개 표준 승인·어휘 승인·체커 구현이나 외부 요청 제출을 뜻하지 않는다.

## 최종 기계 검증

아래 결과는 최종 리뷰 수정까지 포함한 감사 구현 트리 SHA `b9254672f9f188ed2c86e40c0bb9e4aaa5c7f4a1`에서 다시 실행한 결과다. 이 결과를 기록하는 후속 문서 커밋은 이 점검표의 검증 증거 문구만 바꾸며, 감사 대상 구현은 이 SHA로 고정한다.

- `uv sync --locked`: exit 0 (`Resolved 16 packages`, `Checked 13 packages`).
- `uv run pytest -v`: **77 passed in 0.74s**.
- `uv run python scripts/validate_links.py`: exit 0, 출력 없음.
- 대소문자 무관 PDF, DOC/DOCX, EPUB, HWP/HWPX, ODT, RTF, Pages, PPT/PPTX, XLS/XLSX, ZIP, TAR, GZ, 7Z, RAR 원문 확장자 검사: 추적 파일 일치 0개.
- 비밀·정책 문자열 검사: `LICENSES/README.md:7`의 예상된 재배포 금지 정책 문장 1개만 일치했고, 자격증명은 없었다.
- 코퍼스 계약 검사: 후보 10/10이 스키마에 맞고 `estimated_size`가 비어 있지 않다.
- 주장 재고 검사: 전체 95개, `verified` 80개, `secondary` 3개, `unverified` 11개, `contradicted` 1개이다.
- `git diff --check`: exit 0, 출력 없음.
- 증거 전용 문서 커밋 전 `git status --short`: 출력 없음(감사 구현 트리 깨끗함).

## 감사 이후 갱신 이력

위의 감사 표본·기계 검증 수치는 2026-08-08 감사 시점의 기록으로 보존한다.
당시 표기된 SHA `b9254672f9f188ed2c86e40c0bb9e4aaa5c7f4a1`은 공개 이력 정리
전의 로컬 커밋을 가리키며, 같은 구현 트리
(`77bd930348afcb3826ad72bec2d0f5aa5f2f4dd5`)는 공개 이력의 `d03f6516` 커밋에
있다.

- 2026-08-09 연구 보충: OSS 생태계 실사(sourdough-bread/asd-ste100-checker
  확인·epoko77-ai/im-not-ai 추가)와 국내 공공언어·법령 정비 자료(국립국어원
  2종, 법제처 1종) 서지 추가로 주장 재고를 106개(`verified` 96, `secondary` 3,
  `unverified` 5, `contradicted` 2)로 바꾸고 자동 검사 핀도 함께
  갱신했다. 남은 `unverified` 5개는 ETS 2.0 계수 2건, ITS 판본 번호, 번역
  비용 효과, Français Rationalisé 용어집 계수다.

## 저장소 기준과 별도인 외부 행동

- [x] ASD-STE100 Issue 9 공식 사본 신청은 하지 않는다. STE는 비교용 참고자료일 뿐이고 규칙의 근거는 국어 자료다. 공개 페이지로 확인한 STE 주장만 기록한다. (2026-08-18)
- [x] `verified` 주장 원문, 코퍼스 후보 권리·개인정보, 규칙 예문 의미 보존과 자동화 경계를 포함한 Task 8 최종 수동 감사를 수행했다.
- [x] 제3자 원문·PDF·사전·유료 논문을 저장소에 넣지 않는 정책과 자동 검사가 있다. 자세한 로컬 보관 규칙은 [research/sources/README.md](../research/sources/README.md)에서 확인한다.

Issue 9 신청은 진행 조건이 아니다. 공개 요청 URL은 제출 또는 수령 영수증이 아니다.
