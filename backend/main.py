# FastAPI 入口：lifespan 初始化日志/连接池、注册 api_router、挂全局异常
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from app.core.database import create_table
from app.core.logging_conf import init_logger, shutdown
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.exceptions import BizException
from app.api.v1.router import api_router
from app.models.dataseed import data_seed_init


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_logger()
    await create_table()
    await data_seed_init()
    yield
    shutdown()


app = FastAPI(title='学生管理系统', lifespan=lifespan)


# 跨域配置：供未来 Vue3(http://localhost:5173) 联调使用
# 忽略下方函数的静态检查错误
# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(BizException)
async def biz_exception_handler(_request: Request, exp: BizException):
    """_告诉 IDE：这个变量参数我代码里不会使用,
    @app.exception_handler函数要求第一个参数必须是HTTP请求"""
    return JSONResponse(
        status_code=exp.status_code,
        content={'status_code': exp.status_code, 'message': exp.msg, 'data': None}
    )


app.include_router(api_router)


@app.get('/', summary='健康检查')
async def health_check():
    return {'status': 'ok'}
