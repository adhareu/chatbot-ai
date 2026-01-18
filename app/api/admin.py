from fastapi import APIRouter, Header, HTTPException
from app.services.redis_api_key_store import create_api_key, list_api_keys,get_client_plan,set_client_plan
from app.core.redis_client import get_redis_client
from app.services.redis_api_key_store import get_client_plan
import os

redis_client = get_redis_client()
QUOTA_PREFIX = os.getenv("REDIS_QUOTA_PREFIX", "quota:")
router = APIRouter(prefix="/admin", tags=["Admin"])
MASTER_KEY = os.getenv("MASTER_ADMIN_KEY")

def check_master_key(x_master_key: str = Header(...)):
    if x_master_key != MASTER_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

@router.post("/api-keys")
def admin_create_api_key(client_name: str, x_master_key: str = Header(...)):
    check_master_key(x_master_key)
    key = create_api_key(client_name)
    return {"client_name": client_name, "api_key": key}

@router.get("/api-keys")
def admin_list_api_keys(x_master_key: str = Header(...)):
    check_master_key(x_master_key)
    return list_api_keys()

@router.get("/usage")
def admin_usage(x_master_key: str = Header(...)):
    check_master_key(x_master_key)
    keys = redis_client.keys(f"{QUOTA_PREFIX}*")
    usage = {}
    for k in keys:
        client = k.replace(QUOTA_PREFIX, "")
        usage[client] = int(redis_client.get(k))
    return usage
@router.post("/api-keys")
def admin_create_api_key(
    client_name: str,
    plan: str = "free",
    x_master_key: str = Header(...)
):
    check_master_key(x_master_key)
    key = create_api_key(client_name, plan)
    return {
        "client_name": client_name,
        "plan": plan,
        "api_key": key
    }
@router.get("/clients")
def list_clients(x_master_key: str = Header(...)):
    check_master_key(x_master_key)
    keys = redis_client.keys("client_plan:*")
    clients = {}

    for k in keys:
        client = k.replace("client_plan:", "")
        plan = redis_client.get(k)
        usage = redis_client.get(f"quota:{client}") or 0
        clients[client] = {
            "plan": plan,
            "daily_usage": int(usage)
        }
    return clients
@router.get("/analytics/{client_name}")
def get_client_analytics(
    client_name: str,
    x_master_key: str = Header(...)
):
    check_master_key(x_master_key)
    redis_client = get_redis_client()

    total = int(redis_client.get(
        f"analytics:client:{client_name}:total"
    ) or 0)

    last_seen = redis_client.get(
        f"analytics:client:{client_name}:last_seen"
    )

    # Per-endpoint stats
    endpoint_keys = redis_client.keys(
        f"analytics:client:{client_name}:endpoint:*"
    )
    endpoints = {
        k.split(":")[-1]: int(redis_client.get(k))
        for k in endpoint_keys
    }

    # Hourly usage (today)
    hour_keys = redis_client.keys(
        f"analytics:client:{client_name}:hour:*"
    )
    hourly = {
        k.split(":")[-1]: int(redis_client.get(k))
        for k in hour_keys
    }

    return {
        "client": client_name,
        "plan": get_client_plan(client_name),
        "total_requests": total,
        "last_seen": last_seen,
        "per_endpoint": endpoints,
        "hourly_usage": hourly
    }
@router.get("/analytics")
def analytics_all_clients(x_master_key: str = Header(...)):
    check_master_key(x_master_key)
    redis_client = get_redis_client()

    clients = redis_client.keys("client_plan:*")
    result = {}

    for c in clients:
        client = c.replace("client_plan:", "")
        total = redis_client.get(
            f"analytics:client:{client}:total"
        ) or 0
        result[client] = {
            "plan": redis_client.get(c),
            "total_requests": int(total)
        }

    return result


