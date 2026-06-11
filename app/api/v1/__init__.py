from fastapi import APIRouter
from app.api.v1.retention.route import retention_router

api_router = APIRouter()
api_router.include_router(retention_router)

__all__ = []
