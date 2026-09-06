# bcrypt 哈希校验(复用) + JWT 生成/解析（payload 携带 user_id/jurisdiction）
def trans_hash(pwd: str) -> str:
    pass


def verify_hash(pwd: str, hashed_pwd: str) -> bool:
    pass


def create_access_token(username: str, jurisdiction: int,expires: int=None) -> str:
    pass


def decode_token(token) -> dict:  # 解析校验token
    pass