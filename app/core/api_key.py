from app.services.redis_api_key_store import is_valid_api_key

def is_valid_api_key_client(api_key: str) -> bool:
    return is_valid_api_key(api_key)
