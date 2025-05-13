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

def test_sign_up():
    print('회원가입 진행')
    response = client.post("/users/signup", json=user_data)
    print(f"회원가입 응답: {response.json()}")
    assert response.status_code == 200
    # return user_data

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


def test_get_user_me(get_token):
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {get_token['access_token']}"}
    )
    assert response.status_code == 200

def test_update_user(get_token):
    response = client.put(
        "/users/me",
        json={"name":"changedName",
              "old_password": user_data["password"],
              "new_password": user_data["password"]
              },
        headers={"Authorization": f"Bearer {get_token['access_token']}"}
    )
    assert response.status_code==200

def test_get_user_me_use_without_access_token():
    response = client.get(
        "/users/me",
        #headers={"Authorization": f"Bearer {'wrong access_token'}"}
    )
    assert response.status_code == 401

def test_login_fail_wrong_password():
    response = client.post("/users/login", data={ 
        "email": user_data["email"],
        "password": "wrongpassword",
        "device_id": "string4"
    })
    assert response.status_code == 400  
    # assert response.json()["detail"] == "Invalid credentials"

def test_login_fail_unknown_user():
    response = client.post("/users/login", data={  
        "email": "unknown",
        "password": user_data["password"],
        "device_id": "string4"
    })
    assert response.status_code == 404
    
def test_refresh(get_token):
    response = client.post("/users/refresh", json={ 
        "refresh_token": get_token["refresh_token"]
    })
    assert response.status_code ==200
    
def test_delete_user(get_token):
    response = client.request(
        method="DELETE",
        url="/users/me",
        json={"password": user_data["password"]},
        headers={"Authorization": f"Bearer {get_token['access_token']}"}
    )
    assert response.status_code==200