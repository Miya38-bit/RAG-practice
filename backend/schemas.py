from pydantic import BaseModel, Field
from typing import Literal


class SystemMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str = Field(
        min_length=1, max_length=1000, description="メッセージの内容（1-1000文字）"
    )


class ChatRequest(BaseModel):
    messages: list[SystemMessage] = Field(
        min_length=1, max_length=100, description="メッセージの履歴（1-100件）"
    )
