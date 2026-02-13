from exceptions import ConfigurationError
import os
from dotenv import load_dotenv

load_dotenv()


def get_env(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        raise ConfigurationError(f"{key}が設定されていません")
    return value
