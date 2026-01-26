
from clients import openai_client

# 引数からベクトル化したデータを取得
async def get_embedding(text:str):
    response = await openai_client.embeddings.create(
        model='text-embedding-3-small',
        input=text
    )
    return response.data[0].embedding