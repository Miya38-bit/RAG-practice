from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middleware import LoggingMiddleware
from logger import get_logger
from routers import chat
from exception_handlers import rag_exception_handler, general_exception_handler
from exceptions import RAGException

logger = get_logger(__name__)

# FastAPIインスタンスを生成
app = FastAPI()

# 例外ハンドラー設定
# FastAPI の async handler の型定義制限のため、type: ignore を使用
app.add_exception_handler(RAGException, rag_exception_handler) # type: ignore
app.add_exception_handler(Exception, general_exception_handler)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ロギング用ミドルウェア設定
app.add_middleware(LoggingMiddleware)

# ルーター設定
app.include_router(chat.router)

