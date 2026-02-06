from fastapi import Request
from fastapi.responses import JSONResponse
from exceptions import RAGException
from logger import get_logger

logger = get_logger(__name__)


async def rag_exception_handler(request: Request, exc: RAGException)-> JSONResponse:
    logger.error(f"RAG Exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=503,
        content={"message": exc.message, "type": exc.__class__.__name__},
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
