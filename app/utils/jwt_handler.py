from jose import JWTError,jwt
from datetime import datetime,timedelta


SECRET_KEY = 'my-secret-key'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 1440*30000  # 1일

# Access Token 생성
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Refresh Token 생성
def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> dict:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES))
    #to_encode.update({'exp': expire})
    
    return {"refresh_token" : jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM),"expired_at" : expire }

# 토큰 디코딩
def decode_token(token: str) -> dict:
    # 'bearer ' 문자열 제거 (대소문자 구분 없음)
    if token.lower().startswith("bearer "):
        token = token[7:]
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

