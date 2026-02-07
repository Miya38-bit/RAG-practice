from fastapi import Request
from fastapi.responses import JSONResponse
from exceptions import RAGException, SearchError, EmbeddingError, LLMError
from logger import get_logger

logger = get_logger(__name__)


async def rag_exception_handler(request: Request, exc: RAGException)-> JSONResponse:
    # 詳細なエラーはログに記録
    logger.error(f"RAG Exception: {exc.message}", exc_info=True)

    # エラータイプに応じたユーザー向けメッセージ
    if isinstance(exc, SearchError):
        user_message = "検索中にエラーが発生しました。しばらくしてから再度お試しください。"
    elif isinstance(exc, EmbeddingError):
        user_message = "質問の処理中にエラーが発生しました。"
    elif isinstance(exc, LLMError):
        user_message = "回答の生成中にエラーが発生しました。"
    else:
        user_message = "システムエラーが発生しました。"

    return JSONResponse(
        status_code=503,
        content={"message": user_message, "type": exc.__class__.__name__},
    )


async def general_exception_handler(request: Request, exc: Exception)-> JSONResponse:
    logger.critical(f"General Exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "message": "予期せぬエラーが発生しました。",
            "type": "UnexpectedError",
        },
    )
