from fastapi import FastAPI

from app.core.config import settings
from app.api.api_v1.api import api_router


app = FastAPI(openapi_url=f"{settings.API_V1_STR}/openapi.json")

app.include_router(api_router, prefix=settings.API_V1_STR)
