from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from exceptions import ConfigurationError

load_dotenv()

def get_env(key:str) -> str:
    value = os.getenv(key)
    if value is None:
        raise ConfigurationError(f"{key}が設定されていません")
    return value

# 接続定義
service_endpoint = get_env("AZURE_SEARCH_ENDPOINT")
index_name = get_env("AZURE_SEARCH_INDEX_NAME")
credential = AzureKeyCredential(get_env("AZURE_SEARCH_API_KEY"))
open_ai_api_Key = get_env("OPENAI_API_KEY")

def get_search_client():
    # Azure Searchクライアントの作成
    search_client = SearchClient(service_endpoint, index_name, credential)
    return search_client

def get_openai_client():
    # OpenAIクライアントの作成
    openai_client = AsyncOpenAI(api_key=open_ai_api_Key)
    return openai_client
