# preo 검사만 — kubeadm 설치 (KO)

출처: [https://kubernetes.io/ko/docs/setup/production-environment/tools/kubeadm/install-kubeadm/](https://kubernetes.io/ko/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)
라이선스: Kubernetes 웹사이트 문구는 CC BY 4.0. 짧은 요지만 적는다.
날짜: 2026-08-18.
왜: 절차·경고·번역투가 한 발췌에 있다. Mastra 공식 문서는 영어만 있어서 k8s KO를 썼다.
분기: 검사만. 원문을 고치지 않는다.

## 문장

코드 블록·`#### 경고:` 머리말은 문장에서 뺀다. 서술 조각·괄호 안 서술도 센다.

| # | 요지 | 장르 | 통과/실패 | 규칙 ID | MQM | 바꿔 말하기 / 다음 행동 |
|---|---|---|---|---|---|---|
| 1 | 이 글이 kubeadm 설치를 안내함 | 설명 | 통과 | — | — | 이 페이지는 kubeadm 설치 방법만 보여 준다. |
| 2 | 설치 후 클러스터 생성은 다른 페이지 | 설명 | 실패 | KSTL-EXP-002 | Style | kubeadm으로 클러스터를 만드는 안내는 ‘kubeadm으로 클러스터 생성하기’ 페이지에 있다. |
| 3 | 머신 RAM 하한, 미만이면 앱 공간 부족 | 설명 | 통과 | — | — | 머신 RAM이 2GB보다 적으면 앱이 쓸 공간이 거의 없다. |
| 4 | 컨트롤 플레인 CPU 하한 | 설명 | 통과 | — | — | 컨트롤 플레인 머신은 CPU가 2개 이상이어야 한다. |
| 5 | 설치 바이너리가 동적 링킹이고 glibc를 가정 | 설명 | 실패 | KSTL-EXP-003 | Style | kubeadm은 동적 링킹 바이너리로 깔리며 대상에 glibc가 있다고 본다. |
| 6 | 그 가정은 흔한 배포판엔 맞고 알파인 계열엔 아님 | 설명 | 통과 | — | — | glibc 가정은 흔한 리눅스에는 맞지만 알파인처럼 glibc 없는 가벼운 배포판에는 안 맞을 수 있다. |
| 7 | 스왑이 있으면 kubelet 기본은 기동 실패 | 설명 | 통과 | — | — | 노드에 스왑이 잡히면 kubelet은 기본으로 시작하지 않는다. |
| 8 | 스왑을 끄거나 kubelet이 허용해야 함 | 설명 | 실패 | KSTL-EXP-005 | Style | 스왑을 끄거나 kubelet이 스왑을 허용하게 바꿔야 한다. |
| 9 | 스왑을 잠시 끄는 방법 | 절차 | 통과 | — | — | `sudo swapoff -a`로 지금 스왑만 끈다. |
| 10 | 지침이 시스템 업그레이드에서 쿠버네티스 패키지를 뺌 | 경고 | 실패 | KSTL-SAF-001 | Accuracy | 묻기: 이 경고의 회피 행동은 무엇인가? ① 패키지 hold 유지 ② 업그레이드 문서 따르기. 원문에 회피가 없다. |
| 11 | 뺀 이유: kubeadm·쿠버네티스 업그레이드는 별도 주의 | 경고 | 실패 | KSTL-SAF-001 | Accuracy | 묻기: 그 주의의 한 동작과 주체는 누구·무엇인가. 원인만 있고 회피가 없다. |
| 12 | apt 인덱스 갱신 후 리포지터리용 패키지 설치 | 절차 | 실패 | KSTL-DOC-001 | Style | 한 문장에 갱신과 설치가 있다. 다음 한 동작은 `apt` 인덱스 갱신이다. |
| 13 | apt 색인 갱신, 세 도구 설치, 버전 고정 | 절차 | 실패 | KSTL-DOC-001, KSTL-TER-001 | Style, Terminology | 한 문장에 갱신·설치·고정이 있다. 다음 한 동작은 `apt` 색인 갱신이다. |
| 14 | 런타임과 kubelet cgroup 드라이버를 맞출 것, 아니면 오류 | 경고 | 실패 | KSTL-SAF-001, KSTL-SYN-002 | Accuracy | 묻기: cgroup 드라이버를 맞추는 사람은 누구인가? ① 노드 설치자 ② 클러스터 관리자. 원인·결과·회피가 한 문장에 붙어 있다. |

10·11·14는 게이트다. 행위자·회피를 지어내지 않는다.

## 이 보고서 셀프 점검

| ID | 결과 | 메모 |
|---|---|---|
| A1 | 예 | 고친 전문 없음. 통과/실패와 한 줄만. |
| A4 | 예 | 인용한 잠금은 아래와 같다. 손대지 않았다. |
| A5 | 예 | 점수·등급·BLEU 없음. |
| A8 | 예 | 끝은 검사 트레일러. 고침 트레일러 아님. |
| A7 | 예 | SYN-002·SAF-001은 물었다. |

A4 잠금(발췌에 있는 것만, 인용 시 byte 동일):

- `kubeadm`
- `glibc`
- 2GB
- RAM
- 2개
- CPU
- `sudo swapoff -a`
- `apt`
- `sudo apt-get update`
- `sudo apt-get install -y apt-transport-https ca-certificates curl gpg`
- kubelet, kubeadm, kubectl
- `sudo apt-get install -y kubelet kubeadm kubectl`
- `sudo apt-mark hold kubelet kubeadm kubectl`
- cgroup

## 커버리지

| ID | 대상 | 이번 |
|---|---|---|
| F2 | 절차 | yes — 9, 12, 13 |
| F3 | 경고 | yes — 10, 11, 14 |
| F4 | 게이트 | yes — SAF-001, SYN-002 |

D1·D2는 절차·경고에만. 9는 다음 행동이 하나. 12·13은 원문이 둘 이상이라 실패. 10·11·14는 한 동작을 원문에서 확정하지 못해 물었다.

## 집계

문장 14 · 통과 6 · 실패 8

- KSTL-EXP-002 ×1
- KSTL-EXP-003 ×1
- KSTL-EXP-005 ×1
- KSTL-DOC-001 ×2
- KSTL-TER-001 ×1
- KSTL-SAF-001 ×3
- KSTL-SYN-002 ×1

품질 점수 없음.

## 관찰

- 번역투 EXP가 설명문에 바로 걸린다. `통해`·`에 대한`·`에 의해`.
- apt 단계 서술어는 둘·셋인데 아래 셸은 이미 명령이 나뉘어 있다. DOC-001 정탐.
- 패키지 제외 경고는 결과·원인만 있고 회피가 없다. SAF-001은 물어야 한다.
- 같은 개념을 12는 인덱스, 13은 색인이라 한다. TER-001.
- 일반 절차의 생략 주어는 설치 독자 하나로 보고 SYN-002를 걸지 않았다. cgroup 경고만 주체가 갈릴 수 있어 물었다.

통과 6 · 실패 8 · EXP-002 ×1 · EXP-003 ×1 · EXP-005 ×1 · DOC-001 ×2 · TER-001 ×1 · SAF-001 ×3 · SYN-002 ×1
