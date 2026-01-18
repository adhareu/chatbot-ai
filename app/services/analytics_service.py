from datetime import datetime
from app.core.redis_client import get_redis_client

redis_client = get_redis_client()

def track_request(client_id: str, endpoint: str):
    now = datetime.utcnow()
    hour_key = now.strftime("%Y%m%d%H")

    redis_client.incr(f"analytics:client:{client_id}:total")
    redis_client.incr(f"analytics:client:{client_id}:endpoint:{endpoint}")
    redis_client.incr(f"analytics:client:{client_id}:hour:{hour_key}")
    redis_client.set(
        f"analytics:client:{client_id}:last_seen",
        now.isoformat()
    )
