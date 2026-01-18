import os
from app.core.redis_client import get_redis_client
from app.services.redis_api_key_store import get_client_plan
from app.core.plans import PLANS

redis_client = get_redis_client()

QUOTA_PREFIX = os.getenv("REDIS_QUOTA_PREFIX", "quota:")
TTL_SECONDS = 86400

def check_and_increment_quota(client_id: str):
    plan = get_client_plan(client_id)
    limit = PLANS.get(plan)

    # Enterprise = unlimited
    if limit is None:
        return True, "unlimited", "unlimited"

    key = f"{QUOTA_PREFIX}{client_id}"
    current = redis_client.get(key)

    if current is None:
        redis_client.set(key, 1, ex=TTL_SECONDS)
        return True, 1, limit

    current = int(current)

    if current >= limit:
        return False, current, limit

    redis_client.incr(key)
    return True, current + 1, limit
