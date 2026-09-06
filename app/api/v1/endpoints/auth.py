'''路由层只做一件事——从依赖注入拿 operator，从 body 拿参数，转发给 service，再包装响应。
路由里不出现 if/else 权限判断、不出现字符串比对。'''
# /auth/register  /auth/login
# 写接口，收参数调用service层函数，回响应