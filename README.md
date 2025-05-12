# README.md

# 개요

FastAPI를 이용한 JWT로그인/Todo CRUD를 구현한 과제 제출용 프로젝트입니다.

# 환경설치

1. 가상환경 설치 및 활성화

```bash
#가상환경 생성
python -m venv env_temp

#가상환경 활성화
.\env_temp\Scripts\activate
```

활성화 후 터미널에서(env_temp) 확인

1. pip 패키지 설치 및 확인

```bash
#패키지 설치
pip install -r requirements.txt

#설치 패키지 확인
pip list
```

# 서버실행

1. uvicorn 실행

```bash
uvicorn app.main:app --reload  
```

1. 서버 정상 접속 확인

정상적으로 구동이 된다면 [표기된 링크](http://127.0.0.1:8000)로 정상 접속을 확인합니다.

<img src="/public/paste-image/README/2025-05-13-01-33-21.png" width="75%" />
<img src="/paste-image/README/2025-05-13-01-37-02.png" width="75%" />

# API 명세정보

서버가 정상 구동된 다음, 아래 링크에서 API 정보를 확인할 수 있습니다.

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

[http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

<img src="/paste-image/README/![alt%20text](image-2.png).png" width="75%" />