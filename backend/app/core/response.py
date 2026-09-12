# 成功统一响应体 {code, message, data}
from typing import Any
from pydantic import BaseModel


class SuccessResponse(BaseModel):
    status_code: int = 0
    message: str = "success"
    data: Any = None
