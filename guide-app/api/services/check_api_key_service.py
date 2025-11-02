from fastapi import HTTPException

from core.config import settings

API_KEY = settings.jwt.api_key


def check_api_key(api_key: str) -> None:
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API key.")
