from fastapi import APIRouter, status
from fastapi.requests import Request

router = APIRouter(tags=["Core Endpoints"])

@router.get("/health", status_code=status.HTTP_200_OK)
async def healthcheck(request: Request) -> dict:
    return {"version": request.app.version}