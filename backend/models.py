import uuid
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import ClassVar, Literal

# 型定義
Role = Literal["system", "user", "assistant"]

# チャットモデルの定義
class Conversation(SQLModel, table=True):
    __tablename__: ClassVar[str] = "conversations"  # type: ignore
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    title: str | None = None
    created_at: datetime = Field(default_factory=datetime.now)

    messages: list["Message"] = Relationship(
        back_populates="conversation", sa_relationship_kwargs={"cascade": "all, delete"}
    )


# Message ベースモデル
class MessageBase(SQLModel):
    role: str
    content: str


# DBメッセージモデルの定義
class Message(MessageBase, table=True):
    __tablename__: ClassVar[str] = "messages"  # type: ignore
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    conversation_id: str = Field(foreign_key="conversations.id")
    created_at: datetime = Field(default_factory=datetime.now)

    conversation: "Conversation" = Relationship(back_populates="messages")

# API リクエスト用モデル
class ChatRequest(SQLModel):
    conversation_id: str | None = None
    messages: list[MessageBase] = Field(min_length=1, max_length=100)
