# bcrypt 哈希校验(复用) + JWT 生成/解析（payload 携带 user_id/jurisdiction）
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import settings


def trans_hash(pwd: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    pwd_hash = bcrypt.hashpw(pwd.encode('utf-8'), salt=salt)
    return pwd_hash.decode('utf-8')


def verify_hash(pwd: str, hashed_pwd: str) -> bool:
    new_pwd_bytes = pwd.encode('utf-8')
    return bcrypt.checkpw(new_pwd_bytes, hashed_pwd.encode('utf-8'))


def create_access_token(username: str, jurisdiction: str, expires: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    payload = {
        "sub": username,
        "jurisdiction": jurisdiction,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=expires),  # 过期时间
        "iat": datetime.now(timezone.utc)  # 签发时间
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token) -> dict:  # 解析校验token
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
