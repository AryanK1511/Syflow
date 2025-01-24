import logging

from backend.app.config import settings

logger = logging.getLogger("uvicorn")
logger.setLevel(settings.LOG_LEVEL)
