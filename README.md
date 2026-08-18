# preo

한국어 기술문서의 꼬인 문장을 풉니다.

```
로드되어지면 → 로드되면
배포에 대한 절차 → 배포 절차
만료된 경우 → 만료되면
대시보드를 통해 확인 → 대시보드에서 확인
스케줄러에 의해 실행 → 스케줄러가 실행
```

**before** — FastAPI

이 경우, OpenAPI는 여러분의 API 스키마를 어떻게 정의하는지 지시하는 규격입니다.

**after**

OpenAPI는 API 스키마를 어떻게 적을지 정해 둔 규격이다.

이미 읽히면 안 건드린다: 위 코드를 `main.py`에 복사합니다.

**before** — Kubernetes

이는 스왑이 비활성화되거나 kubelet에 의해 용인되어야 함을 의미한다.

**after**

스왑을 끄거나, kubelet이 스왑을 허용해야 한다.

인용: [FastAPI 첫걸음](https://fastapi.tiangolo.com/ko/tutorial/first-steps/), [kubeadm 설치하기](https://kubernetes.io/ko/docs/setup/production-environment/tools/kubeadm/install-kubeadm/) (CC BY 4.0). 명령·URL·숫자는 그대로 둔다.

```
npx skills add domuk-k/preo
```

또는 `/plugin marketplace add domuk-k/preo` 후 `/plugin install preo@preo`.

“이 문서 풀어줘” · “검사만 해줘” · “풀어로 써줘”

규칙: [standard/README.md](standard/README.md). 연구: [research/bibliography.md](research/bibliography.md).

```bash
uv sync --locked && uv run pytest && uv run python scripts/validate_links.py
```

> ASD 또는 STEMG와 제휴하거나 이들의 승인을 받은 프로젝트가 아닙니다.
> ASD-STE100은 참고자료입니다. 표준 원문이나 통제 사전을 재배포하지 않습니다.

[라이선스](LICENSES/README.md) · [Apache 2.0](LICENSE) · [CC BY 4.0](LICENSES/CC-BY-4.0.txt) · [기여](CONTRIBUTING.md)
