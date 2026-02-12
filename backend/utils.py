from clients import (
    openai_client as default_openai_client,
    search_client as default_search_client,
)
from openai import AsyncOpenAI
from azure.search.documents import SearchClient
from logger import get_logger
from exceptions import EmbeddingError, SearchError, LLMError
from typing import List, AsyncGenerator
from schemas import SystemMessage, Role
from exceptions import ConfigurationError
import os
from dotenv import load_dotenv

logger = get_logger(__name__)


load_dotenv()


def get_env(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        raise ConfigurationError(f"{key}が設定されていません")
    return value


# 引数からベクトル化したデータを取得
async def get_embedding(
    text: str, openai_client: AsyncOpenAI | None = None
) -> List[float]:
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
    text_query: str | None = None,
    search_client: SearchClient | None = None,
    use_semantic_search: bool = True,
    filter: str | None = None,
) -> List[dict]:
    # 引数にsearch_clientが渡されなかった場合は、デフォルトのsearch_clientを使用
    client = search_client or default_search_client
    try:
        results = client.search(
            search_text=text_query,
            vector_queries=[  # type: ignore
                {
                    "vector": vector_query,
                    "k": 2,
                    "fields": "embedding",
                    "kind": "vector",
                }
            ],
            query_type="semantic" if use_semantic_search else "simple",
            semantic_configuration_name="my-semantic-config"
            if use_semantic_search
            else None,
            filter=filter,
        )
        return list(results)
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
            messages=messages,  # type: ignore
        )
        result = response.choices[0].message.content
        if result is None:
            raise LLMError("LLMからの応答が空です")
        return result
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
            messages=messages,  # type: ignore
            stream=True,
        )
        async for chunk in response:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
    except Exception as e:
        raise LLMError(f"LLM応答中にエラーが発生しました: {str(e)}")


# ユーザーのメッセージを作成
def create_system_message(role: Role, content: str) -> SystemMessage:
    return SystemMessage(role=role, content=content)
