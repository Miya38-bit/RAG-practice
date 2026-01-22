import os
from openai import OpenAI
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def chat_test():
    try:
        # APIを叩く
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "あなたは優秀なエンジニアのメンターです。",
                },
                {
                    "role": "user",
                    "content": "PythonでRAGを構築する際のコツを1つ教えて。",
                },
            ],
        )
        # 回答を表示
        print("AIの回答:")
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"エラーが発生しました: {e}")


if __name__ == "__main__":
    chat_test()
