from fastapi import APIRouter

from .endpoints import authentication, aws

api_router = APIRouter()
api_router.include_router(
    authentication.router, prefix="/auth", tags=["authentication"]
)
api_router.include_router(aws.router, prefix="/aws", tags=["aws"])
