import json
from typing import List, Dict
from app.core.redis_client import get_redis_client

redis_client = get_redis_client()

def _key(session_id: str) -> str:
    return f"chat_history:{session_id}"

def get_history(session_id: str) -> List[Dict]:
    data = redis_client.get(_key(session_id))
    if not data:
        return []
    return json.loads(data)

def append_message(session_id: str, role: str, content: str):
    history = get_history(session_id)
    history.append({
        "role": role,
        "content": content
    })
    redis_client.set(_key(session_id), json.dumps(history), ex=3600)
