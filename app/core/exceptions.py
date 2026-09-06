# BizException 体系(迁移 exception.py) + 各 HTTP 异常 handler
class BizException(Exception):
    def __init__(self, msg: str, status_code: int = 400):
        super().__init__(msg)
        self.status_code = status_code


class InvalidCredentialsError(BizException):  # 登录失败 → 401
    def __init__(self, msg='登录失败'):
        super().__init__(msg, status_code=401)


class UsernameDuplicatedError(BizException):  # 注册重名 → 409
    def __init__(self, msg='注册重名'):
        super().__init__(msg, status_code=409)


class UserNotFoundError(BizException):  # 目标用户不存在 → 404
    def __init__(self, msg='用户不存在'):
        super().__init__(msg, status_code=404)


class PermissionDeniedError(BizException):  # 权限不足 → 403
    def __init__(self, msg='权限不足'):
        super().__init__(msg, status_code=403)


class OldPasswordError(BizException):   # 原密码错 → 400
    def __init__(self, msg='原密码错误'):
        super().__init__(msg, status_code=400)
