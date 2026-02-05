import logging
import json
from datetime import datetime


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.now().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # extra属性があれば追加
        if hasattr(record, "extra_fields"):
            log_data.update(record.extra_fields)
        # pythonの辞書をJSON形式で出力
        return json.dumps(log_data, ensure_ascii=False)

# モジュールごとにloggerを取得する関数
def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # 出力先設定
    handler = logging.StreamHandler()

    # 出力フォーマット設定
    handler.setFormatter(JSONFormatter())

    # 出力先（ハンドラー）をロガーに追加
    logger.addHandler(handler)

    return logger
