from utils import get_env
from azure.core.credentials import AzureKeyCredential

# Azure AI Search 設定
AZURE_SEARCH_ENDPOINT = get_env("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_INDEX_NAME = get_env("AZURE_SEARCH_INDEX_NAME")
AZURE_SEARCH_API_KEY = get_env("AZURE_SEARCH_API_KEY")
AZURE_SEARCH_CREDENTIAL = AzureKeyCredential(AZURE_SEARCH_API_KEY)

# OpenAI 設定
OPENAI_API_KEY = get_env("OPENAI_API_KEY")
EMBEDDING_MODEL = get_env("EMBEDDING_MODEL")
LLM_MODEL = get_env("LLM_MODEL")
