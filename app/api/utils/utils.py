from fastapi import Header, HTTPException
from app.config.config import config

def verify_api_key(api_key: str = Header(None)):
    if api_key != config.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")