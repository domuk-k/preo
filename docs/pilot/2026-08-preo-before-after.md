# preo before / after

검사만 리허설에서 **고침 규칙이 걸린 문장**만 다시 쓴다. 게이트는 안 고친다.
명령·URL·숫자·코드는 byte 동일. 합격선이 아니다.

출처: [kubeadm 설치 (KO)](https://kubernetes.io/ko/docs/setup/production-environment/tools/kubeadm/install-kubeadm/) CC BY 4.0,
[FastAPI 첫걸음 (KO)](https://fastapi.tiangolo.com/ko/tutorial/first-steps/).

## 고침 — k8s

### EXP-002 `~에 대한`

**before**

이 설치 프로세스를 수행한 후 kubeadm으로 클러스터를 만드는 방법에 대한
자세한 내용은 kubeadm으로 클러스터 생성하기 페이지를 참고한다.

**after**

이 설치를 끝낸 뒤, kubeadm으로 클러스터를 만드는 방법은 kubeadm으로
클러스터 생성하기 페이지에 있다.

잠금: 설치 다음 → 클러스터 생성 안내. 페이지 이름 그대로.

### EXP-003 `~를 통해`

**before**

`kubeadm` 설치는 동적 링킹을 사용하는 바이너리를 통해 수행되며 대상
시스템이 `glibc`를 제공한다고 가정한다.

**after**

`kubeadm`은 동적 링킹 바이너리로 설치되며, 대상 시스템에 `glibc`가
있다고 가정한다.

잠금: 동적 링킹, `glibc` 가정. `kubeadm`·`glibc` 그대로.

### EXP-005 `~에 의해`

**before**

이는 스왑이 비활성화되거나 kubelet에 의해 용인되어야 함을 의미한다.

**after**

스왑을 끄거나, kubelet이 스왑을 허용해야 한다.

잠금: 끄기 **또는** 허용. 둘 다 필요하진 않음.

### DOC-001 한 문장에 행동 둘·셋

**before**

`apt` 패키지 인덱스를 업데이트하고 쿠버네티스 `apt` 리포지터리를
사용하는 데 필요한 패키지를 설치한다.

**after**

`apt` 패키지 인덱스를 업데이트한다. 쿠버네티스 `apt` 리포지터리에 필요한
패키지를 설치한다.

아래 셸은 이미 나뉘어 있으므로 명령은 안 건드린다.

```shell
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gpg
```

**before**

`apt` 패키지 색인을 업데이트하고, kubelet, kubeadm, kubectl을 설치하고
해당 버전을 고정한다.

**after**

`apt` 패키지 색인을 업데이트한다. kubelet, kubeadm, kubectl을 설치한다.
해당 버전을 고정한다.

```shell
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
```

`인덱스`/`색인`은 용어표가 없어 하나로 합치지 않았다.

## 안 고침 — 게이트

원문에 없는 회피·주어를 채우지 않는다.

| before (요지) | 하는 일 |
|---|---|
| 지침이 시스템 업그레이드에서 쿠버네티스 패키지를 뺀다 | 묻기: 회피 행동이 뭔가 |
| cgroup 드라이버를 맞출 것, 아니면 kubelet 오류 | 묻기: 맞추는 사람은 누구인가 |
| FastAPI: 파일 경로를 넘기면 앱 객체를 추정한다 | 묻기: 추정하는 주체가 `fastapi dev`인가 독자인가 |

## 이미 읽힘 — FastAPI

고칠 표면이 거의 없었다. 예:

**before = after**

위 코드를 `main.py`에 복사합니다.

라이브 서버를 실행합니다: `fastapi dev`

브라우저로 http://127.0.0.1:8000를 여세요.

`"경로"는 일반적으로 "엔드포인트" 또는 "라우트"라고도 불립니다.`
(동의어를 설명하는 문장이라 하나로 강제하지 않음.)
