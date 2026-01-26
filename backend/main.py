from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from utils import get_embedding
from clients import openai_client, search_client

# FastAPIインスタンスを生成
app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    messages: list[dict[str, str]]


@app.post("/chat")
async def create_chat(request: ChatRequest):
    try:
        # 通訳用の質問作成
        history_messages = f"これまでの会話履歴から質問の意図を誰が見ても意味がわかる検索ワードに書き直してください\n 【質問】{request.messages[-1]['content']}\n【会話履歴】\n"
        for message in request.messages:
            history_messages += f"{message['role']}: {message['content']}\n"

        # 質問の意図を検索ワードに書き直してもらう
        response_rewrite = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": history_messages
                }
            ]
        )
        print("検索ワード: ", response_rewrite.choices[0].message.content)

        # ベクトル化
        print("Embedding作成中...")
        vector_query = await get_embedding(response_rewrite.choices[0].message.content)

        # ベクトルデータから参考情報検索
        print("ベクトルデータから参考情報検索中...")
        results = search_client.search(
            search_text=None,
            vector_queries=[
                {
                    "vector": vector_query,
                    "k": 2,
                    "fields": "embedding",
                    "kind": "vector",
                }
            ],
        )

        # 参考情報の作成
        context = ""
        for result in results:
            context += f"【出典: {result['source']} (P.{result['page']}) / カテゴリ: {result['category']}】\n"
            context += f"{result['content']}\n\n"

        system_messages = {
            "role": "system",
            "content": f"以下の情報を元に質問に答えてください。\n\n【参考情報】\n{context}",
        }
        # 参考情報をもとに質問応答
        response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[system_messages] + request.messages,
        )
        print("合計トークン数: ", response.usage.total_tokens)
        print("プロンプトトークン数: ", response.usage.prompt_tokens)
        print("応答トークン数: ", response.usage.completion_tokens)
        return {"message": response.choices[0].message.content, "status": "success"}
    except Exception as e:
        return {"message": str(e), "status": "error"}
