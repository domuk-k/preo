# Redish·xl8 딥리서치 — sulsul QA에 무엇을 가져올까

조사일: 2026-08-18. 원전·기관 페이지를 기준으로 적는다. sulsul은 번역기가
아니라 **같은 한국어를 다시 쓰는 도구**다. 그래도 두 전통이 묻는 질문은
같다. “뜻이 살았나, 원어민이 읽히나, 읽고 할 일을 할 수 있나.”

## 1. Redish — 문서를 제품처럼 시험한다

Janice (Ginny) Redish는 평이한 언어(plain language)와 사용성 연구자다.
대표작은 *Letting Go of the Words*, *A Practical Guide to Usability Testing*
(Dumas와 공저). 웹·공공 문서를 “글”이 아니라 **쓰는 사람(user)이 있는
기능 문서**로 본다. 허구·시가 아니라 안내, 매뉴얼, 공지, 약관이 대상이다
([redish.net](https://redish.net/), Jarrett·Redish
[UXmatters / Effortmark 2020](https://www.effortmark.co.uk/how-to-test-the-usability-of-documents/)).

Redish와 Caroline Jarrett이 문서에 쓰는 기법은 셋이다. Digital.gov 2021
워크숍 제목도 이 셋이다.

### 1.1 바꿔 말하기 (paraphrase)

참가자가 문서를 **조각(bit)** 단위로 읽는다. 조각은 한 문장, 짧은 단락,
목록 하나처럼 **의미가 있으면서 한 번에 잡을 수 있는 크기**다. 읽고 나서
진행자가 묻는다. “방금 읽은 게, 당신 말로는 뭐예요?”

기록할 것:

- 맞게 이해한 것
- 오해한 것
- 빠진 것
- 원문과 **다른 단어**로 말한 것

소리 내어 읽게 하면 어디서 막히는지도 들린다. 끝에 “이 글을 읽고 이제
뭘 하겠어요?”를 묻는다.

**설명문·조건문·한 줄 안내**에 맞다. sulsul 층 2의 원형이다.

### 1.2 플러스·마이너스 (plus–minus)

네덜란드 de Jong·Schellens의 기법이다. Redish/Jarrett이 문서 시험에
가져왔다. 참가자가 읽으면서 여백에 `+`/`−`를 찍고, 그다음 인터뷰에서
이유를 말한다.

`+`/`−`의 뜻을 **미리 정해야** 한다. 예: 맑음/안 맑음, 믿음/불신,
이 말투가 우리 팀 말투다/아니다. 정하지 않으면 톤·감정·이해가 한 바구니에
섞인다.

**직관·과교정·말투**를 찾는 데 맞다. 설문 네 칸보다 원인에 가깝다.

### 1.3 과업 시험 (task-based)

매뉴얼처럼 **처음부터 끝까지 안 읽는** 문서용이다. 시나리오를 주고
답을 찾게 하거나, 지시대로 하게 한다. 웹 사용성 시험과 같다. 찾는 위치와
이해한 행동이 둘 다 대상이다.

**절차문·경고·설치 안내**에 맞다. “다음 행동이 뭔가?”만 묻는 약식과
같다.

### 1.4 문서 목적 → 기법

| 문서가 하는 일 | 쓸 기법 |
|---|---|
| 자세히 설명한다 (읽고 이해) | 바꿔 말하기 |
| 감을 주거나 감정을 만든다 (안심, 신뢰) | 플러스·마이너스 |
| 답을 찾거나 지시를 따른다 | 과업 시험 |

### 1.5 Redish가 분명히 거부하는 것

Jarrett·Redish, [「Readability Formulas: 7 Reasons to Avoid Them」](https://www.uxmatters.com/mt/archives/2019/07/readability-formulas-7-reasons-to-avoid-them-and-what-to-do-instead.php)
(UXmatters, 2019). 문장 길이·음절 공식으로 합격선을 두지 말고, **사람을
앉혀 이해·과업을 보라**는 입장이다. 이 저장소의 “이독성 점수를 만들지
않는다”와 같다.

참가자는 **그 문서를 쓸 사람**이다. 저자나 모델이 아니다. 인원은
사용성 시험처럼 작아도 문제를 드러낸다. 선호 투표의 n=3과는 목적이 다르다.

## 2. xl8 — 번역 품질을 어떻게 재나

`xl8`은 업계에서 translate를 줄여 쓰는 말이다. 여기서는
(1) 번역 QA 전통 전체와 (2) 미디어 MT 회사
[XL8](https://www.xl8.ai/blog/machine-translation-evaluation-how-xl8-gets-it-right)
(Kim, 2022)의 실무를 같이 본다.

sulsul은 한→한 재작성이다. 출발문은 원문 한국어, 도착문은 고친 한국어.
번역의 **adequacy / fluency** 짝이 그대로 대응한다.

### 2.1 사람이 매기는 네 세대

XL8 글과 WMT 역사가 같은 순서를 쓴다.

| 방법 | 하는 일 | 문제 |
|---|---|---|
| Adequacy + Fluency (1–5) | 뜻 보존 / 자연스러움을 눈금으로 | 눈금이 사람마다 다름. WMT 초기 |
| Ranking | 같은 문장의 여러 번역을 순위 | 시스템은 고르기 쉽다. 절대 품질은 안 나옴 |
| Direct Assessment (0–100) | 한 번역의 품질을 연속 눈금 | 2017부터 WMT 공식. 주로 adequacy |
| MQM | 오류 유형·심각도를 찍고 점수로 환산 | 정밀하고 비싸다. 산업 QA의 기본 |

핵심 분리: **adequacy = 뜻이 같나**, **fluency = 도착어 원어민에게 읽히나**.
둘이 충돌하면(유창한데 틀림 / 맞는데 어색) 한 점수로 합치지 말라는 게
이 전통의 교훈이다. 국립국어원의 정확성/소통성, 우리 층 0/층 1과 같다.

비전문가 평가는 자동 지표보다 나쁠 수 있다(Freitag 외 2021를 XL8이
인용). **도착어 원어민이면서 출발을 읽을 수 있는 사람**이 평가해야 한다.
sulsul이면 한국어 원어민이면 충분하다. 출발과 도착이 같은 언어다.

### 2.2 MQM — 오류를 종류로 찍는다

[MQM Council](https://www.themqm.org/)의 상위 차원 7개(현행 2.x):

1. **Terminology** — 용어가 규범과 안 맞음
2. **Accuracy** — 첨가·생략·오역으로 명제가 깨짐
3. **Linguistic conventions** (옛 Fluency) — 문법·맞춤법·구두점
4. **Style** — 문법적이지만 말투·가이드에 안 맞음
5. **Locale conventions** — 날짜·숫자 등 로케일
6. **Audience appropriateness** — 그 독자에게 부적절
7. **Design and markup** — 서식, 코드, UI 문자열

절차: 명세(표본 크기, 심각도, 합격선) → 유형·심각도 주석 → 점수·원인
분석. 심각도는 보통 Major / Minor / Neutral.

sulsul에 쓸 **작은 부분집합**:

| MQM | sulsul에서 |
|---|---|
| Accuracy | 층 0. 불변식 깨짐 |
| Terminology | KSTL-TER-001. 한 개념 두 말 |
| Style | 층 3. 말투 깨짐, STY-001 과통일 |
| Linguistic conventions | 고치다 문법 깨짐 |
| Audience appropriateness | 개발자 문서에 공공문체 강제 |
| Design and markup | 코드·명령·URL byte 보존 실패 |

Locale은 한→한이라 거의 안 쓴다.

### 2.3 XL8 회사가 실제로 하는 일

Kim(2022)이 밝힌 조건 세 가지:

1. **공개 벤치 세트를 시험 데이터로 쓰지 않는다.** 학습 오염과 도메인
   불일치를 막기 위해서다.
2. **평가자는 도착어 원어민 프로 번역가**다.
3. **문장 단위 이진.** 문장 전체가 맞을 때만 정답. 부분 점수는 없다.
   “80%”는 100문장 중 80이 통째로 맞다는 뜻이다.

엔진 출시마다 2,400문장, 장르 6개(다큐·드라마·SF·리얼리티·코미디·K-드라마).
개발 중에는 BLEU, chrF, COMET. 사람은 여러 엔진 출력을 **무작위 순서**로
본다.

가져올 것: 이진 문장 통과, 블라인드 순서, 장르(문서 종류)를 섞어 집계,
공개 벤치를 학습에 안 섞기. 가져오지 말 것: BLEU/COMET으로 sulsul을
채점하기. 참조 번역이 없고, 좋은 재작성은 원문과 표면이 달라야 한다.
BLEU는 바로 그 차이를 감점한다. HTER(사람이 고칠 편집량)만 개념적으로
가깝다. 우리 층 3 수락/거절이 그 짝이다.

### 2.4 자동 지표를 sulsul에 쓰면

| 지표 | sulsul에 |
|---|---|
| BLEU, TER, chrF | 원문과 고친문의 표면 거리. 잘 고칠수록 나빠질 수 있음. 쓰지 않음 |
| BERTScore, COMET | 의미 유사. 층 0 보조 신호 후보는 되나 합격선 아님 |
| 규칙 히트 수 | 이미 있음. 품질이 아님 |
| HTER식 수락률 | 층 3. 사람이 남긴 편집 비율 |

## 3. 둘을 겹치면

Redish는 **독자가 해내는가**를 본다. xl8/MQM은 **도착문이 원문과 어떤
차원에서 어긋나는가**를 본다. sulsul QA는 둘 다 필요하다. 이해만 보면
예쁜 오역을 놓치고, 오류 유형만 보면 “읽히나”를 놓친다.

| 이미 둔 층 | Redish | xl8 / MQM |
|---|---|---|
| 0 의미 | 바꿔 말하기에서 빠짐·오해 | Accuracy, Adequacy |
| 1 직관 | plus–minus의 − | Fluency / Style / Audience |
| 2 과업 | 바꿔 말하기 끝 질문, 과업 시험 | (번역 QA에는 원래 없음. 문서 사용성) |
| 3 과교정 | plus–minus의 “더 나쁨” | Style, HTER 거절 |

번역 QA에 없고 Redish에만 있는 것: **읽고 나서 할 수 있나.** 기술문서
스킬이면 이쪽이 본진이다.

Redish에 없고 xl8에만 있는 것: **오류를 유형으로 모아 규칙을 고친다.**
거절이 STY에 몰리면 STY-001을 고친다.

## 4. sulsul 라운드에 그대로 쓰는 절차

기존 3자 비교를 버리지 않는다. 진행만 이렇게 바꾼다.

1. **문서 목적으로 기법을 고른다.** 설명 문단 = 바꿔 말하기. 절차 문단 =
   과업. 말투·과교정 의심 = plus–minus.
2. **Adequacy를 먼저 끊는다.** 바꿔 말하기에서 핵심이 빠지거나 바뀌면
   그 문장은 이진 실패. 자연스러움 점수를 주지 않는다.
3. **Fluency는 plus–minus로 받는다.** 네 칸 예/아니오 설문은 보조.
   `−`의 이유를 `번역투` / `챗봇` / `말투` / `두 번 읽음`으로만 코딩한다.
4. **문장 이진 통과율을 장르별로 적는다.** 설명 / 절차 / 경고. XL8의
   장르 분할과 같다. 한 숫자로 합치지 않는다.
5. **MQM-lite로 거절을 찍는다.** Accuracy / Terminology / Style /
   Conventions / Audience / Markup. 규칙 ID와 같이 집계한다.
6. **평가자는 한국어 원어민.** 가능하면 그 문서를 읽는 개발자.
   출력은 블라인드 순서. 공개 벤치(쿠버네티스·React 공식문)는 학습용
   파일럿과 평가 세트를 섞지 않는다.
7. **BLEU류는 넣지 않는다.** 공식 점수도 만들지 않는다.

최소 인원: 문제를 찾으려면 Redish식 1:1을 5명 전후. 선호를 가르려면
지금처럼 3명 이상 블라인드. 둘은 다른 실험이다. 한 라운드에 섞지 말 것.

## 출처

- Janice (Ginny) Redish, [redish.net](https://redish.net/).
- Caroline Jarrett · Ginny Redish, “How to test the usability of documents”,
  UXmatters / Effortmark, 2020.
  <https://www.effortmark.co.uk/how-to-test-the-usability-of-documents/>
- Jarrett · Redish, “Readability Formulas: 7 Reasons to Avoid Them”,
  UXmatters, 2019.
- Digital.gov, Plain language: Test for understanding; 2021 Redish 워크숍
  (paraphrase, plus/minus, task).
- Menno de Jong · Peter Jan Schellens, plus–minus method,
  *IEEE Transactions on Professional Communication*, 2000.
- Kang Kim, “Machine Translation Evaluation: How XL8 Gets It Right”,
  XL8 Blog, 2022-12-12.
- MQM Council, typology and scoring. <https://www.themqm.org/>
- White · O’Connell 1996 (adequacy/fluency); Graham 외 2013 (DA);
  Lommel 외 2014 (MQM); Freitag 외 2021 (전문가 vs 비전문가).
