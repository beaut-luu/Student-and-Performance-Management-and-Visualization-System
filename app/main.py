# FastAPI 入口：lifespan 初始化日志/连接池、注册 api_router、挂全局异常
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.logging_conf import init_logger, shutdown


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_logger()
    yield
    shutdown()


app = FastAPI(lifespan=lifespan)
