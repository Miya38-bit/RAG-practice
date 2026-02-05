from clients import (
    openai_client as default_openai_client,
    search_client as default_search_client,
)
from openai import AsyncOpenAI
from azure.search.documents import SearchClient
from logger import get_logger
from exceptions import EmbeddingError, SearchError, LLMError
from typing import List, AsyncGenerator
from schemas import SystemMessage

logger = get_logger(__name__)


# 引数からベクトル化したデータを取得
async def get_embedding(text: str, openai_client: AsyncOpenAI = None) -> List[float]:
    # 引数にopenai_clientが渡されなかった場合は、デフォルトのopenai_clientを使用
    client = openai_client or default_openai_client
    try:
        response = await client.embeddings.create(
            model="text-embedding-3-small", input=text
        )
        return response.data[0].embedding
    except Exception as e:
        raise EmbeddingError(f"Embedding作成中にエラーが発生しました: {str(e)}")


# ベクトルデータから参考情報検索
async def search_vector(
    vector_query: List[float],
    search_client: SearchClient | None = None,
) -> List[dict]:
    # 引数にsearch_clientが渡されなかった場合は、デフォルトのsearch_clientを使用
    client = search_client or default_search_client
    try:
        results = client.search(
            search_text=None,
            vector_queries=[
                {
                    "vector": vector_query,
                    "k": 2,
                    "fields": "embedding",
                    "kind": "vector",
                }
            ],
        )
        return results
    except Exception as e:
        raise SearchError(f"検索中にエラーが発生しました: {str(e)}")


# LLM応答取得
async def get_llm_response(
    messages: list[SystemMessage], openai_client: AsyncOpenAI | None = None
) -> str:
    # 引数にopenai_clientが渡されなかった場合は、デフォルトのopenai_clientを使用
    client = openai_client or default_openai_client
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise LLMError(f"LLM応答中にエラーが発生しました: {str(e)}")


# LLM応答取得(ストリーミング)
async def stream_llm_response(
    messages: list[SystemMessage], openai_client: AsyncOpenAI | None = None
) -> AsyncGenerator[str, None]:
    # 引数にopenai_clientが渡されなかった場合は、デフォルトのopenai_clientを使用
    client = openai_client or default_openai_client
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            stream=True,
        )
        async for chunk in response:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
    except Exception as e:
        raise LLMError(f"LLM応答中にエラーが発生しました: {str(e)}")


# ユーザーのメッセージを作成
def create_system_message(role: str, content: str) -> SystemMessage:
    return SystemMessage(role=role, content=content)
