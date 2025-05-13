# test_login.py
from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)


user_data = {
        "email": "tester@example.com",  # 이메일 형식 수정
        "name": "pytest",
        "password": "1234"
    }

@pytest.fixture
def get_token():
    # 로그인 요청 (username, password에 맞는 값을 사용)
    response = client.post(
        "/users/login",
        data={"email": user_data["email"],
              "password": user_data["password"],
              "device_id": "string4"}
    )
    print(f"로그인 응답: {response.json()}")
    assert response.status_code == 200
    # 응답에서 access_token 추출하여 반환
    token = response.json()
    return token  # token["access_token"], token["refresh_token"]



def test_sign_up():
    print('회원가입 진행')
    response = client.post("/users/signup", json=user_data)
    print(f"회원가입 응답: {response.json()}")
    assert response.status_code == 200
    #return user_data

def test_login_success():
    response = client.post("/users/login", data={  
        "email": user_data["email"],
        "password": user_data["password"],
        "device_id": "string2"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    
def test_create_todo(get_token):
    response = client.post("/todos", 
    json={
            "title": "first",
            "description": "string",
            "todo_date": "2025-05-13T12:09:48.432Z"
    },
    headers={"Authorization": f"Bearer {get_token['access_token']}"}
    )
    assert response.status_code==200
    response = client.post("/todos", 
    json={
            "title": "second",
            "description": "string",
            "todo_date": "2025-05-14"
    },
    headers={"Authorization": f"Bearer {get_token['access_token']}"}
    )
    assert response.status_code==200
    
    response = client.post("/todos", 
    json={
            "title": "third",
            "description": "string",
            "todo_date": "2025-05-13T05:09:48.432Z"
    },
    headers={"Authorization": f"Bearer {get_token['access_token']}"}
    )
    assert response.status_code==200
    
def test_update_todo(get_token):
    response = client.put("/todos/3", 
    json={
            "title": "update test title",
            "description": "update description",
            "todo_date": "2025-05-15",
            "complete": 1
        },
    headers={"Authorization": f"Bearer {get_token['access_token']}"}
    )
    assert response.status_code==200

def test_get_todos(get_token):
    response = client.get("/todos/2", 
    headers={"Authorization": f"Bearer {get_token['access_token']}"}
    )
    print(f'get todo/2: {len(response.json())}')
    assert response.status_code==200
    
def test_get_todos_search(get_token):
    response = client.get("/todos/search/?date=2025-05-13", 
    headers={"Authorization": f"Bearer {get_token['access_token']}"}
    )
    json_data = response.json()
    assert len(json_data)==2
    
def test_delete_todos(get_token):
    response = client.request(
        method="DELETE",
        url="/todos/3",
        headers={"Authorization": f"Bearer {get_token['access_token']}"}
    )
    assert response.status_code==200

def test_delete_user(get_token):
    response = client.request(
        method="DELETE",
        url="/users/me",
        json={"password": user_data["password"]},
        headers={"Authorization": f"Bearer {get_token['access_token']}"}
    )
    assert response.status_code==200
    
