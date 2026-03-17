from fastapi import Header, HTTPException

from app.config import API_KEY


async def verify_api_key(x_api_key: str = Header(default=None)) -> str:
    if x_api_key is None or x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden: invalid or missing API key")
    return x_api_key
