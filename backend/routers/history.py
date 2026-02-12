from fastapi import APIRouter, Depends, HTTPException
from repositories.conversation_repository import ConversationRepository
from dependencies import get_conversation_repository
from models import Conversation, Message

router = APIRouter(prefix="/api/v1/conversations", tags=["conversations"])

# 会話作成
@router.post("/", response_model=Conversation)
def create_conversation(
    repo: ConversationRepository = Depends(get_conversation_repository),
) -> Conversation:
    return repo.create_conversation()


# 会話一覧取得
@router.get("/", response_model=list[Conversation])
def get_all_conversations(
    repo: ConversationRepository = Depends(get_conversation_repository),
) -> list[Conversation]:
    return repo.get_all_conversations()


# 特定の会話取得
@router.get("/{conversation_id}", response_model=Conversation)
def get_conversation(
    conversation_id: str,
    repo: ConversationRepository = Depends(get_conversation_repository),
) -> Conversation:
    conversation = repo.get_conversation(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


# メッセージ一覧取得
@router.get("/{conversation_id}/messages", response_model=list[Message])
def get_messages(
    conversation_id: str,
    repo: ConversationRepository = Depends(get_conversation_repository),
) -> list[Message]:
    return repo.get_messages(conversation_id)


# 会話削除
@router.delete("/{conversation_id}", response_model=dict)
def delete_conversation(
    conversation_id: str,
    repo: ConversationRepository = Depends(get_conversation_repository),
) -> dict:
    success = repo.delete_conversation(conversation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"message": "Conversation deleted successfully"}
