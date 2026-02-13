from openai import AsyncOpenAI
from azure.search.documents.aio import SearchClient
from sqlmodel import Session
from database import get_session
from repositories.conversation_repository import ConversationRepository
from repositories.search_repository import SearchRepository
from services.chat_service import ChatService
from fastapi import Depends
import config


# SearchClientの依存関係注入
def get_search_client():
    # Azure Searchクライアントの作成
    search_client = SearchClient(
        config.AZURE_SEARCH_ENDPOINT,
        config.AZURE_SEARCH_INDEX_NAME,
        config.AZURE_SEARCH_CREDENTIAL,
    )
    return search_client


# OpenAIクライアントの依存関係注入
def get_openai_client():
    # OpenAIクライアントの作成
    openai_client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)
    return openai_client


# ConversationRepositoryの依存関係注入
def get_conversation_repository(
    session: Session = Depends(get_session),
) -> ConversationRepository:
    return ConversationRepository(session)


# SearchRepositoryの依存関係注入
def get_search_repository(
    search_client: SearchClient = Depends(get_search_client),
) -> SearchRepository:
    return SearchRepository(search_client)


# ChatServiceの依存関係注入
def get_chat_service(
    openai_client: AsyncOpenAI = Depends(get_openai_client),
    search_repository: SearchRepository = Depends(get_search_repository),
    conversation_repository: ConversationRepository = Depends(
        get_conversation_repository
    ),
) -> ChatService:
    return ChatService(
        openai_client, search_repository, conversation_repository
    )