from fastapi import APIRouter
from utils import (
    get_embedding,
    search_vector,
    get_llm_response,
    stream_llm_response,
    create_system_message,
)
from fastapi.responses import StreamingResponse
from schemas import ChatRequest
from fastapi import Depends
from dependencies import get_openai_client, get_search_client
from openai import AsyncOpenAI
from azure.search.documents import SearchClient
from logger import get_logger

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])
logger = get_logger(__name__)


@router.post("/", response_model=None)
async def chat(
    request: ChatRequest,
    openai_client: AsyncOpenAI = Depends(get_openai_client),
    search_client: SearchClient = Depends(get_search_client),
) -> StreamingResponse:
    # 通訳用の質問作成
    history_messages = f"これまでの会話履歴から質問の意図を誰が見ても意味がわかる検索ワードに書き直してください\n 【質問】{request.messages[-1].content}\n【会話履歴】\n"
    for message in request.messages:
        history_messages += f"{message.role}: {message.content}\n"

    # 質問の意図を検索ワードに書き直してもらう
    response_rewrite = await get_llm_response(
        [create_system_message("user", history_messages)],
        openai_client,
    )

    # 検索ワードをさらにベクトル化
    vector_query = await get_embedding(response_rewrite, openai_client)

    # ベクトルデータから参考情報検索
    results = await search_vector(vector_query, search_client)

    # 参考情報の作成
    context = ""
    for result in results:
        context += f"【出典: {result['source']} (P.{result['page']}) / カテゴリ: {result['category']}】\n"
        context += f"{result['content']}\n\n"

    system_messages = create_system_message(
        "system",
        f"以下の情報を元に質問に答えてください。\n\n【参考情報】\n{context}",
    )

    return StreamingResponse(
        stream_llm_response([system_messages] + request.messages, openai_client),
        media_type="text/event-stream",
    )
