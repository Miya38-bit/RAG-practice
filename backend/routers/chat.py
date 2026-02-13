from fastapi import APIRouter
from services.chat_service import ChatService
from dependencies import get_chat_service
from models import ChatRequest
from fastapi import Depends
from logger import get_logger
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])
logger = get_logger(__name__)


@router.post("/", response_model=None)
async def chat(
    request: ChatRequest, service: ChatService = Depends(get_chat_service)
) -> StreamingResponse:
    return StreamingResponse(
        service.process_chat(request), media_type="text/event-stream"
    )
