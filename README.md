# README.md

# 목차
1. [개요](#개요)   
2. [환경설치](#환경설치)   
3. [DB 초기화](#DB-초기화)   
4. [서버실행](#서버실행)
5. [단위테스트](#단위-테스트)
6. [API 명세정보](#API-명세정보)
8. [JWT 발급 및 검증흐름 다이어그램](#JWT-발급-및-검증흐름-다이어그램)

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
# DB 초기화
```bash
python init_db.py
```
# 서버실행

1. uvicorn 실행

```bash
uvicorn app.main:app --reload  
```

1. 서버 정상 접속 확인

정상적으로 구동이 된다면 [표기된 링크](http://127.0.0.1:8000)로 정상 접속을 확인합니다.

<img src="/public/paste-image/README/2025-05-13-01-33-21.png" width="75%" />
<img src="/public/paste-image/README/2025-05-13-01-37-02.png" width="75%" />

# 단위 테스트
uvicorn을 실행한 터미널은 그대로 유지하고, 

새로운 터미널을 가상환경 활성화 상태에서
아래 명령어로 테스트 코드를 실행합니다.
## test_login.py
```bash
pytest tests/test_login.py -v
```
테스트는 아래 단계로 진행됩니다.

1. 회원가입
2. 로그인 및 토큰 발행 확인
3. 사용자 정보 조회(유효한 토큰)
4. 사용자 정보 수정
5. 사용자 정보 조회(토큰 없음) - 401
6. 로그인 시도(잘못된 암호) -400
7. 로그인 시도(잘못된 email) - 404 
8. access_token 갱신
9. 사용자 정보 삭제
![image](https://github.com/user-attachments/assets/0f15318c-b642-4d0c-8ed5-d0bc379f6a88)

## test_todo.py
```bash
pytest tests/test_todo.py -v
```
테스트는 아래 단계로 진행됩니다.
1. 회원가입
2. 로그인 및 토큰 발행 확인
3. 일정 정보 생성
4. 일정 정보 수정
5. 특정 일정 정보 조회
6. 일정 정보 검색(Search)
7. 일정 정보 삭제
8. 사용자 삭제
![image](https://github.com/user-attachments/assets/e0fb7142-206d-48c1-ae90-162899bd8501)

# API 명세정보

서버가 정상 구동된 다음, 아래 링크에서 API 정보를 확인할 수 있습니다.

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

[http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

<img src="/public/paste-image/README/2025-05-13-01-39-35.png" width="75%" />

# JWT 발급 및 검증흐름 다이어그램
<details>
<summary>
  원본파일 확인하기
</summary>
  
[draw.io](https://draw.io)를 통해 원본파일([diagrams.drawio](https://github.com/idleh4021/FastAPI_JWT_Sample/blob/main/diagrams.drawio))을 확인하실 수 있습니다.
![image](https://github.com/user-attachments/assets/33119001-0ede-4f22-8072-2f1a062c9fa2)
</details>

![image](https://github.com/user-attachments/assets/1293b54c-2210-4903-94c8-e1785b14cd88)

