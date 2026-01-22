from fastapi import FastAPI
from dotenv import load_dotenv
import os
from openai import AsyncOpenAI
from pydantic import BaseModel
from typing import Optional

# 環境変数を読み込む
load_dotenv()
# FastAPIインスタンスを生成
app = FastAPI()
# OpenAIクライアントを生成
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None


@app.get("/")
async def read_root():
    return {"message": "Hello World", "status": "success"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id, "description": f"これはアイテム {item_id} です"}


@app.post("/chat")
async def create_chat(request: ChatRequest):
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": request.message,
                }
            ],
        )
        return {"message": response.choices[0].message.content, "status": "success"}
    except Exception as e:
        return {"message": str(e), "status": "error"}


print("--- 現在のルーティングテーブル ---")
for route in app.routes:
    # 組み込みの /docs や /openapi.json 以外を表示
    if hasattr(route, "path"):
        print(f"Path: {route.path: <20} | Methods: {route.methods}")
print("----------------------------------")
