import os
import redis
import uuid
from app.core.redis_client import get_redis_client
from app.core.plans import PLANS
redis_client = get_redis_client()
API_KEY_PREFIX = os.getenv("REDIS_API_KEY_PREFIX", "api_key:")

def create_api_key(client_name: str, plan: str = "free") -> str:
    if plan not in PLANS:
        raise ValueError("Invalid plan")

    key = str(uuid.uuid4())
    redis_client.set(f"{API_KEY_PREFIX}{key}", client_name)
    redis_client.set(f"client_plan:{client_name}", plan)
    return key


def list_api_keys() -> dict:
    keys = redis_client.keys(f"{API_KEY_PREFIX}*")
    result = {}
    for k in keys:
        client_name = redis_client.get(k)
        api_key = k.replace(API_KEY_PREFIX, "")
        result[api_key] = client_name
    return result

def is_valid_api_key(api_key: str) -> bool:
    return redis_client.exists(f"{API_KEY_PREFIX}{api_key}") == 1

def get_client_plan(client_name: str) -> str:
    return redis_client.get(f"client_plan:{client_name}") or "free"

def set_client_plan(client_name: str, plan: str):
    if plan not in PLANS:
        raise ValueError("Invalid plan")
    redis_client.set(f"client_plan:{client_name}", plan)
    
def get_client_name_from_key(api_key: str) -> str:
    return redis_client.get(f"{API_KEY_PREFIX}{api_key}")
