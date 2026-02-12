import uuid
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import ClassVar


# チャットモデルの定義
class Conversation(SQLModel, table=True):
    __tablename__: ClassVar[str] = "conversations" #type: ignore
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)

    messages: list["Message"] = Relationship(
        back_populates="conversation", sa_relationship_kwargs={"cascade": "all, delete"}
    )


# メッセージモデルの定義
class Message(SQLModel, table=True):
    __tablename__: ClassVar[str] = "messages" #type: ignore
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    conversation_id: str = Field(foreign_key="conversations.id")
    role: str
    content: str
    created_at: datetime = Field(default_factory=datetime.now)

    conversation: Conversation | None = Relationship(back_populates="messages")
