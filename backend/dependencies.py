from openai import AsyncOpenAI


from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from utils import get_env
from sqlmodel import Session
from database import get_session
from repositories.conversation_repository import ConversationRepository
from fastapi import Depends


# 接続定義
service_endpoint = get_env("AZURE_SEARCH_ENDPOINT")
index_name = get_env("AZURE_SEARCH_INDEX_NAME")
credential = AzureKeyCredential(get_env("AZURE_SEARCH_API_KEY"))
open_ai_api_Key = get_env("OPENAI_API_KEY")


# SearchClientの依存関係注入
def get_search_client():
    # Azure Searchクライアントの作成
    search_client = SearchClient(service_endpoint, index_name, credential)
    return search_client


# OpenAIクライアントの依存関係注入
def get_openai_client():
    # OpenAIクライアントの作成
    openai_client = AsyncOpenAI(api_key=open_ai_api_Key)
    return openai_client


# ConversationRepositoryの依存関係注入
def get_conversation_repository(
    session: Session = Depends(get_session),
) -> ConversationRepository:
    return ConversationRepository(session)
