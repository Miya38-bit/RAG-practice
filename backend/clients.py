

from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

load_dotenv()

# 接続定義
service_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")
credential = AzureKeyCredential(os.getenv("AZURE_SEARCH_API_KEY"))

# Azure Searchクライアントの作成
search_client = SearchClient(service_endpoint, index_name, credential)
# OpenAIクライアントを生成
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))