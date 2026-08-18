# 발췌 — FastAPI 첫걸음

출처: <https://fastapi.tiangolo.com/ko/tutorial/first-steps/>
표시: 페이지가 “AI와 사람이 함께한 번역”이라고 밝힘.
용도: preo 셀프 QA 픽스처. k8s와 다른 장르(프레임워크 튜토리얼). 전문을 저장하지 않는다.

이 번역은 사람의 안내를 받아 AI가 만들었습니다. 원문의 의미를
오해하거나 부자연스러워 보이는 등 오류가 있을 수 있습니다.

가장 단순한 FastAPI 파일은 다음과 같이 보일 것입니다:

```python
from fastapi import FastAPI
app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Hello World"}
```

위 코드를 `main.py`에 복사합니다.

라이브 서버를 실행합니다:

```
$ fastapi dev
```

해당 줄은 로컬 머신에서 애플리케이션이 서비스되는 URL을 보여줍니다.

브라우저로 http://127.0.0.1:8000를 여세요.

아래와 같은 JSON 응답을 볼 수 있습니다:

```
{"message": "Hello World"}
```

이제 http://127.0.0.1:8000/docs로 가봅니다.

"스키마"는 무언가의 정의 또는 설명입니다. 이를 구현하는 코드가 아니라
추상적인 설명일 뿐입니다.

이 경우, OpenAPI는 여러분의 API 스키마를 어떻게 정의하는지 지시하는
규격입니다.

"경로"는 일반적으로 "엔드포인트" 또는 "라우트"라고도 불립니다.

`fastapi dev` 명령어에 파일 경로를 전달할 수도 있으며, 그러면 사용할
FastAPI 애플리케이션 객체를 추정합니다:

```
$ fastapi dev main.py
```

하지만 매번 `fastapi` 명령어를 호출할 때마다 올바른 path\\entrypoint를
전달해야 합니다.
