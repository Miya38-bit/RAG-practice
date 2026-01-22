from fastapi import FastAPI
from dotenv import load_dotenv
import os
from openai import AsyncOpenAI
from pydantic import BaseModel
from typing import Optional
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

# 環境変数を読み込む
load_dotenv()

# 接続定義
service_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")
credential = AzureKeyCredential(os.getenv("AZURE_SEARCH_API_KEY"))

# OpenAIクライアントを生成
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# Azure Searchクライアントを生成
search_client = SearchClient(service_endpoint, index_name, credential)

# FastAPIインスタンスを生成
app = FastAPI()

# 引数からベクトル化したデータを取得
async def get_embedding(test:str):
    response = await openai_client.embeddings.create(
        model = "text-embedding-3-small",
        input = test
    )
    return response.data[0].embedding

class ChatRequest(BaseModel):
    message: str

# @app.get("/")
# async def read_root():
#     return {"message": "Hello World", "status": "success"}


# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id": item_id, "description": f"これはアイテム {item_id} です"}


@app.post("/chat")
async def create_chat(request: ChatRequest):
    try:
        # ベクトル化
        print("Embedding作成中...")
        vector_query = await get_embedding(request.message)

        # ベクトルデータから参考情報検索
        print("ベクトルデータから参考情報検索中...")
        results = search_client.search(
            search_text=None,
            vector_queries=[
                {
                    "vector":vector_query,
                    "k":1,
                    "fields":"embedding",
                    "kind":"vector"
                }
            ]
        )

        # 参考情報の作成
        context = "".join(result["content"] for result in results)
        print("参考情報:", context)

        # 参考情報をもとに質問応答
        response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"以下の情報を元に質問に答えてください。\n\n【参考情報】\n{context}\n\n【質問】\n{request.message}"
                }
            ],
        )
        return {"message": response.choices[0].message.content, "status": "success"}
    except Exception as e:
        return {"message": str(e), "status": "error"}


# print("--- 現在のルーティングテーブル ---")
# for route in app.routes:
#     # 組み込みの /docs や /openapi.json 以外を表示
#     if hasattr(route, "path"):
#         print(f"Path: {route.path: <20} | Methods: {route.methods}")
# print("----------------------------------")
