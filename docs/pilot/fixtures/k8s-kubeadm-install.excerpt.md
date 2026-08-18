# 발췌 — kubeadm 설치하기

출처: <https://kubernetes.io/ko/docs/setup/production-environment/tools/kubeadm/install-kubeadm/>
라이선스: 쿠버네티스 웹사이트 문서, CC BY 4.0.
용도: preo 셀프 QA 픽스처(A4 byte 보존, F2 절차, F3 경고). 전문을 저장하지 않는다.

이 페이지에서는 `kubeadm` 툴박스 설치 방법을 보여준다. 이 설치 프로세스를
수행한 후 kubeadm으로 클러스터를 만드는 방법에 대한 자세한 내용은
kubeadm으로 클러스터 생성하기 페이지를 참고한다.

머신당 2GB 이상의 RAM (이보다 적으면 앱을 위한 공간이 거의 남지 않는다).
컨트롤 플레인 머신에는 2개 이상의 CPU.

`kubeadm` 설치는 동적 링킹을 사용하는 바이너리를 통해 수행되며 대상
시스템이 `glibc`를 제공한다고 가정한다. 이는 많은 리눅스 배포판에서
합리적인 가정이지만 알파인 리눅스와 같이 기본적으로 `glibc`를 포함하지
않는 커스텀 및 경량 배포판에서는 항상 그런 것은 아니다.

노드에서 스왑 메모리가 감지되면 kubelet의 기본 동작은 시작에 실패하는
것이다. 이는 스왑이 비활성화되거나 kubelet에 의해 용인되어야 함을
의미한다. 스왑을 비활성화하려면, `sudo swapoff -a`를 사용하여 일시적으로
스와핑을 비활성화할 수 있다.

#### 경고:

이 지침은 모든 시스템 업그레이드에서 모든 쿠버네티스 패키지를 제외한다.
이는 kubeadm 및 쿠버네티스를 업그레이드 하는 데 특별한 주의가 필요하기
때문이다.

1. `apt` 패키지 인덱스를 업데이트하고 쿠버네티스 `apt` 리포지터리를
   사용하는 데 필요한 패키지를 설치한다.

```shell
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gpg
```

2. 쿠버네티스 패키지 리포지터리용 공개 서명 키를 다운로드한다.

```shell
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.36/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
```

4. `apt` 패키지 색인을 업데이트하고, kubelet, kubeadm, kubectl을
   설치하고 해당 버전을 고정한다.

```shell
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
```

#### 경고:

컨테이너 런타임과 kubelet의 cgroup 드라이버를 일치시켜야 하며, 그렇지
않으면 kubelet 프로세스에 오류가 발생한다.
