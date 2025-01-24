import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.v1.router import api_router
from backend.app.config import settings
from backend.app.logger import logger
from backend.app.middleware import TokenVerificationMiddleware
from backend.app.response import success_response

file_path = os.path.abspath(__file__)
relative_path = file_path.split("Syflow")[-1]


def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(TokenVerificationMiddleware)
    app.include_router(api_router, prefix="/api/v1")

    return app


# ========== FAST API APPLICATION ==========
app = create_app()


# ========== HEALTH CHECK ROUTE ==========
@app.get("/health")
def health_check():
    logger.debug(f"{relative_path}: Hitting the Health Check Route")
    return success_response("Server is Healthy")
