from fastapi import APIRouter, Header, HTTPException
from app.core.api_key import is_valid_api_key_client as is_valid_api_key
from app.core.security import create_access_token
from app.services.redis_api_key_store import get_client_name_from_key
router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/token")
def get_token(x_api_key: str = Header(...)):
    if not is_valid_api_key(x_api_key):
        raise HTTPException(status_code=401, detail="Invalid API Key")
    client_name = get_client_name_from_key(x_api_key)
    token = create_access_token({"client": client_name})
    return {"access_token": token, "token_type": "bearer"}
