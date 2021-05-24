from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from starlette import status
import os

API_KEY = os.getenv("API_KEY")

API_KEY_HEADER = APIKeyHeader(name="Authorization")


def verify_api_key(api_key: str = Depends(API_KEY_HEADER)):
    if api_key == API_KEY:
        return True

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key")
