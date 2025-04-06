from fastapi import FastAPI
from src import version
from src.core.api import router as core_router
from src.core.logs import logger
from src.content.api import router as content_router

app = FastAPI(version=version)
# apply middleware
app.include_router(core_router)
app.include_router(content_router)

logger.info("App is ready")