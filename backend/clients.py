from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from exceptions import ConfigurationError

load_dotenv()

# 接続定義
service_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
if service_endpoint is None:
    raise ConfigurationError("AZURE_SEARCH_ENDPOINT is not set")
index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")
if index_name is None:
    raise ConfigurationError("AZURE_SEARCH_INDEX_NAME is not set")
azure_search_credential = os.getenv("AZURE_SEARCH_API_KEY")
if azure_search_credential is None:
    raise ConfigurationError("AZURE_SEARCH_API_KEY is not set")
credential = AzureKeyCredential(azure_search_credential)

# Azure Searchクライアントの作成
search_client = SearchClient(service_endpoint, index_name, credential)
# OpenAIクライアントを生成
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))