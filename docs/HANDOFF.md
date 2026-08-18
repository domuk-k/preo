# ASD-STE100 조사 기록 및 한국어 통제 기술 언어 OSS 기획

- 작성 시점: 2026-08-08
- 목적: 이후 연구자와 개발자가 이 문서만 보고도 작업을 이어갈 수 있도록 현재까지 조사한 내용을 정리하고, 한국어 버전 OSS 프로젝트의 방향과 로드맵을 제시한다.
- 제품 이름: preo (풀어). 규칙 ID의 `KSTL-` 접두사는 식별자일 뿐이다.

preo는 국어가 중심이다. ASD-STE100은 비교용 참고자료일 뿐이며 규칙의 근거가
아니다. Issue 9 공식 사본 신청은 진행 조건이 아니다.

> 2026-08-08에 공식 기관 페이지와 원문 논문을 기준으로 확실성 수준을
> 재검토했다. 원자 단위 주장과 상태는 [`research/claims.yaml`](../research/claims.yaml),
> 출처 정보는 [`research/bibliography.md`](../research/bibliography.md)에 있다.
> `unverified`와 `secondary` 표시는 후속 조사 단서이며 확정 사실이 아니다.
> 2026-08-09에 OSS 생태계 실사와 국내 공공언어·법령 정비 자료 조사를 보충해
> 반영했다.
> 2026-08-10에 규칙 후보에서 생성되는 sulsul 스킬 v0을 추가했다. 설계는
> `docs/superpowers/specs/2026-08-10-sulsul-skill-v0-design.md`, 구현 계획은
> `docs/superpowers/plans/2026-08-10-sulsul-skill-v0.md`에 있다.

## 1. ASD-STE100 핵심 요약

### 정의

ASD-STE100 Simplified Technical English는 ASD/STEMG가 관리하는 통제 자연어이자
기술문서용 국제 표준이다. 유럽 항공사들이 영어 지식이 제한된 독자도 정비 문서를
더 쉽게 이해하도록 요청한 데서 개발이 시작되었다. Issue 9은 2025-01-15에
발행되었고 이때 국제 규격(specification)에서 국제 표준(standard)으로 전환되었다
([`asd-ste-home`](../research/bibliography.md#asd-ste-home),
[`asd-ste-about`](../research/bibliography.md#asd-ste-about)).

### 구조

- Part 1: Writing Rules. Issue 9은 9개 섹션, 53개 규칙으로 구성되며 문법,
  문체, 문장 구조, 단어 선택을 다룬다.
- Part 2: Controlled Dictionary. 약 900개 승인 단어를 수록하며, 일반적으로
  각 단어는 한 의미와 한 품사로 승인된다.

두 수치는 STEMG의 Issue 9 공식 설명에서 확인했다
([`asd-ste-about`](../research/bibliography.md#asd-ste-about)).

### 핵심 원칙

공식 공개 설명에서 확인한 원칙은 승인 단어를 일반적으로 한 의미·한 품사로
제한하고, 회사·산업·주제 분야의 기술 명사와 기술 동사를 허용한다는 것이다
([`asd-ste-about`](../research/bibliography.md#asd-ste-about)). 능동태 선호와 절차문
20단어·설명문 25단어 같은 세부 규칙은 Issue 9 공식 사본을 직접 대조하기 전까지
연구 단서로만 유지하며 KSTL 규칙의 확정 근거로 쓰지 않는다.

### 역사

- 1970년대 후반: 유럽 항공사들의 요청에 따라 AECMA가 AIA의 지원을 받아
  개발을 시작했다.
- 1983년: Simplified English Working Group이 구성되었다.
- 1986년: 첫 가이드가 발행되었고 같은 해 ATA 100 기술 출판 규격의 요구사항이
  되었다. 초기 기록의 `1987년` 표기는 STEMG 공식 연혁과 충돌하므로 폐기한다.
- 2004년: ASD 출범에 따라 작업 그룹 명칭이 STEMG로 바뀌었다.
- 2005년: 국제 규격이 되었다.
- 2025년: Issue 9에서 국제 표준으로 전환되었다.

연도는 STEMG 공식 연혁을 따른다
([`asd-ste-home`](../research/bibliography.md#asd-ste-home),
[`asd-ste-about`](../research/bibliography.md#asd-ste-about)).

Issue 9 공식 사본은 STEMG 요청 양식에서 무료로 받을 수 있다. ASD-STE100은
ASD의 저작권·상표 대상이므로 이 저장소에는 사본을 재배포하지 않는다
([`asd-ste-downloads`](../research/bibliography.md#asd-ste-downloads)).

## 2. 학술·언어학적 연구와 피드백

### 주요 연구 방향

아래 항목은 초기 조사에서 만든 문헌 탐색 지도이며, 이 단계에서 개별 연구의
결과를 검증했다는 뜻은 아니다.

- 항공 정비 매뉴얼이 실제로 STE를 구현하는 방식을 분석하는 코퍼스 기반 장르 연구
- Lexical Constructional Model 등을 적용한 구문·의미론 연구
- Subject fields를 ISO 표준과 맞추기 위한 STEMG 내부 용어 체계 개선
- 가독성과 번역성 실증 평가

### 비판적 피드백

- 제한 어휘의 표현력, 규칙의 언어학적 근거, 실제 문서의 준수율, 가독성 평가에
  관한 비판은 관련 원문을 아직 대조하지 않은 `unverified` 문헌 탐색 단서이다.
  저자명이나 연구 결과를 확정해 인용하기 전에 1차 논문을 서지 원장에 추가한다.
- 체커는 모든 규칙을 자동 검사할 수 없고 잘못된 피드백을 낼 수 있다. STEMG는
  도구가 작성자나 표준을 대체할 수 없으며 작성자가 명료성·정확성·준수의 최종
  책임을 진다고 명시한다
  ([`asd-ste-tools`](../research/bibliography.md#asd-ste-tools)).

### 보고된 긍정적 효과

- **미검증 연구 단서:** 번역 비용 `30~40%` 절감 수치는 현재 확보한 추적 가능한
  1차 사례 연구로 확인하지 못했다. 근거를 확보하기 전에는 효과 크기로 인용하지
  않는다.
- STEMG는 STE의 목적을 이해 지원, 언어 장벽 감소, 인적 요인 위험 감소로
  설명한다. 그러나 이를 KSTL 또는 모든 도메인에서 입증된 안전성·이해도 효과로
  일반화하지 않는다
  ([`asd-ste-about`](../research/bibliography.md#asd-ste-about)).
- AI 작성 지원은 가능하지만 STEMG는 사람의 감독과 검증을 요구한다. AI 사용
  증가율이나 효과에 관한 수량적 주장은 아직 기록하지 않는다.

## 3. 다른 언어에서의 시도

| 언어 | 이름 | 개발 주체 | 특징 |
|---|---|---|---|
| 프랑스어 | Français Rationalisé | GIFAS | 비교 후보이다. 용어집의 정확한 표제어 수는 `unverified`이다. |
| 스페인어 | Español Técnico Simplificado(ETS) | Ilaria Gobbi | 2014년 박사논문의 코퍼스 기반 2부 구조 시제품에서 시작했다. Aracne는 *ETS 2.0*을 2026-02-13 발행했다. 정확한 2.0 규칙·사전 수는 `unverified`이다. |
| 이탈리아어 | Italiano Tecnico Semplificato(ITS) | COM&TEC | COM&TEC의 공식 프로젝트이다. `53개 지침·약 1,000개 표제어`는 업체 공개 설명에 따른 `secondary` 수치이며 공식 공개 페이지에서는 확인되지 않는다. |
| 중국어·러시아어·독일어 등 | Controlled Chinese, Simplified Technical Russian, CLAT 등 | 기업 또는 연구 단위 | 공개 범위가 작거나 내부 사용에 머무는 사례가 많다. |

ETS 2014의 쓰기·문체 규칙과 제한 사전이라는 2부 구조는 Bologna 대학 저장소에서,
ETS 2.0의 존재와 서지는 출판사 카탈로그에서 확인했다
([`gobbi-2014-thesis`](../research/bibliography.md#gobbi-2014-thesis),
[`ets-2-publisher`](../research/bibliography.md#ets-2-publisher)). ITS의 개발 주체와
목적은 공식 사이트에서 확인했다
([`its-official`](../research/bibliography.md#its-official)). 언어별 설계와 번역 효과는
각 원문을 확보해 별도로 평가해야 한다.

### 한국어 관련 기존 연구

한국어 통제언어 연구도 일부 존재한다.

- Hong·Kim, “Controlled Korean for Korean-English MT”
  ([`hong-kim-2008`](../research/bibliography.md#hong-kim-2008))
- 류수린·임병화·정동규, 「통제언어 모형개발의 필요성과 방향 — 기술문서에서
  나타난 한국어 표현을 중심으로 —」
  ([`ryu-im-jeong-2008`](../research/bibliography.md#ryu-im-jeong-2008))
- 임병화·남유선, 「기술문서의 조건 부사어 통제 — 번역성 제고 방안을
  중심으로 —」 ([`im-nam-2009`](../research/bibliography.md#im-nam-2009))
- 최지영·최명원, 「통제언어의 관점에서 본 기술문서의 화행표현」
  ([`choi-choi-2008`](../research/bibliography.md#choi-choi-2008))
- 권민재·남유선·홍우평 및 함수진·류수린의 후속·관련 연구
  ([`kwon-nam-hong-2008`](../research/bibliography.md#kwon-nam-hong-2008),
  [`ham-ryu-2010`](../research/bibliography.md#ham-ryu-2010))

네 편의 구조화된 원문 검토는
[`research/korean-controlled-language.md`](../research/korean-controlled-language.md)에
있다. Hong·Kim의 결과는 한국어→영어 MT에 한정되며, 류수린 외의 모형 규칙은
저자들이 충분한 한국어 데이터로 검증되지 않았다고 명시한다. 따라서 기존 연구는
KSTL 후보 규칙의 근거이지만 공개 표준·승인 어휘·검사 도구가 이미 완성되었다는
근거는 아니다.

학술 논문 밖의 국내 제도적 선례도 있다. 국립국어원은 2021년 「행정문서 표현
개선 및 쉬운 공공언어 쓰기 지침 개발」 연구 보고서를 발간했고
([`nikl-plain-language-guideline-2021`](../research/bibliography.md#nikl-plain-language-guideline-2021)),
『쉬운 공문서 쓰기 길잡이』를 공개 배포한다
([`nikl-easy-public-doc-guide`](../research/bibliography.md#nikl-easy-public-doc-guide)).
법제처는 알기 쉬운 법령 만들기 사업의 「알기 쉬운 법령 정비기준」을
공식 자료실에서 유지한다
([`moleg-easy-law-standards`](../research/bibliography.md#moleg-easy-law-standards)).
이들은 공공·법령 문장을 대상으로 한 국내 통제·순화 선례이며, KSTL은 절차·안전·
유지보수 기술 문서와 기계 판독 가능한 데이터 계약이라는 점에서 구별된다.

2026-08-09 스윕에서 확인한 미검토 조사 단서(서지 원장 미등재, 원문 검토 전에는
인용하지 않는다):

- 최지영, 「기술문서 3항술어구문의 어순 — 통제언어의 관점에서」, 『독어독문학』
  50(3), 2009. <https://www.kci.go.kr/kciportal/landing/article.kci?arti_id=ART001383040>
- 이성화·김세현, 「영-한 및 한-영 기계번역 품질향상을 위한 프리에디팅 기법
  제안」, 『번역학연구』 19(5), 2018. <https://www.kci.go.kr/kciportal/landing/article.kci?arti_id=ART002414141>
- 진용주 외, 「프리에디팅이 기계번역 품질에 미치는 영향 고찰」, 『통번역학연구』
  22(3), 2018. 검색 결과로만 확인했다.
- 강현철, 「알기 쉬운 법령만들기 사업의 성과와 전망」, 『법제연구』 57, 2019.
  <https://www.kci.go.kr/kciportal/landing/article.kci?arti_id=ART002533042>
- 카카오엔터프라이즈 기술 블로그의 기술문서 쉽게 쓰기 지침. 자동 접근이 차단되어
  검색 결과로만 확인했다.

2026-08-10 가독성 지표 조사에서 확인한 미검토 단서(서지 원장 미등재). 확인된
모든 한국어 가독성 지표는 교육 텍스트로 검증되었고, 기술문서 대상으로 검증된
지표는 찾지 못했다:

- 조용구, 「국어 이독성 공식 개발 연구」, 『독서연구』 41, 2016.
  <https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART002171615>
- 서혁 외, 텍스트 복잡도 상세화 공식, 『국어교육학연구』 47, 2013.
  <https://www.kci.go.kr/kciportal/landing/article.kci?arti_id=ART001797415>
- 조용구·이경남, KReaD 지수 개발, 『독서연구』 56, 2020.
  <https://www.kci.go.kr/kciportal/landing/article.kci?arti_id=ART002616815>
- 최소영 외, 교과 교육용 텍스트 이독성 분석, 『교육과정평가연구』 27(1), 2024.
  <https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART003054810>
- (주)낱말 LQ 지수, 대교 KReaD 상용 서비스, KICE 이독성 지수(연구 단계),
  국립국어원 공공언어 진단의 수치 평정 체계. 검색과 보도 자료로만 확인했다.

## 4. 기존 OSS 및 도구 생태계

2026-08-09 실사 결과로 갱신한다.

- [`sourdough-bread/asd-ste100-checker`](../research/bibliography.md#sourdough-checker-repo)는
  실존하는 Apache-2.0 공개 저장소로, 결정론적 Python 엔진 위에 agent skill·
  MCP·LSP 표면을 얹고 CLI를 제공한다. 다만 2026-07-24 생성된 초기 단계
  프로젝트로 커밋 19개가 모두 생성 당일이고 발행된 릴리스가 없다. Issue 9
  PDF에서 추출한 사전·규칙 JSON을 저장소에 커밋하며 재배포 위험 감수 문구를
  두는데, KSTL은 파생 통제 사전을 커밋하지 않으므로 이 방식을 따르지 않는다.
  아키텍처(하나의 결정론적 엔진 위 다중 표면)는 KSTL 참조 설계 후보다.
- [`epoko77-ai/im-not-ai`](../research/bibliography.md#im-not-ai-repo)는 AI가
  생성한 한국어 문장을 사람 문체로 재작성하는 MIT 라이선스 Claude Code 스킬로,
  분류 ID·심각도 등급을 붙인 구조화 마크다운 규칙을 쓴다. 한국어 글쓰기
  스킬 수요를 보여주는 인접 선례이며, KSTL은
  문체 자연화가 아니라 검증 가능한 통제 기술 언어 표준·데이터라는 점에서
  구별되고 그 이상을 목표로 한다.
- 그 외 2025~2026년에 ASD-STE100을 에이전트 스킬로 포장한 소규모 저장소가
  다수 등장했다. 개별 인용 전에 저장소별로 소유자·라이선스·기능을 확인한다.

KSTL은 사전, 규칙 엔진, 체커, 에이전트 인터페이스를 느슨하게 결합하는 방향을
유지한다. 규칙·어휘의 단일 원천은 `standard/`의 기계 판독 데이터이고, 스킬과
체커는 그 데이터에서 파생되는 표면이다.

## 5. 한국어 버전의 언어학적 과제

한국어는 교착어이며 경어 체계와 한자어·순우리말 이중 어휘 체계를 갖는다. 따라서 STE를 직역해서는 실용적인 통제언어를 만들기 어렵다.

필수 연구 항목은 다음과 같다.

1. 조사와 어미 중 무엇을 통제하고 무엇을 허용할지 정한다.
2. 기술 문서의 기본 경어체 또는 평어체 정책을 정한다.
3. 한자어와 순우리말에 `한 단어 = 한 의미` 원칙을 적용하는 방법을 설계한다.
4. 긴 수식어와 명사 나열을 제한하거나 재구성하는 규칙을 만든다.
5. 조건문과 조건 부사어 통제 규칙을 기존 한국어 연구와 연결한다.
6. 산업별 기술 명사와 기술 동사를 등록하고 확장하는 절차를 만든다.

### 평가할 가설

- 문서 가독성이 높아지고 오해율이 낮아지는가.
- 사람 번역과 기계번역의 일관성이 높아지는가.
- AI 에이전트의 한국어 기술 문서 생성·검증이 더 안정적인가.

이는 기대 효과를 확정한 문장이 아니라 Phase 3에서 비교 실험으로 검증할 가설이다.

## 6. OSS 프로젝트 비전

### 이름 후보

- Korean Simplified Technical Language(KSTL)
- 한국어 기술 통제 언어
- 한국어 간소 기술어

### 목표

한국어 절차·안전·유지보수 문서를 명확하고 일관되게 작성하기 위한 공개 표준, 사전, 규칙 엔진, 체커, 에이전트 스킬을 만든다.

### 권장 구성 요소

1. Markdown과 JSON으로 배포하는 표준 문서 및 승인 어휘 사전
2. Python 기반 규칙 엔진과 체커
3. CLI, MCP, LSP 인터페이스
4. Claude, Cursor, Codex 등을 위한 에이전트 스킬
5. 가독성, 오해율, 번역성을 평가하는 코퍼스와 벤치마크
6. 기여 가이드와 STEMG 형태의 유지보수 그룹

### 라이선스

- 코드와 테스트: Apache License 2.0
- 자체 작성 표준 문서와 데이터: Creative Commons Attribution 4.0 International
- 제3자 표준·논문·코퍼스: 원 저작권과 이용 조건을 별도로 기록하고 준수

정확한 파일 범위와 기여 조건은 `LICENSES/README.md`와 `CONTRIBUTING.md`를
따른다.

## 7. 연구·개발 로드맵

### Phase 0: 준비, 1~2개월

- ASD-STE100 Issue 9 공식 문서를 확보하고 상세 분석한다.
- 기존 한국어 통제언어 논문 전문을 수집하고 정리한다.
- ETS, Français Rationalisé, ITS 규칙 비교표를 작성한다.
- 국방, 항공, 기계, IT 분야의 공개 한국어 기술 문서를 대상으로 코퍼스 후보를 수집한다.

### Phase 1: 언어 설계, 3~6개월

- 문장 길이, 능동태, 조사·어미, 조건문 등을 포함한 핵심 규칙 초안을 만든다.
- 빈도와 의미 통제를 기준으로 기본 어휘 사전 v0.1을 만든다.
- 소규모 파일럿 텍스트에 규칙을 적용하고 문제를 기록한다.

### Phase 2: 도구 프로토타입, 4~8개월

- 규칙 엔진과 기본 체커를 구현한다.
- 사전 조회 CLI를 구현한다.
- 기본 에이전트 스킬을 제공한다.

### Phase 3: 평가 및 공개

- 가독성과 오해율을 측정하는 실험을 수행한다.
- 커뮤니티 피드백을 수집한다.
- v1.0을 공개하고 유지보수 체계를 운영한다.

## 8. 즉시 실행할 작업

- STE Issue 9 신청: **하지 않음.** 비교용 참고자료이며 진행 조건이 아니다.
- [x] 기존 한국어 통제언어 논문 4편의 원문을 열람하고 구조화해 요약한다.
- [x] ETS, ITS, Français Rationalisé의 규칙 구조 비교표를 작성한다.
- [x] 프로젝트 디렉터리와 초기 핸드오프 문서를 만든다.
- [x] 공개 자료 중심의 한국어 기술 문서 코퍼스 수집 계획을 세운다.

## 9. 리스크와 주의사항

- ASD-STE100 상표와 저작권을 확인한다. 공식 문서를 무단 재배포하지 않는다. 규칙을 참고하되 한국어 특성에 맞게 독자적으로 설계한다.
- 완벽한 통제를 목표로 삼지 않는다. 실용성과 사용자 수용성을 함께 평가한다.
- 초기부터 기술 작가, 번역가, 언어학 연구자, AI 개발자가 참여할 수 있는 구조를 만든다.
- AI 에이전트가 주요 사용자가 될 가능성을 고려해 규칙과 사전을 기계 판독 가능한 형식으로 관리한다.
- 조사 기록의 주장마다 원문 출처, 접근일, 라이선스 상태를 남긴다.

## 10. 다음 작업 산출물

Phase 0에서는 다음 문서를 우선 만든다.

1. `docs/phase-0-checklist.md`: 담당자, 완료 조건, 산출물을 포함한 상세 체크리스트
2. `docs/rule-template.md`: 규칙 ID, 목적, 허용·금지 예문, 자동 검사 가능성을 기록하는 템플릿
3. `docs/corpus-guide.md`: 수집 범위, 라이선스, 개인정보 제거, 메타데이터 규격을 정의한 가이드
4. `research/bibliography.md`: 논문과 표준의 정확한 서지정보 및 검증 상태
5. `research/language-comparison.md`: ETS, ITS, Français Rationalisé 비교표

## 11. 인수인계 원칙

이 문서는 현재 조사 기록과 OSS 기획의 기준점이다. 후속 작업자는 Phase 0부터 시작하고, 검증한 사실에는 출처를 연결하며, 확인되지 않은 내용은 확정 사실처럼 사용하지 않는다.
