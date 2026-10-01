# 汇总子路由 → /api/v1
from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, activity


api_router = APIRouter(prefix='/api/v1')
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(activity.router)
