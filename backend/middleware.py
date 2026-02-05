import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from logger import get_logger

logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # リクエストIDを生成
        request_id = str(uuid.uuid4())

        # 開始時刻を記録
        start_time = time.time()

        # リクエスト情報をログに出力
        logger.info(
            "リクエスト受信",
            extra={
                "extra_fields": {
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                }
            },
        )

        # リクエストを処理
        response = await call_next(request)

        # 処理時間を計算
        process_time = time.time() - start_time

        # レスポンスヘッダーに処理時間を追加
        response.headers["X-Process-Time"] = str(process_time)

        # レスポンス情報をログに出力
        logger.info(
            "リクエスト完了",
            extra={
                "extra_fields": {"request_id": request_id, "process_time": process_time}
            },
        )

        return response
