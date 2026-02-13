'''
Azure AI Searchにサンプルデータの内容を登録する
'''

import asyncio
import json
from utils import get_env
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.aio import SearchClient
from openai import AsyncOpenAI

# 接続定義
service_endpoint = get_env("AZURE_SEARCH_ENDPOINT")
index_name = get_env("AZURE_SEARCH_INDEX_NAME")
credential = AzureKeyCredential(get_env("AZURE_SEARCH_API_KEY"))
open_ai_api_Key = get_env("OPENAI_API_KEY")

# Azure AI Searchクライアントの作成
search_client = SearchClient(service_endpoint, index_name, credential)

# OpenAIクライアントの作成
openai_client = AsyncOpenAI(api_key=open_ai_api_Key)

# JSONファイルの読み込み
json_data = json.load(open('handbook_data.json', 'r', encoding='utf-8'))

async def get_embedding(text: str) -> list[float]:
    try:
        response = await openai_client.embeddings.create(
            model="text-embedding-3-small", input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f'Embedding生成に失敗しました: {e}')
        return []


# ベクトル化とデータ登録
async def main():
    print('ベクトル化実行中...')
    for doc in json_data:
        doc['embedding'] = await get_embedding(doc['content'])
        doc['page'] = str(doc['page'])

    try:
        print('登録中...')
        await search_client.upload_documents(json_data)
    except Exception as e:
        print(f'登録に失敗しました: {e}')
        return

    print(f'{len(json_data)}件登録しました。')


if __name__ == "__main__":
    asyncio.run(main())
