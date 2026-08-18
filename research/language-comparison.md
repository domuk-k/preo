# 통제 기술언어의 언어간 비교

이 비교는 2026-08-08에 다시 열어 확인한 표준 관리 기관, 개발 주체,
출판사, 대학 저장소의 자료에 한정한다. 각 셀의 `근거`는
`research/claims.yaml`의 원자적 주장 ID이고, `출처`는
`research/bibliography.md`의 서지 ID이다. `verified`는 1차·공식·기관
자료에서 확인했다는 뜻이고, `secondary`는 2차 자료의 보고이며,
`unverified`는 공개 근거로 확인하지 못했다는 뜻이다.

| 이름 | 언어 | 관리 주체·저자 | 첫 확인 발행 | 최신 확인 버전 | 공개적으로 확인한 구조 | STE와의 관계 | 접근 조건 | 근거 상태 | preo 시사점 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **ASD-STE100 Simplified Technical English (STE)** | 영어.<br>출처: `asd-ste-home` | ASD Simplified Technical English Maintenance Group(STEMG)가 유지 관리를 담당한다.<br>근거: `ste.stewardship`<br>출처: `asd-ste-about` | AECMA Simplified English Guide, 1986.<br>근거: `ste.history.first-guide`<br>출처: `asd-ste-home`, `asd-ste-about` | **Issue 9**, 2025-01-15.<br>근거: `ste.issue-9.release-date`<br>출처: `asd-ste-home`, `asd-ste-about` | 쓰기 규칙 53개·9개 섹션과 통제 사전(승인 단어 약 900개).<br>근거: `ste.issue-9.rule-count`, `ste.issue-9.section-count`, `ste.issue-9.dictionary-size`<br>출처: `asd-ste-about` | 비교의 기준이 되는 STE 자체이다.<br>출처: `asd-ste-home` | Issue 9 공식 사본은 무료이지만 요청 양식으로 받는다. ASD 저작권·상표이므로 재배포 권리를 뜻하지 않는다.<br>근거: `ste.issue-9.copy-cost`, `ste.issue-9.copy-access`<br>출처: `asd-ste-downloads`, `asd-ste-home` | 표의 수치·버전·구조: `verified`.<br>출처: `asd-ste-about` | 규칙과 사전을 분리하고 버전을 명시하는 관리 모형은 참고하되, 영어 수치를 한국어에 옮기지 않는다.<br>근거: `ste.issue-9.section-count`, `ste.issue-9.rule-count`<br>출처: `asd-ste-about` |
| **Español Técnico Simplificado (ETS)** | 스페인어.<br>출처: `gobbi-2014-thesis` | Ilaria Gobbi가 학위논문에서 개발한 코퍼스 기반 통제언어이다.<br>근거: `ets.v0.corpus-basis`<br>출처: `gobbi-2014-thesis` | 2014년 학위논문의 **`Versión 0`**. 2015년 EUS 상용판은 별도 서지로 확인한다(`secondary`).<br>근거: `ets.v0.version-label`, `ets.v0.publication-year`, `ets.2015.publication-year`<br>출처: `gobbi-2014-thesis`, `ets-2015-catalog` | **Español Técnico Simplificado 2.0**, 2026-02-13.<br>근거: `ets.v2.release-date`<br>출처: `ets-2-publisher` | v0: `Reglas de escritura + Diccionario`; 섹션 1–8의 번호 규칙 59개, 섹션 9는 후속 정의 예정. 2.0: `규칙 + 통제 사전`; **2.0 규칙 수와 사전 표제어 수는 확인하지 못함**.<br>근거: `ets.v0.rules-component`, `ets.v0.dictionary-component`, `ets.v0.numbered-section-count`, `ets.v0.rule-count`, `ets.v0.section-9-status`, `ets.v2.rules-component`, `ets.v2.dictionary-component`, `ets.v2.rule-count`, `ets.v2.dictionary-size`<br>출처: `gobbi-2014-thesis`, `ets-2-publisher` | v0는 STE를 참조하여 스페인어 코퍼스로 설계했고, 2.0은 ASD-STE100 Issue 9을 기반으로 한다.<br>근거: `ets.v0.corpus-basis`, `ets.v2.ste-issue-basis`<br>출처: `gobbi-2014-thesis`, `ets-2-publisher` | v0 학위논문은 대학 저장소에서 열람할 수 있다. 2015년판과 2.0은 상용 출판물이며, 무료 열람이 공개 라이선스를 뜻하지 않는다.<br>출처: `gobbi-2014-thesis`, `ets-2015-catalog`, `ets-2-publisher` | v0 구조·59개: `verified`; 2015 발행: `secondary`; 2.0 버전·구조: `verified`; 2.0 정확한 계수: `unverified`.<br>출처: `gobbi-2014-thesis`, `ets-2015-catalog`, `ets-2-publisher` | 같은 이름의 v0·2015년판·2.0을 별도 버전으로 관리하고, 한 판본의 계수를 다른 판본에 전이하지 않아야 한다.<br>근거: `ets.v0.rule-count`, `ets.v2.rule-count`<br>출처: `gobbi-2014-thesis`, `ets-2-publisher` |
| **Italiano Tecnico Semplificato (ITS)** | 이탈리아어.<br>출처: `its-official` | COM&TEC이 코퍼스 기반 프로젝트를 기획·조정했고, Ilaria Gobbi가 책의 저자이다.<br>근거: `its.ownership`, `its.book-author`<br>출처: `its-official-structure`, `its-comtec-2016` | COM&TEC의 종이책·ePub 출간 공지, 2016-11-02.<br>근거: `its.first-book-release-date`<br>출처: `its-comtec-2016` | 현재 공식 사이트에서 판본 번호는 **확인하지 못함**.<br>근거: `its.latest-version-label`<br>출처: `its-official`, `its-official-structure`, `its-comtec-2016` | 공식: 166쪽의 `Istruzioni Linguistiche + Dizionario`. 2차 자료: 지침 53개, 일반·비전문 표제어 약 1,000개.<br>근거: `its.page-count`, `its.rules-component`, `its.dictionary-component`, `its.instruction-count`, `its.dictionary-size`<br>출처: `its-official-structure`, `its-free-edit` | 공식 페이지는 ITS를 통제 자연언어로 규정하지만, 검토한 공개 근거만으로 STE 파생 버전이나 일대일 대응을 주장하지 않는다.<br>출처: `its-official`, `its-official-structure` | 종이·디지털 상품이고 상표·저작권으로 보호된다. 공개 라이선스 근거는 없다.<br>근거: `its.rights.trademark-protection`, `its.rights.copyright-protection`, `its.access.print-availability`, `its.access.digital-availability`<br>출처: `its-official-structure` | 주체·공식 구조·쪽수: `verified`; 53개·약 1,000개: `secondary`; 현재 판본 번호: `unverified`.<br>출처: `its-official-structure`, `its-free-edit` | 형태·통사 지침과 사전을 함께 설계하되, 공식으로 검증되지 않은 2차 계수를 제품 요구사항으로 삼지 않아야 한다.<br>근거: `its.instruction-count`, `its.dictionary-size`<br>출처: `its-free-edit` |
| **Français Rationalisé (GIFAS Rationalized French)** | 프랑스어.<br>출처: `gobbi-2014-thesis` | GIFAS가 개발·관리했다.<br>근거: `francais-rationalise.stewardship`<br>출처: `gobbi-2014-thesis` | 1990년 GIFAS 가이드의 일부로 규칙을 확인했다.<br>근거: `francais-rationalise.first-guide-rules-year`<br>출처: `gobbi-2014-thesis` | **`Guide du Français Rationalisé` 제2판**, 1999.<br>근거: `francais-rationalise.second-edition-year`<br>출처: `gobbi-2014-thesis` | `Règles d’écriture + Glossaire`; 규칙 7개 섹션·50개. **Glossaire 표제어 수는 확인하지 못함**.<br>근거: `francais-rationalise.rules-component`, `francais-rationalise.glossary-component`, `francais-rationalise.section-count`, `francais-rationalise.rule-count`, `francais-rationalise.glossary-size`<br>출처: `gobbi-2014-thesis`, `fr-le-bris-2016` | AECMA Simplified English Issue 1에서 출발했지만, 적용 가능한 규칙은 번역하고 나머지는 수정·제거하며 프랑스어 규칙을 추가했다. 따라서 완성본은 **단순 번역**이 아니다.<br>근거: `francais-rationalise.ste-issue-1-basis`, `francais-rationalise.ste-rules-translated`, `francais-rationalise.ste-rules-adapted`, `francais-rationalise.ste-rules-removed`, `francais-rationalise.new-rules-added`<br>출처: `gobbi-2014-thesis` | 공식 개방형 GIFAS 가이드나 공개 라이선스를 확인하지 못했다. 공개 학술 분석만 사용한다.<br>출처: `gobbi-2014-thesis`, `fr-le-bris-2016` | 주체·1999년판·구조·7개·50개: `verified`; Glossaire 계수: `unverified`.<br>출처: `gobbi-2014-thesis`, `fr-le-bris-2016` | 영어 규칙을 번역하는 것이 아니라 한국어의 교착어적 형태·조사·어미·어순에 맞게 통제 범주를 재설계해야 한다.<br>근거: `francais-rationalise.ste-rules-adapted`, `francais-rationalise.new-rules-added`<br>출처: `gobbi-2014-thesis` |

## 한국어 설계 시사점

### 관찰

- STE, ETS, ITS, Français Rationalisé의 공개 근거는 모두 규칙 부분과
  어휘 자원을 구별한다. 그러나 계수의 공개 수준과 근거 상태는
  다르다. [출처: `asd-ste-about`, `gobbi-2014-thesis`,
  `ets-2-publisher`, `its-official-structure`, `its-free-edit`,
  `fr-le-bris-2016`]
- Français Rationalisé는 STE를 참조했지만 프랑스어에 맞지 않는 규칙을
  수정·제거하고 새 규칙을 더했다. 이는 언어간 통제언어 설계가
  단순 번역으로 완료되지 않음을 보여 준다. [근거:
  `francais-rationalise.ste-rules-adapted`,
  `francais-rationalise.ste-rules-removed`,
  `francais-rationalise.new-rules-added`; 출처: `gobbi-2014-thesis`]
- ETS v0의 59개 계수는 2014년 `Versión 0`에만 속한다. ETS 2.0,
  ITS의 공식 계수, Français Rationalisé의 Glossaire 계수로 옮겨 적을
  수 없다. [근거: `ets.v0.rule-count`, `ets.v2.rule-count`,
  `ets.v2.dictionary-size`, `its.instruction-count`, `its.dictionary-size`,
  `francais-rationalise.glossary-size`; 출처: `gobbi-2014-thesis`,
  `ets-2-publisher`, `its-free-edit`, `fr-le-bris-2016`]

### 설계 추론과 평가 가설

- **설계 추론:** preo는 STE의 영어 문법 규칙을 번역하는 대신,
  한국어 형태론과 통사론에 맞게 통제 범주를 적응시켜야 한다. 조사,
  어미, 서술 형식, 성분 생략, 어순과 같은 한국어 현상은 별도의
  코퍼스·사용자 검증을 필요로 한다. 이 추론은 FR의 언어별 적응 사례와
  한국어 통제언어 연구의 설계 결론을 함께 보아 도출한다. [근거:
  `francais-rationalise.ste-rules-adapted`,
  `korean.hong-kim.design-language-properties`,
  `korean.ryu-im-jeong.lexicon-model`, `korean.ryu-im-jeong.grammar-model`;
  출처: `gobbi-2014-thesis`, `hong-kim-2008`, `ryu-im-jeong-2008`]
- **평가 가설:** preo 문서가 다른 언어의 통제 기술언어로 더 일관되게
  기계번역될 수 있다는 명제는 검증할 가설이지 보장된 결과가 아니다.
  번역 방향, MT 시스템, 텍스트 영역, 평가 지표와 비통제 기준선을
  명시한 독립 실험이 필요하다. 저자의 설계 목표는 독립 재현 결과와
  구별한다. [근거: `korean.hong-kim.translation-direction`,
  `korean.hong-kim.design-mt-system`; 출처: `hong-kim-2008`]

## 범위와 재사용 제한

이 문서는 구조·버전·계수·접근 조건의 메타데이터만 비교한다.
ASD-STE100, ETS, ITS, GIFAS 가이드의 보호된 규칙 문구나 사전·용어집
내용을 복제하지 않는다. “가장 STE와 유사하다”같은 순위는 비교
척도가 없으므로 제시하지 않는다.
