# 迁移 logger.py 的队列异步写文件思路，lifespan 中 init/shutdown
# 原样照搬 logger.py 中的代码，将atexit(shutdown)改为lifespan(init/shutdown)
import logging
from logging.handlers import TimedRotatingFileHandler, QueueHandler, QueueListener
import os
import queue
from fastapi import FastAPI
from contextlib import asynccontextmanager


# 保存 listener 的模块级引用
_listener: "QueueListener | None" = None


def init_logger():
    # 设置一个全局变量防止后台线程被Python垃圾回收
    global _listener
    # 设置logger主体
    logger = logging.getLogger('user_sys')
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    if logger.handlers:
        return logger

    # 设置file handler的格式化格式
    file_fm = logging.Formatter('%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s',
                                datefmt='%Y-%m-%d %H:%M:%S'
                                )  # 文件

    # 设置控制台handler
    console_handler = logging.StreamHandler()  # 实例化
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(file_fm)  # 传入我们写的格式化类

    # 设置file handler
    log_path = os.path.join(os.path.dirname(__file__), 'logs')  # 当前路径下的logs文件夹
    os.makedirs(log_path, exist_ok=True)  # 根据地址创建文件，如果已经存在就跳过
    file_handler = TimedRotatingFileHandler(
        f'{log_path}/app.log',
        when='MIDNIGHT',
        interval=1,
        backupCount=7,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(file_fm)

    # 将console_handler添加到logger主线程同步输出将file_handler加到队列中后台写入文件
    logger.addHandler(console_handler)
    # 将file_handler加到队列中后台写入文件
    log_queue = queue.Queue(-1)  # -1代表队列无上限
    logger.addHandler(QueueHandler(log_queue))  # QueueHandler代表动作：将数据传进一个队列
    # 从队列log_queue中取出数据交给file_handler处理，也可以传入多个handler
    _listener = QueueListener(log_queue, file_handler)  # 分工安排
    _listener.start()  # 开始干活

    return logger


def shutdown():
    # 程序退出时的清理：listener 没初始化就直接跳过
    if _listener is not None:
        _listener.stop()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_logger()
    yield
    shutdown()


# app = FastAPI(lifespan=init_loger)
