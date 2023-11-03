from fastapi import HTTPException, Security
from fastapi.security import api_key

api_key_header = api_key.APIKeyHeader(name="X-API-KEY")

API_KEY = "123"

async def validate_api_key(key: str = Security(api_key_header)):
    if key != API_KEY:
        raise HTTPException(
            status_code=401, detail="Unauthorized - API Key is wrong"
        )
    return None