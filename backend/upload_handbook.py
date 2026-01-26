'''
Azure AI Searchにサンプルデータの内容を登録する
'''

import asyncio
import json
from utils import get_embedding
from clients import search_client

# JSONファイルの読み込み
json_data = json.load(open('handbook_data.json', 'r', encoding='utf-8'))

# ベクトル化とデータ登録
async def main():
    print('ベクトル化実行中...')
    for doc in json_data:
        doc['embedding'] = await get_embedding(doc['content'])
        doc['page'] = str(doc['page'])

    try:
        print('登録中...')
        search_client.upload_documents(json_data)
    except Exception as e:
        print(f'登録に失敗しました: {e}')
        return

    print(f'{len(json_data)}件登録しました。')


if __name__ == "__main__":
    asyncio.run(main())
