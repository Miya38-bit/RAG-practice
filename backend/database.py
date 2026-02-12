from sqlmodel import create_engine, Session
from dotenv import load_dotenv
from utils import get_env

# 環境変数を読み込む
load_dotenv()

# DATABASE_URL を取得
DATABASE_URL = get_env("DATABASE_URL")

# エンジンを作成
engine = create_engine(DATABASE_URL)

# セッションを取得するための関数
def get_session():
    with Session(engine) as session:
        yield session
