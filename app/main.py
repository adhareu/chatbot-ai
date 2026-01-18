import logging
from dotenv import load_dotenv
load_dotenv()
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from fastapi import Request
from app.core.logger import setup_logger
from fastapi import FastAPI
from fastapi import Depends
from fastapi.openapi.utils import get_openapi

from app.schemas import ChatRequest, ChatResponse
from app.services.chat_service import generate_reply
from app.api.auth import router as auth_router
from app.core.dependencies import get_current_client
from app.api.admin import router as admin_router
from app.services.quota_service import check_and_increment_quota
from fastapi import HTTPException
from app.services.analytics_service import track_request
setup_logger()
logger = logging.getLogger("app")


app = FastAPI(title="AI Chatbot API")
app.include_router(auth_router)
app.include_router(admin_router)
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="AI Chatbot API",
        version="0.1.0",
        description="AI Chatbot with JWT Authentication",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Apply globally (optional but recommended)
    openapi_schema["security"] = [
        {"BearerAuth": []}
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
@limiter.limit("5/minute")
def chat(
    request: Request,
    payload: ChatRequest,
    client=Depends(get_current_client)
):
    client_id = client["client"]

    allowed, used, limit = check_and_increment_quota(client_id)

    if not allowed:
        raise HTTPException(
            status_code=429,
            detail=f"Daily quota exceeded ({limit} requests/day)"
        )
    
    logger.info(
        f"Chat | client={client_id} | usage={used}/{limit} | session={payload.session_id}"
    )

    reply = generate_reply(
        message=payload.message,
        session_id=payload.session_id
    )
    track_request(
    client_id=client_id,
    endpoint="chat"
    )
    return ChatResponse(reply=reply, session_id=payload.session_id)

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests. Please slow down."}
    )
app.openapi = custom_openapi