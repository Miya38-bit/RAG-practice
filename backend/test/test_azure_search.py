'''
OpenAIとAzure AI Searchを組み合わせたベクトル検索の確認
'''

from dotenv import load_dotenv
import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from openai import AsyncOpenAI
import asyncio

load_dotenv()

# 接続定義
service_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")
credential = AzureKeyCredential(os.getenv("AZURE_SEARCH_API_KEY"))

# ドキュメント定義
docs = [
    {"id": "1", "content": "今日はとても良い天気で、散歩日和です。"},
    {"id": "2", "content": "最近、美味しいコーヒーを淹れることにハマっています。"},
    {"id": "3", "content": "来週の旅行の計画を立てるのが楽しみです。"},
]

# OpenAIクライアントの作成
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# Azure Searchクライアントの作成
search_client = SearchClient(service_endpoint, index_name, credential)


# 引数からベクトル化したデータを取得
async def get_embedding(text):
    response = await openai_client.embeddings.create(
        model="text-embedding-3-small", input=text
    )
    return response.data[0].embedding


async def main():
    # ベクトル化
    print("Embedding作成中...")
    for doc in docs:
        doc["embedding"] = await get_embedding(doc["content"])

    # ドキュメントをアップロード
    print("Azureへ登録中...")
    search_client.upload_documents(docs)

    vector_queries = await get_embedding("美味しいご飯の話")

    # ベクトル検索
    print("検索中...")
    results = search_client.search(
        search_text=None,
        vector_queries=[
            {
                "vector":vector_queries,
                "k":1,
                "fields":"embedding",
                "kind":"vector"
            }
        ]
    )

    # 結果表示
    for result in results:
        print(result["content"])

# メイン
if __name__ == "__main__":
    asyncio.run(main())
