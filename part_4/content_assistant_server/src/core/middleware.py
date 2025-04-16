from functools import lru_cache
from fastapi import FastAPI, Request
from src.settings import settings
from fastapi.middleware.cors import CORSMiddleware

## this file will be used in part 4

# @lru_cache
# def get_settings():
#     return settings

def add_cors_middleware(app: FastAPI) -> FastAPI: 
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    
    return app

# async def add_settings_to_request(request: Request, call_next):
#     request.state.settings = get_settings()
#     response = await call_next(request)
#     return response

# def add_settings_middleware(app: FastAPI) -> FastAPI:
#     app.middleware("http")(add_settings_to_request)
#     return app

MIDDLEWARE = [add_cors_middleware]

def apply_middleware(app: FastAPI) -> FastAPI:
    for middleware in MIDDLEWARE:
        app = middleware(app)
    return app